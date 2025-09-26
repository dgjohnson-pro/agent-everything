# agent-everything
v2 design for agent tools using modern framework
# Streamlit + LangChain Agent + Ollama

Minimal chatbot UI using **Streamlit**, a **LangChain agent**, and a local **Ollama** model (`llama3.2:latest`).  
Includes two tools: Python REPL and DuckDuckGo search.

---

## Project Structure
```text
.
├── app.py # Streamlit chat UI with LangChain agent
├── requirements.txt # Python dependencies
├── Dockerfile # App container build
├── docker-compose.yml # Multi-service stack (Ollama + App)
└── README.md # This file
```
---

## Prerequisites

- Docker + Docker Compose  
- ~12 GB free disk space (for `llama3.2:latest` model)  

---

## Quickstart

1. Clone the repo.  
2. Build and start services:
   ```bash
   docker compose up --build
3. Open http://localhost:8501 in your browser.
The first run will automatically pull llama3.2:latest into a shared Docker volume.
---
## Configuration
- Change the model by setting MODEL:
  ```bash
  MODEL=llama3.2:3b-instruct docker compose up --build
- Override the system prompt with:
  ```bash
  SYSTEM_PROMPT="Answer only in JSON." docker compose up
---
## Notes
- Models are cached in the ollama_models Docker volume.
- Subsequent runs reuse the model without re-pulling.
- All inference is local; no API keys required.
