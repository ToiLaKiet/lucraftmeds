"""Utilities for splitting source documents into embedding-ready chunks."""

from collections.abc import Iterable

from langchain_core.documents import Document
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
