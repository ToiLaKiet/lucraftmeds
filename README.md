# lucraftmeds

`lucraftmeds` is a retrieval-augmented generation (RAG) project with separate
pipelines for document indexing and online querying.

## Project Structure

### Configuration and entry points

| Path | Description |
| --- | --- |
| `README.md` | Project overview, setup instructions, usage, and architecture. |
| `requirements.txt` | Python dependencies. |
| `.env` | API keys and other sensitive settings. This file is not committed to Git. |
| `.gitignore` | Files and directories that Git should ignore. |
| `config.yaml` | Model, chunking, index, database, cache, and evaluation settings. |
| `main.py` | Application entry point for the API process. |
| `Dockerfile` / Compose file | Containers for the API, workers, Redis, and vector database. |

### Data and indexing

| Directory | Description |
| --- | --- |
| `data/` | Raw documents, parsed files, and the golden evaluation set. Keep data separate from application code. |
| `schemas/` | Pydantic models for documents, chunks, and query results. |
| `ingestion/` | Connectors and parsers for PDFs, HTML, tables, OCR, and websites. |
| `chunking/` | Document-specific chunking strategies, parent-child relationships, and token limits. |
| `embeddings/` | Chunk embedding logic and embedding-model version tracking. |
| `vectordb/` | Dense vector index operations for Qdrant, Pinecone, or Milvus. |
| `lexical/` | BM25 and keyword indexes used in hybrid search. |

### Retrieval and generation

| Directory | Description |
| --- | --- |
| `retrieval/` | Hybrid search, metadata filters, and reciprocal rank fusion (RRF). |
| `rerank/` | Cross-encoder reranking of the top candidates. |
| `query/` | Query rewriting, routing, multi-query expansion, and HyDE. |
| `cache/` | Exact and semantic caching to reduce latency and LLM cost. |
| `prompts/` | Versioned prompt templates. |
| `llm/` | LLM client with retries, timeouts, and model fallback. |
| `generation/` | Grounded answer generation with citations and an “I don't know” fallback. |

### Operations and quality

| Directory | Description |
| --- | --- |
| `eval/` | Golden datasets and faithfulness, recall@k, and RAGAS metrics. |
| `observability/` | Traces, per-stage latency, cost, and quality dashboards. |
| `security/` | Authentication, chunk-level access control, and PII redaction. |
| `api/` | FastAPI serving layer; indexing runs separately. |
| `pipelines/` | Offline indexing and online query pipelines. |
| `jobs/` | Scheduled indexing, reindexing, and nightly evaluation jobs. |
| `tests/` | Unit, integration, and retrieval regression tests. |
| `logs/` | Structured logs for debugging and monitoring. |
| `utils/` | Shared helper functions. |
