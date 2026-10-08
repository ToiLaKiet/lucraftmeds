<div align="center">

# LucraftMeds

**A RAG-powered AI chatbot system serving accurate medical consultant demands.**

LucraftMeds turns trusted medical sources into searchable knowledge and delivers
grounded answers with relevant context, helping users find reliable health
information quickly and clearly.

<br/>

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)
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
├── lucraftmeds@be/                         # Medical knowledge backend
│   ├── api/                                # Exposes backend capabilities to clients
│   │   └── fastapi.py                      # HTTP API application
│   ├── chunking/                           # Prepares medical content for retrieval
│   │   └── chunking.py                     # Semantic splitting and token limits
│   ├── tests/                              # Validates backend data-processing behavior
│   │   └── test_chunking.py                # Semantic chunking tests
│   ├── config.yaml                         # Models and service configuration
│   ├── main.py                             # Backend application entry point
│   └── requirements.txt                    # Backend Python dependencies
├── lucraftmeds@fe/
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

- Python `3.10+`
- Node.js `20+` and npm
- JupyterLab or Jupyter Notebook
- Qdrant for vector storage

## Run the Backend

```bash
cd lucraftmeds@be
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create `lucraftmeds@be/.env` and add the required local environment variables.
The backend start command will be added when the API entry point is finalized.

## Run the Frontend

```bash
cd lucraftmeds@fe/fe
npm install
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

For a production build:

```bash
npm run build
npm run start
```
