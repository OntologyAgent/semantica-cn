/**
 * termType.ts — 词条类型（类/属性/个体）的归一、映射与树过滤。
 *
 * 类型由数据侧写进 skos:notation。ontology-load 路径的节点属性键带前缀
 * （skos:notation），vocabulary-import 路径不带（notation），两者都读；
 * 未知值一律归 null，不猜类型。
 */
import type { ConceptNode } from './types';
import type en from '../../i18n/locales/en.json';

/** en.json 的扁平键联合——i18next 严格键类型（见 src/i18n/types.d.ts）。 */
export type TranslationKey = keyof typeof en.translation;

export type TermTypeValue = 'class' | 'property' | 'individual';

export const TERM_TYPE_ORDER: readonly TermTypeValue[] = ['class', 'property', 'individual'];

export const TERM_TYPE_COLORS: Record<TermTypeValue, string> = {
  class: '#79c0ff', // 类=蓝
  property: '#d2a8ff', // 属性=紫
  individual: '#7ee787', // 个体=绿
};

export const TERM_TYPE_LABEL_KEYS: Record<TermTypeValue, TranslationKey> = {
  class: 'vocabulary.termType.class',
  property: 'vocabulary.termType.property',
  individual: 'vocabulary.termType.individual',
};

const TYPE_ALIASES: Record<string, TermTypeValue> = {
  '类': 'class', class: 'class',
  '属性': 'property', property: 'property', attribute: 'property',
  '个体': 'individual', individual: 'individual', instance: 'individual',
};

export function normalizeTermType(raw: unknown): TermTypeValue | null {
  if (typeof raw !== 'string') return null;
  return TYPE_ALIASES[raw.trim().toLowerCase()] ?? null;
}

export interface GraphNodeSnapshot {
  id: string;
  properties?: Record<string, unknown>;
}

/** Graph-node list → uri→归一类型 映射（无类型的节点不进映射）。 */
export function buildTypeByUri(nodes: GraphNodeSnapshot[]): Partial<Record<string, TermTypeValue>> {
  const map: Partial<Record<string, TermTypeValue>> = {};
  for (const node of nodes) {
    const props = node.properties ?? {};
    const raw = props['skos:notation'] ?? props['notation'];
    const value = Array.isArray(raw) ? raw[0] : raw;
    const normalized = normalizeTermType(value);
    if (normalized) map[node.id] = normalized;
  }
  return map;
}

/**
 * 类型过滤：保留命中类型的节点，以及通往命中节点的路径（父节点作为结构
 * 通道保留）；子树内无命中的分支整体剪掉。null 过滤器原样返回。
 */
export function filterConceptTree(
  nodes: ConceptNode[],
  activeType: TermTypeValue | null,
  typeByUri: Readonly<Partial<Record<string, TermTypeValue>>>,
): ConceptNode[] {
  if (!activeType) return nodes;
  const visit = (list: ConceptNode[]): ConceptNode[] => {
    const kept: ConceptNode[] = [];
    for (const node of list) {
      const children = node.children ? visit(node.children) : [];
      if (typeByUri[node.uri] === activeType || children.length > 0) {
        kept.push({ ...node, children });
      }
    }
    return kept;
  };
  return visit(nodes);
}
