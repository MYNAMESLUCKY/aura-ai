from langchain_core.messages import SystemMessage, HumanMessage
import json

FACT_PROMPT = SystemMessage(
    content=(
        "You extract explicit, long-term personal facts.\n"
        "Return ONLY valid JSON.\n\n"
        "Rules:\n"
        "- Only store stable facts (name, preferences)\n"
        "- Do NOT infer\n"
        "- If none, return {}\n\n"
        "Examples:\n"
        "Input: My name is Lucky\n"
        "Output: {\"name\": \"Lucky\"}\n\n"
        "Input: I like Python\n"
        "Output: {\"favourite_language\": \"Python\"}\n\n"
        "Input: Hello\n"
        "Output: {}\n"
    )
)

def extract_facts(llm, user_input: str) -> dict:
    messages = [
        FACT_PROMPT,
        HumanMessage(content=user_input),
    ]

    response = llm.invoke(messages).content.strip()

    try:
        data = json.loads(response)
        if isinstance(data, dict):
            return data
    except Exception:
        pass

    return {}
