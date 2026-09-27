"""Call a provider through a LangChain chat-model wrapper."""

import argparse
import os


PROMPT = "Explain what an API is in one simple sentence."

KEYS = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}


def build_model(provider: str, model_name: str):
    """Create the provider-specific LangChain chat model."""

    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI(model=model_name)

    if provider == "gemini":
        from langchain_google_genai import ChatGoogleGenerativeAI

        return ChatGoogleGenerativeAI(model=model_name)

    if provider == "groq":
        from langchain_groq import ChatGroq

        return ChatGroq(model=model_name)

    if provider == "openrouter":
        from langchain_openrouter import ChatOpenRouter

        return ChatOpenRouter(model=model_name)

    raise ValueError(f"Unsupported provider: {provider}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, choices=KEYS)
    parser.add_argument(
        "--model",
        required=True,
        help="Model ID from the provider's model list",
    )
    args = parser.parse_args()

    key_name = KEYS[args.provider]
    if not os.environ.get(key_name):
        parser.error(
            f"{key_name} is missing. "
            "Add it to .env and run with uv run --env-file .env."
        )

    model = build_model(
        provider=args.provider,
        model_name=args.model,
    )

    response = model.invoke(PROMPT)

    print(f"Provider: {args.provider}")
    print(f"Requested model: {args.model}")
    print(f"LangChain wrapper: {type(model).__name__}")
    print(f"Response type: {type(response).__name__}")
    print(f"Answer: {response.content}")
    print(f"Usage metadata: {response.usage_metadata}")
    print(f"Response metadata: {response.response_metadata}")


if __name__ == "__main__":
    main()
