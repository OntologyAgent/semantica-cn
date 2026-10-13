import assert from "node:assert/strict";
import test from "node:test";

import {
  buildClassTree,
  buildPropertyCards,
  classDisplayLabel,
} from "../src/workspaces/OntologyWorkspace/schemaTabModel.ts";

const CLASS = "owl:Class";
const OBJ = "owl:ObjectProperty";
const DATA = "owl:DatatypeProperty";

function node(id: string, type: string, properties: Record<string, unknown> = {}, content?: string) {
  return { id, type, entity_type: type, content: content ?? id, properties };
}

function edge(source: string, target: string, type: string) {
  return { source, target, type };
}

function schemaFixture() {
  const nodes = [
    node("az:Resource", CLASS, { "skos:prefLabel": "资源" }),
    node("az:Policy", CLASS, { "rdfs:label": "政策类", "rdfs:comment": "Policy class" }),
    node("az:Contract", CLASS, {}, "合同"),
    node("az:appliesTo", OBJ, { "az:asciiId": "applies_to" }),
    node("az:amount", DATA, { "skos:notation": "amount" }),
    node("az:party", "owl:AnnotationProperty", {}),
    node("az:doc1", "entity", {}), // 非模式节点，必须被忽略
  ];
  const edges = [
    edge("az:Policy", "az:Resource", "rdfs:subClassOf"),
    edge("az:Contract", "az:Resource", "rdfs:subClassOf"),
    edge("az:appliesTo", "az:Policy", "rdfs:domain"),
    edge("az:appliesTo", "az:Contract", "rdfs:range"),
    edge("az:amount", "az:Contract", "rdfs:domain"),
    edge("az:doc1", "az:Policy", "rdf:type"), // 实例边，必须被忽略
  ];
  return { nodes, edges };
}

test("classDisplayLabel prefers prefLabel, falls back to label/content/uri", () => {
  assert.equal(classDisplayLabel(node("a", CLASS, { "skos:prefLabel": "政策" })), "政策");
  assert.equal(classDisplayLabel(node("a", CLASS, { "rdfs:label": "L" })), "L");
  assert.equal(classDisplayLabel(node("a", CLASS, {}, "C")), "C");
  assert.equal(classDisplayLabel(node("http://x/y/az:Tail", CLASS, {})), "Tail");
});

test("buildClassTree nests children under their subClassOf parents", () => {
  const tree = buildClassTree(schemaFixture().nodes, schemaFixture().edges);
  const root = tree.find((entry) => entry.uri === "az:Resource");
  assert.ok(root);
  assert.deepEqual(
    root.children.map((child) => child.uri).sort(),
    ["az:Contract", "az:Policy"],
  );
  assert.equal(root.label, "资源");
  const policy = root.children.find((child) => child.uri === "az:Policy");
  assert.equal(policy!.label, "政策类");
});

test("buildClassTree keeps orphan classes as roots and survives cycles", () => {
  const nodes = [node("a", CLASS), node("b", CLASS), node("orphan", CLASS)];
  const edges = [
    edge("a", "b", "rdfs:subClassOf"),
    edge("b", "a", "rdfs:subClassOf"),
  ];
  const tree = buildClassTree(nodes, edges);
  // Cycle members and the orphan are all promoted to roots; no hang.
  assert.deepEqual(
    tree.map((entry) => entry.uri).sort(),
    ["a", "b", "orphan"],
  );
  const a = tree.find((entry) => entry.uri === "a")!;
  assert.deepEqual(a.children.map((child) => child.uri), ["b"]);
});

test("buildPropertyCards collects signatures, asciiId, and kind", () => {
  const cards = buildPropertyCards(schemaFixture().nodes, schemaFixture().edges);
  assert.deepEqual(cards.map((card) => card.uri), ["az:amount", "az:appliesTo", "az:party"]);
  const appliesTo = cards.find((card) => card.uri === "az:appliesTo")!;
  assert.equal(appliesTo.kind, OBJ);
  assert.deepEqual(appliesTo.domains, ["az:Policy"]);
  assert.deepEqual(appliesTo.ranges, ["az:Contract"]);
  assert.equal(appliesTo.asciiId, "applies_to");
  const amount = cards.find((card) => card.uri === "az:amount")!;
  assert.equal(amount.asciiId, "amount");
  assert.equal(amount.kind, DATA);
});

test("instance-level edges never leak into schema structures", () => {
  const cards = buildPropertyCards(schemaFixture().nodes, schemaFixture().edges);
  const appliesTo = cards.find((card) => card.uri === "az:appliesTo")!;
  // rdf:type (az:doc1 → az:Policy) must not appear as domain/range
  assert.deepEqual(appliesTo.ranges, ["az:Contract"]);
});

test("empty graph yields empty structures", () => {
  assert.deepEqual(buildClassTree([], []), []);
  assert.deepEqual(buildPropertyCards([], []), []);
});
