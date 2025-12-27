import os
from aura.db import init_aura_db

from aura.config import load_config
from aura.ollama_utils import (
    is_ollama_running,
    get_available_models,
)
from aura.features.memory import get_db


def run_doctor():
    print("\n🩺 Aura Doctor Report\n")

    # ---------------- CONFIG ----------------
    try:
        config = load_config()
        print("✅ Config file loaded")
    except Exception as e:
        print("❌ Config error:", e)
        print("   → Try: aura /config reset")
        return

    llm_cfg = config.get("llm", {})
    model = llm_cfg.get("model")

    if not model:
        print("⚠️ No model configured")
        print("   → Run setup wizard again")
    else:
        print(f"ℹ️ Configured model: {model}")

    # ---------------- OLLAMA ----------------
    if not is_ollama_running():
        print("❌ Ollama is NOT running")
        print("   → Start with: ollama serve")
        return
    else:
        print("✅ Ollama service reachable")

    try:
        models = get_available_models()
    except Exception as e:
        print("❌ Failed to fetch Ollama models:", e)
        models = []

    if not models:
        print("⚠️ Ollama running but no models available")
        print("   → Run: ollama pull <model>")
    elif model and model not in models:
        print(f"⚠️ Selected model not found: {model}")
        print("   Available models:")
        for i, m in enumerate(models, 1):
            print(f"     {i}) {m}")
    elif model:
        print(f"✅ Model found: {model}")

    # ---------------- TAVILY ----------------
    if os.getenv("TAVILY_API_KEY"):
        print("✅ Tavily API key set")
    else:
        print("⚠️ Tavily API key not set")
        print("   → Web search disabled")
        print("   → Set env: TAVILY_API_KEY")

    # ---------------- DATABASE ----------------
    try:
        db = get_db()
        db.execute("SELECT 1")
        db.close()
        print("✅ SQLite database reachable")
    except Exception as e:
        print("❌ Database error:", e)
        print("   → Try deleting ~/.aura/aura.db")

    print("\n🧠 Doctor check complete\n")
