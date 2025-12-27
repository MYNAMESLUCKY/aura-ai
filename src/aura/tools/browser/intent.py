from langchain_core.messages import SystemMessage, HumanMessage
import json

BROWSER_INTENT_PROMPT = SystemMessage(
    content=(
        "You convert user requests into browser actions.\n\n"
        "Return ONLY valid JSON.\n\n"
        "Schema:\n"
        "{\n"
        '  "action": "open_url" | "search",\n'
        '  "query": string\n'
        "}\n\n"
        "Examples:\n"
        "User: open youtube\n"
        'Output: {"action":"open_url","query":"https://youtube.com"}\n\n'
        "User: i want to watch netflix\n"
        'Output: {"action":"open_url","query":"https://netflix.com"}\n\n'
        "User: play believer by imagine dragons\n"
        'Output: {"action":"search","query":"believer imagine dragons youtube"}\n"
    )
)

def parse_browser_intent(llm, user_input: str) -> dict | None:
    messages = [
        BROWSER_INTENT_PROMPT,
        HumanMessage(content=user_input),
    ]

    response = llm.invoke(messages).content.strip()

    try:
        return json.loads(response)
    except Exception:
        return None
