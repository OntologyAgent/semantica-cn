import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToString } from "react-dom/server";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import en from "../src/i18n/locales/en.json";

(globalThis as typeof globalThis & { React: typeof React }).React = React;

// The panel's chrome is translated through react-i18next; seed a synchronous
// English instance before importing the component so SSR output carries the
// en copy the assertions below match against.
if (!i18next.isInitialized) {
  i18next.use(initReactI18next).init({
    lng: "en",
    fallbackLng: "en",
    resources: { en: { translation: en.translation } },
  });
}

import { PropertyPanel } from "../src/workspaces/VocabularyWorkspace/PropertyPanel.tsx";
import type { ConceptNode, ConceptDetail } from "../src/workspaces/VocabularyWorkspace/types.ts";

const concept = (overrides: Partial<ConceptNode> = {}): ConceptNode => ({
  uri: "http://example.org/ns#Demo",
  pref_label: "Demo Concept",
  alt_labels: [],
  ...overrides,
});

// ─── Bug capture: hierarchy description was never rendered ───────────────────
// The hierarchy endpoint has always delivered `description` on ConceptNode
// (vocabulary-import path), but the panel only drew prefLabel/URI/altLabels/
// narrower. Rendering the selected concept must surface its description.
test("renders the concept description from hierarchy data", () => {
  const html = renderToString(React.createElement(PropertyPanel, {
    concept: concept({ description: "A crisp hierarchy description." }),
  }));
  assert.equal(html.includes("A crisp hierarchy description."), true);
});

test("renders definition and scope note from the concept detail endpoint payload", () => {
  const detail: ConceptDetail = {
    uri: "http://example.org/ns#Demo",
    pref_label: "Demo Concept",
    definition: "Defined by the ontology load path.",
    scope_note: "Use for demo purposes only.",
  };
  const html = renderToString(React.createElement(PropertyPanel, {
    concept: concept(),
    detail,
  }));
  assert.equal(html.includes("Defined by the ontology load path."), true);
  assert.equal(html.includes("Use for demo purposes only."), true);
});

test("detail definition wins over the hierarchy description", () => {
  const detail: ConceptDetail = {
    uri: "http://example.org/ns#Demo",
    pref_label: "Demo Concept",
    definition: "From detail endpoint.",
    scope_note: null,
  };
  const html = renderToString(React.createElement(PropertyPanel, {
    concept: concept({ description: "From hierarchy." }),
    detail,
  }));
  assert.equal(html.includes("From detail endpoint."), true);
  assert.equal(html.includes("From hierarchy."), false);
});

test("falls back to hierarchy description when detail definition is null", () => {
  // vocabulary-import concepts: the detail endpoint has no definition for
  // them, so the panel must keep showing the hierarchy description.
  const detail: ConceptDetail = {
    uri: "http://example.org/ns#Demo",
    pref_label: "Demo Concept",
    definition: null,
    scope_note: null,
  };
  const html = renderToString(React.createElement(PropertyPanel, {
    concept: concept({ description: "Hierarchy fallback text." }),
    detail,
  }));
  assert.equal(html.includes("Hierarchy fallback text."), true);
});

test("hides the definition and scope-note sections when both sources are empty", () => {
  const html = renderToString(React.createElement(PropertyPanel, {
    concept: concept(),
    detail: { uri: "http://example.org/ns#Demo", pref_label: "Demo Concept", definition: null, scope_note: null },
  }));
  assert.equal(html.includes("vocabulary.definition"), false, "definition header must not render without content");
  assert.equal(html.includes("vocabulary.scopeNote"), false, "scope-note header must not render without content");
});

// ─── fetchConceptDetail contract: URI encoding ───────────────────────────────
// SKOS URIs routinely contain '#' (and '/'); unencoded, '#' truncates the
// request path at the fragment. The fetch must percent-encode the whole URI.
test("fetchConceptDetail percent-encodes the concept URI into the request path", async () => {
  const calls: string[] = [];
  const originalFetch = globalThis.fetch;
  globalThis.fetch = (async (input: RequestInfo | URL) => {
    calls.push(String(input));
    return {
      ok: true,
      json: async () => ({ uri: "x", pref_label: "x", definition: null, scope_note: null }),
    } as Response;
  }) as typeof fetch;
  try {
    const { fetchConceptDetail } = await import("../src/workspaces/VocabularyWorkspace/queries.ts");
    await fetchConceptDetail("http://example.org/ns#Demo Concept");
    assert.equal(calls.length, 1);
    assert.equal(
      calls[0],
      "/api/ontology/skos/concept/http%3A%2F%2Fexample.org%2Fns%23Demo%20Concept",
      "the URI must be percent-encoded as a single path segment",
    );
  } finally {
    globalThis.fetch = originalFetch;
  }
});
