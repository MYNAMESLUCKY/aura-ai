from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

from aura.identity import load_identity_metadata
from aura.features.summarizer import maybe_summarize
from aura.features.memory import (
    init_db,
    create_conversation,
    save_message,
    load_messages,
)
from aura.features.tools import inject_tools, handle_command
from aura.features.user_memory import init_user_memory
from aura.features.vector_memory import (
    retrieve_memories,
    maybe_store_memory,
)
from aura.tools.registry import handle_tools

tool_result = handle_tools(llm, user_input)
if tool_result:
    print("Aura:", tool_result)
    continue


def start_chat(llm):
    # --- Init ---
    init_db()
    init_user_memory()
    identity = load_identity_metadata()
    user_id = identity["user_id"]

    conversation_id = create_conversation()

    system_prompt = SystemMessage(
        content="You are Aura, a helpful, accurate, and concise AI assistant."
    )

    print("\n(Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()

        # EXIT
        if user_input.lower() in ("exit", "quit"):
            print("👋 Bye!")
            break

        # Slash commands
        if handle_command(user_input):
            continue

        # --- Retrieve semantic memories ---
        memories = retrieve_memories(user_id, user_input, limit=5)

        messages = [system_prompt]

        if memories:
            memory_block = "\n".join(f"- {m}" for m in memories)
            messages.append(
                SystemMessage(
                    content=(
                        "Relevant past information about the user:\n"
                        f"{memory_block}"
                    )
                )
            )

        # Tool context (web search)
        inject_tools(llm, user_input, messages)

        # Conversation history
        history = load_messages(conversation_id, limit=10)
        for role, content in history:
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))

        # Current input
        messages.append(HumanMessage(content=user_input))

        # Model call
        response = llm.invoke(messages).content.strip()

        if not response:
            print("⚠️ Empty response.")
            continue

        print("Aura:", response)

        # Persist
        save_message(conversation_id, "user", user_input)
        save_message(conversation_id, "assistant", response)

        # Store semantic memory AFTER response
        maybe_store_memory(user_id, user_input)

        # Summarize if needed
        new_cid = maybe_summarize(llm, conversation_id)
        if new_cid:
            conversation_id = new_cid
