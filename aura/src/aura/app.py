from langchain_ollama import ChatOllama
import sys
import io

from aura.config import load_config
from aura.features.chat import start_chat
from aura.ollama_utils import is_ollama_running, get_available_models
from aura.db import init_aura_db

# Set UTF-8 encoding for Windows compatibility
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def run_agent():
    init_aura_db()
    config = load_config()

    llm_provider = config["llm"]["provider"]
    model_name = config["llm"]["model"]

    if llm_provider != "ollama":
        print("❌ Only Ollama is supported right now.")
        return

    # 🔍 Check Ollama availability
    if not is_ollama_running():
        print("❌ Ollama is not running.")
        print("➡️ Start it with: `ollama serve`")
        return

    # 🔍 Check model availability
    available_models = get_available_models()
    if model_name not in available_models:
        print(f"❌ Model '{model_name}' not found in Ollama.")
        print("➡️ Available models:")
        for m in available_models:
            print(f"   - {m}")
        print(f"\n➡️ Pull model with: `ollama pull {model_name}`")
        return

    # 🔒 Stable, non-streaming LLM
    llm = ChatOllama(
        model=model_name,
        temperature=0.1,
        streaming=False,
        stop=["...", "…"],
    )

    print("\n🤖 Aura AI is ready!")
    print(f"LLM Provider: {llm_provider}")
    print(f"Model: {model_name}")
    

    # Delegate everything else to the chat orchestrator
    start_chat(llm)
