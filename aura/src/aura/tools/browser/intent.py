from langchain_core.messages import SystemMessage, HumanMessage
import json


INTENT_PROMPT = SystemMessage(
    content=(
        "You are a tool-intent extractor.\n\n"
        "If the user request can be satisfied by opening a website, "
        "You have fufill the request of the user by using all the possible means and using all the possible tools that are avaialble to you,"
        "For requests involving opening websites, searching online,"
        "playing media, or browsing information, you MUST return JSON.\n\n"
        "Even if the user asks for information, "
        "prefer browser usage when a website exists.\n\n"
        "Return ONLY valid JSON.\n"
        "If uncertain, still return a best-effort browser intent.\n\n"
        "Schema:\n"
        "{\n"
        '  "tool": "browser",\n'
        '  "action": "open|search|play",\n'
        '  "query": "<what should be opened or searched>"\n'
        "}\n\n"
        "Only return {} if a browser is truly irrelevant."
    )
)


def parse_browser_intent(llm, user_input: str) -> dict | None:
    messages = [
        INTENT_PROMPT,
        HumanMessage(content=user_input),
    ]

    try:
        raw = llm.invoke(messages).content.strip()

        # 🔒 Hard cleanup (handles model chatter)
        if not raw.startswith("{"):
            raw = raw[raw.find("{"):]

        data = json.loads(raw)

        # 🔐 STRICT validation - check for action field, not platform
        if (
            isinstance(data, dict)
            and data.get("tool") == "browser"
            and data.get("action") in ["open", "search", "play"]
            and data.get("query")
        ):
            return data

    except Exception as e:
        print(f"⚠️ Browser intent parsing failed: {e}")

    return None
