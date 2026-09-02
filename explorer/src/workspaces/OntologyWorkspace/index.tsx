import { useCallback, useEffect, useState } from "react";
import { useTranslation } from "react-i18next";
import {
  BookMarked,
  GitMerge,
  HeartPulse,
  Layers,
  Shield,
  Sliders,
} from "lucide-react";
import type en from "../../i18n/locales/en.json";
import { AlignmentsTab } from "./AlignmentsTab";
import { HealthTab } from "./HealthTab";
import { OntologyManager } from "./OntologyManager";
import { OntologyEditor } from "./OntologyEditor";
import { ShaclStudio } from "./ShaclStudio";
import { VersionsTab } from "./VersionsTab";

export type OntologyHubTab =
  | "registry"
  | "editor"
  | "versions"
  | "alignments"
  | "health"
  | "shacl";

type TranslationKey = keyof typeof en.translation;

const TAB_PARAM = "ontologyTab";

const TABS: {
  id: OntologyHubTab;
  labelKey: TranslationKey;
  icon: typeof GitMerge;
}[] = [
  { id: "registry", labelKey: "ontologyHub.shell.tabRegistry", icon: BookMarked },
  { id: "editor", labelKey: "ontologyHub.shell.tabEditor", icon: Sliders },
  { id: "versions", labelKey: "ontologyHub.shell.tabVersions", icon: Layers },
  { id: "alignments", labelKey: "ontologyHub.shell.tabAlignments", icon: GitMerge },
  { id: "health", labelKey: "ontologyHub.shell.tabHealth", icon: HeartPulse },
  { id: "shacl", labelKey: "ontologyHub.shell.tabShacl", icon: Shield },
];

function readTabParam(): OntologyHubTab {
  try {
    const params = new URLSearchParams(window.location.search);
    const raw = params.get(TAB_PARAM);
    if (raw && TABS.some((t) => t.id === raw)) return raw as OntologyHubTab;
  } catch {
    // ignore
  }
  return "registry";
}

function writeTabParam(tab: OntologyHubTab) {
  try {
    const params = new URLSearchParams(window.location.search);
    params.set(TAB_PARAM, tab);
    window.history.replaceState(null, "", `?${params.toString()}`);
  } catch {
    // ignore
  }
}

interface OntologyWorkspaceProps {
  onJumpToGraphNode?: (nodeId: string) => void;
}

export function OntologyWorkspace({ onJumpToGraphNode }: OntologyWorkspaceProps) {
  const { t } = useTranslation();
  const [activeTab, setActiveTab] = useState<OntologyHubTab>(readTabParam);

  useEffect(() => {
    writeTabParam(activeTab);
  }, [activeTab]);

  const handleTabChange = useCallback((tab: OntologyHubTab) => {
    setActiveTab(tab);
  }, []);

  const handleFixInEditor = useCallback((entityUri: string) => {
    const params = new URLSearchParams(window.location.search);
    params.set(TAB_PARAM, "editor");
    params.set("ontologyEntity", entityUri);
    window.history.replaceState(null, "", `?${params.toString()}`);
    setActiveTab("editor");
  }, []);

  const renderTab = () => {
    switch (activeTab) {
      case "registry":
        return <OntologyManager />;
      case "editor":
        return <OntologyEditor />;
      case "versions":
        return <VersionsTab />;
      case "alignments":
        return <AlignmentsTab />;
      case "health":
        return <HealthTab onFixInEditor={handleFixInEditor} />;
      case "shacl":
        return <ShaclStudio onJumpToNode={onJumpToGraphNode} />;
    }
  };

  return (
    <div className="ws-page">
      {/* Internal sub-tab bar */}
      <div style={{ display: "flex", gap: 4, padding: "8px 16px", borderBottom: "1px solid var(--ws-border)", background: "rgba(0,0,0,0.18)", flexShrink: 0, flexWrap: "wrap" }}>
        {TABS.map(({ id, labelKey, icon: Icon }) => {
          const active = activeTab === id;
          return (
            <button
              key={id}
              onClick={() => handleTabChange(id)}
              style={{ display: "inline-flex", alignItems: "center", gap: 6, padding: "6px 13px", borderRadius: 999, border: `1px solid ${active ? "var(--ws-border-strong)" : "transparent"}`, background: active ? "var(--ws-accent-soft)" : "transparent", color: active ? "var(--ws-text)" : "var(--ws-text-muted)", fontSize: 12, fontWeight: 600, cursor: "pointer", transition: "160ms ease" }}
            >
              <Icon size={13} />
              {t(labelKey)}
            </button>
          );
        })}
      </div>
      <div style={{ flex: 1, minHeight: 0, overflow: "hidden" }}>{renderTab()}</div>
    </div>
  );
}

