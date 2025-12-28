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

create a folder of your choice (example : test_folder) if you are using Windows
________________________________________________________________-------
git clone <your-repo>
cd C:\Users\{username}\OneDrive\Desktop\test_folder\aura-ai\aura
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -e.
__________________________________________________________________-----

```
---
-Now Running the AI model is an important part :-
--1)First check if the Ollama Model is running well in your localhost:{port} usually 11434 port.
--2)Now in your terminal you can use the Aura-AI with the command "aura"
--3)It will take up some time to load and for the first query and after that everything goes smoothly based on your internet speed.
---
