/**
 * TermTypeBadge.tsx — 词条类型小徽标（类=蓝 / 属性=紫 / 个体=绿）。
 *
 * 传入原始 notation 值；归一后命中已知类型显示本地化标签，未知非空值
 * 以中性灰原样显示（宁可见也不吞数据），空值不渲染。
 */
import type { CSSProperties } from 'react';
import { useTranslation } from 'react-i18next';
import { normalizeTermType, TERM_TYPE_COLORS, TERM_TYPE_LABEL_KEYS } from './termType';

function chipStyle(color: string): CSSProperties {
  return {
    marginLeft: 6, padding: '1px 6px', borderRadius: 4,
    fontSize: 10, lineHeight: '16px', flexShrink: 0,
    color, background: `${color}1a`, border: `1px solid ${color}55`,
  };
}

export function TermTypeBadge({ value }: { value: string | null | undefined }) {
  const { t } = useTranslation();
  const type = normalizeTermType(value);

  if (type) {
    const color = TERM_TYPE_COLORS[type];
    return <span style={chipStyle(color)}>{t(TERM_TYPE_LABEL_KEYS[type])}</span>;
  }
  if (!value) return null;
  return <span style={chipStyle('#8b949e')}>{value}</span>;
}
