from langchain_core.messages import SystemMessage, HumanMessage
import json


INTENT_PROMPT = SystemMessage(
    content=(
        "You extract browser intents from user requests.\n\n"
        "If the user wants to open a website or play media, "
        "return a JSON object in this format:\n\n"
        "{\n"
        '  "tool": "browser",\n'
        '  "platform": "<youtube|netflix|google|website>",\n'
        '  "action": "<open|search|play>",\n'
        '  "query": "<what to search or play>"\n'
        "}\n\n"
        "If the request is NOT about using a browser, return {}.\n\n"
        "Return ONLY valid JSON."
    )
)


def parse_browser_intent(llm, user_input: str) -> dict | None:
    messages = [
        INTENT_PROMPT,
        HumanMessage(content=user_input),
    ]

    try:
        raw = llm.invoke(messages).content.strip()
        data = json.loads(raw)
        if data.get("tool") == "browser":
            return data
    except Exception:
        pass

    return None
