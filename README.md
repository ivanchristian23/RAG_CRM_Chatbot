# 🤖 CRM RAG Chatbot using LLaMA, Ollama, and Microsoft Dynamics 365

This project is an AI-powered chatbot that uses **Retrieval-Augmented Generation (RAG)** to answer questions based on **Microsoft Dynamics 365 CRM contact data**. It uses a Python backend, FAISS for vector search, and a locally served LLaMA model via **Ollama**.

---

## 🚀 Features

- 🔐 Connects to Microsoft Dynamics 365 using OAuth2 (Client Credentials)
- 📄 Extracts enriched contact data: name, email, job title, phone, company
- 🔎 Embeds data using `SentenceTransformer` and stores in FAISS vector DB
- 💬 Answers user questions using LLaMA3 locally (via Ollama)
- ⚡ Built with FastAPI for easy web deployment

---

## 🛠 Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) installed with `llama3` model
- Microsoft Dynamics 365 access + Azure App Registration
- Local environment variables configured

---

## 📦 Installation

```bash
git clone https://github.com/yourusername/crm-rag-chatbot.git
cd crm-rag-chatbot
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
