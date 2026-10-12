import test from "node:test";
import assert from "node:assert/strict";
import { parseDefinitionMarkers } from "../src/workspaces/VocabularyWorkspace/definitionMarkers.ts";

// 数据侧把结构化信息内嵌进 skos:definition，五种形态：
// 〖谓词 ascii名〗、〖A → B〗（签名）、〖传递〗等特征词、〖与「X」互逆〗、
// 〖语境〗（其后文本属语境注记）。解析目标是正文干净、结构归位。
test("parses predicate, signature, and feature markers out of the definition body", () => {
  const parsed = parseDefinitionMarkers(
    "集团与其所包含的成员企业实体之间的关系，即集团包含某成员实体。 〖谓词 includes〗〖集团 → 企业实体〗〖传递〗〖与「属于」互逆〗",
  );
  assert.equal(parsed.text, "集团与其所包含的成员企业实体之间的关系，即集团包含某成员实体。");
  assert.equal(parsed.predicate, "includes");
  assert.equal(parsed.signature, "集团 → 企业实体");
  assert.deepEqual(parsed.features, ["传递", "与「属于」互逆"]);
});

test("route the text after 〖语境〗 into the context field, not the body", () => {
  const parsed = parseDefinitionMarkers(
    "中国是指中华人民共和国，不包括香港特别行政区、澳门特别行政区和台湾地区〖语境〗仅为本协议之目的",
  );
  assert.equal(parsed.text, "中国是指中华人民共和国，不包括香港特别行政区、澳门特别行政区和台湾地区");
  assert.equal(parsed.context, "仅为本协议之目的");
});

test("unknown markers are preserved verbatim instead of dropped", () => {
  const parsed = parseDefinitionMarkers("定义正文。 〖枚举〗〖自定义注记〗");
  assert.equal(parsed.text, "定义正文。");
  assert.deepEqual(parsed.others, ["枚举", "自定义注记"]);
});

test("clean definitions without markers pass through unchanged", () => {
  const parsed = parseDefinitionMarkers("一个民事主体通过出资、股权等形式实施管理或调控的关系。");
  assert.equal(parsed.text, "一个民事主体通过出资、股权等形式实施管理或调控的关系。");
  assert.equal(parsed.predicate, undefined);
  assert.equal(parsed.signature, undefined);
  assert.equal(parsed.context, undefined);
  assert.deepEqual(parsed.features, []);
  assert.deepEqual(parsed.others, []);
});

test("known OWL feature words are recognized as features", () => {
  const parsed = parseDefinitionMarkers("关系。 〖对称〗〖非对称〗〖自反〗〖非自反〗〖传递〗");
  assert.deepEqual(parsed.features, ["对称", "非对称", "自反", "非自反", "传递"]);
  assert.deepEqual(parsed.others, []);
});
