import i18next from 'i18next';
import { initReactI18next } from 'react-i18next';

import en from './locales/en.json';
import zh from './locales/zh.json';

export const SUPPORTED_LANGUAGES = ['en', 'zh'] as const;
export type SupportedLanguage = (typeof SUPPORTED_LANGUAGES)[number];

/** localStorage key recording the user's explicit language choice. */
export const LANGUAGE_STORAGE_KEY = 'semantica.explorer.lang';

const resources = {
  en: { translation: en.translation },
  zh: {
    // INV-1 (FR-006): zh must not miss any en key (`satisfies typeof en.translation`)
    // and must not introduce keys absent from en (unknown keys fall through to `never`).
    translation: zh.translation satisfies {
      [K in keyof typeof zh.translation]: K extends keyof typeof en.translation
        ? string
        : never;
    } satisfies typeof en.translation,
  },
} as const;

function isSupportedLanguage(value: unknown): value is SupportedLanguage {
  return value === 'en' || value === 'zh';
}

function readStoredLanguage(): string | null {
  try {
    return window.localStorage.getItem(LANGUAGE_STORAGE_KEY);
  } catch {
    // Private mode / disabled storage counts as a miss for this step.
    return null;
  }
}

/**
 * Resolve the initial language, first hit wins:
 * 1. URL `?lang=` (`en` | `zh`, for e2e and deep links)
 * 2. `localStorage[semantica.explorer.lang]` (`en` | `zh`)
 * 3. `navigator.language` starting with `zh` (zh / zh-CN / zh-TW …)
 * 4. Fallback `en`
 *
 * Any step that throws (private mode, blocked storage) counts as a miss.
 */
export function resolveInitialLanguage(): SupportedLanguage {
  try {
    const param = new URLSearchParams(window.location.search).get('lang');
    if (isSupportedLanguage(param)) {
      return param;
    }
  } catch {
    // fall through to the next detection step
  }

  try {
    const stored = readStoredLanguage();
    if (isSupportedLanguage(stored)) {
      return stored;
    }
  } catch {
    // fall through to the next detection step
  }

  try {
    if (typeof navigator !== 'undefined' && navigator.language?.toLowerCase().startsWith('zh')) {
      return 'zh';
    }
  } catch {
    // fall through to the fallback language
  }

  return 'en';
}

/**
 * Sync `<html lang>` and `document.title` with the active language.
 * Driven by the `languageChanged` event (also covers `?lang=` / storage hits),
 * never by the toggle component itself.
 */
export function syncDocumentLanguage(language: string | undefined): void {
  const active = language ?? i18next.language;
  if (active === 'zh') {
    document.documentElement.lang = 'zh-CN';
    document.title = '知识探索器 · Semantica';
  } else {
    document.documentElement.lang = 'en';
    document.title = 'Semantica Knowledge Explorer';
  }
}

// `lng` is passed explicitly so the first render already uses the resolved
// language (no fallback flash). Resources are inlined: init completes synchronously.
void i18next.use(initReactI18next).init({
  resources,
  lng: resolveInitialLanguage(),
  fallbackLng: 'en',
  interpolation: { escapeValue: false },
  react: { useSuspense: false },
});

i18next.on('languageChanged', syncDocumentLanguage);
syncDocumentLanguage(i18next.language);

export default i18next;
