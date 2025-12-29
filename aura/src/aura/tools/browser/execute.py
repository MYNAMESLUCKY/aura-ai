import webbrowser
import re
from aura.features.web_search import run_web_search


_URL_REGEX = re.compile(r"https?://[^\s)]+", re.IGNORECASE)


def execute_browser_intent(intent: dict) -> str:
    """
    Executes a browser intent.
    Priority:
    1. Direct URL (best case)
    2. Tavily fallback with domain filtering
    """

    # ---------- 1️⃣ Direct URL ----------
    url = intent.get("url")
    if isinstance(url, str) and url.startswith("http"):
        try:
            webbrowser.open(url)
            return f"🌐 Opened: {url}"
        except Exception as e:
            print(f"⚠️ Failed to open URL {url}: {e}")
            return f"⚠️ Failed to open browser: {e}"

    # ---------- 2️⃣ Tavily Fallback ----------
    query = intent.get("query")

    if not query:
        return "⚠️ No query provided for browser action."

    try:
        web_result = run_web_search(query)
    except Exception as e:
        print(f"⚠️ Web search error: {e}")
        return f"⚠️ Web search unavailable: {e}"

    if not web_result or web_result.startswith("⚠️"):
        return "⚠️ Web search unavailable."

    # ---------- 3️⃣ Extract ALL URLs ----------
    urls = _URL_REGEX.findall(web_result)
    if not urls:
        return "⚠️ Couldn't find a suitable link to open."

    # ---------- 4️⃣ Open the first valid URL ----------
    try:
        webbrowser.open(urls[0])
        return f"🌐 Opened result: {urls[0]}"
    except Exception as e:
        print(f"⚠️ Failed to open browser with URL {urls[0]}: {e}")
        return f"⚠️ Failed to open browser: {e}"
