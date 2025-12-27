import os
import winreg
from pathlib import Path

BROWSERS = {
    "chrome": [
        r"Google\Chrome\Application\chrome.exe",
    ],
    "edge": [
        r"Microsoft\Edge\Application\msedge.exe",
    ],
    "firefox": [
        r"Mozilla Firefox\firefox.exe",
    ],
    "opera": [
        r"Opera\launcher.exe",
    ],
}

PROGRAM_DIRS = [
    os.environ.get("PROGRAMFILES"),
    os.environ.get("PROGRAMFILES(X86)"),
    os.environ.get("LOCALAPPDATA"),
]


def _find_in_registry(exe_name: str) -> str | None:
    """Check Windows registry for app path"""
    paths = [
        winreg.HKEY_LOCAL_MACHINE,
        winreg.HKEY_CURRENT_USER,
    ]

    for root in paths:
        try:
            key = winreg.OpenKey(
                root,
                rf"Software\Microsoft\Windows\CurrentVersion\App Paths\{exe_name}"
            )
            value, _ = winreg.QueryValueEx(key, "")
            return value
        except FileNotFoundError:
            continue

    return None


def detect_browsers() -> list[dict]:
    found = []

    for name, rel_paths in BROWSERS.items():
        exe_name = rel_paths[0].split("\\")[-1]

        # 1️⃣ Registry check
        reg_path = _find_in_registry(exe_name)
        if reg_path and Path(reg_path).exists():
            found.append({
                "name": name,
                "path": reg_path,
            })
            continue

        # 2️⃣ Common install directories
        for base in PROGRAM_DIRS:
            if not base:
                continue
            for rel in rel_paths:
                full = Path(base) / rel
                if full.exists():
                    found.append({
                        "name": name,
                        "path": str(full),
                    })
                    break

    return found
