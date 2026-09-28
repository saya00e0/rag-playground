import unittest

from graph.builder import ChunkRef, GraphBuilder, graph_statistics
from graph.extractor import Extraction, Entity, Relation, normalize_entity, parse_extraction
from graph.retriever import GraphRetriever


class ExtractorTests(unittest.TestCase):
    def test_normalize_entity_merges_simple_variants(self):
        self.assertEqual(normalize_entity(" BERT model "), "bert")
        self.assertEqual(normalize_entity("BERT"), "bert")

    def test_parse_extraction_rejects_extra_top_level_keys(self):
        with self.assertRaisesRegex(ValueError, "only entities and relations"):
            parse_extraction('{"entities": [], "relations": [], "note": "bad"}')

    def test_parse_extraction_rejects_out_of_vocabulary_relation(self):
        payload = '{"entities":[{"name":"田中健","type":"person"},{"name":"Catalog Service","type":"service"}],"relations":[{"source":"田中健","target":"Catalog Service","type":"owns"}]}'
        with self.assertRaisesRegex(ValueError, "outside the configured vocabulary"):
            parse_extraction(payload)

    def test_parse_extraction_excludes_undeclared_relation_endpoint(self):
        payload = '{"entities":[{"name":"田中健","type":"person"}],"relations":[{"source":"田中健","target":"Catalog Service","type":"responsible_for"}]}'
        extraction = parse_extraction(payload)
        self.assertEqual(extraction.relations, ())
        self.assertEqual(len(extraction.rejected_relations), 1)


class GraphTests(unittest.TestCase):
    def setUp(self):
        builder = GraphBuilder()
        builder.add_extraction(
            ChunkRef("docs/a.txt", 0),
            Extraction(
                entities=(Entity("田中健", "person"), Entity("Catalog Service", "service")),
                relations=(Relation("田中健", "Catalog Service", "owns"),),
            ),
        )
        builder.add_extraction(
            ChunkRef("docs/b.txt", 0),
            Extraction(
                entities=(Entity("Catalog Service", "service"), Entity("Vector Index", "service")),
                relations=(Relation("Catalog Service", "Vector Index", "queries"),),
            ),
        )
        self.graph = builder.build()

    def test_graph_preserves_chunk_provenance(self):
        node = next(node for node in self.graph["nodes"] if node["id"] == "catalog service")
        self.assertEqual(set(node["chunk_refs"]), {"docs/a.txt#0", "docs/b.txt#0"})
        self.assertEqual(graph_statistics(self.graph)["edge_count"], 2)

    def test_retrieval_traverses_from_named_seed(self):
        result = GraphRetriever(self.graph).retrieve("田中健の担当サービスは？", depth=1, max_chunks=5)
        self.assertEqual(result[0].source, "docs/a.txt")
        self.assertEqual([item.source for item in result], ["docs/a.txt", "docs/b.txt"])


if __name__ == "__main__":
    unittest.main()
