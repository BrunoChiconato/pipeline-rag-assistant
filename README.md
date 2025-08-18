# Pipeline RAG Assistant

![Python](https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-agents-lightgrey?style=for-the-badge)

> **One-liner**: A LangGraph-powered assistant that **observes Airflow pipelines** and **answers questions** using **RAG over logs & docs**, with streaming UX and a simple web UI.

## Table of Contents

- [About the Project](#about-the-project)
- [Built With](#built-with)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Environment](#environment)
- [Usage](#usage)
- [Testing](#testing)
- [Roadmap](#roadmap)
- [Contributing](#contributing)
- [Contact & Acknowledgements](#contact--acknowledgements)

## About the Project

**Problem:** Pipeline owners and analysts struggle to **quickly pinpoint failures or anomalies** in ETL jobs and logs scattered across tools.  
**Solution:** This assistant exposes a **chat interface** backed by **LangGraph agents** that can:
- call **Airflow’s REST API** to fetch DAG/task status & logs,
- run **RAG** against a **vector store (pgvector/PGVector)** with historical logs, runbooks and docs,
- **stream** partial responses for better UX.

**Goals**
- First-class **observability & triage** for job runs.
- **Explainability**: cite where an answer came from (log snippet, doc).
- **Extensibility**: add more tools (e.g., metrics, cloud storage, incident pages).

## Built With

- **LangGraph** (agent orchestration & streaming)
- **LangChain Tools** (tool-calling)
- **FastAPI** (API)
- **Streamlit** (UI)
- **PostgreSQL + pgvector** (vector store) via **LangChain PGVector**
- **Azure OpenAI / OpenAI** (embeddings & chat)

## Architecture

```mermaid
graph TD
  U[User: CLI/Streamlit] --> API[FastAPI / /query]
  API --> AG[LangGraph Agent<br/>create_react_agent]
  AG -->|Tool| AF[Airflow REST API<br/>/dags/.../taskInstances/.../logs]
  AG -->|Retriever| VS[(Postgres + pgvector)]
  VS --> EMB["Embeddings<br/>(Azure OpenAI / OpenAI)"]
  AG --> OUT[Streaming tokens & steps]
```

**Notes**

* Agent orchestration & streaming via **LangGraph** (`stream()` / `astream()` with `stream_mode="updates" | "messages"`).
* **Airflow Stable REST API** is used for listing runs and paginating task logs with a continuation token.
* A **pgvector** vector store, integrated through **LangChain PGVector**.

## Getting Started

### Prerequisites

* **Python 3.12**
* **Docker & Docker Compose**
* **PostgreSQL 16**
* API keys: **OpenAI** (or **Azure OpenAI**)

### Installation

```bash
# 1) Clone
git clone https://github.com/BrunoChiconato/pipeline-rag-assistant.git
cd pipeline-rag-assistant

# 2) Create & activate venv
python3 -m venv .venv
source .venv/bin/activate

# 3) Install deps
pip install -r requirements.txt

# 4) Start Postgres + pgvector (dev)
docker compose up -d pgvector

# 5) Prepare DB schema (pgvector tables/collections)
python scripts/setup_vector_store.py
```

### Environment

```bash
cp .env.example .env
# Fill with your keys:
# OPENAI_API_KEY=...
# or Azure:
# AZURE_OPENAI_API_KEY=...
# AZURE_OPENAI_ENDPOINT=...
# AZURE_OPENAI_API_VERSION=2024-XX-XX
# DATABASE_URL=postgresql+psycopg://user:pass@localhost:5432/pgv
# AIRFLOW_BASE_URL=https://seu-airflow
# AIRFLOW_TOKEN=...
```

## Usage

**Ingest sample docs/logs to the vector store**

```bash
python scripts/ingest_docs.py --path data/examples
```

**Run API (FastAPI)**

```bash
uvicorn app.api:app --reload --port 8000
```

**Query (curl)**

```bash
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question":"Why did DAG my_dag fail yesterday?"}'
```

**Optional UI (Streamlit)**

```bash
streamlit run app/ui.py
```

> Streaming: server streams **LLM tokens** and **agent step updates** for a responsive UX.

## Testing

```bash
pytest
# coverage (optional)
pytest --cov=src --cov-report=html
# open htmlcov/index.html
```

## Roadmap

* v0.1: Single RAG agent + Airflow logs/tool + PGVector retriever.
* v0.2: Better citations (log line anchors), eval suite (golden Q\&A).
* v0.3: Additional tools (cloud metrics, data quality checks), tracing.

## Contributing

PRs are welcome! Please open an **Issue** first for discussion and follow a feature branch flow:

1. `git checkout -b feature/awesome`
2. `git commit -m "feat: add awesome"`
3. `git push origin feature/awesome`
4. Open a Pull Request

See `CONTRIBUTING.md` (to be added).

## Contact & Acknowledgements

* Author: Bruno Chiconato – [LinkedIn](https://www.linkedin.com/in/brunochiconato/)
* Thanks: LangGraph, LangChain, pgvector, Streamlit, Airflow communities.

**References**

* LangGraph: prebuilt `create_react_agent`, persistence/streaming.
* LangChain Tools & PGVector integration.
* pgvector (Postgres extension).
* Airflow Stable REST API (task logs & continuation token).
* Streaming chat completions.