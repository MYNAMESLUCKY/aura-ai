from langchain_core.messages import SystemMessage, HumanMessage
import json


INTENT_PROMPT = SystemMessage(
    content=(
        "You are a tool-intent extractor for browser actions.\n\n"
        "For any request to open/visit/play/search on a website, extract the intent as JSON.\n\n"
        "CRITICAL RULES:\n"
        "1. For well-known sites, ALWAYS return the direct URL:\n"
        '   - YouTube -> "https://www.youtube.com"\n'
        '   - Spotify -> "https://open.spotify.com"\n'
        '   - GitHub -> "https://github.com"\n'
        '   - Wikipedia -> "https://en.wikipedia.org"\n'
        '   - Netflix -> "https://www.netflix.com"\n'
        "2. For search/query requests, return what to search for\n"
        "3. For unknown sites, return the site name to search for\n\n"
        "Schema:\n"
        "{\n"
        '  "tool": "browser",\n'
        '  "action": "open|search|play",\n'
        '  "query": "<direct URL or search term>"\n'
        "}\n\n"
        "Return ONLY valid JSON.\n"
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
            start_idx = raw.find("{")
            if start_idx == -1:
                return None
            raw = raw[start_idx:]

        # 🔒 Extract ONLY the JSON object (handle trailing data)
        brace_count = 0
        json_end = 0
        for i, char in enumerate(raw):
            if char == "{":
                brace_count += 1
            elif char == "}":
                brace_count -= 1
                if brace_count == 0:
                    json_end = i + 1
                    break

        if json_end == 0:
            print("⚠️ Browser intent parsing failed: No valid JSON object found")
            return None

        raw = raw[:json_end]
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
