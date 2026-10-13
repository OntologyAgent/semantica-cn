/**
 * Pure model for the Ontology Hub schema tab (class tree + property
 * signatures). Everything is derived from graph nodes/edges already injected
 * by ontology-load: classes are owl:Class nodes linked by rdfs:subClassOf,
 * properties are owl:*Property nodes with rdfs:domain/rdfs:range edges.
 */

export type SchemaGraphNode = {
  id: string;
  type?: string;
  content?: string;
  properties?: Record<string, unknown>;
};

export type SchemaGraphEdge = {
  source: string;
  target: string;
  type: string;
};

export type SchemaClassNode = {
  uri: string;
  label: string;
  children: SchemaClassNode[];
};

export type SchemaPropertyCard = {
  uri: string;
  label: string;
  kind: string;
  domains: string[];
  ranges: string[];
  inverseOf: string[];
  asciiId?: string;
  comment?: string;
};

const CLASS_TYPES = new Set(["owl:Class", "rdfs:Class"]);
const PROPERTY_TYPES = new Set([
  "owl:ObjectProperty",
  "owl:DatatypeProperty",
  "owl:AnnotationProperty",
  "rdf:Property",
]);

const SIGNATURE_EDGES = new Set(["rdfs:domain", "rdfs:range", "owl:inverseOf"]);

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

export function classDisplayLabel(node: SchemaGraphNode): string {
  // content that merely echoes the id carries no label information.
  const content = typeof node.content === "string" && node.content.trim() && node.content !== node.id
    ? node.content
    : undefined;
  return (
    text(node.properties, ["skos:prefLabel", "rdfs:label"])
    || content
    || uriTail(node.id)
  );
}

function isClass(node: SchemaGraphNode): boolean {
  return node.type !== undefined && CLASS_TYPES.has(node.type);
}

function isProperty(node: SchemaGraphNode): boolean {
  return node.type !== undefined && PROPERTY_TYPES.has(node.type);
}

export function buildClassTree(nodes: SchemaGraphNode[], edges: SchemaGraphEdge[]): SchemaClassNode[] {
  const classNodes = new Map(nodes.filter(isClass).map((node) => [node.id, node]));
  const parents = new Map<string, Set<string>>();
  const children = new Map<string, string[]>();
  for (const edge of edges) {
    if (edge.type !== "rdfs:subClassOf") {
      continue;
    }
    if (!classNodes.has(edge.source) || !classNodes.has(edge.target) || edge.source === edge.target) {
      continue;
    }
    if (!parents.has(edge.source)) {
      parents.set(edge.source, new Set());
    }
    parents.get(edge.source)!.add(edge.target);
    if (!children.has(edge.target)) {
      children.set(edge.target, []);
    }
    children.get(edge.target)!.push(edge.source);
  }

  // Nodes reachable from parentless roots stay nested; cycle members (and
  // nodes whose ancestry only loops) are promoted to roots so nothing hangs
  // or disappears.
  const rooted = new Set<string>();
  const queue = [...classNodes.keys()].filter((uri) => !parents.has(uri));
  while (queue.length) {
    const uri = queue.shift()!;
    if (rooted.has(uri)) {
      continue;
    }
    rooted.add(uri);
    for (const child of children.get(uri) ?? []) {
      queue.push(child);
    }
  }

  const buildNode = (uri: string, ancestors: Set<string>): SchemaClassNode => {
    const node = classNodes.get(uri)!;
    const childNodes: SchemaClassNode[] = [];
    for (const child of children.get(uri) ?? []) {
      if (ancestors.has(child)) {
        continue; // cycle back-edge: rendered from the promoted root instead
      }
      childNodes.push(buildNode(child, new Set(ancestors).add(uri)));
    }
    childNodes.sort((left, right) => left.label.localeCompare(right.label));
    return { uri, label: classDisplayLabel(node), children: childNodes };
  };

  const roots = [...classNodes.keys()]
    .filter((uri) => rooted.has(uri) ? !parents.has(uri) : true)
    .sort();
  return roots.map((uri) => buildNode(uri, new Set()));
}

export function buildPropertyCards(
  nodes: SchemaGraphNode[],
  edges: SchemaGraphEdge[],
): SchemaPropertyCard[] {
  const propertyNodes = nodes.filter(isProperty);
  const signatures = new Map<string, { domains: string[]; ranges: string[]; inverseOf: string[] }>();
  const ensure = (uri: string) => {
    if (!signatures.has(uri)) {
      signatures.set(uri, { domains: [], ranges: [], inverseOf: [] });
    }
    return signatures.get(uri)!;
  };
  for (const edge of edges) {
    if (!SIGNATURE_EDGES.has(edge.type)) {
      continue;
    }
    const entry = ensure(edge.source);
    if (edge.type === "rdfs:domain") {
      entry.domains.push(edge.target);
    } else if (edge.type === "rdfs:range") {
      entry.ranges.push(edge.target);
    } else {
      entry.inverseOf.push(edge.target);
    }
  }

  return propertyNodes
    .map((node) => {
      const entry = signatures.get(node.id) ?? { domains: [], ranges: [], inverseOf: [] };
      return {
        uri: node.id,
        label: classDisplayLabel(node),
        kind: node.type ?? "rdf:Property",
        domains: [...new Set(entry.domains)].sort(),
        ranges: [...new Set(entry.ranges)].sort(),
        inverseOf: [...new Set(entry.inverseOf)].sort(),
        asciiId: text(node.properties, ["az:asciiId", "skos:notation"]),
        comment: text(node.properties, ["rdfs:comment", "skos:definition"]),
      };
    })
    .sort((left, right) => left.label.localeCompare(right.label));
}
