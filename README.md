# 🤖 Aura — Local AI Assistant with Persistent Memory

Aura is a privacy-first, local AI assistant powered by Ollama.
It features **persistent identity**, **long-term memory**, **semantic (RAG) recall**, 
and **optional live web search** — all stored locally on your machine.

---

## ✨ Key Features

- 🔐 **Persistent Identity**
  - One-time generated user ID
  - Memory survives restarts

- 🧠 **Hybrid Memory System**
  - Short-term chat memory
  - Long-term factual memory
  - Semantic vector memory (RAG)

- 🔎 **Optional Web Search**
  - Uses Tavily (only when needed)
  - Disabled by default unless API key is set

- ⚙️ **Model Agnostic**
  - Uses Ollama
  - Switch models anytime

- 🩺 **Built-in Diagnostics**
  - Doctor command
  - Config migration
  - Model inspection

---

## 📦 Installation

### 1. Prerequisites
- Python 3.10+
- Ollama installed and running

```bash
ollama pull deepseek-v3.1:671b-cloud


________________________________________________________________
cd aura
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
__________________________________________________________________

```
## 🔑 TAVILY API KEY 

### set "TAVILY_API_KEY" to access the web search functionality
```bash
$env:TAVILY_API_KEY="tvly-xxxxx
```