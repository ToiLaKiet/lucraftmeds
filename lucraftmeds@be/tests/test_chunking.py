import unittest

from langchain_core.documents import Document

"""Utilities for splitting source documents into embedding-ready chunks."""

from collections.abc import Iterable

from langchain_text_splitters import RecursiveCharacterTextSplitter


def chunk_documents(
    documents: Iterable[Document],
    *,
    chunk_size: int = 1000,
    chunk_overlap: int = 150,
) -> list[Document]:
    """Split non-blank documents while preserving their source metadata."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than zero")
    if chunk_overlap < 0:
        raise ValueError("chunk_overlap must be non-negative")
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    non_blank_documents = (
        document for document in documents if document.page_content.strip()
    )
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len,
        keep_separator=True,
        add_start_index=True,
        strip_whitespace=True,
    )
    return splitter.split_documents(non_blank_documents)


class ChunkDocumentsTests(unittest.TestCase):
    def test_short_document_stays_whole_and_preserves_metadata(self):
        metadata = {
            "doc_id": "medical-1",
            "title": "Chăm sóc sức khỏe",
            "url": "https://example.com/medical-1",
            "author": "LucraftMeds",
            "source": "example.com",
        }
        chunks = chunk_documents(
            [Document(page_content="Nội dung y khoa bằng tiếng Việt.", metadata=metadata)]
        )

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0].page_content, "Nội dung y khoa bằng tiếng Việt.")
        self.assertEqual(chunks[0].metadata, {**metadata, "start_index": 0})

    def test_long_document_is_split_with_overlap_and_start_indexes(self):
        text = "0123456789" * 8
        chunks = chunk_documents(
            [Document(page_content=text, metadata={"doc_id": "medical-2"})],
            chunk_size=20,
            chunk_overlap=5,
        )

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(chunk.page_content for chunk in chunks))
        self.assertTrue(all(len(chunk.page_content) <= 20 for chunk in chunks))
        self.assertTrue(
            all(
                current.page_content[-5:] == following.page_content[:5]
                for current, following in zip(chunks, chunks[1:])
            )
        )
        self.assertTrue(
            all(isinstance(chunk.metadata["start_index"], int) for chunk in chunks)
        )

    def test_multiple_documents_do_not_mix_metadata(self):
        documents = [
            Document(page_content="A" * 30, metadata={"doc_id": "a"}),
            Document(page_content="B" * 30, metadata={"doc_id": "b"}),
        ]

        chunks = chunk_documents(documents, chunk_size=20, chunk_overlap=5)

        self.assertEqual({chunk.metadata["doc_id"] for chunk in chunks}, {"a", "b"})
        for chunk in chunks:
            expected_character = chunk.metadata["doc_id"].upper()
            self.assertEqual(set(chunk.page_content), {expected_character})

    def test_empty_and_blank_documents_return_no_chunks(self):
        self.assertEqual(chunk_documents([]), [])
        self.assertEqual(
            chunk_documents([Document(page_content=" \n\t", metadata={"doc_id": "blank"})]),
            [],
        )

    def test_invalid_chunk_settings_raise_value_error(self):
        invalid_settings = (
            {"chunk_size": 0, "chunk_overlap": 0},
            {"chunk_size": 10, "chunk_overlap": -1},
            {"chunk_size": 10, "chunk_overlap": 10},
            {"chunk_size": 10, "chunk_overlap": 11},
        )

        for settings in invalid_settings:
            with self.subTest(settings=settings), self.assertRaises(ValueError):
                chunk_documents([], **settings)


if __name__ == "__main__":
    unittest.main()
