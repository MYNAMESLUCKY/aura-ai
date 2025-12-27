from aura.tools.intent import needs_browser
from aura.tools.browser.detect import detect_browsers
from aura.tools.browser.intent import parse_browser_intent
from aura.tools.browser.executor import execute_browser_action

def handle_tools(llm, user_input: str) -> str | None:
    if not needs_browser(user_input):
        return None

    browsers = detect_browsers()
    if not browsers:
        return "❌ No supported browser found on your system."

    intent = parse_browser_intent(llm, user_input)
    if not intent:
        return "❌ I couldn’t understand the browser request."

    return execute_browser_action(intent)
