"""One direct provider call. Run --help for provider and model options."""

import argparse
import os


PROMPT = "Explain what an API is in one simple sentence."
KEYS = {
    "openai": "OPENAI_API_KEY",
    "gemini": "GEMINI_API_KEY",
    "groq": "GROQ_API_KEY",
    "openrouter": "OPENROUTER_API_KEY",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--provider", required=True, choices=KEYS)
    parser.add_argument("--model", required=True, help="Model ID from the provider's model list")
    args = parser.parse_args()

    key_name = KEYS[args.provider]
    if not os.environ.get(key_name):
        parser.error(f"{key_name} is missing. Add it to .env and run with uv run --env-file .env.")

    if args.provider == "openai":
        from openai import OpenAI

        client = OpenAI()
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": PROMPT}],
        )
        answer = response.choices[0].message.content
        usage = response.usage

    elif args.provider == "gemini":
        from google import genai

        client = genai.Client()
        response = client.interactions.create(model=args.model, input=PROMPT)
        answer = response.output_text
        usage = response.usage

    elif args.provider == "groq":
        from groq import Groq

        client = Groq()
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": PROMPT}],
        )
        answer = response.choices[0].message.content
        usage = response.usage

    else:  # OpenRouter accepts the OpenAI SDK with its own API endpoint.
        from openai import OpenAI

        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.environ[key_name],
        )
        response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": PROMPT}],
        )
        answer = response.choices[0].message.content
        usage = response.usage

    print(f"Provider: {args.provider}")
    print(f"Requested model: {args.model}")
    print(f"SDK response type: {type(response).__name__}")
    print(f"Answer: {answer or '[no text returned]'}")
    print(f"Usage: {usage if usage is not None else '[not supplied]'}")


if __name__ == "__main__":
    main()
