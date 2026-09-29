#!/bin/bash
# Nightly verification gate for the semantica-cn fork (runs on the maintainer's
# macOS machine). Runs the unit-test suite in the lockfile environment and
# diffs the failure set against the recorded platform baseline.
#
#   exit 0  no new failures (gate passed)
#   exit 1  new failures appeared (regression — do not push/release)
#
# The baseline (tools/nightly/baseline_failures.txt) covers environment-only
# failures: macOS system proxy (SSRF guard), Python 3.13 MagicMock ordering,
# and service-dependent tests that upstream marks as non-integration.
# Refresh the baseline ONLY after confirming a failure is environmental.
set -u
cd "$(dirname "$0")/../.."

BASELINE=tools/nightly/baseline_failures.txt
LOG=$(mktemp)

# Keep the env in sync with the lockfile so new upstream test deps (extras)
# are present; keep this extras list aligned with the fork's test needs —
# all-extras is not installable on macOS (faiss-gpu / cuda-bindings).
uv sync --frozen --extra explorer --extra vectorstore-qdrant --extra embeddings-local \
  --extra viz --extra graph-embeddings --extra ingest-tableau --extra nlp-langdetect -q

env -u HTTP_PROXY -u HTTPS_PROXY -u http_proxy -u https_proxy \
  uv run --frozen pytest -m "not integration" -q > "$LOG" 2>&1
tail -1 "$LOG"

grep -E "^FAILED" "$LOG" | sed 's/^FAILED //;s/ - .*//' | sort > /tmp/nightly-failures.txt
sort "$BASELINE" > /tmp/nightly-baseline.txt

NEW=$(comm -23 /tmp/nightly-failures.txt /tmp/nightly-baseline.txt)
FIXED=$(comm -13 /tmp/nightly-failures.txt /tmp/nightly-baseline.txt)

echo "failures: $(wc -l < /tmp/nightly-failures.txt | tr -d ' ')  (baseline: $(wc -l < /tmp/nightly-baseline.txt | tr -d ' '))"
[ -n "$FIXED" ] && echo "fixed vs baseline (consider refreshing it):" && echo "$FIXED"

if [ -n "$NEW" ]; then
  echo "NEW FAILURES (regression!):"
  echo "$NEW"
  exit 1
fi
echo "GATE PASSED: no new failures"
exit 0
