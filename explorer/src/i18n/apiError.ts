/**
 * API error wrapping for user-facing surfaces (P1, FR-003).
 *
 * Pure functions only: no React, no i18next import, no side effects. Callers
 * translate the returned `wrapperKey` themselves (so `useTranslation` stays in
 * charge of reactivity) and decide whether to render `detail` (empty string =
 * hide the section). The backend `detail` text is passed through verbatim —
 * never truncated, rewritten, or translated.
 */

export interface ApiErrorView {
  /** i18n key under `graph.errors.*` for the human-facing wrapper line. */
  wrapperKey: string;
  /** Backend `detail` verbatim, or "" when unavailable (callers hide it). */
  detail: string;
}

function extractDetail(body: unknown): string {
  if (body !== null && typeof body === 'object') {
    const detail = (body as { detail?: unknown }).detail;
    if (typeof detail === 'string') {
      return detail;
    }
  }
  return '';
}

/**
 * Map a failed response to its wrapper view. `status === undefined` means the
 * request never completed (network error, DNS failure, aborted fetch).
 */
export function describeApiError(status: number | undefined, body: unknown): ApiErrorView {
  let wrapperKey: string;
  if (status === undefined) {
    wrapperKey = 'graph.errors.network';
  } else if (status === 401) {
    wrapperKey = 'graph.errors.unauthorized';
  } else if (status === 403) {
    wrapperKey = 'graph.errors.forbidden';
  } else if (status === 404) {
    wrapperKey = 'graph.errors.notFound';
  } else if (status >= 500) {
    wrapperKey = 'graph.errors.serverError';
  } else {
    wrapperKey = 'graph.errors.requestFailed';
  }
  return { wrapperKey, detail: extractDetail(body) };
}

/**
 * Read a failed `Response` defensively: bodies that are empty, HTML error
 * pages, or malformed JSON degrade to `detail: ""` instead of throwing.
 */
export async function describeResponseError(response: Response): Promise<ApiErrorView> {
  let body: unknown = null;
  try {
    body = await response.json();
  } catch {
    body = null;
  }
  return describeApiError(response.status, body);
}
