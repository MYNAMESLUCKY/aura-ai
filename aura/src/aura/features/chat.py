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
from aura.features.user_memory import (
    init_user_memory,
    load_facts,
    save_fact,
)
from aura.features.memory_extractor import extract_facts
from aura.features.vector_memory import (
    retrieve_memories,
    maybe_store_memory,
)
from aura.tools.registry import handle_tools


def start_chat(llm):
    # ---------- Init ----------
    init_db()
    init_user_memory()

    identity = load_identity_metadata()
    user_id = identity["user_id"]

    conversation_id = create_conversation()

    def build_system_prompt():
        facts = load_facts(user_id)
        if facts:
            facts_block = "\n".join(f"- {k}: {v}" for k, v in facts.items())
        else:
            facts_block = "No known user facts."

        return SystemMessage(
            content=(
                "You are Aura, a helpful, accurate, and concise AI assistant.\n\n"
                "Known user facts:\n"
                f"{facts_block}"
            )
        )

    system_prompt = build_system_prompt()

    print("\n(Type 'exit' to quit)\n")

    while True:
        user_input = input("You: ").strip()

        # 1️⃣ Exit
        if user_input.lower() in ("exit", "quit"):
            print("👋 Bye!")
            break

        # 2️⃣ Slash commands
        if handle_command(user_input):
            continue

        # 3️⃣ TOOL HANDLING
        tool_result = handle_tools(llm, user_input)
        if tool_result:
            print("Aura:", tool_result)
            continue

        # 4️⃣ Extract & save STRUCTURED facts
        facts = extract_facts(llm, user_input)
        if facts:
            for key, value in facts.items():
                save_fact(user_id, key, value)
            system_prompt = build_system_prompt()

        # 5️⃣ Retrieve semantic memories
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

        # 6️⃣ Web search (optional)
        inject_tools(llm, user_input, messages)

        # 7️⃣ Conversation history
        history = load_messages(conversation_id, limit=10)
        for role, content in history:
            if role == "user":
                messages.append(HumanMessage(content=content))
            else:
                messages.append(AIMessage(content=content))

        # 8️⃣ Current input
        messages.append(HumanMessage(content=user_input))

        # 9️⃣ Model call
        try:
            response = llm.invoke(messages).content.strip()
        except Exception as e:
            print("⚠️ Model error:", e)
            continue

        if not response:
            print("⚠️ Empty response.")
            continue

        print("Aura:", response)

        # 🔟 Persist chat
        save_message(conversation_id, "user", user_input)
        save_message(conversation_id, "assistant", response)

        # 1️⃣1️⃣ Store vector memory
        maybe_store_memory(user_id, user_input)

        # 1️⃣2️⃣ Summarize if needed
        new_cid = maybe_summarize(llm, conversation_id)
        if new_cid:
            conversation_id = new_cid
            system_prompt = build_system_prompt()
