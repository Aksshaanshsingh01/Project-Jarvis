from ollama import chat
from memory.memory_manager import MemoryManager
from voice.speaker import speak
from voice.listener import listen

# Turn this off when you don't need debugging information
DEBUG = False

print("Jarvis is online. Type 'exit' to quit.\n")

memory_manager = MemoryManager()

conversation = [
    {
        "role": "system",
        "content": ""
    }
]

MAX_HISTORY = 6

while True:

    # -----------------------------
    # Get user input
    # -----------------------------
    mode = input("\n(T)ext or (V)oice? ").strip().lower()

    if mode == "v":

        print("\nJarvis: Listening...")
        user_input = listen()

        # Voice recognition failed
        if not user_input:
            print("\nJarvis: I didn't catch that. Please try again.\n")
            continue

        user_input = user_input.strip()
        print(f"\nYou: {user_input}")

    elif mode == "t":

        user_input = input("You: ").strip()

    else:

        print("\nJarvis: Please enter T for text or V for voice.\n")
        continue

    # -----------------------------
    # Skip empty input
    # -----------------------------
    if not user_input:
        continue

    # -----------------------------
    # Save memory command
    # -----------------------------
    if user_input.lower().startswith("remember"):

        fact = (
            user_input.replace("remember that", "")
            .replace("remember", "")
            .strip()
        )

        if fact:

            memory_manager.save_memory(fact)

            print("\nJarvis: I'll remember that.\n")
            speak("I'll remember that.")

        else:

            print(
                "\nJarvis: Please tell me what you want me to remember.\n"
            )

        continue

    # -----------------------------
    # Exit command
    # -----------------------------
    if user_input.lower() == "exit":

        print("Jarvis shutting down...")
        speak("Shutting down. Goodbye.")
        break

    # -----------------------------
    # Retrieve memories
    # -----------------------------
    memories = memory_manager.get_memories()

    if DEBUG:
        print("\nDEBUG MEMORIES:")
        print(memories)
        print()

    memory_context = "\n".join(memories)

    # -----------------------------
    # Update system prompt
    # -----------------------------
    conversation[0]["content"] = f"""
You are Jarvis, an advanced personal AI assistant inspired by Iron Man's J.A.R.V.I.S.

Your name is Jarvis.

Never mention Qwen, Alibaba Cloud, or that you are an AI model.

Your personality traits:
- Intelligent
- Warm and conversational
- Slightly witty
- Efficient and concise
- Loyal and supportive

Speak naturally like a real assistant.
Avoid sounding robotic or overly formal.

When answering personal questions, use User Facts confidently.

Keep responses under 3 sentences unless more detail is requested.

User Facts:
{memory_context}

If the user asks about any information contained in User Facts,
answer using those facts directly.

If the user asks whether you remember something,
answer directly using User Facts.

If the information is not present in User Facts,
honestly say that you do not remember.
"""

    if DEBUG:
        print("\nSYSTEM PROMPT:")
        print(conversation[0]["content"])
        print()

    # -----------------------------
    # Add user message to history
    # -----------------------------
    conversation.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    # Keep only recent messages
    messages = [conversation[0]] + conversation[-MAX_HISTORY:]

    # -----------------------------
    # Call model
    # -----------------------------
    try:

        if DEBUG:
            print("About to call model...\n")

        response = chat(
            model="qwen3:8b",
            messages=messages,
            options={
                "num_predict": 150,
                "temperature": 0.7
            }
        )

        if DEBUG:
            print("Model responded successfully.\n")

        assistant_reply = response["message"]["content"].strip()

        # Debug raw output
        if DEBUG:
            print("RAW RESPONSE:")
            print(repr(assistant_reply))
            print()

        # Prevent blank responses
        if not assistant_reply:

            assistant_reply = (
                "I'm sorry, I don't have enough information to answer that."
            )

        # Save assistant response
        conversation.append(
            {
                "role": "assistant",
                "content": assistant_reply
            }
        )

        print(f"\nJarvis: {assistant_reply}\n")

        # Speak response
        speak(assistant_reply)

    except Exception as e:

        print("\nJarvis: Sorry, something went wrong.\n")

        if DEBUG:
            print(f"ERROR: {e}\n")