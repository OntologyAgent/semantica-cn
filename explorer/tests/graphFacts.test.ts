import assert from "node:assert/strict";
import test from "node:test";

import { businessEdgesToFacts } from "../src/workspaces/GraphWorkspace/graphFacts.ts";

function node(id: string, type: string, properties: Record<string, unknown> = {}, content?: string) {
  return { id, type, entity_type: type, content: content ?? id, properties };
}

function edge(id: string, source: string, target: string, type: string, properties: Record<string, unknown> = {}) {
  return { id, source, target, type, properties };
}

function fixture() {
  const nodes = [
    node("https://az/ContractA", "instance", { layer: "instance", "skos:prefLabel": "华跃合同A" }, "华跃合同A"),
    node("https://az/PolicyB", "instance", { layer: "instance" }, "返利政策B"),
    node("https://az/appliesTo", "owl:ObjectProperty", { "skos:prefLabel": "适用于", "az:asciiId": "applies_to" }, "适用于"),
    node("https://az/amount", "owl:DatatypeProperty", { "rdfs:label": "金额", "skos:notation": "amount" }, "金额"),
    node("https://az/DocC", "class", {}, "https://az/DocC"),
  ];
  const edges = [
    edge("e1", "https://az/ContractA", "https://az/PolicyB", "适用于", { layer: "business" }),
    edge("e2", "https://az/ContractA", "https://az/PolicyB", "plain_predicate", { layer: "business" }),
    edge("e3", "https://az/ContractA", "https://az/DocC", "适用于", { layer: "schema" }),
    edge("e4", "https://az/ContractA", "https://az/PolicyB", "适用于", { layer: "inferred" }),
    edge("e5", "https://az/ContractA", "https://az/PolicyB", "适用于", {}),
  ];
  return { nodes, edges };
}

test("business edges become predicate(subject, object) lines", () => {
  const facts = businessEdgesToFacts(fixture().nodes, fixture().edges);
  assert.deepEqual(facts, [
    "applies_to(华跃合同A, 返利政策B)",
    "plain_predicate(华跃合同A, 返利政策B)",
  ]);
});

test("ascii mapping prefers az:asciiId and skos:notation of the matching property node", () => {
  const { nodes, edges } = fixture();
  edges.push(edge("e6", "https://az/ContractA", "https://az/PolicyB", "金额", { layer: "business" }));
  const facts = businessEdgesToFacts(nodes, edges);
  assert.ok(facts.includes("amount(华跃合同A, 返利政策B)"));
});

test("unmapped edge types fall back to the raw type", () => {
  const facts = businessEdgesToFacts(fixture().nodes, fixture().edges);
  assert.ok(facts.some((line) => line.startsWith("plain_predicate(")));
});

test("schema, inferred, and layerless edges are excluded", () => {
  const facts = businessEdgesToFacts(fixture().nodes, fixture().edges);
  assert.equal(facts.length, 2);
  assert.ok(!facts.some((line) => line.startsWith("适用于(")));
});

test("node labels fall back through prefLabel/content to uri tail", () => {
  const { nodes, edges } = fixture();
  // DocC has no real label: content echoes the id → uri tail
  edges.push(edge("e7", "https://az/DocC", "https://az/PolicyB", "plain_predicate", { layer: "business" }));
  const facts = businessEdgesToFacts(nodes, edges);
  assert.ok(facts.some((line) => line.startsWith("plain_predicate(DocC,")));
});

test("empty graph yields no facts", () => {
  assert.deepEqual(businessEdgesToFacts([], []), []);
});
