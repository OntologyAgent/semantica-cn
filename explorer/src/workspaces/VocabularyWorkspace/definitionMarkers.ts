/**
 * definitionMarkers.ts — 把数据侧内嵌在 skos:definition 里的结构化标记
 * 解析出来，正文保持干净。
 *
 * 标记形态（sinopharm 词表约定）：
 *   〖谓词 ascii名〗     — 英文谓词名（az:asciiId 的镜像）
 *   〖A → B〗           — 值域签名（domain → range）
 *   〖传递〗〖对称〗…    — OWL 特征词
 *   〖与「X」互逆〗      — 互逆关系注记
 *   〖语境〗其后文本     — 语境注记（归入 scope note 通道）
 * 未识别标记不丢弃，原样进 others。
 */

const MARKER_RE = /〖([^〗]*)〗/g;
const PREDICATE_RE = /^谓词\s+(.+)$/;

const KNOWN_FEATURES = new Set(['传递', '对称', '非对称', '自反', '非自反']);

export interface ParsedDefinition {
  /** 干净的定义正文。 */
  text: string;
  /** 英文谓词名（〖谓词 includes〗）。 */
  predicate?: string;
  /** 值域签名（〖集团 → 企业实体〗）。 */
  signature?: string;
  /** 内嵌语境注记（〖语境〗之后的文本）。 */
  context?: string;
  /** OWL 特征词与互逆注记。 */
  features: string[];
  /** 未识别标记，原样保留。 */
  others: string[];
}

function squash(parts: string[]): string {
  return parts.join(' ').replace(/\s+/g, ' ').trim();
}

export function parseDefinitionMarkers(raw: string): ParsedDefinition {
  const parsed: ParsedDefinition = { text: '', features: [], others: [] };
  const bodyParts: string[] = [];
  const contextParts: string[] = [];
  let last = 0;
  let inContext = false;

  for (const match of raw.matchAll(MARKER_RE)) {
    const between = raw.slice(last, match.index);
    (inContext ? contextParts : bodyParts).push(between);
    last = match.index + match[0].length;
    inContext = false; // 任何标记之后默认回到正文

    const content = match[1].trim();
    if (!content) continue;
    if (content === '语境') {
      inContext = true;
      continue;
    }
    const predicate = content.match(PREDICATE_RE);
    if (predicate) {
      parsed.predicate = predicate[1].trim();
      continue;
    }
    if (content.includes('→')) {
      parsed.signature = content;
      continue;
    }
    if (KNOWN_FEATURES.has(content) || content.endsWith('互逆')) {
      parsed.features.push(content);
      continue;
    }
    parsed.others.push(content);
  }
  (inContext ? contextParts : bodyParts).push(raw.slice(last));

  parsed.text = squash(bodyParts);
  const context = squash(contextParts);
  if (context) parsed.context = context;
  return parsed;
}
