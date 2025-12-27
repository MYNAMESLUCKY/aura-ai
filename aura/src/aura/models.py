from aura.ollama_utils import get_available_models, is_ollama_running
from aura.config import load_config, save_config
from aura.db import init_aura_db


def run_models():
    # ---- Ollama safety ----
    if not is_ollama_running():
        print("❌ Ollama is not running.")
        print("   → Start Ollama and try again.")
        return

    # ---- Config safety ----
    config = load_config()
    config.setdefault("llm", {})
    current_model = config["llm"].get("model")

    models = get_available_models()

    if not models:
        print("❌ No Ollama models found.")
        print("   → Run: ollama pull <model>")
        return

    print("\n📦 Available Ollama Models\n")

    for i, model in enumerate(models, 1):
        marker = " (current)" if model == current_model else ""
        print(f"{i}) {model}{marker}")

    choice = input("\nSelect model number (or press Enter to cancel): ").strip()

    if not choice:
        print("❎ Model switch cancelled")
        return

    if not choice.isdigit():
        print("❌ Invalid selection")
        return

    index = int(choice) - 1
    if index < 0 or index >= len(models):
        print("❌ Invalid selection")
        return

    selected_model = models[index]

    if selected_model == current_model:
        print("ℹ️ Model already selected")
        return

    config["llm"]["model"] = selected_model
    save_config(config)

    print(f"\n✅ Model updated to: {selected_model}")
    print("🔁 Please restart Aura to use the new model\n")
