import i18next from "i18next";
import type { FocusedUnavailableReason, GroupedViewUnavailableReason } from "./types";

export function groupedViewReasonText(
  reason: GroupedViewUnavailableReason | null | undefined,
): string | null {
  if (!reason) {
    return null;
  }

  switch (reason.code) {
    case "communities-undetected":
      return i18next.t("graph.grouped.reason.communities-undetected");
    case "community-nodes-missing":
      return i18next.t("graph.grouped.reason.community-nodes-missing");
    case "invalid-community-layout":
      return i18next.t("graph.grouped.reason.invalid-community-layout", { nodeId: reason.nodeId });
    case "missing-grouped-node":
      return i18next.t("graph.grouped.reason.missing-grouped-node", { edgeId: reason.edgeId });
  }
}

export function focusedUnavailableReasonText(
  reason: FocusedUnavailableReason | null | undefined,
): string | null {
  if (!reason) {
    return null;
  }

  return i18next.t(`graph.focused.reason.${reason.code}`);
}
