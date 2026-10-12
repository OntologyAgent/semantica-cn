import test from "node:test";
import assert from "node:assert/strict";
import React from "react";
import { renderToString } from "react-dom/server";
import i18next from "i18next";
import { initReactI18next } from "react-i18next";
import en from "../src/i18n/locales/en.json";

(globalThis as typeof globalThis & { React: typeof React }).React = React;

if (!i18next.isInitialized) {
  i18next.use(initReactI18next).init({
    lng: "en",
    fallbackLng: "en",
    resources: { en: { translation: en.translation } },
  });
}

import {
  normalizeTermType,
  buildTypeByUri,
  filterConceptTree,
  type TermTypeValue,
} from "../src/workspaces/VocabularyWorkspace/termType.ts";
import { TermTypeBadge } from "../src/workspaces/VocabularyWorkspace/TermTypeBadge.tsx";
import type { ConceptNode } from "../src/workspaces/VocabularyWorkspace/types.ts";

// ─── normalizeTermType: notation 值归一 ───────────────────────────────────────
// 数据侧写中文（类/属性/个体）或英文（class/property/individual），大小写与
// 修饰词都可能出现；未知值归 null（不猜类型）。
test("normalizeTermType maps Chinese and English notation values", () => {
  assert.equal(normalizeTermType("类"), "class");
  assert.equal(normalizeTermType("CLASS"), "class");
  assert.equal(normalizeTermType("属性"), "property");
  assert.equal(normalizeTermType("Property"), "property");
  assert.equal(normalizeTermType("个体"), "individual");
  assert.equal(normalizeTermType("Individual"), "individual");
});

test("normalizeTermType returns null for absent or unknown values", () => {
  assert.equal(normalizeTermType(null), null);
  assert.equal(normalizeTermType(undefined), null);
  assert.equal(normalizeTermType(""), null);
  assert.equal(normalizeTermType("概念"), null);
});

// ─── buildTypeByUri: 图节点属性 → uri→类型映射 ───────────────────────────────
// 两条导入路径的键名不同（skos:notation vs notation），都读；数组取首个。
test("buildTypeByUri reads both prefixed and unprefixed notation keys", () => {
  const nodes = [
    { id: "u1", properties: { "skos:notation": "属性" } },
    { id: "u2", properties: { notation: "class" } },
    { id: "u3", properties: { notation: ["个体"] } },
    { id: "u4", properties: { "skos:prefLabel": "无类型" } },
  ];
  const map = buildTypeByUri(nodes as never[]);
  assert.equal(map["u1"], "property");
  assert.equal(map["u2"], "class");
  assert.equal(map["u3"], "individual");
  assert.equal(map["u4"], undefined);
});

// ─── filterConceptTree: 类型过滤器剪枝语义 ───────────────────────────────────
// 保留：自身命中类型的节点；以及通往命中节点的路径（父节点保留为结构通道）。
// 丢弃：子树内无任何命中的分支。
test("filterConceptTree keeps matches and the path to them, prunes the rest", () => {
  const tree: ConceptNode[] = [
    {
      uri: "root-a", pref_label: "A", alt_labels: [],
      children: [
        { uri: "a-prop", pref_label: "A1", alt_labels: [] },
        { uri: "a-plain", pref_label: "A2", alt_labels: [] },
      ],
    },
    { uri: "root-b", pref_label: "B", alt_labels: [] },
  ];
  const typeByUri: Record<string, TermTypeValue> = { "a-prop": "property", "root-b": "individual" };
  const filtered = filterConceptTree(tree, "property", typeByUri);

  assert.equal(filtered.length, 1, "root-b (individual) pruned under property filter");
  assert.equal(filtered[0].uri, "root-a", "parent kept as path to the matching child");
  assert.equal(filtered[0].children?.length, 1);
  assert.equal(filtered[0].children?.[0].uri, "a-prop");
});

test("filterConceptTree with null filter returns the tree unchanged", () => {
  const tree: ConceptNode[] = [
    { uri: "u1", pref_label: "x", alt_labels: [] },
    { uri: "u2", pref_label: "y", alt_labels: [] },
  ];
  assert.equal(filterConceptTree(tree, null, {}).length, 2);
});

// ─── TermTypeBadge 渲染 ───────────────────────────────────────────────────────
test("TermTypeBadge renders a localized chip for each known type", () => {
  assert.equal(renderToString(React.createElement(TermTypeBadge, { value: "类" })).includes("Class"), true);
  assert.equal(renderToString(React.createElement(TermTypeBadge, { value: "属性" })).includes("Property"), true);
  assert.equal(renderToString(React.createElement(TermTypeBadge, { value: "个体" })).includes("Individual"), true);
});

test("TermTypeBadge renders nothing without a type and shows unknown values raw", () => {
  assert.equal(renderToString(React.createElement(TermTypeBadge, { value: null })), "");
  assert.equal(renderToString(React.createElement(TermTypeBadge, { value: undefined })), "");
  const unknown = renderToString(React.createElement(TermTypeBadge, { value: "枚举" }));
  assert.equal(unknown.includes("枚举"), true, "unknown values stay visible verbatim");
});
