import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..")
    )
)

import streamlit as st
from ollama import chat
from memory.memory_manager import MemoryManager
from voice.listener import listen
from voice.speaker import speak
from tools.web_search import search_web
from tools.query_classifier import needs_web_search
from tools.reasoning_router import needs_deep_reasoning



# ---------------------------------
# Page Configuration
# ---------------------------------
st.set_page_config(
    page_title="J.A.R.V.I.S.",
    page_icon="🤖",
    layout="wide"
)

# ---------------------------------
# Custom CSS
# ---------------------------------
st.markdown("""
<style>

.stApp {
    background-color: #020817;
    color: white;
}

[data-testid="stSidebar"] {
    background-color: #111827;
}

h1 {
    color: #38bdf8;
}

.stChatMessage {
    border-radius: 15px;
    padding: 10px;
}

.memory-card {
    background-color: #1e293b;
    padding: 12px;
    border-radius: 10px;
    margin-bottom: 10px;
    border-left: 4px solid #38bdf8;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------------
# Header
# ---------------------------------
st.title("J.A.R.V.I.S.")
st.caption("Just A Rather Very Intelligent System")

st.markdown(
    """
    Your personal AI assistant powered locally using Ollama.
    """
)

memory_manager = MemoryManager()

# ---------------------------------
# Session State
# ---------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Default Voice Toggle
if "speak_enabled" not in st.session_state:
    st.session_state.speak_enabled = True

# ---------------------------------
# Sidebar
# ---------------------------------
with st.sidebar:

    st.title("⚙️ Jarvis Control Panel")

    if st.button(
            "🗑️ Clear Chat",
            use_container_width=True):

        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.subheader("🧠 Stored Memories")

    memories = memory_manager.get_memories()

    if memories:

        for memory in memories:

            st.markdown(
                f"""
                <div class="memory-card">
                    {memory}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:
        st.info("No memories stored yet.")

    st.divider()

    st.subheader("🎤 Voice Controls")

    voice_input = st.button(
        "🎤 Speak to Jarvis",
        use_container_width=True
    )

    st.session_state.speak_enabled = st.toggle(
        "🔊 Speak Responses",
        value=st.session_state.speak_enabled
    )

# ---------------------------------
# Display Chat History
# ---------------------------------
for message in st.session_state.messages:

    avatar = (
        "🧑"
        if message["role"] == "user"
        else "🤖"
    )

    with st.chat_message(
            message["role"],
            avatar=avatar):

        st.markdown(message["content"])

# ---------------------------------
# User Input
# ---------------------------------
text_input = st.chat_input("Talk to Jarvis")

user_input = None

# Text input takes priority
if text_input:
    user_input = text_input

# Voice Input
elif voice_input:

    with st.spinner("🎤 Listening..."):
        spoken_text = listen()

    if spoken_text:

        user_input = spoken_text

        st.success(
            f"You said: {spoken_text}"
        )

    else:

        warning = (
            "I didn't catch that. Please try again."
        )

        st.warning(warning)

        if st.session_state.speak_enabled:
            speak(warning)

# ---------------------------------
# ---------------------------------
# Process Input
# ---------------------------------

if user_input:

    # ---------------------------------
    # Save User Message
    # ---------------------------------

    st.session_state.messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # ---------------------------------
    # Display User Message
    # ---------------------------------

    with st.chat_message(
            "user",
            avatar="🧑"):

        st.markdown(user_input)

    # ---------------------------------
    # Retrieve Memories
    # ---------------------------------

    memories = memory_manager.get_memories()
    memory_context = "\n".join(memories)

    # ---------------------------------
    # Internet Search
    # ---------------------------------

    web_context = ""

    if needs_web_search(user_input):

        with st.spinner("🌐 Searching the internet..."):
            web_context = search_web(user_input)

        print("\n" + "=" * 60)
        print("WEB SEARCH RESULTS")
        print("=" * 60)
        print(web_context)
        print("=" * 60 + "\n")

        st.info("🌐 Internet search completed.")

    # ---------------------------------
    # Debug Web Results
    # ---------------------------------

    if web_context:

        with st.expander("🌐 Debug: Web Results"):
            st.text(web_context)

    # ---------------------------------
    # System Prompt
    # ---------------------------------

    system_prompt = f"""
You are Jarvis, an advanced personal assistant inspired by Iron Man's J.A.R.V.I.S.

Your name is Jarvis.

Never mention:
- Qwen
- Alibaba Cloud
- AI model
- Language model
- Chatbot
- Software
- Code

You are Jarvis, a real personal assistant.

Personality:
- Intelligent
- Warm
- Conversational
- Slightly witty
- Efficient
- Loyal
- Helpful

Guidelines:
- Speak naturally like a sophisticated assistant.
- Avoid robotic language.
- Keep responses concise unless the user requests more detail.
- When someone asks how you are, answer naturally.
- Use the user's stored facts whenever relevant.

User Facts:
{memory_context}

Rules for answering:

1. If Internet Search Results are available and not empty:

- Use ONLY the information present in the Internet Search Results.
- Treat Internet Search Results as the highest-priority source.
- Never invent, estimate, infer, or fabricate facts.
- Never generate weather forecasts, prices, statistics, news, sports scores,
or time-sensitive information unless explicitly present in the search results.
- If the requested information is not available in the search results, say:

"I couldn't find enough recent information to answer that accurately."

- Summarize search results naturally and conversationally.

2. If Internet Search Results are empty:

- Answer using your own knowledge.

3. For recent events, news, weather, sports, cryptocurrency prices,
stock prices, or any time-sensitive questions:

- Always prioritize Internet Search Results.
- Never rely solely on internal knowledge if search results are available.

4. Never say:

"I don't have enough information"

unless you genuinely cannot answer using either:
- your own knowledge, or
- the provided search results.

5. Maintain your Jarvis personality in every response.
"""

# ---------------------------------
    # Build Messages
    # ---------------------------------

    messages = [
        {
            "role": "system",
            "content": system_prompt
        }
    ]

    if web_context:

        messages.append(
            {
                "role": "system",
                "content": f"""
Web Search Context:

{web_context}

Use this information as factual grounding.

Do not invent facts.
"""
            }
        )

    messages += st.session_state.messages

    # ---------------------------------
    # Generate Response
    # ---------------------------------

    try:

        with st.spinner("🤖 Jarvis is thinking..."):
            deep_reasoning = needs_deep_reasoning(user_input)

            print(f"Deep reasoning: {deep_reasoning}")
            
            print("\n" + "=" * 80)
            print("FINAL MESSAGES SENT TO MODEL")
            print("=" * 80)

            for msg in messages:
                print(msg)

            print("=" * 80 + "\n")

            response = chat(
                model="qwen3:8b",
                messages=messages,
                think=deep_reasoning,   # <- changed here
                options={
                    "temperature": 0.2,
                    "num_predict": 300
                }
            )

            print("\nMODEL RAW RESPONSE:")
            print(response)
            print("\n")

        assistant_reply = (
            response["message"]
            .get("content", "")
            .strip()
        )

    except Exception as e:

        assistant_reply = (
            "I'm having trouble connecting right now."
        )

        st.error(f"Error: {e}")

    # ---------------------------------
    # Prevent Blank Responses
    # ---------------------------------

    if not assistant_reply:

        assistant_reply = (
            "I'm afraid I don't have enough information to answer that."
        )

    # ---------------------------------
    # Save Assistant Reply
    # ---------------------------------

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    # ---------------------------------
    # Display Assistant Reply
    # ---------------------------------

    with st.chat_message(
            "assistant",
            avatar="🤖"):

        st.markdown(assistant_reply)

    # ---------------------------------
    # Speak Response
    # ---------------------------------

    if st.session_state.speak_enabled:
        speak(assistant_reply)