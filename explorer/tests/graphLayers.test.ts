import assert from "node:assert/strict";
import test from "node:test";
import Graph from "graphology";

import {
  applyLayerFilter,
  graphHasLayerData,
  nodeVisibleInPreset,
  type LayerPreset,
} from "../src/workspaces/GraphWorkspace/graphLayers.ts";

function nodeAttrs(layer?: string, extra: Record<string, unknown> = {}) {
  const properties: Record<string, unknown> = { ...extra };
  if (layer !== undefined) properties.layer = layer;
  return { label: "n", content: "n", properties };
}

function edgeAttrs(layer?: string) {
  const properties: Record<string, unknown> = {};
  if (layer !== undefined) properties.layer = layer;
  return { properties };
}

/** instance/class/property/rules nodes, business/schema/inferred edges. */
function layeredGraph(): Graph {
  const graph = new Graph();
  graph.addNode("contract-1", nodeAttrs("instance"));
  graph.addNode("contract-2", nodeAttrs("instance"));
  graph.addNode("contract-3", nodeAttrs("instance"));
  graph.addNode("policy-class", nodeAttrs("class"));
  graph.addNode("amount-prop", nodeAttrs("property"));
  graph.addNode("rules-lib", nodeAttrs("rules"));
  graph.addNode("injected-bare", nodeAttrs()); // load 注入、未合并、无 layer
  graph.addEdgeWithKey("e-biz", "contract-1", "contract-2", edgeAttrs("business"));
  // schema edges are property→class signatures (domain/range); instance→class
  // rdf:type edges legitimately vanish with the instance in the ontology preset
  graph.addEdgeWithKey("e-schema", "amount-prop", "policy-class", edgeAttrs("schema"));
  graph.addEdgeWithKey("e-inferred", "contract-1", "contract-3", edgeAttrs("inferred"));
  graph.addEdgeWithKey("e-bare", "contract-2", "injected-bare", edgeAttrs());
  return graph;
}

test("graphHasLayerData detects layer markers and their absence", () => {
  assert.equal(graphHasLayerData(layeredGraph()), true);
  const plain = new Graph();
  plain.addNode("a", nodeAttrs());
  plain.addNode("b", nodeAttrs());
  plain.addEdgeWithKey("ab", "a", "b", edgeAttrs());
  assert.equal(graphHasLayerData(plain), false);
});

test("applyLayerFilter returns null when the graph carries no layer data", () => {
  const plain = new Graph();
  plain.addNode("a", nodeAttrs());
  assert.equal(applyLayerFilter(plain, "business", true), null);
});

test("business preset keeps instance nodes and business edges only", () => {
  const result = applyLayerFilter(layeredGraph(), "business", false)!;
  assert.deepEqual([...result.nodes()].sort(), ["contract-1", "contract-2", "contract-3"]);
  assert.deepEqual([...result.edges()].sort(), ["e-biz"]);
});

test("ontology preset keeps class/property nodes and schema edges only", () => {
  const result = applyLayerFilter(layeredGraph(), "ontology", false)!;
  assert.deepEqual([...result.nodes()].sort(), ["amount-prop", "policy-class"]);
  assert.deepEqual([...result.edges()].sort(), ["e-schema"]);
});

test("all preset shows every layered node, hides layerless ones", () => {
  const result = applyLayerFilter(layeredGraph(), "all", true)!;
  assert.deepEqual(
    [...result.nodes()].sort(),
    ["amount-prop", "contract-1", "contract-2", "contract-3", "policy-class", "rules-lib"],
  );
  // inferred visible with the toggle on
  assert.deepEqual([...result.edges()].sort(), ["e-biz", "e-inferred", "e-schema"]);
});

test("inferred toggle hides inferred edges in every preset (global semantics)", () => {
  for (const preset of ["all", "business", "ontology"] as LayerPreset[]) {
    const result = applyLayerFilter(layeredGraph(), preset, false)!;
    assert.equal(result.hasEdge("e-inferred"), false, `preset=${preset}`);
  }
  const on = applyLayerFilter(layeredGraph(), "business", true)!;
  assert.equal(on.hasEdge("e-inferred"), true);
});

test("layerless nodes and edges never appear in any preset when layer data exists", () => {
  for (const preset of ["all", "business", "ontology"] as LayerPreset[]) {
    const result = applyLayerFilter(layeredGraph(), preset, true)!;
    assert.equal(result.hasNode("injected-bare"), false, `preset=${preset}`);
    assert.equal(result.hasEdge("e-bare"), false, `preset=${preset}`);
  }
});

test("filtering never mutates the input graph", () => {
  const graph = layeredGraph();
  applyLayerFilter(graph, "business", false);
  assert.equal(graph.hasNode("policy-class"), true);
  assert.equal(graph.hasEdge("e-schema"), true);
});

test("dropping a node removes its incident edges (endpoint consistency)", () => {
  // ontology preset drops contract-1, so e-biz/e-inferred must vanish with it
  const result = applyLayerFilter(layeredGraph(), "ontology", true)!;
  assert.equal(result.hasEdge("e-biz"), false);
  assert.equal(result.hasEdge("e-inferred"), false);
  assert.equal(result.hasEdge("e-schema"), true);
});

test("nodeVisibleInPreset answers selection-clearing queries synchronously", () => {
  const graph = layeredGraph();
  assert.equal(nodeVisibleInPreset(graph, "contract-1", "business"), true);
  assert.equal(nodeVisibleInPreset(graph, "contract-1", "ontology"), false);
  assert.equal(nodeVisibleInPreset(graph, "policy-class", "ontology"), true);
  assert.equal(nodeVisibleInPreset(graph, "rules-lib", "all"), true);
  assert.equal(nodeVisibleInPreset(graph, "rules-lib", "business"), false);
  assert.equal(nodeVisibleInPreset(graph, "injected-bare", "all"), false);
  assert.equal(nodeVisibleInPreset(graph, "missing-node", "all"), false);
});
