import subprocess
import sys
from aura.config import load_config
from aura.version import __version__


def check_for_updates():
    config = load_config()
    auto_update = config.get("app", {}).get("auto_update", True)

    if not auto_update:
        return

    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "aura-ai"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            timeout=10,
        )
    except Exception:
        # Silent fail – never block startup
        pass
