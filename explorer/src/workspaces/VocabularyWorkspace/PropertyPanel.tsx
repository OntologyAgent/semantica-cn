/**
 * src/workspaces/VocabularyWorkspace/PropertyPanel.tsx
 *
 * Detail panel for a selected SKOS concept — shows preferred label,
 * URI, definition, scope note, alt labels, and narrower concepts.
 */
import { useTranslation } from 'react-i18next';
import type { ConceptNode, ConceptDetail } from './types';
import { parseDefinitionMarkers } from './definitionMarkers';

interface PropertyPanelProps {
  concept: ConceptNode | null;
  /** Payload from GET /api/ontology/skos/concept/{uri}; fills definition/scope note for ontology-loaded concepts. */
  detail?: ConceptDetail | null;
}

export function PropertyPanel({ concept, detail }: PropertyPanelProps) {
  const { t } = useTranslation();
  if (!concept) {
    return (
      <div style={{
        display: 'flex', flexDirection: 'column', alignItems: 'center',
        justifyContent: 'center', height: '100%', color: '#8b949e',
        textAlign: 'center', padding: 40,
      }}>
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none"
          stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"
          strokeLinejoin="round" style={{ marginBottom: 16, opacity: 0.4 }}>
          <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
        </svg>
        <p style={{ fontSize: 15, fontWeight: 500, marginBottom: 4 }}>{t('vocabulary.noConceptSelected')}</p>
        <p style={{ fontSize: 13 }}>{t('vocabulary.noConceptHint')}</p>
      </div>
    );
  }

  // Detail endpoint first, hierarchy description as fallback — ontology-load
  // and vocabulary-import store the definition under different keys.
  const definition = detail?.definition || concept.description || null;
  // 数据侧把〖谓词〗〖签名〗〖特征〗〖语境〗内嵌进定义文本；解析后正文干净，
  // 结构进徽标行，语境注记并入语境通道。
  const parsed = definition ? parseDefinitionMarkers(definition) : null;
  const scopeNote = parsed?.context || detail?.scope_note || null;
  const editorialNote = detail?.editorial_note || null;
  // Same regime for synonyms: hierarchy alt_labels is empty on the
  // ontology-load path, the detail payload carries them there.
  const altLabels = detail?.alt_labels?.length ? detail.alt_labels : concept.alt_labels;

  return (
    <div style={{ padding: 28, overflowY: 'auto', height: '100%' }}>
      {/* Header */}
      <div style={{ borderBottom: '1px solid rgba(88,166,255,0.2)', paddingBottom: 20, marginBottom: 24 }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 8 }}>
          <span style={{
            display: 'inline-block', width: 8, height: 8, borderRadius: '50%',
            background: '#d2a8ff', boxShadow: '0 0 8px rgba(210,168,255,0.6)',
          }} />
          <span style={{ color: '#d2a8ff', fontSize: 12, fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.06em' }}>
            {t('vocabulary.skosConcept')}
          </span>
        </div>
        <h2 style={{ margin: 0, color: '#fff', fontSize: 22, fontWeight: 700, wordBreak: 'break-word' }}>
          {concept.pref_label}
        </h2>
      </div>

      {/* URI Badge */}
      <div style={{
        marginBottom: 20, padding: '8px 14px',
        background: 'rgba(88,166,255,0.08)',
        border: '1px solid rgba(88,166,255,0.2)',
        borderRadius: 6, fontSize: 13, color: '#79c0ff',
        fontFamily: "'JetBrains Mono', monospace",
        wordBreak: 'break-all',
      }}>
        {concept.uri}
      </div>

      {/* Definition — 正文 + 结构化标记（谓词名/签名/特征），不内联糊排 */}
      {definition ? (
        <section style={{ marginBottom: 24 }}>
          <h4 style={{
            color: '#8b949e', fontSize: 12, textTransform: 'uppercase',
            letterSpacing: '0.08em', marginBottom: 10,
          }}>
            {t('vocabulary.definition')}
          </h4>
          {parsed?.text ? (
            <p style={{ margin: 0, color: '#c9d1d9', fontSize: 14, lineHeight: 1.6 }}>
              {parsed.text}
            </p>
          ) : null}
          {parsed && (parsed.predicate || parsed.signature || parsed.features.length > 0 || parsed.others.length > 0) ? (
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginTop: 10 }}>
              {parsed.predicate ? (
                <span style={{
                  padding: '2px 8px', borderRadius: 4, fontSize: 12,
                  fontFamily: "'JetBrains Mono', monospace",
                  color: '#d2a8ff', background: 'rgba(210,168,255,0.08)',
                  border: '1px solid rgba(210,168,255,0.3)',
                }}>
                  {parsed.predicate}
                </span>
              ) : null}
              {parsed.signature ? (
                <span style={{
                  padding: '2px 8px', borderRadius: 4, fontSize: 12,
                  fontFamily: "'JetBrains Mono', monospace",
                  color: '#79c0ff', background: 'rgba(121,192,255,0.08)',
                  border: '1px solid rgba(121,192,255,0.25)',
                }}>
                  {parsed.signature}
                </span>
              ) : null}
              {parsed.features.map((feature) => (
                <span key={feature} style={{
                  padding: '2px 8px', borderRadius: 4, fontSize: 12,
                  color: '#e3b341', background: 'rgba(227,179,65,0.08)',
                  border: '1px solid rgba(227,179,65,0.3)',
                }}>
                  {feature}
                </span>
              ))}
              {parsed.others.map((other) => (
                <span key={other} style={{
                  padding: '2px 8px', borderRadius: 4, fontSize: 12,
                  color: '#8b949e', background: 'rgba(139,148,158,0.08)',
                  border: '1px solid rgba(139,148,158,0.3)',
                }}>
                  {other}
                </span>
              ))}
            </div>
          ) : null}
        </section>
      ) : null}

      {/* Scope Note — 「语境」徽标行：徽标 + 左边线引注块，与定义段视觉区分 */}
      {scopeNote ? (
        <section style={{ marginBottom: 24 }}>
          <div style={{ marginBottom: 10 }}>
            <span style={{
              display: 'inline-block', padding: '2px 10px', borderRadius: 999,
              fontSize: 11, fontWeight: 600, letterSpacing: '0.05em',
              color: '#79c0ff', background: 'rgba(121,192,255,0.1)',
              border: '1px solid rgba(121,192,255,0.3)',
                textTransform: 'uppercase',
            }}>
              {t('vocabulary.scopeNote')}
            </span>
          </div>
          <p style={{
            margin: 0, color: '#c9d1d9', fontSize: 13, lineHeight: 1.6,
            fontStyle: 'italic', paddingLeft: 10,
            borderLeft: '2px solid rgba(121,192,255,0.35)',
          }}>
            {scopeNote}
          </p>
        </section>
      ) : null}
      {editorialNote ? (
        <section style={{ marginBottom: 24 }}>
          <div style={{ marginBottom: 10 }}>
            <span style={{
              display: 'inline-block', padding: '2px 10px', borderRadius: 999,
              fontSize: 11, fontWeight: 600, letterSpacing: '0.05em',
              color: '#e3b341', background: 'rgba(227,179,65,0.1)',
              border: '1px solid rgba(227,179,65,0.3)',
                textTransform: 'uppercase',
            }}>
              {t('vocabulary.editorialNote')}
            </span>
          </div>
          <p style={{
            margin: 0, color: '#8b949e', fontSize: 12, lineHeight: 1.6,
            paddingLeft: 10,
          }}>
            {editorialNote}
          </p>
        </section>
      ) : null}

      {/* Alt Labels */}
      {altLabels && altLabels.length > 0 && (
        <section style={{ marginBottom: 24 }}>
          <h4 style={{
            color: '#8b949e', fontSize: 12, textTransform: 'uppercase',
            letterSpacing: '0.08em', marginBottom: 10,
          }}>
            {t('vocabulary.altLabels')}
          </h4>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {altLabels.map((lbl, i) => (
              <span key={i} style={{
                background: '#21262d', color: '#c9d1d9',
                padding: '4px 10px', borderRadius: 4, fontSize: 13,
                border: '1px solid rgba(255,255,255,0.06)',
              }}>
                {lbl}
              </span>
            ))}
          </div>
        </section>
      )}

      {/* Children summary */}
      <section style={{
        background: 'rgba(0,0,0,0.2)', padding: 16, borderRadius: 8,
        border: '1px solid rgba(255,255,255,0.05)',
      }}>
        <h4 style={{
          color: '#8b949e', fontSize: 12, textTransform: 'uppercase',
          letterSpacing: '0.08em', marginBottom: 10,
        }}>
          {t('vocabulary.narrowerConcepts')}
        </h4>
        {concept.children && concept.children.length > 0 ? (
          <div style={{ display: 'flex', flexDirection: 'column', gap: 6 }}>
            {concept.children.map((child) => (
              <span key={child.uri} style={{
                color: '#c9d1d9', fontSize: 13, padding: '6px 10px',
                background: 'rgba(88,166,255,0.06)', borderRadius: 4,
                border: '1px solid rgba(88,166,255,0.12)',
              }}>
                {child.pref_label}
              </span>
            ))}
          </div>
        ) : (
          <p style={{ margin: 0, color: '#484f58', fontStyle: 'italic', fontSize: 13 }}>
            {t('vocabulary.leafConcept')}
          </p>
        )}
      </section>
    </div>
  );
}
