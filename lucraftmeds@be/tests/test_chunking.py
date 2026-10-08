import unittest

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from chunking.chunking import chunk_documents


class TopicEmbeddings(Embeddings):
    """Deterministic embeddings with one clear topic boundary."""

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        midpoint = len(texts) // 2
        return [
            [1.0, 0.0] if index < midpoint else [0.0, 1.0]
            for index in range(len(texts))
        ]

    def embed_query(self, text: str) -> list[float]:
        return [1.0, 0.0]


class ChunkDocumentsTests(unittest.TestCase):
    def setUp(self):
        self.embeddings = TopicEmbeddings()

    def test_splits_at_semantic_boundary_and_preserves_metadata(self):
        metadata = {
            "doc_id": "medical-1",
            "title": "Tài liệu tổng hợp",
            "url": "https://example.com/medical-1",
            "author": "LucraftMeds",
            "source": "example.com",
        }
        text = (
            "Tim bơm máu đi khắp cơ thể. "
            "Huyết áp phản ánh lực của máu. "
            "Các hành tinh quay quanh ngôi sao. "
            "Tàu vũ trụ hoạt động ngoài khí quyển."
        )

        chunks = chunk_documents(
            [Document(page_content=text, metadata=metadata)],
            self.embeddings,
            breakpoint_threshold_amount=50,
        )

        self.assertEqual(len(chunks), 2)
        self.assertIn("Huyết áp", chunks[0].page_content)
        self.assertNotIn("hành tinh", chunks[0].page_content)
        self.assertIn("hành tinh", chunks[1].page_content)
        self.assertEqual(chunks[0].metadata, {**metadata, "start_index": 0})
        self.assertEqual(
            chunks[1].metadata,
            {**metadata, "start_index": len(chunks[0].page_content)},
        )

    def test_single_sentence_stays_whole(self):
        chunks = chunk_documents(
            [Document(page_content="Nội dung y khoa bằng tiếng Việt.", metadata={})],
            self.embeddings,
        )

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].page_content, "Nội dung y khoa bằng tiếng Việt.")
        self.assertEqual(chunks[0].metadata["start_index"], 0)

    def test_multiple_documents_do_not_mix_metadata(self):
        documents = [
            Document(page_content="Thông tin tim mạch.", metadata={"doc_id": "a"}),
            Document(page_content="Thông tin hô hấp.", metadata={"doc_id": "b"}),
        ]

        chunks = chunk_documents(documents, self.embeddings)

        self.assertEqual([chunk.metadata["doc_id"] for chunk in chunks], ["a", "b"])

    def test_empty_and_blank_documents_return_no_chunks(self):
        self.assertEqual(chunk_documents([], self.embeddings), [])
        self.assertEqual(
            chunk_documents(
                [Document(page_content=" \n\t", metadata={"doc_id": "blank"})],
                self.embeddings,
            ),
            [],
        )

    def test_invalid_settings_raise_value_error(self):
        with self.assertRaises(ValueError):
            chunk_documents(
                [],
                self.embeddings,
                breakpoint_threshold_type="unknown",  # type: ignore[arg-type]
            )

        for kwargs in (
            {"min_tokens": 0},
            {"max_tokens": 0},
            {"min_tokens": 4, "max_tokens": 3},
        ):
            with self.assertRaises(ValueError):
                chunk_documents([], self.embeddings, **kwargs)

    def test_max_tokens_splits_oversized_chunks(self):
        chunks = chunk_documents(
            [Document(page_content="one two three four five", metadata={})],
            self.embeddings,
            max_tokens=2,
        )

        self.assertEqual(
            [chunk.page_content for chunk in chunks],
            ["one two", "three four", "five"],
        )
        self.assertTrue(all(len(chunk.page_content.split()) <= 2 for chunk in chunks))
        self.assertEqual([chunk.metadata["start_index"] for chunk in chunks], [0, 8, 19])

    def test_min_tokens_merges_small_semantic_chunks(self):
        chunks = chunk_documents(
            [
                Document(
                    page_content="one two. three four. five six. seven eight.",
                    metadata={},
                )
            ],
            self.embeddings,
            breakpoint_threshold_amount=50,
            min_tokens=4,
        )

        self.assertTrue(all(len(chunk.page_content.split()) >= 4 for chunk in chunks))

    def test_custom_token_counter_is_used(self):
        chunks = chunk_documents(
            [Document(page_content="aa bb cc", metadata={})],
            self.embeddings,
            max_tokens=4,
            token_count=len,
        )

        self.assertEqual([chunk.page_content for chunk in chunks], ["aa", "bb", "cc"])


if __name__ == "__main__":
    unittest.main()
