/**
 * src/workspaces/GraphWorkspace/EdgeReasoningBlock.tsx
 *
 * Reasoning provenance for a selected edge. POST /api/reason stores the
 * inference trail as edge properties (inferred / inferred_from /
 * reasoning_mode / rules); this block surfaces it so inferred edges are
 * distinguishable from factual ones in the edge inspector card.
 */
import { useTranslation } from 'react-i18next';
import { MetricChip } from '../../ui/primitives';

export function EdgeReasoningBlock({ properties }: { properties: Record<string, unknown> }) {
  const { t } = useTranslation();

  const inferred = properties.inferred === true || properties.inferred === 'true';
  if (!inferred) return null;

  const mode = typeof properties.reasoning_mode === 'string' ? properties.reasoning_mode : null;
  const fact = typeof properties.inferred_from === 'string' ? properties.inferred_from : null;
  const rules = Array.isArray(properties.rules)
    ? properties.rules.filter((rule): rule is string => typeof rule === 'string')
    : [];

  return (
    <div style={{
      background: 'rgba(210,168,255,0.06)',
      border: '1px solid rgba(210,168,255,0.25)',
      borderRadius: 8, padding: 12, display: 'flex',
      flexDirection: 'column', gap: 10,
    }}>
      <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center' }}>
        <span style={{
          display: 'inline-flex', alignItems: 'center', gap: 6,
          color: '#d2a8ff', fontSize: 12, fontWeight: 700,
          textTransform: 'uppercase', letterSpacing: '0.06em',
        }}>
          <span aria-hidden>⚡</span>
          {t('graph.edge.inferred')}
        </span>
        {mode ? <MetricChip tone="warm">{t('graph.edge.reasoningMode', { mode })}</MetricChip> : null}
      </div>

      {fact ? (
        <div>
          <div style={{
            color: 'rgba(127, 208, 255, 0.68)', fontSize: 10,
            letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 4,
          }}>
            {t('graph.edge.inferredFrom')}
          </div>
          <div style={{
            color: '#dce7f4', fontSize: 12,
            fontFamily: "'JetBrains Mono', monospace",
            wordBreak: 'break-word',
          }}>
            {fact}
          </div>
        </div>
      ) : null}

      {rules.length > 0 ? (
        <div>
          <div style={{
            color: 'rgba(127, 208, 255, 0.68)', fontSize: 10,
            letterSpacing: '0.06em', textTransform: 'uppercase', marginBottom: 6,
          }}>
            {t('graph.edge.rules')}
          </div>
          <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
            {rules.map((rule) => (
              <span key={rule} style={{
                background: '#21262d', color: '#c9d1d9',
                padding: '3px 8px', borderRadius: 4, fontSize: 12,
                border: '1px solid rgba(255,255,255,0.06)',
              }}>
                {rule}
              </span>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}
