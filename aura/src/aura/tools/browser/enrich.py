from aura.features.web_search import run_web_search
from langchain_core.messages import SystemMessage, HumanMessage


def enrich_browser_intent(llm, user_input: str) -> dict | None:
    web_context = run_web_search(user_input)
    if not web_context:
        return None

    prompt = [
        SystemMessage(
            content=(
                "From the web results below, extract ONE best direct URL "
                "that satisfies the user's intent.\n\n"
                "Rules:\n"
                "- Prefer official sites\n"
                "- Prefer watch/play pages\n"
                "- Return ONLY the URL\n"
            )
        ),
        HumanMessage(content=web_context),
    ]

    url = llm.invoke(prompt).content.strip()

    if url.startswith("http"):
        return {
            "tool": "browser",
            "site": "web",
            "url": url,
            "action": "open",
        }

    return None
