import webbrowser

def execute_browser_action(action: dict, preferred_browser=None) -> str:
    action_type = action.get("action")
    query = action.get("query")

    if not query:
        return "❌ Invalid browser request."

    if action_type == "open_url":
        webbrowser.open(query)
        return f"✅ Opened {query}"

    if action_type == "search":
        url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
        webbrowser.open(url)
        return f"🔍 Searching for: {query}"

    return "❌ Unknown browser action."
