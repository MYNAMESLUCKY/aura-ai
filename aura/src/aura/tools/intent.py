import re

_BROWSER_PATTERNS = re.compile(
    r"\b("
    r"youtube|netflix|google|search|watch|browse|open\s+website|"
    r"open\s+youtube|open\s+netflix|play\s+video"
    r")\b",
    re.IGNORECASE,
)

def needs_browser(user_input: str) -> bool:
    return bool(_BROWSER_PATTERNS.search(user_input))
