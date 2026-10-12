// queries.ts
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import type { VocabularyScheme, ConceptNode, ConceptDetail, ImportResponse } from './types';
import { buildTypeByUri, type GraphNodeSnapshot } from './termType';

const fetchSchemes = async (): Promise<VocabularyScheme[]> => {
  const res = await fetch('/api/vocabulary/schemes');
  if (!res.ok) throw new Error('Failed to fetch vocabularies');
  return res.json();
};

const fetchHierarchy = async (schemeUri: string): Promise<ConceptNode[]> => {
  const res = await fetch(`/api/vocabulary/hierarchy?scheme=${encodeURIComponent(schemeUri)}`);
  if (!res.ok) throw new Error('Failed to fetch hierarchy');
  return res.json();
};

// Updated to return the ImportResponse
const importVocabulary = async (file: File): Promise<ImportResponse> => {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch('/api/vocabulary/import', {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Failed to import vocabulary');
  return res.json(); 
};

export const useVocabularies = () => {
  return useQuery({ 
    queryKey: ['vocabularies'], 
    queryFn: fetchSchemes 
  });
};

export const useConceptHierarchy = (schemeUri: string | undefined) => {
  return useQuery({
    queryKey: ['hierarchy', schemeUri],
    queryFn: () => fetchHierarchy(schemeUri!),
    enabled: !!schemeUri,
  });
};

// SKOS URIs routinely contain '#' and '/'; the whole URI must be percent-
// encoded so it travels as a single path segment instead of being truncated
// at the fragment.
export const fetchConceptDetail = async (uri: string): Promise<ConceptDetail> => {
  const res = await fetch(`/api/ontology/skos/concept/${encodeURIComponent(uri)}`);
  if (!res.ok) throw new Error('Failed to fetch concept detail');
  return res.json();
};

export const useConceptDetail = (uri: string | undefined) => {
  return useQuery({
    queryKey: ['conceptDetail', uri],
    queryFn: () => fetchConceptDetail(uri!),
    enabled: !!uri,
    retry: false,
  });
};

// 词条类型走图节点全量属性（含前缀键 skos:notation）——hierarchy 端点只读
// 不带前缀的 notation 键，ontology-load 的词表在那儿恒为 null。
const fetchConceptNodes = async (): Promise<GraphNodeSnapshot[]> => {
  const res = await fetch(`/api/graph/nodes?type=${encodeURIComponent('skos:Concept')}&limit=5000`);
  if (!res.ok) throw new Error('Failed to fetch concept nodes');
  const body = await res.json();
  return body.nodes ?? [];
};

export const useConceptTypes = () => {
  return useQuery({
    queryKey: ['conceptTypes'],
    queryFn: fetchConceptNodes,
    select: buildTypeByUri,
    retry: false,
  });
};

export const useImportVocabulary = () => {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: importVocabulary,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['vocabularies'] });
    },
  });
};