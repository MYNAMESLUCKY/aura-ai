import shutil

KNOWN_BROWSERS = {
    "chrome": ["chrome", "google-chrome"],
    "edge": ["msedge"],
    "opera": ["opera"],
    "firefox": ["firefox"],
}

def detect_browsers() -> list[str]:
    available = []

    for name, binaries in KNOWN_BROWSERS.items():
        for bin in binaries:
            if shutil.which(bin):
                available.append(name)
                break

    return available
