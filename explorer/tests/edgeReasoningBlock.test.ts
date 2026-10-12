import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToString } from "react-dom/server";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import en from "../src/i18n/locales/en.json";

(globalThis as typeof globalThis & { React: typeof React }).React = React;

if (!i18next.isInitialized) {
  i18next.use(initReactI18next).init({
    lng: "en",
    fallbackLng: "en",
    resources: { en: { translation: en.translation } },
  });
}

import { EdgeReasoningBlock } from "../src/workspaces/GraphWorkspace/EdgeReasoningBlock.tsx";
import { EDGE_REASONING_KEYS } from "../src/workspaces/GraphWorkspace/edgeReasoningKeys.ts";

// Reasoning flags as written by POST /api/reason → session.add_edge kwargs:
// inferred (bool), inferred_from (fact string), reasoning_mode, rules (list).
const inferredProps = {
  inferred: true,
  inferred_from: "candidate(Metformin, Alzheimer's)",
  reasoning_mode: "forward",
  rules: ["if_treats_then_candidate", "dedup_by_confidence"],
};

test("renders badge, mode, fact, and rules for an inferred edge", () => {
  const html = renderToString(React.createElement(EdgeReasoningBlock, { properties: inferredProps }));
  assert.equal(html.includes("Inferred edge"), true, "inferred badge must render");
  assert.equal(html.includes("Reasoning: forward"), true, "reasoning mode must render");
  assert.equal(html.includes("candidate(Metformin, Alzheimer&#x27;s)"), true, "inferred-from fact must render");
  assert.equal(html.includes("if_treats_then_candidate"), true, "rule ids must render");
  assert.equal(html.includes("dedup_by_confidence"), true, "all rule ids must render");
});

test("renders nothing for a factual edge without inference flags", () => {
  const html = renderToString(React.createElement(EdgeReasoningBlock, {
    properties: { weight: 0.9, source_doc: "report.md" },
  }));
  assert.equal(html, "");
});

test("renders nothing when inferred is explicitly false", () => {
  const html = renderToString(React.createElement(EdgeReasoningBlock, {
    properties: { ...inferredProps, inferred: false },
  }));
  assert.equal(html, "");
});

test("tolerates string-typed inferred flag from stringified properties", () => {
  const html = renderToString(React.createElement(EdgeReasoningBlock, {
    properties: { inferred: "true", inferred_from: "fact(x, y)" },
  }));
  assert.equal(html.includes("Inferred edge"), true);
  assert.equal(html.includes("fact(x, y)"), true);
});

test("badge renders alone when fact, mode and rules are missing", () => {
  const html = renderToString(React.createElement(EdgeReasoningBlock, { properties: { inferred: true } }));
  assert.equal(html.includes("Inferred edge"), true);
  assert.equal(html.includes("undefined"), false, "no literal undefined may leak into the markup");
});

test("non-string rule entries are dropped instead of rendered", () => {
  const html = renderToString(React.createElement(EdgeReasoningBlock, {
    properties: { inferred: true, rules: ["valid-rule", 42, null] },
  }));
  assert.equal(html.includes("valid-rule"), true);
  assert.equal(html.includes("42"), false);
});

test("EDGE_REASONING_KEYS covers exactly the four reasoning flags", () => {
  assert.deepEqual([...EDGE_REASONING_KEYS].sort(), ["inferred", "inferred_from", "reasoning_mode", "rules"]);
});
