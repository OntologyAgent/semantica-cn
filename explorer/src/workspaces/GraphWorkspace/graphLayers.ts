import type Graph from "graphology";

/**
 * Layer switching for the unified single-instance graph view.
 *
 * Data contract (unified panorama export):
 * - node.properties.layer ∈ {instance, class, property, rules}
 * - edge.properties.layer ∈ {business, schema, inferred}
 *
 * Layerless nodes/edges (ontology-load injections that have not merged with a
 * mounted node sharing the same az: URI) stay hidden while the graph carries
 * any layer data; graphs without layer data bypass filtering entirely so
 * plain datasets render exactly as before.
 */

export type LayerPreset = "all" | "business" | "ontology";

const PRESET_NODE_LAYERS: Record<LayerPreset, ((layer: string) => boolean)> = {
  // "all" shows every node that carries any layer value, including rules.
  all: (layer) => layer.length > 0,
  business: (layer) => layer === "instance",
  ontology: (layer) => layer === "class" || layer === "property",
};

const PRESET_EDGE_LAYERS: Record<LayerPreset, Set<string>> = {
  // inferred edges are governed solely by their dedicated toggle, so "all"
  // with the toggle off means contract facts plus schema structure.
  all: new Set(["business", "schema"]),
  business: new Set(["business"]),
  ontology: new Set(["schema"]),
};

function nodeLayer(graph: Graph, nodeId: string): string {
  const properties = graph.getNodeAttribute(nodeId, "properties") as Record<string, unknown> | undefined;
  const layer = properties?.layer;
  return typeof layer === "string" ? layer : "";
}

function edgeLayer(graph: Graph, edgeId: string): string {
  const properties = graph.getEdgeAttribute(edgeId, "properties") as Record<string, unknown> | undefined;
  const layer = properties?.layer;
  return typeof layer === "string" ? layer : "";
}

export function graphHasLayerData(graph: Graph): boolean {
  return graph.someNode((nodeId) => nodeLayer(graph, nodeId) !== "");
}

/** Whether a node survives the given preset (edges never affect node visibility). */
export function nodeVisibleInPreset(graph: Graph, nodeId: string, preset: LayerPreset): boolean {
  if (!graph.hasNode(nodeId)) {
    return false;
  }
  return PRESET_NODE_LAYERS[preset](nodeLayer(graph, nodeId));
}

/**
 * Copy the display graph and drop everything outside the preset.
 *
 * Returns null when the graph carries no layer data at all — callers keep the
 * original graph in that case (zero-regression bypass for plain datasets).
 * Drop order is nodes first (graphology removes incident edges with them),
 * then remaining edges whose layer is out of scope or layerless.
 */
export function applyLayerFilter(
  graph: Graph,
  preset: LayerPreset,
  inferredEdgesEnabled: boolean,
): Graph | null {
  if (!graphHasLayerData(graph)) {
    return null;
  }

  const nodeAllowed = PRESET_NODE_LAYERS[preset];
  const edgeLayers = new Set(PRESET_EDGE_LAYERS[preset]);
  if (inferredEdgesEnabled) {
    edgeLayers.add("inferred");
  }

  const filtered = graph.copy();
  for (const nodeId of filtered.nodes()) {
    if (!nodeAllowed(nodeLayer(filtered, nodeId))) {
      filtered.dropNode(nodeId);
    }
  }
  for (const edgeId of filtered.edges()) {
    if (!edgeLayers.has(edgeLayer(filtered, edgeId))) {
      filtered.dropEdge(edgeId);
    }
  }
  return filtered;
}
