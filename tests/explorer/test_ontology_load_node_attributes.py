"""Injected-node attributes via ontology-load (fork fix).

The load path dropped ``skos:prefLabel`` at ingestion (only ``rdfs:label``
was read), so TTLs using SKOS-style Chinese labels injected nodes whose
inspector panels rendered bare. Labels now fall back to skos:prefLabel and
the graph converter mirrors the label as ``skos:prefLabel`` alongside
``rdfs:label``/``rdfs:comment`` in node properties.
"""

import tempfile
from pathlib import Path

from semantica.explorer.routes.ontology import _convert_ontology_to_graph
from semantica.ingest.ontology_ingestor import OntologyIngestor

_TTL = """@prefix az: <http://example.com/az/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
az:Policy a owl:Class ;
    skos:prefLabel "政策" ;
    rdfs:comment "Policy class" .
az:appliesTo a owl:ObjectProperty ;
    skos:prefLabel "适用于" ;
    rdfs:comment "政策适用关系" .
"""


def _ingest() -> dict:
    with tempfile.NamedTemporaryFile(mode="w", suffix=".ttl", delete=False, encoding="utf-8") as f:
        f.write(_TTL)
        path = f.name
    try:
        return OntologyIngestor().ingest_ontology(path).data
    finally:
        Path(path).unlink(missing_ok=True)


class TestIngestorPrefLabelFallback:
    def test_class_label_falls_back_to_skos_pref_label(self):
        data = _ingest()
        cls = data["classes"][0]
        assert cls["uri"] == "http://example.com/az/Policy"
        assert cls["label"] == "政策"
        assert cls["description"] == "Policy class"

    def test_property_label_falls_back_to_skos_pref_label(self):
        data = _ingest()
        prop = data["properties"][0]
        assert prop["uri"] == "http://example.com/az/appliesTo"
        assert prop["label"] == "适用于"
        assert prop["description"] == "政策适用关系"


class TestConverterNodeAttributes:
    def test_injected_nodes_carry_preflabel_and_comment(self):
        nodes, _edges = _convert_ontology_to_graph(_ingest())
        by_id = {node["id"]: node for node in nodes}
        cls = by_id["http://example.com/az/Policy"]
        assert cls["properties"]["skos:prefLabel"] == "政策"
        assert cls["properties"]["rdfs:comment"] == "Policy class"
        prop = by_id["http://example.com/az/appliesTo"]
        assert prop["properties"]["skos:prefLabel"] == "适用于"
        assert prop["properties"]["rdfs:comment"] == "政策适用关系"
