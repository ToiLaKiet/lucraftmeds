"""Utilities for splitting documents at semantic topic boundaries."""

from collections.abc import Iterable
from typing import Literal

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker


BreakpointThresholdType = Literal[
    "percentile", "standard_deviation", "interquartile", "gradient"
]


def chunk_documents(
    documents: Iterable[Document],
    embeddings: Embeddings,
    *,
    breakpoint_threshold_type: BreakpointThresholdType = "percentile",
    breakpoint_threshold_amount: float | None = None,
) -> list[Document]:
    """Split non-blank documents by semantic similarity."""
    if breakpoint_threshold_type not in {
        "percentile",
        "standard_deviation",
        "interquartile",
        "gradient",
    }:
        raise ValueError(f"unsupported breakpoint threshold: {breakpoint_threshold_type}")

    non_blank_documents = [
        document for document in documents if document.page_content.strip()
    ]
    if not non_blank_documents:
        return []

    splitter = SemanticChunker(
        embeddings,
        add_start_index=True,
        breakpoint_threshold_type=breakpoint_threshold_type,
        breakpoint_threshold_amount=breakpoint_threshold_amount,
    )
    return splitter.split_documents(non_blank_documents)
