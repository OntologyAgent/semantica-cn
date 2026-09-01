import { useTranslation } from 'react-i18next';

import { LANGUAGE_STORAGE_KEY, type SupportedLanguage } from './index';

const OPTIONS: Array<{ code: SupportedLanguage; label: string }> = [
  { code: 'zh', label: '中' },
  { code: 'en', label: 'EN' },
];

/**
 * Compact 中/EN language switch. Reads the active language through the
 * `useTranslation()` subscription (never a module-level variable), so consumers
 * re-render when it changes. Persistence failures are silent: the choice then
 * applies to the current session only.
 */
export function LanguageToggle() {
  const { i18n, t } = useTranslation();
  const current = i18n.resolvedLanguage ?? i18n.language;

  const selectLanguage = (next: SupportedLanguage) => {
    if (next === current) {
      return;
    }
    void i18n.changeLanguage(next);
    try {
      window.localStorage.setItem(LANGUAGE_STORAGE_KEY, next);
    } catch {
      // Storage unavailable (private mode): keep the language for this session only.
    }
  };

  return (
    <div
      className="language-toggle"
      role="group"
      aria-label={t('language.toggle')}
      style={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 2,
        padding: 2,
        borderRadius: 999,
        border: '1px solid var(--panel-border)',
        background: 'rgba(7, 17, 31, 0.55)',
      }}
    >
      {OPTIONS.map((option) => {
        const active = current === option.code;
        return (
          <button
            key={option.code}
            type="button"
            onClick={() => selectLanguage(option.code)}
            aria-pressed={active}
            style={{
              border: 'none',
              borderRadius: 999,
              padding: '2px 8px',
              fontSize: 12,
              lineHeight: 1.4,
              cursor: 'pointer',
              background: active ? 'var(--ws-accent-soft)' : 'transparent',
              color: active ? 'var(--accent-strong)' : 'var(--text-muted)',
            }}
          >
            {option.label}
          </button>
        );
      })}
    </div>
  );
}
