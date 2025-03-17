## RHInfra Assistant
This project aims to deliver a low-level solution design document in word file format (.doc) to the enterprise users who are willing to accelerate theri solution designing using the reasoning power of `Meta's Llama-3.2-3B-Instruct` model.

This model is used in the agentic workflow consiting of three agents:
- Planner
- Designer (has access to vectorDB)
- Writer

Together they try to create a solution which can be deployed in an enterprise environment under real-time situations.

#### Tech Stack
This project uses the following:
- CrewAI
- Langchain
- Ollama (Embedding model)
- vLLM (Text Generation model)
- ChromaDB (Vector Database)
- Docker (for vLLM, ollama and chromadb containerization)
- Devcontainers (for development)

#### Update
This project is currently in progress. Will be updated soon...

---
