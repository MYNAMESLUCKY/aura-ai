import json
from langchain_core.messages import SystemMessage, HumanMessage


FACT_PROMPT = SystemMessage(
    content=(
        "You extract long-term personal facts about the USER.\n\n"
        "Rules:\n"
        "- Extract ONLY explicit, stable personal facts\n"
        "- Do NOT infer\n"
        "- Do NOT summarize\n"
        "- Do NOT explain\n"
        "- Output VALID JSON ONLY\n"
        "- If no facts are present, output {}\n\n"
        "Allowed fact types:\n"
        "- name\n"
        "- favourite_language\n"
        "- favourite_color\n"
        "- profession\n"
        "- hobby\n"
        "- location\n\n"
        "Examples:\n"
        "User: My name is Lucky\n"
        "Output: {\"name\": \"Lucky\"}\n\n"
        "User: I love Python\n"
        "Output: {\"favourite_language\": \"Python\"}\n\n"
        "User: Hello\n"
        "Output: {}\n"
    )
)


_ALLOWED_KEYS = {
    "name",
    "favourite_language",
    "favourite_color",
    "profession",
    "hobby",
    "location",
}


def extract_facts(llm, user_input: str) -> dict:
    """
    Extract safe, explicit long-term facts from user input.
    """

    messages = [
        FACT_PROMPT,
        HumanMessage(content=user_input),
    ]

    try:
        # Force deterministic behavior
        response = llm.invoke(
            messages,
            temperature=0,
        ).content.strip()

        data = json.loads(response)

        if not isinstance(data, dict):
            return {}

        # 🛑 HARD FILTER: allow only known keys
        clean_facts = {
            k: str(v)
            for k, v in data.items()
            if k in _ALLOWED_KEYS and isinstance(v, (str, int))
        }

        return clean_facts

    except Exception:
        # Silent fail → no memory corruption
        return {}
