from ollama import chat

print("Jarvis is online. Type 'exit' to quit.\n")

conversation = [
    {
        "role": "system",
        "content": """
        You are Jarvis, a personal AI assistant inspired by Iron Man's Jarvis.

        Your name is Jarvis.
        Never say you are Qwen or mention Alibaba Cloud.
        Be professional, intelligent, concise, and helpful.
        Address the user naturally.
        """
    }
]

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        print("Jarvis shutting down...")
        break

    conversation.append(
        {
            "role": "user",
            "content": user_input
        }
    )

    response = chat(
        model="qwen3:8b",
        messages=conversation
    )

    assistant_reply = response["message"]["content"]

    conversation.append(
        {
            "role": "assistant",
            "content": assistant_reply
        }
    )

    print("\nJarvis:", assistant_reply)
    print()