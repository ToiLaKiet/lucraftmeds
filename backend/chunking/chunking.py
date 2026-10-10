"""Utilities for splitting documents at semantic topic boundaries."""

from collections.abc import Iterable
import re
from typing import Callable, Literal

from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_experimental.text_splitter import SemanticChunker


BreakpointThresholdType = Literal[
    "percentile", "standard_deviation", "interquartile", "gradient"
]


def _default_token_count(text: str) -> int:
    """Count whitespace-delimited tokens without requiring a tokenizer package."""
    return len(re.findall(r"\S+", text))


def _split_to_token_limit(
    document: Document,
    max_tokens: int,
    token_count: Callable[[str], int],
) -> list[Document]:
    """Split a document into the largest whitespace-aligned pieces that fit."""
    text = document.page_content
    if token_count(text) <= max_tokens:
        return [document]

    pieces: list[Document] = []
    offset = 0
    while offset < len(text):
        remainder = text[offset:]
        if token_count(remainder) <= max_tokens:
            end = len(text)
        else:
            low, high = 1, len(remainder)
            while low < high:
                midpoint = (low + high + 1) // 2
                if token_count(remainder[:midpoint]) <= max_tokens:
                    low = midpoint
                else:
                    high = midpoint - 1
            end = offset + low
            whitespace = text.rfind(" ", offset, end + 1)
            if whitespace > offset:
                end = whitespace

        content = text[offset:end].strip()
        if content:
            metadata = dict(document.metadata)
            metadata["start_index"] = document.metadata.get("start_index", 0) + offset
            pieces.append(Document(page_content=content, metadata=metadata))
        offset = end
        while offset < len(text) and text[offset].isspace():
            offset += 1

    return pieces


def _merge_small_chunks(
    chunks: list[Document],
    min_tokens: int,
    max_tokens: int | None,
    token_count: Callable[[str], int],
) -> list[Document]:
    """Merge undersized adjacent chunks when doing so respects the maximum."""
    merged: list[Document] = []
    for chunk in chunks:
        if merged and token_count(merged[-1].page_content) < min_tokens:
            content = f"{merged[-1].page_content} {chunk.page_content}"
            if max_tokens is None or token_count(content) <= max_tokens:
                previous = merged[-1]
                merged[-1] = Document(
                    page_content=content, metadata=previous.metadata
                )
                continue
        merged.append(chunk)

    if len(merged) > 1 and token_count(merged[-1].page_content) < min_tokens:
        content = f"{merged[-2].page_content} {merged[-1].page_content}"
        if max_tokens is None or token_count(content) <= max_tokens:
            previous = merged[-2]
            merged[-2:] = [
                Document(page_content=content, metadata=previous.metadata)
            ]
    return merged


def chunk_documents(
    documents: Iterable[Document],
    embeddings: Embeddings,
    *,
    breakpoint_threshold_type: BreakpointThresholdType = "percentile",
    breakpoint_threshold_amount: float | None = None,
    min_tokens: int | None = None,
    max_tokens: int | None = None,
    token_count: Callable[[str], int] = _default_token_count,
) -> list[Document]:
    """Split documents semantically and enforce optional token-count bounds.

    ``token_count`` can be replaced with the embedding model's tokenizer for
    model-exact limits. By default, tokens are whitespace-delimited words.
    A minimum is best-effort when a whole document is shorter than the limit.
    """
    if breakpoint_threshold_type not in {
        "percentile",
        "standard_deviation",
        "interquartile",
        "gradient",
    }:
        raise ValueError(f"unsupported breakpoint threshold: {breakpoint_threshold_type}")
    if min_tokens is not None and min_tokens <= 0:
        raise ValueError("min_tokens must be greater than zero")
    if max_tokens is not None and max_tokens <= 0:
        raise ValueError("max_tokens must be greater than zero")
    if min_tokens is not None and max_tokens is not None and min_tokens > max_tokens:
        raise ValueError("min_tokens cannot be greater than max_tokens")

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
    chunks: list[Document] = []
    for document in non_blank_documents:
        document_chunks = splitter.split_documents([document])
        if max_tokens is not None:
            document_chunks = [
                piece
                for chunk in document_chunks
                for piece in _split_to_token_limit(chunk, max_tokens, token_count)
            ]
        if min_tokens is not None:
            document_chunks = _merge_small_chunks(
                document_chunks, min_tokens, max_tokens, token_count
            )
        chunks.extend(document_chunks)
    return chunks
