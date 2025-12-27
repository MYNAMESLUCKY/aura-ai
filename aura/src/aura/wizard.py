from pathlib import Path
import yaml
import sys

from aura.ollama_utils import is_ollama_running, get_available_models

CONFIG_DIR = Path.home() / ".aura"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


def run_wizard_if_needed():
    if CONFIG_FILE.exists():
        return

    print("\n✨ Welcome to Aura AI ✨")
    print("Let’s get you set up (takes ~2 minutes)\n")

    CONFIG_DIR.mkdir(exist_ok=True)

    # ---------------- LLM SETUP ----------------
    print("🔍 Checking Ollama...")

    if not is_ollama_running():
        print("\n❌ Ollama is not running.")
        print("👉 Please install and start Ollama first:")
        print("https://ollama.com")
        print("\nThen run `aura` again.\n")
        sys.exit(1)

    models = get_available_models()

    if not models:
        print("\n❌ No Ollama models found.")
        print("👉 Pull a model first, for example:")
        print("   ollama pull llama3.1")
        sys.exit(1)

    print("\n📦 Available Ollama models:")
    for i, name in enumerate(models, 1):
        print(f"  {i}) {name}")

    choice = input("\nSelect model number: ").strip()

    try:
        model = models[int(choice) - 1]
    except (ValueError, IndexError):
        print("❌ Invalid selection")
        sys.exit(1)

    # ---------------- OTHER OPTIONS ----------------
    enable_web = input("\nEnable web search? (y/n) [y]: ") or "y"
    auto_update = input("Enable auto-updates? (y/n) [y]: ") or "y"

    config = {
        "app": {
            "version": "0.1.0",
            "auto_update": auto_update.lower() == "y",
        },
        "llm": {
            "provider": "ollama",
            "model": model,
        },
        "web": {
            "enabled": enable_web.lower() == "y",
        },
    }

    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(config, f)

    print("\n✅ Setup complete!")
    print(f"🧠 Selected model: {model}")
    print("Run `aura` anytime to start chatting.\n")
