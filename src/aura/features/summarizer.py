from langchain_core.messages import SystemMessage, HumanMessage

from aura.features.memory import (
    load_messages,
    save_message,
    create_conversation,
)

SUMMARY_TRIGGER = 20  # messages


def maybe_summarize(llm, conversation_id):
    """
    Summarize long conversations into a compact system message.
    Returns new conversation_id if summarization occurred.
    """

    messages = load_messages(conversation_id, limit=SUMMARY_TRIGGER + 1)

    # Not long enough → do nothing
    if len(messages) <= SUMMARY_TRIGGER:
        return None

    # 🛑 Prevent summarizing an already summarized conversation
    first_role, first_content = messages[0]
    if first_role == "system" and first_content.startswith("Conversation summary:"):
        return None

    # Build clean text block
    convo_text = "\n".join(
        f"{role}: {content}"
        for role, content in messages
    )

    summary_prompt = [
        SystemMessage(
            content=(
                "You are summarizing a conversation for memory compression.\n"
                "Rules:\n"
                "- Be factual and concise\n"
                "- Preserve user preferences, facts, and decisions\n"
                "- Do NOT add new information\n"
                "- Use bullet points\n"
            )
        ),
        HumanMessage(content=convo_text),
    ]

    # 🔒 Deterministic summarization
    summary = llm.invoke(
        summary_prompt,
        temperature=0,
    ).content.strip()

    # Start a new conversation seeded with the summary
    new_cid = create_conversation()

    save_message(
        new_cid,
        "system",
        f"Conversation summary:\n{summary}"
    )

    return new_cid
