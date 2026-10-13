"""URI passthrough in the SPARQL graph builder (fork fix).

`_build_rdflib_graph` wrapped every node id as ``http://semantica.local/entity/<id>``.
Once mounted graphs carry real az: URIs as node ids (id-unification plan),
entities became double-wrapped (`semantica.local/entity/https://demo…`)
and bare-URI queries returned nothing. Node ids that already are http(s)
URIs must be used as-is; other ids keep the wrapper.
"""

import pytest

rdflib = pytest.importorskip("rdflib")
pytest.importorskip("fastapi")

from semantica.context.context_graph import ContextGraph  # noqa: E402
from semantica.explorer.routes.sparql import _build_rdflib_graph  # noqa: E402
from semantica.explorer.session import GraphSession  # noqa: E402

DEMO = "https://demo.local/ontology/az/HuayueHoldings"
POLICY = "https://demo.local/ontology/az/DemoPolicy"


def _sample_session() -> GraphSession:
    graph = ContextGraph(advanced_analytics=False)
    graph.add_node(DEMO, node_type="company", content="华跃演示", layer="instance")
    graph.add_node(POLICY, node_type="policy", content="返利政策", layer="instance")
    graph.add_node("plain_id", node_type="concept", content="Plain")
    graph.add_edge(DEMO, POLICY, edge_type="适用于", weight=1.0, layer="business")
    graph.add_edge("plain_id", "plain_id2", edge_type="used_in", weight=0.5)
    return GraphSession(graph)


def _query_rows(graph: rdflib.Graph, query: str):
    return list(graph.query(query))


class TestUriPassthrough:
    def test_bare_uri_subject_query_returns_triples(self):
        g = _build_rdflib_graph(_sample_session())
        rows = _query_rows(
            g,
            f"SELECT ?p ?o WHERE {{ <{DEMO}> ?p ?o }}",
        )
        predicates = {str(row[0]) for row in rows}
        # rdf:type, rdfs:label, and the business predicate at minimum
        assert len(rows) >= 3
        assert any("rdf-schema#label" in p for p in predicates)

    def test_business_edge_connects_bare_uri_subject_and_object(self):
        g = _build_rdflib_graph(_sample_session())
        rows = _query_rows(
            g,
            f"SELECT ?p WHERE {{ <{DEMO}> ?p <{POLICY}> }}",
        )
        assert len(rows) == 1
        assert "适用于" in str(rows[0][0])

    def test_non_uri_ids_keep_entity_namespace_wrapper(self):
        g = _build_rdflib_graph(_sample_session())
        rows = _query_rows(
            g,
            "SELECT ?p ?o WHERE { <http://semantica.local/entity/plain_id> ?p ?o }",
        )
        # rdf:type + rdfs.label + used_in self-loop edge
        assert len(rows) >= 3

    def test_no_double_wrapped_uris_exist(self):
        g = _build_rdflib_graph(_sample_session())
        for subject, _, _ in g:
            assert not str(subject).startswith(
                "http://semantica.local/entity/https://"
            ), f"double-wrapped subject: {subject}"
