from pathlib import Path
import re
from langchain_core.messages import SystemMessage

from aura.features.web_search import run_web_search

# ---------------- CONFIG ----------------
CONFIG_FILE = Path.home() / ".aura" / "config.yaml"


# =========================
# 1️⃣ COMMAND HANDLING
# =========================
def handle_command(command: str) -> bool:
    cmd = command.strip().lower()

    if cmd == "/config reset":
        if CONFIG_FILE.exists():
            CONFIG_FILE.unlink()
            print("✅ Config reset.")
            print("🔁 Restart Aura to reconfigure.")
        else:
            print("ℹ️ No config file found.")
        return True

    if cmd == "/config show":
        if CONFIG_FILE.exists():
            print("\n📄 Current config:\n")
            print(CONFIG_FILE.read_text())
        else:
            print("ℹ️ No config file found.")
        return True

    if cmd in ("/help", "/commands"):
        print("""
Available commands:
  /config show    → Show current config
  /config reset   → Reset config
  /exit           → Exit Aura
        """)
        return True

    return False


# =========================
# 2️⃣ FAST & SAFE TOOL DECISION
# =========================
_WEB_PATTERNS = re.compile(
    r"\b("
    r"weather|temperature|forecast|"
    r"date|time|today|now|"
    r"news|headline|breaking|latest|"
    r"price|cost|rate|"
    r"stock|crypto|bitcoin"
    r")\b",
    re.IGNORECASE,
)


def needs_web_search(user_input: str) -> bool:
    """
    Deterministic check for real-time info needs.
    NO LLM CALLS HERE.
    """
    return bool(_WEB_PATTERNS.search(user_input))


# =========================
# 3️⃣ SAFE TOOL CONTEXT CREATION
# =========================
def inject_tools(llm, user_input: str, messages: list):
    """
    Inject authoritative web context for real-time queries.
    """

    if not needs_web_search(user_input):
        return None

    try:
        web_context = run_web_search(user_input)
    except Exception as e:
        print("⚠️ Web search failed:", e)
        return None

    if not web_context:
        return None

    messages.append(
        SystemMessage(
            content=(
                "The following information is REAL-TIME data retrieved from the web.\n"
                "It is the PRIMARY source of truth for answering the user's question.\n"
                "Use it directly and do NOT rely on prior knowledge.\n\n"
                f"{web_context}"
            )
        )
    )

    return web_context
