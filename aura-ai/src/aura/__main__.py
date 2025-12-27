import sys
import warnings

warnings.filterwarnings(
    "ignore",
    category=UserWarning,
    module="langchain_tavily",
)

from aura.wizard import run_wizard_if_needed
from aura.updater import check_for_updates
from aura.app import run_agent
from aura.doctor import run_doctor
from aura.models import run_models
from aura.migrator import migrate_config_if_needed


def print_help():
    print("""
Aura AI – CLI Assistant

Usage:
  aura               Start chat
  aura doctor        Run system diagnostics
  aura models        List available models
  aura help          Show this help message
""")


def main():
    # First-run setup & migrations
    run_wizard_if_needed()
    migrate_config_if_needed()

    # ---- CLI command handling ----
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()

        if cmd in ("help", "--help", "-h"):
            print_help()
            return

        if cmd == "doctor":
            run_doctor()
            return

        if cmd == "models":
            run_models()
            return

        print(f"❌ Unknown command: {cmd}")
        print("Run `aura help` to see available commands.")
        return

    # ---- Normal chat mode ----
    # Non-blocking update check
    check_for_updates()

    # Start chat ONCE
    run_agent()


if __name__ == "__main__":
    main()
