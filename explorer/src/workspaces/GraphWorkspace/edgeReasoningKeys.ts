/**
 * src/workspaces/GraphWorkspace/edgeReasoningKeys.ts
 *
 * Edge property keys owned by the reasoning block; the generic edge-property
 * grid filters them out so the flags are not shown twice.
 */
export const EDGE_REASONING_KEYS = ['inferred', 'inferred_from', 'reasoning_mode', 'rules'] as const;
