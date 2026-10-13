/**
 * Convert the session graph's business layer into reasoner facts for the
 * Reasoning Playground ("pull facts from graph" button).
 *
 * Predicate transliteration: an edge type (often a Chinese prefLabel) maps
 * to the ASCII identifier carried by the matching owl:*Property schema
 * node (az:asciiId, falling back to skos:notation); unmapped types pass
 * through verbatim. Subjects/objects use node display labels.
 */

export type FactGraphNode = {
  id: string;
  type?: string;
  content?: string;
  properties?: Record<string, unknown>;
};

export type FactGraphEdge = {
  source: string;
  target: string;
  type: string;
  properties?: Record<string, unknown>;
};

const PROPERTY_TYPES = new Set([
  "owl:ObjectProperty",
  "owl:DatatypeProperty",
  "owl:AnnotationProperty",
  "rdf:Property",
]);

function text(properties: Record<string, unknown> | undefined, keys: string[]): string | undefined {
  for (const key of keys) {
    const value = properties?.[key];
    if (typeof value === "string" && value.trim()) {
      return value;
    }
  }
  return undefined;
}

function uriTail(uri: string): string {
  const index = Math.max(uri.lastIndexOf("/"), uri.lastIndexOf("#"), uri.lastIndexOf(":"));
  return index >= 0 && index < uri.length - 1 ? uri.slice(index + 1) : uri;
}

function displayLabel(node: FactGraphNode): string {
  // content that merely echoes the id carries no label information.
  const content = typeof node.content === "string" && node.content.trim() && node.content !== node.id
    ? node.content
    : undefined;
  return text(node.properties, ["skos:prefLabel", "rdfs:label"]) || content || uriTail(node.id);
}

function asciiIdOf(node: FactGraphNode): string | undefined {
  return text(node.properties, ["az:asciiId", "skos:notation"]);
}

export function businessEdgesToFacts(nodes: FactGraphNode[], edges: FactGraphEdge[]): string[] {
  const labels = new Map(nodes.map((node) => [node.id, displayLabel(node)]));
  const asciiByEdgeType = new Map<string, string>();
  for (const node of nodes) {
    if (!node.type || !PROPERTY_TYPES.has(node.type)) {
      continue;
    }
    const asciiId = asciiIdOf(node);
    if (!asciiId) {
      continue;
    }
    // Match edge types spelled as the property's prefLabel or its label.
    for (const key of ["skos:prefLabel", "rdfs:label"]) {
      const spelling = text(node.properties, [key]);
      if (spelling && !asciiByEdgeType.has(spelling)) {
        asciiByEdgeType.set(spelling, asciiId);
      }
    }
  }

  const labelOf = (id: string) => labels.get(id) ?? uriTail(id);
  return edges
    .filter((edge) => edge.properties?.layer === "business")
    .map((edge) => {
      const predicate = asciiByEdgeType.get(edge.type) ?? edge.type;
      return `${predicate}(${labelOf(edge.source)}, ${labelOf(edge.target)})`;
    });
}
