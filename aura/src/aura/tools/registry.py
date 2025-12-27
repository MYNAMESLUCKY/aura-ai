from aura.tools.browser.intent import parse_browser_intent
from aura.tools.browser.execute import execute_browser_intent


def handle_tools(llm, user_input: str) -> str | None:
    # Browser intent
    intent = parse_browser_intent(llm, user_input)
    if intent:
        return execute_browser_intent(intent)

    return None
