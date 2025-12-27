from packaging.version import Version

from aura.version import __version__
from aura.config import load_config, save_config
from aura.db import init_aura_db


def migrate_config_if_needed():
    """
    Migrate config.yaml safely across Aura versions.
    """

    config = load_config()

    app_cfg = config.get("app", {})
    current_version = app_cfg.get("version")

    target_version = Version(__version__)

    # Normalize missing version (very old configs)
    if not current_version:
        app_cfg["version"] = __version__
        app_cfg.setdefault("auto_update", True)
        config["app"] = app_cfg
        save_config(config)
        return

    parsed_current = Version(current_version)

    # Already up-to-date
    if parsed_current == target_version:
        return

    # ---- MIGRATIONS ----
    # Example:
    # if parsed_current < Version("0.6.0"):
    #     config.setdefault("web", {}).setdefault("enabled", False)

    # Always bump version last
    app_cfg["version"] = __version__
    config["app"] = app_cfg

    save_config(config)
