import type { CSSProperties } from "react";
import { useTranslation } from "react-i18next";
import i18next from "i18next";
import type { TFunction } from "i18next";

import type { GraphPlugin, GraphPluginContext } from "./types";

const NEIGHBORHOOD_PANEL_ID = "neighborhood-panel";
const MAX_NEIGHBORS = 10;

function maxWeightBetween(graphRef: any, sourceId: string, targetId: string): number {
  let weight = 0;
  graphRef.forEachDirectedEdge(sourceId, targetId, (_edgeId: string, attrs: { weight?: number }) => {
    weight = Math.max(weight, Number(attrs.weight ?? 0));
  });
  return weight;
}

function formatNeighborMeta(
  neighbor: { nodeType: string; degree: number; weight: number },
  t: TFunction,
) {
  const parts = [neighbor.nodeType, t("graph.neighborhood.metaDegree", { degree: neighbor.degree })];
  if (neighbor.weight > 0) {
    parts.push(t("graph.edge.weight", { weight: neighbor.weight.toFixed(2) }));
  }
  return parts.join(" · ");
}

// Panel body is a real component so its strings subscribe to languageChanged
// and refresh instantly — the panel descriptor itself is memoized by the host
// (collectPluginPanels) and would otherwise pin translations at memo time.
// eslint-disable-next-line react-refresh/only-export-components -- panel body stays beside its plugin definition
function NeighborhoodPanelContent({
  context,
  selected,
}: {
  context: GraphPluginContext;
  selected: ReturnType<GraphPluginContext["getSelectedNodeState"]>;
}) {
  const { t } = useTranslation();
  if (!selected) {
    return <div style={emptyTextStyle}>{t("graph.neighborhood.selectNodePrompt")}</div>;
  }

  const neighbors = context.graph
    .neighbors(selected.id)
    .map((neighborId) => {
      const attrs = context.graph.getNodeAttributes(neighborId);
      const weight = Math.max(
        maxWeightBetween(context.graph, selected.id, neighborId),
        maxWeightBetween(context.graph, neighborId, selected.id),
      );
      return {
        id: neighborId,
        label: String(attrs.label || neighborId),
        nodeType: String(attrs.nodeType || t("graph.inspector.entityFallback")),
        color: String(attrs.baseColor || attrs.color || context.theme.palette.semantic[0]),
        weight,
        degree: context.graph.degree(neighborId),
      };
    })
    .sort((left, right) => {
      if (right.weight !== left.weight) {
        return right.weight - left.weight;
      }
      if (right.degree !== left.degree) {
        return right.degree - left.degree;
      }
      return left.label.localeCompare(right.label);
    })
    .slice(0, MAX_NEIGHBORS);
  const hiddenNeighborCount = context.getDisplayState().selectedCollapsedNeighborIds.length;
  const aggregatedEdgeCount = context.displayGraph
    .edges()
    .map((edgeId) => context.displayGraph.getEdgeAttributes(edgeId) as { isAggregated?: boolean })
    .filter((attrs) => attrs.isAggregated).length;

  return (
    <div style={panelBodyStyle}>
      <div style={panelEyebrowStyle}>{selected.label}</div>
      <div style={summaryStyle}>
        {t("graph.neighborhood.directNeighborsInFullGraph", { count: selected.neighborCount.toLocaleString() })}
      </div>
      <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>
        <button
          type="button"
          onClick={() => context.dispatchAction({ type: "collapseNeighborhood" })}
          disabled={!selected.canCollapseNeighborhood || selected.isNeighborhoodCollapsed}
          style={controlButtonStyle}
        >
          {t("graph.neighborhood.collapseNeighborhood")}
        </button>
        <button
          type="button"
          onClick={() => context.dispatchAction({ type: "expandNeighborhood" })}
          disabled={!selected.isNeighborhoodCollapsed}
          style={controlButtonStyle}
        >
          {t("graph.neighborhood.expandNeighborhood")}
        </button>
      </div>
      {hiddenNeighborCount > 0 ? (
        <div style={summaryStyle}>
          {t("graph.neighborhood.hiddenNeighborsCollapsed", { count: hiddenNeighborCount.toLocaleString() })}
        </div>
      ) : null}
      {aggregatedEdgeCount > 0 ? (
        <div style={summaryStyle}>
          {aggregatedEdgeCount === 1
            ? t("graph.neighborhood.aggregatedBundlesOne", { count: aggregatedEdgeCount.toLocaleString() })
            : t("graph.neighborhood.aggregatedBundlesMany", { count: aggregatedEdgeCount.toLocaleString() })}
        </div>
      ) : null}
      {neighbors.length ? (
        <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          {neighbors.map((neighbor) => (
            <button
              key={neighbor.id}
              type="button"
              onClick={() => context.dispatchAction({ type: "selectNode", nodeId: neighbor.id })}
              style={neighborButtonStyle}
            >
              <span
                style={{
                  ...swatchStyle,
                  background: neighbor.color,
                  boxShadow: `0 0 16px ${neighbor.color}40`,
                }}
              />
              <div style={{ minWidth: 0, flex: 1, textAlign: "left" }}>
                <div style={rowTitleStyle}>{neighbor.label}</div>
                <div style={rowMetaStyle}>{formatNeighborMeta(neighbor, t)}</div>
              </div>
            </button>
          ))}
        </div>
      ) : (
        <div style={emptyTextStyle}>{t("graph.neighborhood.noNeighbors")}</div>
      )}
    </div>
  );
}

export const neighborhoodPanelPlugin: GraphPlugin = {
  id: "neighborhood-panel",
  mount: () => {},
  unmount: () => {},
  onStateChange: () => {},
  toolbarItems: (context) => [
    {
      id: "neighborhood-toggle",
      label: "Neighbors",
      title: "Toggle neighborhood panel",
      active: context.isPanelOpen(NEIGHBORHOOD_PANEL_ID),
      order: 30,
      onClick: () => context.dispatchAction({ type: "togglePanel", panelId: NEIGHBORHOOD_PANEL_ID }),
    },
  ],
  renderPanel: (context) => {
    const selected = context.getSelectedNodeState();

    return {
      id: NEIGHBORHOOD_PANEL_ID,
      title: i18next.t("graph.neighborhood.panelTitle"),
      placement: "bottom",
      order: 20,
      defaultOpen: false,
      preferredWidth: 360,
      preferredHeight: 260,
      content: <NeighborhoodPanelContent context={context} selected={selected} />,
    };
  },
};

const panelBodyStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 12,
};

const panelEyebrowStyle: CSSProperties = {
  color: "#f3f7fd",
  fontSize: 14,
  fontWeight: 700,
};

const summaryStyle: CSSProperties = {
  color: "#8ea4be",
  fontSize: 12,
  lineHeight: 1.5,
};

const neighborButtonStyle: CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 10,
  width: "100%",
  padding: "8px 10px",
  background: "rgba(255,255,255,0.025)",
  border: "1px solid rgba(255,255,255,0.06)",
  borderRadius: 12,
  cursor: "pointer",
};

const controlButtonStyle: CSSProperties = {
  padding: "7px 10px",
  background: "rgba(255,255,255,0.03)",
  border: "1px solid rgba(255,255,255,0.08)",
  borderRadius: 10,
  color: "#dce7f4",
  cursor: "pointer",
  fontSize: 12,
};

const swatchStyle: CSSProperties = {
  width: 10,
  height: 10,
  borderRadius: 999,
  flexShrink: 0,
};

const rowTitleStyle: CSSProperties = {
  color: "#f3f7fd",
  fontSize: 13,
  fontWeight: 600,
  overflow: "hidden",
  textOverflow: "ellipsis",
  whiteSpace: "nowrap",
};

const rowMetaStyle: CSSProperties = {
  color: "#8ea4be",
  fontSize: 12,
};

const emptyTextStyle: CSSProperties = {
  color: "#8ea4be",
  fontSize: 12,
  lineHeight: 1.5,
};
