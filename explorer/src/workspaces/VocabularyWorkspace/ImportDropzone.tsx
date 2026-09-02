/**
 * ImportDropzone.tsx
 *
 * Drag & drop upload zone for SKOS .ttl / .rdf files.
 * Styled for the Palantir dark theme.
 */
import React, { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { useTranslation } from 'react-i18next';
import { UploadCloud, CheckCircle2, Loader2 } from 'lucide-react';
import { useImportVocabulary } from './queries';
import type { ImportResponse } from './types';

export const ImportDropzone: React.FC = () => {
  const { t } = useTranslation();
  const [file, setFile] = useState<File | null>(null);
  const [importResult, setImportResult] = useState<ImportResponse | null>(null);
  const importMutation = useImportVocabulary();

  const onDrop = useCallback((acceptedFiles: File[]) => {
    if (acceptedFiles.length > 0) {
      const selectedFile = acceptedFiles[0];
      setFile(selectedFile);
      setImportResult(null);

      importMutation.mutate(selectedFile, {
        onSuccess: (data) => {
          setImportResult(data);
          setTimeout(() => {
            setFile(null);
            setImportResult(null);
          }, 4000);
        },
        onError: (err) => {
          console.error("Upload failed:", err);
          setFile(null);
        }
      });
    }
  }, [importMutation]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'text/turtle': ['.ttl'],
      'application/rdf+xml': ['.rdf', '.owl']
    },
    maxFiles: 1
  });

  return (
    <div>
      <div
        {...getRootProps()}
        style={{
          border: `2px dashed ${isDragActive ? '#58a6ff' : 'rgba(88,166,255,0.25)'}`,
          backgroundColor: isDragActive ? 'rgba(88,166,255,0.06)' : 'rgba(0,0,0,0.2)',
          borderRadius: 8,
          padding: '16px 12px',
          textAlign: 'center',
          cursor: 'pointer',
          transition: 'all 0.2s ease',
        }}
      >
        <input {...getInputProps()} />

        {importMutation.isPending ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', color: '#8b949e' }}>
            <Loader2 className="animate-spin" size={20} style={{ marginBottom: 6 }} />
            <span style={{ fontSize: 12 }}>{t('vocabulary.uploadingFile', { name: file?.name })}</span>
          </div>
        ) : importResult ? (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', color: '#3fb950' }}>
            <CheckCircle2 size={20} style={{ marginBottom: 6 }} />
            <span style={{ fontSize: 12, fontWeight: 500 }}>{t('vocabulary.importSuccessful')}</span>
            <span style={{ fontSize: 11, marginTop: 2, color: '#56d364' }}>
              {t('vocabulary.importSummary', { nodes: importResult.nodes_added, edges: importResult.edges_added })}
            </span>
          </div>
        ) : (
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', color: '#8b949e' }}>
            <UploadCloud size={20} style={{ marginBottom: 6, color: isDragActive ? '#58a6ff' : '#484f58' }} />
            <span style={{ fontSize: 12, fontWeight: 500, color: '#c9d1d9' }}>
              {isDragActive ? t('vocabulary.dropHere') : t('vocabulary.importVocabulary')}
            </span>
            <span style={{ fontSize: 11, marginTop: 2 }}>{t('vocabulary.formatHint')}</span>
          </div>
        )}
      </div>
      {importMutation.isError && (
        <p style={{ color: '#f85149', fontSize: 11, marginTop: 6, textAlign: 'center' }}>
          {t('vocabulary.uploadFailed')}
        </p>
      )}
    </div>
  );
};