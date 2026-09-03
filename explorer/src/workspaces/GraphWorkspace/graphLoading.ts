import type { GraphLoadPhase, GraphLoadProgress, GraphLoadProgressKind, GraphLayoutSource, GraphLayoutState } from "./types";

export const GRAPH_LOAD_STAGE_SEQUENCE: Exclude<GraphLoadPhase, "ready">[] = [
  "bootstrapping",
  "fetching_nodes",
  "fetching_edges",
  "computing_styling",
  "hydrating_scene",
  "stabilizing_layout",
];

export function getGraphLoadTitle(phase: GraphLoadPhase): string {
  switch (phase) {
    case "bootstrapping":
      return "Preparing graph session";
    case "fetching_nodes":
      return "Loading nodes";
    case "fetching_edges":
      return "Loading relationships";
    case "computing_styling":
      return "Computing node styling";
    case "hydrating_scene":
      return "Hydrating graph scene";
    case "stabilizing_layout":
      return "Stabilizing layout";
    case "ready":
    default:
      return "Graph ready";
  }
}

/** Translation keys mirroring getGraphLoadTitle, for i18n-aware renderers. */
export type GraphLoadTitleKey =
  | "graph.loading.preparing"
  | "graph.loading.titleNodes"
  | "graph.loading.titleEdges"
  | "graph.loading.titleStyling"
  | "graph.loading.titleScene"
  | "graph.loading.titleStabilizing"
  | "graph.loading.titleReady";

export function getGraphLoadTitleKey(phase: GraphLoadPhase): GraphLoadTitleKey {
  switch (phase) {
    case "bootstrapping":
      return "graph.loading.preparing";
    case "fetching_nodes":
      return "graph.loading.titleNodes";
    case "fetching_edges":
      return "graph.loading.titleEdges";
    case "computing_styling":
      return "graph.loading.titleStyling";
    case "hydrating_scene":
      return "graph.loading.titleScene";
    case "stabilizing_layout":
      return "graph.loading.titleStabilizing";
    case "ready":
    default:
      return "graph.loading.titleReady";
  }
}

export function getGraphLoadStageLabel(phase: Exclude<GraphLoadPhase, "ready">): string {
  switch (phase) {
    case "bootstrapping":
      return "Prepare";
    case "fetching_nodes":
      return "Nodes";
    case "fetching_edges":
      return "Relations";
    case "computing_styling":
      return "Styling";
    case "hydrating_scene":
      return "Scene";
    case "stabilizing_layout":
      return "Layout";
    default:
      return "Stage";
  }
}

export function createGraphLoadProgress(input: {
  phase: GraphLoadPhase;
  message: string;
  progressKind: GraphLoadProgressKind;
  loaded?: number | null;
  total?: number | null;
  nodesLoaded?: number;
  nodesTotal?: number | null;
  edgesLoaded?: number;
  edgesTotal?: number | null;
  showGraphBehind?: boolean;
  layoutSource?: GraphLayoutSource;
  layoutState?: GraphLayoutState;
}): GraphLoadProgress {
  const phaseIndex = GRAPH_LOAD_STAGE_SEQUENCE.indexOf(input.phase as Exclude<GraphLoadPhase, "ready">);

  return {
    phase: input.phase,
    title: getGraphLoadTitle(input.phase),
    message: input.message,
    progressKind: input.progressKind,
    loaded: input.loaded ?? null,
    total: input.total ?? null,
    nodesLoaded: input.nodesLoaded ?? 0,
    nodesTotal: input.nodesTotal ?? null,
    edgesLoaded: input.edgesLoaded ?? 0,
    edgesTotal: input.edgesTotal ?? null,
    showGraphBehind: input.showGraphBehind ?? false,
    stageIndex: phaseIndex >= 0 ? phaseIndex + 1 : GRAPH_LOAD_STAGE_SEQUENCE.length,
    stageCount: GRAPH_LOAD_STAGE_SEQUENCE.length,
    layoutSource: input.layoutSource,
    layoutState: input.layoutState,
  };
}
