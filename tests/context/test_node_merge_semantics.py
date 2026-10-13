"""Node id-merge semantics for ContextGraph (fork extension).

The data-side pipeline mounts a panorama context.json whose node ids share the
az: URI namespace with nodes injected via /api/ontology/load. Re-adding a node
under an existing id must MERGE properties (keep what is there, fold in what is
new) instead of replacing the stored node — otherwise whichever side lands
first silently loses its attributes (e.g. layer vs rdfs:comment).
"""

from semantica.context.context_graph import ContextGraph


class TestSameIdNodeMerge:
    def test_readd_merges_properties_instead_of_replacing(self):
        graph = ContextGraph()
        graph.add_node("az:Policy", "class", content="Policy",
                       **{"rdfs:comment": "政策类", "skos:prefLabel": "Policy"})
        graph.add_node("az:Policy", "class", content="Policy", layer="class")

        node = graph.nodes["az:Policy"]
        merged = {**node.metadata, **node.properties}
        assert merged.get("layer") == "class"
        assert merged.get("rdfs:comment") == "政策类"
        assert merged.get("skos:prefLabel") == "Policy"

    def test_readd_keeps_existing_content_and_type(self):
        graph = ContextGraph()
        graph.add_node("az:Policy", "class", content="政策")
        graph.add_node("az:Policy", "entity", content="az:Policy")

        node = graph.nodes["az:Policy"]
        assert node.content == "政策"
        assert node.node_type == "class"

    def test_readd_returns_true_so_batch_counts_stay_stable(self):
        graph = ContextGraph()
        assert graph.add_node("az:Policy", "class", content="Policy") is True
        assert graph.add_node("az:Policy", "class", content="Policy", layer="class") is True

    def test_add_nodes_dict_batch_merges_same_id(self):
        graph = ContextGraph()
        graph.add_nodes([
            {"id": "az:Policy", "type": "class", "content": "Policy",
             "properties": {"rdfs:comment": "政策类"}},
        ])
        graph.add_nodes([
            {"id": "az:Policy", "type": "class", "content": "Policy",
             "properties": {"layer": "class"}},
        ])

        node = graph.nodes["az:Policy"]
        merged = {**node.metadata, **node.properties}
        assert merged.get("layer") == "class"
        assert merged.get("rdfs:comment") == "政策类"

    def test_distinct_ids_are_unaffected(self):
        graph = ContextGraph()
        graph.add_node("az:Policy", "class", content="Policy", layer="class")
        graph.add_node("az:Contract", "instance", content="Contract", layer="instance")

        assert set(graph.nodes) == {"az:Policy", "az:Contract"}
        assert graph.nodes["az:Contract"].properties.get("layer") == "instance"
