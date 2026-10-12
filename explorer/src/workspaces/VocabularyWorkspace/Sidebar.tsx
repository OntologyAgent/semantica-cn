/**
 * src/workspaces/VocabularyWorkspace/Sidebar.tsx
 *
 * Left sidebar for the Vocabulary workspace.
 * - Lists available SKOS ConceptSchemes
 * - Shows the concept hierarchy tree for the active scheme
 * - Includes the import dropzone
 */
import { useMemo, useState, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { useVocabularies, useConceptHierarchy, useConceptTypes } from './queries';
import { ConceptTree } from './ConceptTree';
import { ImportDropzone } from './ImportDropzone';
import type { ConceptNode, VocabularyScheme } from './types';
import {
  filterConceptTree,
  TERM_TYPE_COLORS,
  TERM_TYPE_LABEL_KEYS,
  TERM_TYPE_ORDER,
  type TermTypeValue,
} from './termType';

interface SidebarProps {
  onSelectConcept: (concept: ConceptNode) => void;
}

function TypeFilterChip({
  active, color, onClick, children,
}: {
  active: boolean;
  color?: string;
  onClick: () => void;
  children: ReactNode;
}) {
  const tone = active ? (color ?? '#79c0ff') : '#8b949e';
  return (
    <button
      onClick={onClick}
      style={{
        padding: '3px 10px', borderRadius: 999, fontSize: 12, cursor: 'pointer',
        color: tone, background: active ? `${tone}1f` : 'transparent',
        border: `1px solid ${active ? `${tone}66` : 'rgba(139,148,158,0.3)'}`,
      }}
    >
      {children}
    </button>
  );
}

export function Sidebar({ onSelectConcept }: SidebarProps) {
  const { t } = useTranslation();
  const { data: schemes = [], isLoading: schemesLoading } = useVocabularies();
  const [activeScheme, setActiveScheme] = useState<string | undefined>();
  const [typeFilter, setTypeFilter] = useState<TermTypeValue | null>(null);
  const { data: typeByUri = {} } = useConceptTypes();

  // Auto-select first scheme
  const selectedSchemeUri = activeScheme ?? schemes[0]?.uri;

  const {
    data: hierarchy = [],
    isLoading: treeLoading,
  } = useConceptHierarchy(selectedSchemeUri);

  // 过滤器只在树上真的有类型数据时出现（数据侧未写 notation 前不显示死 UI）。
  const presentTypes = useMemo(() => {
    const present = new Set<TermTypeValue>();
    const walk = (nodes: ConceptNode[]) => {
      for (const node of nodes) {
        const value = typeByUri[node.uri];
        if (value) present.add(value);
        if (node.children) walk(node.children);
      }
    };
    walk(hierarchy);
    return TERM_TYPE_ORDER.filter((type) => present.has(type));
  }, [hierarchy, typeByUri]);

  const visibleTree = useMemo(
    () => filterConceptTree(hierarchy, typeFilter, typeByUri),
    [hierarchy, typeFilter, typeByUri],
  );

  return (
    <div style={{
      width: 340, display: 'flex', flexDirection: 'column',
      borderRight: '1px solid rgba(88,166,255,0.15)',
      backgroundColor: '#010409', overflow: 'hidden',
    }}>
      {/* Header */}
      <div style={{
        padding: '20px 20px 16px',
        borderBottom: '1px solid rgba(88,166,255,0.15)',
      }}>
        <h2 style={{ fontSize: 18, color: '#c9d1d9', margin: '0 0 4px 0', fontWeight: 600 }}>
          {t('vocabulary.title')}
        </h2>
        <p style={{ color: '#8b949e', fontSize: 13, margin: 0 }}>
          {schemes.length
            ? t(schemes.length === 1 ? 'vocabulary.schemeCountOne' : 'vocabulary.schemeCountOther', { count: schemes.length })
            : t('vocabulary.noVocabularies')}
        </p>
      </div>

      {/* Scheme selector */}
      <div style={{ padding: '12px 16px', borderBottom: '1px solid rgba(88,166,255,0.1)' }}>
        {schemesLoading ? (
          <div style={{ color: '#8b949e', fontSize: 13 }}>{t('vocabulary.loadingSchemes')}</div>
        ) : schemes.length === 0 ? (
          <div style={{ color: '#484f58', fontSize: 13, fontStyle: 'italic' }}>
            {t('vocabulary.noSchemesFound')}
          </div>
        ) : (
          <select
            value={selectedSchemeUri || ''}
            onChange={(e) => setActiveScheme(e.target.value)}
            style={{
              width: '100%', appearance: 'none',
              background: 'rgba(0,0,0,0.3)',
              border: '1px solid rgba(88,166,255,0.2)',
              color: '#c9d1d9', padding: '8px 12px',
              borderRadius: 6, fontSize: 13, cursor: 'pointer',
              outline: 'none',
            }}
          >
            {schemes.map((s: VocabularyScheme) => (
              <option key={s.uri} value={s.uri} style={{ background: '#0d1117' }}>
                {s.label}
              </option>
            ))}
          </select>
        )}
      </div>

      {/* Type filter — only when the tree carries type data */}
      {presentTypes.length > 0 ? (
        <div style={{
          display: 'flex', gap: 6, flexWrap: 'wrap',
          padding: '10px 16px', borderBottom: '1px solid rgba(88,166,255,0.1)',
        }}>
          <TypeFilterChip active={typeFilter === null} onClick={() => setTypeFilter(null)}>
            {t('vocabulary.filterAll')}
          </TypeFilterChip>
          {presentTypes.map((type) => (
            <TypeFilterChip
              key={type}
              active={typeFilter === type}
              color={TERM_TYPE_COLORS[type]}
              onClick={() => setTypeFilter(type)}
            >
              {t(TERM_TYPE_LABEL_KEYS[type])}
            </TypeFilterChip>
          ))}
        </div>
      ) : null}

      {/* Concept Tree */}
      <div style={{
        flex: 1, overflow: 'hidden', display: 'flex', flexDirection: 'column',
      }}>
        {treeLoading ? (
          <div style={{ padding: 20, color: '#8b949e', fontSize: 13, textAlign: 'center' }}>
            {t('vocabulary.loadingHierarchy')}
          </div>
        ) : hierarchy.length === 0 ? (
          <div style={{ padding: 20, color: '#484f58', fontSize: 13, textAlign: 'center', fontStyle: 'italic' }}>
            {selectedSchemeUri
              ? t('vocabulary.noConceptsInScheme')
              : t('vocabulary.selectSchemeHint')}
          </div>
        ) : visibleTree.length === 0 ? (
          <div style={{ padding: 20, color: '#484f58', fontSize: 13, textAlign: 'center', fontStyle: 'italic' }}>
            {t('vocabulary.noTypeMatches')}
          </div>
        ) : (
          <div style={{ flex: 1, overflow: 'hidden' }}>
            <ConceptTree data={visibleTree} onSelectConcept={onSelectConcept} typeByUri={typeByUri} />
          </div>
        )}
      </div>

      {/* Import area */}
      <div style={{
        padding: '12px 16px',
        borderTop: '1px solid rgba(88,166,255,0.15)',
      }}>
        <ImportDropzone />
      </div>
    </div>
  );
}
