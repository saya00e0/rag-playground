import tempfile
import unittest
from pathlib import Path

from eval.dataset import load_dataset
from eval.evaluate_retrieval import score_question, summarize


class DatasetTests(unittest.TestCase):
    def test_load_dataset_parses_valid_record(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dataset.jsonl"
            path.write_text(
                '{"id":"q1","question":"Q?","type":"factual","relevant_docs":["docs/a.txt"],"evidence":"source"}\n',
                encoding="utf-8",
            )
            records = load_dataset(path)
        self.assertEqual(records[0].id, "q1")
        self.assertEqual(records[0].relevant_docs, ("docs/a.txt",))

    def test_load_dataset_rejects_duplicate_ids(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "dataset.jsonl"
            record = '{"id":"q1","question":"Q?","type":"factual","relevant_docs":["docs/a.txt"],"evidence":"source"}\n'
            path.write_text(record + record, encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "duplicate id"):
                load_dataset(path)


class MetricTests(unittest.TestCase):
    def test_score_question_uses_unique_document_ranks(self):
        result = score_question({"a", "b"}, ["x", "a", "a", "b"])
        self.assertEqual(result["recall_at_1"], 0.0)
        self.assertEqual(result["recall_at_3"], 1.0)
        self.assertEqual(result["reciprocal_rank"], 0.5)

    def test_summarize_groups_by_question_type(self):
        result = summarize(
            [
                {"type": "factual", "recall_at_1": 1.0, "recall_at_3": 1.0, "recall_at_5": 1.0, "reciprocal_rank": 1.0, "latency_ms": 10.0},
                {"type": "multi_hop", "recall_at_1": 0.0, "recall_at_3": 1.0, "recall_at_5": 1.0, "reciprocal_rank": 0.5, "latency_ms": 30.0},
            ]
        )
        self.assertEqual(result["aggregate"]["question_count"], 2)
        self.assertEqual(result["aggregate"]["Recall@1"], 0.5)
        self.assertEqual(result["by_type"]["multi_hop"]["mean_latency_ms"], 30.0)


if __name__ == "__main__":
    unittest.main()
