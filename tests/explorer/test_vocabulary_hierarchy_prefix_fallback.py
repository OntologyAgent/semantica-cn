"""Prefix-key fallback for the vocabulary hierarchy summary (fork fix).

The ontology-load path stores node property keys WITH prefixes
(``skos:definition``, ``skos:altLabel``, ``skos:notation``), while
``/api/vocabulary/hierarchy``'s ``_concept_summary`` only read the bare keys
written by the vocabulary-import path — so descriptions arrived as None for
ontology-loaded graphs. Mirror the concept-detail endpoint's fallback
(``bare | prefixed``) so both ingestion paths render.
"""

from semantica.explorer.routes.vocabulary import _concept_summary


class TestConceptSummaryPrefixFallback:
    def test_bare_keys_still_win(self):
        node = {
            "id": "az:Contract",
            "content": "合同",
            "properties": {
                "pref_label": "合同",
                "alt_labels": ["契约"],
                "description": " Bare path description ",
                "notation": "class",
            },
        }
        summary = _concept_summary(node)
        assert summary.pref_label == "合同"
        assert summary.alt_labels == ["契约"]
        assert summary.description == " Bare path description "
        assert summary.notation == "class"

    def test_prefixed_keys_fill_in_when_bare_missing(self):
        node = {
            "id": "az:Policy",
            "content": "Policy",
            "properties": {
                "skos:prefLabel": "政策",
                "skos:altLabel": ["政策类"],
                "skos:definition": "政策类",
                "skos:notation": "class",
            },
        }
        summary = _concept_summary(node)
        assert summary.pref_label == "政策"
        assert summary.alt_labels == ["政策类"]
        assert summary.description == "政策类"
        assert summary.notation == "class"

    def test_prefixed_alt_label_scalar_becomes_list(self):
        node = {
            "id": "az:Policy",
            "properties": {"skos:altLabel": "政策类"},
        }
        summary = _concept_summary(node)
        assert summary.alt_labels == ["政策类"]

    def test_content_fallback_for_pref_label_unchanged(self):
        node = {"id": "az:Bare", "content": "裸节点", "properties": {}}
        summary = _concept_summary(node)
        assert summary.pref_label == "裸节点"
        assert summary.description is None
