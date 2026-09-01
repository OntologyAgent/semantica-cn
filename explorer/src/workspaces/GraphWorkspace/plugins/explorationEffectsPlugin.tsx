import type { CSSProperties } from "react";
import { useTranslation } from "react-i18next";
import i18next from "i18next";
import type { TFunction } from "i18next";

import type {
  GraphDiagnosticsSnapshot,
  GraphEffectAvailability,
  GraphEffectToggle,
} from "../types";
import type en from "../../../i18n/locales/en.json";
import type { GraphPlugin, GraphPluginContext } from "./types";

type TranslationKey = keyof typeof en.translation;

const EFFECTS_PANEL_ID = "effects-panel";

type EffectRowConfig = {
  key: GraphEffectToggle;
  labelKey: TranslationKey;
  descriptionKey: TranslationKey;
};

const EFFECT_ROWS: EffectRowConfig[] = [
  {
    key: "pathPulseEnabled",
    labelKey: "graph.effects.rowPathPulse.label",
    descriptionKey: "graph.effects.rowPathPulse.description",
  },
  {
    key: "pathFlowEnabled",
    labelKey: "graph.effects.rowPathFlow.label",
    descriptionKey: "graph.effects.rowPathFlow.description",
  },
  {
    key: "lensEnabled",
    labelKey: "graph.effects.rowLens.label",
    descriptionKey: "graph.effects.rowLens.description",
  },
  {
    key: "edgeLabelsEnabled",
    labelKey: "graph.effects.rowEdgeLabels.label",
    descriptionKey: "graph.effects.rowEdgeLabels.description",
  },
  {
    key: "legendEnabled",
    labelKey: "graph.effects.rowSemanticLegend.label",
    descriptionKey: "graph.effects.rowSemanticLegend.description",
  },
];

// Maps the effect toggle keys rendered by this plugin to their corresponding
// availability keys in GraphDiagnosticsSnapshot["effectAvailability"]. Kept
// local because this plugin only renders a subset of all effects.
const EFFECT_AVAILABILITY_KEYS: Partial<Record<GraphEffectToggle, keyof GraphDiagnosticsSnapshot["effectAvailability"]>> = {
  pathPulseEnabled: "pathPulse",
  pathFlowEnabled: "pathFlow",
  lensEnabled: "lens",
  edgeLabelsEnabled: "edgeLabels",
  legendEnabled: "legend",
};

function renderAvailabilityText(availability: GraphEffectAvailability, t: TFunction) {
  if (availability.available) {
    if (typeof availability.visibleSegments === "number" && typeof availability.segmentCap === "number") {
      return t("graph.effects.segmentsCount", {
        reason: availability.reason,
        count: availability.visibleSegments,
        total: availability.segmentCap,
      });
    }
    return availability.reason;
  }

  return availability.detail ? `${availability.reason} · ${availability.detail}` : availability.reason;
}

function collectLegendItems(context: Parameters<NonNullable<GraphPlugin["renderPanel"]>>[0]) {
  const groups = new Map<string, { count: number; color: string }>();
  context.graph.forEachNode((_nodeId, attrs) => {
    const semanticGroup = String(attrs.semanticGroup || attrs.nodeType || "entity");
    const color = String(attrs.baseColor || context.theme.palette.semantic[0]);
    const current = groups.get(semanticGroup);
    groups.set(semanticGroup, {
      count: (current?.count ?? 0) + 1,
      color,
    });
  });

  return [...groups.entries()]
    .map(([group, data]) => ({ group, ...data }))
    .sort((left, right) => right.count - left.count)
    .slice(0, context.theme.effects.legend.maxGroups);
}

function EffectToggleRow({
  label,
  description,
  checked,
  availability,
  onToggle,
}: {
  label: string;
  description: string;
  checked: boolean;
  availability: GraphEffectAvailability;
  onToggle: () => void;
}) {
  const { t } = useTranslation();
  return (
    <div style={toggleRowStyle}>
      <div style={{ minWidth: 0, flex: 1 }}>
        <div style={rowTitleStyle}>{label}</div>
        <div style={rowDescriptionStyle}>{description}</div>
        <div style={rowMetaStyle}>{renderAvailabilityText(availability, t)}</div>
      </div>
      <button type="button" onClick={onToggle} style={checked ? toggleButtonActiveStyle : toggleButtonStyle}>
        {checked ? t("graph.effects.toggleOn") : t("graph.effects.toggleOff")}
      </button>
    </div>
  );
}

// Panel body is a real component so its strings subscribe to languageChanged
// and refresh instantly — the panel descriptor itself is memoized by the host
// (collectPluginPanels) and would otherwise pin translations at memo time.
// eslint-disable-next-line react-refresh/only-export-components -- panel body stays beside its plugin definition
function EffectsPanelContent({
  context,
  effectsState,
  diagnosticsSnapshot,
}: {
  context: GraphPluginContext;
  effectsState: ReturnType<GraphPluginContext["getEffectsState"]>;
  diagnosticsSnapshot: ReturnType<GraphPluginContext["getDiagnosticsSnapshot"]>;
}) {
  const { t } = useTranslation();
  const availability = diagnosticsSnapshot?.effectAvailability;
  const legendItems = effectsState.legendEnabled ? collectLegendItems(context) : [];

  return (
    <div style={panelBodyStyle}>
      <div style={panelEyebrowStyle}>{t("graph.effects.eyebrow")}</div>

      <div style={sectionStyle}>
        <div style={sectionTitleStyle}>{t("graph.effects.sectionPathAndFocus")}</div>
        {EFFECT_ROWS.map((row) => (
          <EffectToggleRow
            key={row.key}
            label={t(row.labelKey)}
            description={t(row.descriptionKey)}
            checked={effectsState[row.key]}
            availability={
              (EFFECT_AVAILABILITY_KEYS[row.key] !== undefined
                ? availability?.[EFFECT_AVAILABILITY_KEYS[row.key]!]
                : undefined) ?? {
                enabled: effectsState[row.key],
                available: false,
                reason: "Waiting for graph runtime",
              }
            }
            onToggle={() => context.dispatchAction({ type: "toggleEffect", effect: row.key })}
          />
        ))}
      </div>

      {effectsState.legendEnabled ? (
        <div style={sectionStyle}>
          <div style={sectionTitleStyle}>{t("graph.effects.sectionSemanticLegend")}</div>
          {legendItems.length ? (
            <div style={{ display: "flex", flexDirection: "column", gap: 8 }}>
              {legendItems.map((item) => (
                <div key={item.group} style={legendRowStyle}>
                  <span
                    style={{
                      ...legendSwatchStyle,
                      background: item.color,
                      boxShadow: `0 0 0 1px rgba(255,255,255,0.06), 0 0 14px ${item.color}40`,
                    }}
                  />
                  <div style={{ minWidth: 0, flex: 1 }}>
                    <div style={rowTitleStyle}>{item.group}</div>
                    <div style={rowMetaStyle}>{t("graph.effects.legendNodeCount", { count: item.count.toLocaleString() })}</div>
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div style={emptyTextStyle}>{t("graph.effects.legendEmpty")}</div>
          )}
        </div>
      ) : null}

      {import.meta.env.DEV ? (
        <div style={sectionStyle}>
          <div style={sectionTitleStyle}>{t("graph.effects.sectionDiagnostics")}</div>
          <EffectToggleRow
            label={t("graph.effects.devDiagnosticsLabel")}
            description={t("graph.effects.devDiagnosticsDescription")}
            checked={effectsState.diagnosticsEnabled}
            availability={
              availability?.diagnostics ?? {
                enabled: effectsState.diagnosticsEnabled,
                available: false,
                reason: "Waiting for graph runtime",
              }
            }
            onToggle={() => context.dispatchAction({ type: "toggleEffect", effect: "diagnosticsEnabled" })}
          />
          {effectsState.diagnosticsEnabled && diagnosticsSnapshot ? (
            <details style={detailsStyle}>
              <summary style={summaryStyle}>{t("graph.effects.runtimeSnapshot")}</summary>
              <pre style={diagnosticsPreStyle}>
                {JSON.stringify(diagnosticsSnapshot, null, 2)}
              </pre>
            </details>
          ) : null}
        </div>
      ) : null}
    </div>
  );
}

export const explorationEffectsPlugin: GraphPlugin = {
  id: "exploration-effects",
  mount: () => {},
  unmount: () => {},
  onStateChange: () => {},
  toolbarItems: (context) => [
    {
      id: "effects-toggle",
      label: "Effects",
      title: "Open exploration effects controls",
      active: context.isPanelOpen(EFFECTS_PANEL_ID),
      order: 18,
      onClick: () => context.dispatchAction({ type: "togglePanel", panelId: EFFECTS_PANEL_ID }),
    },
  ],
  renderPanel: (context) => {
    if (!context.isPanelOpen(EFFECTS_PANEL_ID)) {
      return null;
    }

    const effectsState = context.getEffectsState();
    const diagnosticsSnapshot = context.getDiagnosticsSnapshot();

    return {
      id: EFFECTS_PANEL_ID,
      title: i18next.t("graph.effects.panelTitle"),
      placement: "bottom",
      order: 8,
      defaultOpen: false,
      preferredWidth: 420,
      preferredHeight: 320,
      content: (
        <EffectsPanelContent
          context={context}
          effectsState={effectsState}
          diagnosticsSnapshot={diagnosticsSnapshot}
        />
      ),
    };
  },
};

const panelBodyStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 12,
};

const panelEyebrowStyle: CSSProperties = {
  color: "#8ea4be",
  fontSize: 11,
  fontWeight: 700,
  letterSpacing: "0.08em",
  textTransform: "uppercase",
};

const sectionStyle: CSSProperties = {
  display: "flex",
  flexDirection: "column",
  gap: 8,
  padding: "10px 12px",
  borderRadius: 14,
  border: "1px solid rgba(255,255,255,0.06)",
  background: "rgba(255,255,255,0.025)",
};

const sectionTitleStyle: CSSProperties = {
  color: "#dce9f8",
  fontSize: 12,
  fontWeight: 700,
};

const toggleRowStyle: CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 12,
  padding: "8px 0",
};

const rowTitleStyle: CSSProperties = {
  color: "#f3f7fd",
  fontSize: 13,
  fontWeight: 600,
};

const rowDescriptionStyle: CSSProperties = {
  color: "#a1b7cf",
  fontSize: 12,
  lineHeight: 1.45,
};

const rowMetaStyle: CSSProperties = {
  color: "#7fc6ff",
  fontSize: 11,
  lineHeight: 1.45,
};

const toggleButtonStyle: CSSProperties = {
  minWidth: 52,
  padding: "8px 10px",
  borderRadius: 999,
  border: "1px solid rgba(255,255,255,0.08)",
  background: "rgba(255,255,255,0.03)",
  color: "#cfe0f4",
  fontSize: 12,
  fontWeight: 700,
  cursor: "pointer",
};

const toggleButtonActiveStyle: CSSProperties = {
  ...toggleButtonStyle,
  background: "rgba(31, 111, 235, 0.24)",
  border: "1px solid rgba(127, 208, 255, 0.28)",
  color: "#eef6ff",
};

const legendRowStyle: CSSProperties = {
  display: "flex",
  alignItems: "center",
  gap: 10,
  padding: "8px 10px",
  borderRadius: 12,
  border: "1px solid rgba(255,255,255,0.06)",
  background: "rgba(255,255,255,0.025)",
};

const legendSwatchStyle: CSSProperties = {
  width: 10,
  height: 10,
  borderRadius: 999,
  flexShrink: 0,
};

const detailsStyle: CSSProperties = {
  borderRadius: 12,
  border: "1px solid rgba(255,255,255,0.05)",
  background: "rgba(0,0,0,0.14)",
  overflow: "hidden",
};

const summaryStyle: CSSProperties = {
  cursor: "pointer",
  padding: "10px 12px",
  color: "#c6d4e3",
  fontSize: 12,
  fontWeight: 700,
  letterSpacing: "0.04em",
  textTransform: "uppercase",
};

const diagnosticsPreStyle: CSSProperties = {
  margin: 0,
  padding: "0 12px 12px",
  color: "#dce9f8",
  fontSize: 11,
  lineHeight: 1.55,
  whiteSpace: "pre-wrap",
  wordBreak: "break-word",
};

const emptyTextStyle: CSSProperties = {
  color: "#8ea4be",
  fontSize: 12,
  lineHeight: 1.5,
};
