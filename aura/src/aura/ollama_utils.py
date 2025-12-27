import requests
from typing import List

OLLAMA_URL = "http://localhost:11434"


def is_ollama_running() -> bool:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except requests.RequestException:
        return False


def get_available_models() -> List[str]:
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        data = r.json()
        return [m.get("name") for m in data.get("models", []) if "name" in m]
    except (requests.RequestException, ValueError):
        # Ollama not running or invalid response
        return []
