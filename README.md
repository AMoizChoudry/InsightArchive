# 📂 InsightArchive: High-Performance Hybrid RAG Agent

**InsightArchive** is a professional-grade Retrieval-Augmented Generation (RAG) platform designed for precision document analysis. Unlike standard RAG wrappers, it implements a **Hybrid Search** architecture and real-time **performance monitoring** to deliver fast, fact-grounded responses from large PDF datasets.

---

### 🏗️ Architectural Choice: Custom Orchestration vs. Assistants API
This system intentionally uses a custom orchestration layer built on the **OpenAI Chat Completions API** rather than the managed Assistants API. This design choice demonstrates engineering depth in several areas:
* **Infrastructure Transparency:** Provides full visibility into the chunking, embedding, and retrieval process rather than relying on a "black-box" service.
* **Granular Performance Profiling:** Enables the precise measurement of **Database Retrieval Latency** vs. **LLM Generation Latency**.
* **Vector Database Control:** Utilizing **LanceDB** locally provides superior control over data indexing and significantly reduces costs compared to cloud-managed storage.
* **Model Agnostic Design:** The orchestration logic is portable to other providers like Anthropic, Groq, or local Llama 3 instances without vendor lock-in.

---

## 🚀 Key Technical Features

### 1. Hybrid Retrieval Engine (Vector + BM25)
To solve the "semantic vs. keyword" trade-off, this system uses **LanceDB** for dual-path retrieval:
* **Vector Search (`text-embedding-3-small`):** Captures semantic meaning and conceptual queries, allowing the agent to understand synonyms and intent.
* **BM25 Keyword Search:** Ensures exact matches for technical terms, part numbers, and identifiers that vector embeddings often overlook.

### 2. Real-Time Latency Monitoring
Production-grade AI requires understanding system bottlenecks. The UI displays:
* **DB Search Latency:** The exact time taken to retrieve relevant context from the local vector store.
* **LLM Generation Latency:** The time taken for the model to formulate a fact-based answer.

### 3. Decoupled Full-Stack Architecture
* **FastAPI Backend:** An asynchronous API handling document ingestion and agentic tool-calling logic.
* **Streamlit Frontend:** A sleek, reactive interface for document management and real-time chat.
* **Agentic Tool Calling:** The LLM autonomously decides when to query the knowledge base using OpenAI function calling.



---

## 🛠️ Tech Stack
* **Language:** Python 3.12+
* **Package Manager:** `uv` (High-performance Python dependency management)
* **LLM:** OpenAI GPT-4o-mini
* **Vector DB:** LanceDB (Serverless, Disk-based)
* **Frameworks:** FastAPI & Streamlit

---

## 🏁 Getting Started

### 1. Installation
Clone the repository and install dependencies using `uv`:
```powershell
git clone [https://github.com/AMoizChoudry/InsightArchive.git](https://github.com/AMoizChoudry/InsightArchive.git)
cd InsightArchive
uv sync

### 2. Environment Setup
Create a `.env` file in the root directory and add your API key:

```plaintext
OPENAI_API_KEY=sk-your-key-here

### 3. Running the Application
Launch both the backend and frontend simultaneously using the unified runner script:

```powershell
uv run run_app.py

Backend: http://localhost:8000

Frontend: http://localhost:8501

📖 Usage Guide

Ingestion: Upload a PDF and click Index Document. Wait for the "SUCCESS" notification in the UI.

Querying: Ask questions in the chat; the agent will automatically use the search_pdf tool to retrieve facts.

Metrics: Analyze the latency statistics provided at the bottom of each response to monitor performance.

Maintenance: Use the Wipe Database button to clear the index and reset the environment for new documents.