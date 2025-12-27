import yaml
from pathlib import Path

CONFIG_DIR = Path.home() / ".aura"
CONFIG_FILE = CONFIG_DIR / "config.yaml"


# 🔒 Canonical defaults (single source of truth)
DEFAULT_CONFIG = {
    "app": {
        "version": "0.1.0",
        "auto_update": True,
    },
    "llm": {
        "provider": "ollama",
        "model": "llama3",
    },
    "web": {
        "enabled": False,
    },
}


def load_config() -> dict:
    """
    Load Aura configuration safely.
    Always returns a complete config dictionary.
    """

    # Ensure directory exists
    CONFIG_DIR.mkdir(exist_ok=True)

    if not CONFIG_FILE.exists():
        return DEFAULT_CONFIG.copy()

    try:
        with open(CONFIG_FILE, "r") as f:
            data = yaml.safe_load(f) or {}
    except Exception:
        # Corrupt config → fall back safely
        return DEFAULT_CONFIG.copy()

    # Merge defaults with loaded config
    return _merge_dicts(DEFAULT_CONFIG, data)


def save_config(config: dict):
    """
    Persist Aura configuration safely.
    """

    CONFIG_DIR.mkdir(exist_ok=True)

    with open(CONFIG_FILE, "w") as f:
        yaml.safe_dump(config, f, sort_keys=False)


def _merge_dicts(defaults: dict, override: dict) -> dict:
    """Recursively merge override onto defaults."""
    result = defaults.copy()

    for key, value in override.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = _merge_dicts(result[key], value)
        else:
            result[key] = value

    return result
