import type { CSSProperties } from "react";
import { useTranslation } from "react-i18next";
import i18next from "i18next";
import type { TFunction } from "i18next";

import type { GraphPlugin, GraphPluginContext } from "./types";

const TEMPORAL_PANEL_ID = "temporal-panel";

function formatTemporalLabel(value: Date | null, t: TFunction) {
  if (!value) {
    return t("graph.temporalOverlay.noTimeSelected");
  }
  return `${value.getFullYear()}/${String(value.getMonth() + 1).padStart(2, "0")}`;
}

// Overlay chip body is a real component so its strings subscribe to
// languageChanged — the host memoizes plugin overlay elements and would
// otherwise pin translations at memo time.
// eslint-disable-next-line react-refresh/only-export-components -- overlay chip stays beside its plugin definition
function TemporalOverlayChip({
  currentTime,
  activeNodeCount,
}: {
  currentTime: Date;
  activeNodeCount: number | null | undefined;
}) {
  const { t } = useTranslation();
  return (
    <div style={overlayChipStyle}>
      <span style={overlayChipTitleStyle}>{t("graph.temporalOverlay.overlayChipTitle")}</span>
      <span>{formatTemporalLabel(currentTime, t)}</span>
      {typeof activeNodeCount === "number" ? (
        <span style={overlayChipCountStyle}>
          {t("graph.hud.activeCount", { count: activeNodeCount.toLocaleString() })}
        </span>
      ) : null}
    </div>
  );
}

// Panel body is a real component so its strings subscribe to languageChanged
// and refresh instantly — the panel descriptor itself is memoized by the host
// (collectPluginPanels) and would otherwise pin translations at memo time.
// eslint-disable-next-line react-refresh/only-export-components -- panel body stays beside its plugin definition
function TemporalPanelContent({ temporal }: { temporal: ReturnType<GraphPluginContext["getTemporalState"]> }) {
  const { t } = useTranslation();
  return (
    <div style={panelBodyStyle}>
      <div style={panelEyebrowStyle}>{t("graph.temporalOverlay.eyebrow")}</div>
      <div style={detailRowStyle}>
        <span style={detailLabelStyle}>{t("graph.temporalOverlay.labelCurrent")}</span>
        <span style={detailValueStyle}>{formatTemporalLabel(temporal?.currentTime ?? null, t)}</span>
      </div>
      <div style={detailRowStyle}>
        <span style={detailLabelStyle}>{t("graph.temporalOverlay.labelBounds")}</span>
        <span style={detailValueStyle}>
          {(temporal?.minDate ?? "1970")} → {(temporal?.maxDate ?? "now")}
        </span>
      </div>
      <div style={detailRowStyle}>
        <span style={detailLabelStyle}>{t("graph.temporalOverlay.labelActiveNodes")}</span>
        <span style={detailValueStyle}>
          {typeof temporal?.activeNodeCount === "number"
            ? temporal.activeNodeCount.toLocaleString()
            : t("graph.temporalOverlay.valueAll")}
        </span>
      </div>
    </div>
  );
}

export const temporalOverlayPlugin: GraphPlugin = {
  id: "temporal-overlay",
  mount: () => {},
  unmount: () => {},
  onStateChange: () => {},
  toolbarItems: (context) => [
    {
      id: "temporal-toggle",
      label: "Temporal",
      title: "Toggle temporal context panel",
      active: context.isPanelOpen(TEMPORAL_PANEL_ID),
      order: 40,
      onClick: () => context.dispatchAction({ type: "togglePanel", panelId: TEMPORAL_PANEL_ID }),
    },
  ],
  renderOverlay: (context) => {
    const temporal = context.getTemporalState();
    if (!temporal?.currentTime) {
      return null;
    }

    return {
      id: "temporal-overlay-chip",
      layer: 1,
      order: 10,
      element: (
        <TemporalOverlayChip
          currentTime={temporal.currentTime}
          activeNodeCount={temporal.activeNodeCount}
        />
      ),
    };
  },
  renderPanel: (context) => {
    if (!context.isPanelOpen(TEMPORAL_PANEL_ID)) {
      return null;
    }

    const temporal = context.getTemporalState();
    return {
      id: TEMPORAL_PANEL_ID,
      title: i18next.t("graph.temporalOverlay.panelTitle"),
      placement: "bottom",
      order: 30,
      defaultOpen: false,
      preferredWidth: 320,
      preferredHeight: 220,
      content: <TemporalPanelContent temporal={temporal} />,
    };
  },
};

const overlayChipStyle: CSSProperties = {
  position: "absolute",
  left: 140,
  bottom: 26,
  display: "inline-flex",
  alignItems: "center",
  gap: 10,
  padding: "8px 12px",
  borderRadius: 999,
  border: "1px solid rgba(127, 208, 255, 0.18)",
  background: "linear-gradient(135deg, rgba(6, 15, 27, 0.88), rgba(11, 22, 39, 0.76))",
  boxShadow: "0 12px 30px rgba(0, 0, 0, 0.28)",
  color: "#dce9f8",
  fontSize: 11,
  letterSpacing: "0.05em",
  textTransform: "uppercase",
  pointerEvents: "none",
};

const overlayChipTitleStyle: CSSProperties = {
  color: "#7fc6ff",
  fontWeight: 700,
};

const overlayChipCountStyle: CSSProperties = {
  color: "#8ea4be",
};

const panelBodyStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 10,
};

const panelEyebrowStyle: CSSProperties = {
  color: "#8ea4be",
  fontSize: 11,
  fontWeight: 700,
  letterSpacing: "0.08em",
  textTransform: "uppercase",
};

const detailRowStyle: CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  gap: 16,
  padding: "8px 10px",
  borderRadius: 12,
  border: "1px solid rgba(255,255,255,0.06)",
  background: "rgba(255,255,255,0.025)",
};

const detailLabelStyle: CSSProperties = {
  color: "#8ea4be",
  fontSize: 12,
};

const detailValueStyle: CSSProperties = {
  color: "#f3f7fd",
  fontSize: 12,
  fontWeight: 600,
};
