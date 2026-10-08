<div align="center">

# LucraftMeds

**A medical Retrieval-Augmented Generation platform.**

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
├── lucraftmeds@be/
│   ├── api/
│   ├── chunking/
│   ├── tests/
│   ├── config.yaml
│   ├── main.py
│   └── requirements.txt
├── lucraftmeds@fe/
│   └── fe/
│       ├── app/
│       ├── public/
│       └── package.json
├── lucraftmeds@notebooks/
│   ├── chunkings/
│   ├── crawl4ai-dataset-creation/
│   ├── domains-analyzation/
│   └── preprocessing.ipynb
└── README.md
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
