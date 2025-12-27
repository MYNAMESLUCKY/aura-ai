import os
from langchain_tavily import TavilySearch


def run_web_search(query: str) -> str:
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        return (
            "⚠️ Live web search is unavailable because Tavily is not configured.\n"
            "If real-time information is required, set the environment variable TAVILY_API_KEY."
        )

    # 🔒 Sanitize query
    query = query.strip()
    if len(query) < 6:
        return "⚠️ Web search skipped: query too vague."

    tavily = TavilySearch(
        tavily_api_key=api_key,
        max_results=5,
    )

    try:
        response = tavily.invoke(query)
    except Exception:
        return "⚠️ Web search failed due to a network or API error."

    results = response.get("results", [])
    if not results:
        return "⚠️ Web search returned no useful results."

    lines = []
    for r in results[:5]:
        title = r.get("title", "No title")
        content = r.get("content", "").strip()
        url = r.get("url", "")
        lines.append(f"- {title}: {content} ({url})")

    # 🔥 THIS IS THE IMPORTANT PART
    return (
        "The following information is REAL-TIME data from the web.\n"
        "Use it as the PRIMARY source of truth when answering.\n\n"
        + "\n".join(lines)
    )
