# Lucraft@lucraftmeds

LucraftMeds is a Retrieval-Augmented Generation (RAG) project organized into two independent components: a backend for data processing and queries, and a frontend for the user interface.

## Project Structure

```text
lucraftmeds/
├── lucraftmeds@be/       # Backend and RAG pipeline
├── lucraftmeds@fe/       # Frontend
├── .gitignore
└── README.md
```

All backend source code and resources reside in `lucraftmeds@be/`. Therefore, commands related to Python, indexing, APIs, or tests must be run from this directory.

### Backend

| Path | Purpose |
| --- | --- |
| `lucraftmeds@be/main.py` | Backend application entry point. |
| `lucraftmeds@be/config.yaml` | Configuration for models, chunking, indexes, databases, caching, and evaluation. |
| `lucraftmeds@be/requirements.txt` | Python dependency list. |
| `lucraftmeds@be/.env` | Environment variables and API keys; do not commit this file to Git. |
| `lucraftmeds@be/data/` | Source documents, processed data, and evaluation datasets. |
| `lucraftmeds@be/schemas/` | Schemas for documents, chunks, and query results. |
| `lucraftmeds@be/ingestion/` | Connectors and parsers for PDFs, HTML, tables, OCR, and websites. |
| `lucraftmeds@be/chunking/` | Document chunking strategies and token limit management. |
| `lucraftmeds@be/embeddings/` | Embedding generation and embedding model version management. |
| `lucraftmeds@be/vectordb/` | Vector database integration and operations. |
| `lucraftmeds@be/lexical/` | BM25 and keyword indexes for hybrid search. |
| `lucraftmeds@be/retrieval/` | Hybrid retrieval, metadata filtering, and result fusion. |
| `lucraftmeds@be/rerank/` | Reranking of retrieved results. |
| `lucraftmeds@be/query/` | Query rewriting, routing, multi-query, and HyDE. |
| `lucraftmeds@be/cache/` | Exact and semantic caching. |
| `lucraftmeds@be/prompts/` | Versioned prompt templates. |
| `lucraftmeds@be/generation/` | Generation of grounded answers with source citations. |
| `lucraftmeds@be/api/` | API layer for indexing and queries. |
| `lucraftmeds@be/pipelines/` | Offline indexing and online query pipelines. |
| `lucraftmeds@be/jobs/` | Scheduled indexing, reindexing, and evaluation jobs. |
| `lucraftmeds@be/eval/` | Evaluation of faithfulness, recall@k, and RAG quality. |
| `lucraftmeds@be/observability/` | Tracing, latency, cost, and quality metrics. |
| `lucraftmeds@be/security/` | Authentication, chunk-level access control, and sensitive data handling. |
| `lucraftmeds@be/tests/` | Unit tests, integration tests, and retrieval regression tests. |
| `lucraftmeds@be/logs/` | Logs for monitoring and debugging. |
| `lucraftmeds@be/utils/` | Shared utilities. |

### Frontend

The user interface source code is located in `lucraftmeds@fe/` and is developed independently of the backend.

## Planned Processing Flow

```text
Documents
  -> Ingestion
  -> Chunking
  -> Embeddings + Lexical index
  -> Vector database
  -> Retrieval
  -> Rerank
  -> Generation
  -> Answer with source references
```

## Backend Setup

Navigate to the backend directory before creating the environment or running Python commands:

```bash
cd lucraftmeds@be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `lucraftmeds@be/.env` locally to store the required environment variables. Do not include API keys or sensitive information in the source code.

Once `main.py`, `requirements.txt`, and `config.yaml` are finalized, the backend will be launched from `lucraftmeds@be/`. The specific startup command will be documented here alongside the application entry point.

## Development Conventions

- Run backend commands from `lucraftmeds@be/`.
- Place tests in `lucraftmeds@be/tests/`.
- Do not commit `.env`, logs, sensitive data, or runtime-generated data.
- Update the README when adding entry points, dependencies, or infrastructure services.
