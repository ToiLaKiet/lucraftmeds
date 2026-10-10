<div align="center">

# LucraftMeds

**A RAG-powered AI chatbot system serving accurate medical consultant demands.**

LucraftMeds turns trusted medical sources into searchable knowledge and delivers
grounded answers with relevant context, helping users find reliable health
information quickly and clearly.

<br/>

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)
![Qdrant](https://img.shields.io/badge/Qdrant-DC244C?style=for-the-badge&logo=qdrant&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js%2016-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)
![React](https://img.shields.io/badge/React%2019-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)

</div>

---

<!--
## System Architecture

TODO: Add the system architecture diagram and explanation.
-->

## Directory Structure

```text
lucraftmeds/
├── backend/                                # Medical knowledge backend
│   ├── api/                                # Exposes backend capabilities to clients
│   │   └── fastapi.py                      # HTTP API application
│   ├── chunking/                           # Prepares medical content for retrieval
│   │   └── chunking.py                     # Semantic splitting and token limits
│   ├── generation/                         # RAG answer-generation design
│   │   └── readme.md                       # Streaming generation flow
│   ├── tests/                              # Validates backend data-processing behavior
│   │   └── test_chunking.py                # Semantic chunking tests
│   ├── .python-version                     # Python version used by uv
│   ├── config.yaml                         # Models and service configuration
│   ├── main.py                             # Backend application entry point
│   ├── pyproject.toml                      # Project and dependency declarations
│   ├── uv.lock                             # Reproducible dependency lockfile
│   └── README.md                           # Backend setup and testing guide
├── frontend/
│   └── fe/                                 # User-facing medical search application
│       ├── app/                            # Pages, layouts, and global presentation
│       ├── public/                         # Public images and static resources
│       └── package.json                    # Frontend dependencies and run commands
├── lucraftmeds@notebooks/                  # Medical knowledge preparation workspace
│   ├── crawl4ai-dataset-creation/          # Collects source content from websites
│   │   ├── crawl4ai-html-to-md.ipynb       # Converts web pages into Markdown datasets
│   │   └── drives-merge.ipynb              # Combines collected dataset files
│   ├── domains-analyzation/                # Reviews coverage and quality by source domain
│   │   └── domains-analysis.ipynb           # Analyzes collected medical domains
│   ├── chunkings/                          # Converts cleaned content into retrievable units
│   │   └── bgem3-semantic-chunking.ipynb   # Chunks, embeds, and uploads data to Qdrant
│   └── preprocessing.ipynb                 # Cleans and standardizes collected content
└── README.md                               # Setup and project usage guide
```

## Requirements

- [uv](https://docs.astral.sh/uv/) for Python and backend dependency management
- Python `3.12+` (uv installs it automatically when needed)
- Node.js `20+` and npm
- JupyterLab or Jupyter Notebook
- Qdrant for vector storage

## Run the Backend

```bash
cd backend
uv sync
```

`uv sync` reads `pyproject.toml` and `uv.lock`, installs the required Python
version when necessary, and creates an isolated environment at `backend/.venv`.
Activating the environment manually is not required; use `uv run` for backend
commands.

Create `backend/.env` and add the required local environment variables. The
backend start command will be added when the API entry point is finalized.

See [`backend/README.md`](backend/README.md) for backend development and testing
instructions.

## Run the Frontend

```bash
cd frontend/fe
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

For a production build:

```bash
npm run build
npm run start
```
