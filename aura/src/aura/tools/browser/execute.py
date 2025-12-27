import webbrowser
from aura.features.web_search import run_web_search


def execute_browser_intent(intent: dict) -> str:
    platform = intent.get("platform")
    query = intent.get("query", "")
    domain = intent.get("domain", "")
    site = intent.get("site", "")
    if platform == "youtube":
        search_query = f"site:youtube.com {query}"
    elif platform == "netflix":
        search_query = f"site:netflix.com {query}"
    elif platform == "google":
        search_query = query
    elif platform == "spotify":
        search_query = f"site:open.spotify.com {query}"
    elif platform == "based on user's prompt open the websites using tavily websearch":
        search_query = f"site:{site}.{domain} {query}"
    else:
        search_query = query

    web_result = run_web_search(search_query)

    # Extract first URL (simple & robust)
    url = None
    for line in web_result.splitlines():
        if "http" in line:
            url = line.split("(")[-1].rstrip(")")
            break

    if not url:
        return "⚠️ Couldn't find a suitable link to open."

    webbrowser.open(url)
    return f"🌐 Opened {platform} for: {query}"
