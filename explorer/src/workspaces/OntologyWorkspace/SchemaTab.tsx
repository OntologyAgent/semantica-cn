import { useEffect, useMemo, useState } from "react";
import { useTranslation } from "react-i18next";

import {
  buildClassTree,
  buildPropertyCards,
  type SchemaClassNode,
  type SchemaGraphNode,
  type SchemaGraphEdge,
} from "./schemaTabModel";

type GraphNodesResponse = { nodes: SchemaGraphNode[]; total?: number };
type GraphEdgesResponse = { edges: SchemaGraphEdge[]; total?: number };

const FETCH_LIMIT = 5000;

function ClassTreeNode({
  entry,
  depth,
  selectedUri,
  onSelect,
}: {
  entry: SchemaClassNode;
  depth: number;
  selectedUri: string | null;
  onSelect: (uri: string) => void;
}) {
  const [expanded, setExpanded] = useState(depth < 1);
  const hasChildren = entry.children.length > 0;
  const selected = selectedUri === entry.uri;
  return (
    <div>
      <div style={{ display: "flex", alignItems: "center", gap: 4, paddingLeft: depth * 14 }}>
        {hasChildren ? (
          <button
            type="button"
            onClick={() => setExpanded((current) => !current)}
            style={{ background: "none", border: "none", color: "#8b949e", cursor: "pointer", fontSize: 11, padding: "2px 4px" }}
            aria-expanded={expanded}
          >
            {expanded ? "▾" : "▸"}
          </button>
        ) : (
          <span style={{ display: "inline-block", width: 18 }} />
        )}
        <button
          type="button"
          onClick={() => onSelect(entry.uri)}
          style={{
            background: selected ? "rgba(121,192,255,0.12)" : "transparent",
            border: selected ? "1px solid rgba(121,192,255,0.4)" : "1px solid transparent",
            borderRadius: 6,
            color: selected ? "#79c0ff" : "#c9d1d9",
            cursor: "pointer",
            fontSize: 12,
            padding: "2px 8px",
            textAlign: "left",
          }}
          title={entry.uri}
        >
          {entry.label}
        </button>
      </div>
      {expanded && hasChildren
        ? entry.children.map((child) => (
            <ClassTreeNode
              key={`${entry.uri}>${child.uri}`}
              entry={child}
              depth={depth + 1}
              selectedUri={selectedUri}
              onSelect={onSelect}
            />
          ))
        : null}
    </div>
  );
}

function PropertyCardRow({ label, value }: { label: string; value: string }) {
  return (
    <div style={{ display: "flex", gap: 8, fontSize: 11, lineHeight: 1.6 }}>
      <span style={{ color: "#8b949e", minWidth: 64 }}>{label}</span>
      <span style={{ color: "#c9d1d9", wordBreak: "break-all" }}>{value}</span>
    </div>
  );
}

export function SchemaTab() {
  const { t } = useTranslation();
  const [nodes, setNodes] = useState<SchemaGraphNode[] | null>(null);
  const [edges, setEdges] = useState<SchemaGraphEdge[] | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedClassUri, setSelectedClassUri] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const [nodesResponse, edgesResponse] = await Promise.all([
          fetch(`/api/graph/nodes?limit=${FETCH_LIMIT}`),
          fetch(`/api/graph/edges?limit=${FETCH_LIMIT}`),
        ]);
        if (!nodesResponse.ok || !edgesResponse.ok) {
          throw new Error(`graph fetch failed (${nodesResponse.status}/${edgesResponse.status})`);
        }
        const nodesData = (await nodesResponse.json()) as GraphNodesResponse;
        const edgesData = (await edgesResponse.json()) as GraphEdgesResponse;
        if (!cancelled) {
          setNodes(nodesData.nodes ?? []);
          setEdges(edgesData.edges ?? []);
        }
      } catch (cause) {
        if (!cancelled) {
          setError(cause instanceof Error ? cause.message : String(cause));
        }
      }
    };
    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  const classTree = useMemo(
    () => (nodes && edges ? buildClassTree(nodes, edges) : []),
    [nodes, edges],
  );
  const propertyCards = useMemo(
    () => (nodes && edges ? buildPropertyCards(nodes, edges) : []),
    [nodes, edges],
  );
  const visibleCards = useMemo(() => {
    if (!selectedClassUri) {
      return propertyCards;
    }
    return propertyCards.filter(
      (card) => card.domains.includes(selectedClassUri) || card.ranges.includes(selectedClassUri),
    );
  }, [propertyCards, selectedClassUri]);

  if (error) {
    return <div style={{ padding: 24, color: "#f85149", fontSize: 13 }}>{error}</div>;
  }
  if (nodes === null || edges === null) {
    return <div style={{ padding: 24, color: "#8b949e", fontSize: 13 }}>{t("ontologyHub.schema.loading")}</div>;
  }
  if (classTree.length === 0 && propertyCards.length === 0) {
    return <div style={{ padding: 24, color: "#8b949e", fontSize: 13 }}>{t("ontologyHub.schema.empty")}</div>;
  }

  return (
    <div style={{ display: "flex", height: "100%", minHeight: 0 }}>
      <div style={{ width: 300, flexShrink: 0, overflowY: "auto", borderRight: "1px solid rgba(88,166,255,0.1)", padding: "12px 10px" }}>
        <div style={{ color: "#8b949e", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.6, marginBottom: 10 }}>
          {t("ontologyHub.schema.treeTitle")}
        </div>
        {classTree.map((entry) => (
          <ClassTreeNode
            key={entry.uri}
            entry={entry}
            depth={0}
            selectedUri={selectedClassUri}
            onSelect={(uri) => setSelectedClassUri((current) => (current === uri ? null : uri))}
          />
        ))}
      </div>
      <div style={{ flex: 1, overflowY: "auto", padding: "12px 16px" }}>
        <div style={{ color: "#8b949e", fontSize: 11, textTransform: "uppercase", letterSpacing: 0.6, marginBottom: 10 }}>
          {selectedClassUri
            ? t("ontologyHub.schema.filteredTitle", { count: visibleCards.length })
            : t("ontologyHub.schema.propertiesTitle", { count: propertyCards.length })}
        </div>
        {selectedClassUri ? (
          <button
            type="button"
            onClick={() => setSelectedClassUri(null)}
            style={{
              marginBottom: 10, padding: "3px 10px", borderRadius: 999, fontSize: 12, cursor: "pointer",
              color: "#79c0ff", background: "rgba(121,192,255,0.12)", border: "1px solid rgba(121,192,255,0.4)",
            }}
          >
            {t("ontologyHub.schema.clearFilter")}
          </button>
        ) : null}
        {visibleCards.map((card) => (
          <div
            key={card.uri}
            style={{
              border: "1px solid rgba(88,166,255,0.15)",
              borderRadius: 8,
              padding: "10px 14px",
              marginBottom: 10,
              background: "rgba(121,192,255,0.03)",
            }}
          >
            <div style={{ display: "flex", alignItems: "baseline", gap: 8, marginBottom: 6 }}>
              <span style={{ color: "#d2a8ff", fontSize: 13, fontWeight: 600 }}>{card.label}</span>
              <span style={{ color: "#8b949e", fontSize: 10 }}>{card.kind}</span>
              {card.asciiId ? (
                <span
                  style={{
                    color: "#79c0ff", fontSize: 10, padding: "1px 7px", borderRadius: 999,
                    border: "1px solid rgba(121,192,255,0.35)", background: "rgba(121,192,255,0.08)",
                  }}
                  title={t("ontologyHub.schema.fieldNotation")}
                >
                  {card.asciiId}
                </span>
              ) : null}
            </div>
            <PropertyCardRow label={t("ontologyHub.schema.fieldDomain")} value={card.domains.length ? card.domains.join(", ") : "—"} />
            <PropertyCardRow label={t("ontologyHub.schema.fieldRange")} value={card.ranges.length ? card.ranges.join(", ") : "—"} />
            {card.inverseOf.length
              ? <PropertyCardRow label={t("ontologyHub.schema.fieldInverse")} value={card.inverseOf.join(", ")} />
              : null}
            {card.comment ? <PropertyCardRow label={t("ontologyHub.schema.fieldComment")} value={card.comment} /> : null}
          </div>
        ))}
      </div>
    </div>
  );
}
