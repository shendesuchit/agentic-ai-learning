"""Explore LangChain message roles and explicit conversation history."""

import os

from langchain_groq import ChatGroq
from langchain.messages import AIMessage, HumanMessage, SystemMessage


MODEL_NAME = "openai/gpt-oss-20b"


def show_messages(messages):
    """Print the message history in a readable form."""

    print("\nConversation history:")

    for number, message in enumerate(messages, start=1):
        print(
            f"{number}. "
            f"{type(message).__name__}: "
            f"{message.content}"
        )


def main() -> None:
    if not os.environ.get("GROQ_API_KEY"):
        raise RuntimeError(
            "GROQ_API_KEY is missing. "
            "Run with uv run --env-file .env."
        )

    model = ChatGroq(model=MODEL_NAME)

    print("=== PART 1: Explicit message roles ===")

    messages = [
        SystemMessage(
            content=(
                "You are a patient teacher. "
                "Answer in one simple sentence."
            )
        ),
        HumanMessage(
            content="Explain what an API is."
        ),
    ]

    response = model.invoke(messages)

    print(f"Response type: {type(response).__name__}")
    print(f"Is AIMessage: {isinstance(response, AIMessage)}")
    print(f"Answer: {response.content}")

    print("\n=== PART 2: Build conversation history ===")

    messages.append(response)

    messages.append(
        HumanMessage(
            content=(
                "Now explain the same concept using "
                "a restaurant analogy."
            )
        )
    )

    show_messages(messages)

    follow_up = model.invoke(messages)

    print("\nFollow-up response:")
    print(f"Response type: {type(follow_up).__name__}")
    print(f"Answer: {follow_up.content}")

    messages.append(follow_up)

    print("\n=== FINAL HISTORY ===")
    show_messages(messages)

    print("\n=== PART 3: Isolated call without history ===")

    isolated_response = model.invoke(
        [
            HumanMessage(
                content=(
                    "What concept were we discussing, "
                    "and what analogy did you use?"
                )
            )
        ]
    )

    print(f"Response type: {type(isolated_response).__name__}")
    print(f"Answer: {isolated_response.content}")


if __name__ == "__main__":
    main()
