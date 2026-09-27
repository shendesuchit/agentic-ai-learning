# Direct provider call

[Models](../../README.md) · [LangChain chapters](../../../README.md)

Before using LangChain, it helps to see one ordinary model call. This example sends **the same question** through a provider SDK and prints the text, the SDK response type, and any usage information the provider returns. It makes one API request when you run it.

Choose a provider for which you have an API key. The example model IDs below come from provider documentation; availability and billing depend on your account. You can supply another supported model ID with `--model`.

| Provider | Python package | Key in `.env` | Direct call used here | Documented example model |
| --- | --- | --- | --- | --- |
| OpenAI | `openai` | `OPENAI_API_KEY` | `OpenAI().chat.completions.create(...)` | `gpt-5.5` |
| Gemini | `google-genai` | `GEMINI_API_KEY` | `genai.Client().interactions.create(...)` | `gemini-3.8-flash` |
| Groq | `groq` | `GROQ_API_KEY` | `Groq().chat.completions.create(...)` | `llama-3.3-70b-versatile` |
| OpenRouter | `openai` | `OPENROUTER_API_KEY` | OpenAI SDK pointed at OpenRouter's endpoint | `openai/gpt-4o` |

OpenRouter is an API gateway here, so its example uses the OpenAI-compatible Python SDK. The call still goes to **OpenRouter**, with an OpenRouter key and model ID. Gemini's current direct example uses the Interactions API, which returns a different response object from chat completions. That difference is worth noticing.

## Run one provider

From the repository root in VS Code Terminal, copy `.env.example` to `.env`, then paste **only your own key** on its matching line in `.env`. Git ignores that file. For example, in PowerShell:

```powershell
Copy-Item .env.example .env
```

Then use one command below. Each `uv run` installs only the selected provider's optional SDK into the root project environment and loads the ignored `.env` file. Replace the model ID if your provider account offers a different one.

```powershell
uv run --env-file .env --extra openai python 01-langchain/01-models/experiments/01-provider-specific-baseline/main.py --provider openai --model gpt-5.5
```

```powershell
uv run --env-file .env --extra gemini python 01-langchain/01-models/experiments/01-provider-specific-baseline/main.py --provider gemini --model gemini-3.8-flash
```

```powershell
uv run --env-file .env --extra groq python 01-langchain/01-models/experiments/01-provider-specific-baseline/main.py --provider groq --model llama-3.3-70b-versatile
```

```powershell
uv run --env-file .env --extra openrouter python 01-langchain/01-models/experiments/01-provider-specific-baseline/main.py --provider openrouter --model openai/gpt-4o
```

The [Python code](https://github.com/shendesuchit/agentic-ai-learning/blob/main/01-langchain/01-models/experiments/01-provider-specific-baseline/main.py) keeps the provider calls visible. There is no LangChain import in this experiment.

## What to notice

Use the output to ask a few simple questions. Which SDK class did you receive? Where is the text stored? Is usage information available? If you try another provider, keep the question unchanged, and check whether the response shape and usage fields mean the same thing.

No API call has been run or recorded in this repository yet. The first real result will depend on the selected provider, model, account, and time of the call. A ChatGPT subscription does not itself provide OpenAI API credentials; those are managed separately.

## Provider references

- [OpenAI Python SDK](https://github.com/openai/openai-python) and [Chat Completions reference](https://developers.openai.com/api/reference/resources/chat)
- [Gemini Python quickstart](https://ai.google.dev/gemini-api/docs/get-started)
- [Groq text generation with the Groq SDK](https://console.groq.com/docs/text-chat)
- [OpenRouter with the OpenAI Python SDK](https://openrouter.ai/docs/guides/community/openai-sdk)

[Back to Models](../../README.md)
