# Direct provider call

[Models](../../README.md) · [LangChain chapters](../../../README.md) · [Next: LangChain model wrapper](../02-langchain-model-wrapper/README.md)

Before using LangChain, it helps to see one ordinary model call. This experiment
sends the same small question through a provider SDK and prints the text, the SDK
response type, and any usage information returned by the provider.

## Why this baseline matters

Without a baseline, it is easy to say that a framework "simplifies model calls"
without being able to explain what it actually changed.

This experiment keeps the provider-native route visible:

```text
Application
    |
    v
Provider SDK
    |
    v
Provider API
    |
    v
Hosted model
```

The next experiment keeps the prompt and provider fixed, inserts LangChain, and
compares the application-facing interface.

## Provider routes in the example

Choose a provider for which you have an API key. Model availability and billing
depend on the provider and account. Supply another supported model ID with
`--model` when needed.

| Provider | Python package | Key in `.env` | Direct call used here | Example model |
| --- | --- | --- | --- | --- |
| OpenAI | `openai` | `OPENAI_API_KEY` | `OpenAI().chat.completions.create(...)` | `gpt-5.5` |
| Gemini | `google-genai` | `GEMINI_API_KEY` | `genai.Client().interactions.create(...)` | `gemini-3.8-flash` |
| Groq | `groq` | `GROQ_API_KEY` | `Groq().chat.completions.create(...)` | `openai/gpt-oss-20b` |
| OpenRouter | `openai` | `OPENROUTER_API_KEY` | OpenAI SDK pointed at OpenRouter's endpoint | `openai/gpt-4o` |

OpenRouter is an API gateway in this example, so its direct route uses the
OpenAI-compatible Python SDK with an OpenRouter key and endpoint. Gemini's direct
example uses its own API shape. These differences are part of what the baseline
is meant to expose.

## Run one provider

From the repository root, copy `.env.example` to `.env` if you have not already
done so and add only your own key. Git ignores `.env`.

For the provider we actually tested:

```powershell
uv run --extra groq --env-file .env python 01-langchain/01-models/experiments/01-provider-specific-baseline/main.py --provider groq --model openai/gpt-oss-20b
```

Other provider branches remain available in the code, but we do not describe
them as tested until we run them.

The [Python code](https://github.com/shendesuchit/agentic-ai-learning/blob/main/01-langchain/01-models/experiments/01-provider-specific-baseline/main.py)
keeps the provider calls visible. There is no LangChain import in this experiment.

## Recorded run — Groq

Recorded on 27 September 2026 using:

- provider: `groq`
- requested model: `openai/gpt-oss-20b`
- prompt: `Explain what an API is in one simple sentence.`

Observed output:

```text
SDK response type: ChatCompletion
Answer: An API is a set of rules and tools that lets different software programs communicate with each other.
```

Observed usage:

```text
prompt_tokens: 81
completion_tokens: 91
total_tokens: 172
reasoning_tokens: 63
```

This is a record of one real request, not a performance benchmark. Another call
may generate different text and token counts.

## What to notice

### Class and response shape

Our application instantiated the provider SDK class:

```python
from groq import Groq

client = Groq()
```

The call was provider-shaped:

```python
response = client.chat.completions.create(...)
```

and the response type was:

```text
ChatCompletion
```

The answer was extracted through the provider/OpenAI-compatible response shape:

```python
response.choices[0].message.content
```

This gives us something concrete to compare with LangChain.

### Model is not the same as provider

The requested model ID contains `openai`, but the request was served by Groq:

```text
model:    openai/gpt-oss-20b
provider: Groq
```

Keeping these concepts separate becomes important when the same model family can
be served by multiple inference providers.

## What this experiment proves

- Our local Groq key and SDK path worked.
- The selected model accepted the prompt.
- The provider SDK returned a `ChatCompletion`.
- Usage information included prompt, completion, total, and reasoning-token details.

It does **not** prove that other provider branches work, that the output is
deterministic, or that this model/provider is the best choice for a product.

## Interview questions

| Question | Short answer |
| --- | --- |
| Why create a direct SDK baseline before using LangChain? | To see the provider-native call and response shape so we can identify what LangChain actually abstracts. |
| What response type did our Groq SDK call return? | `ChatCompletion`. |
| Did the model name and provider name match? | No. We requested `openai/gpt-oss-20b`, but Groq served the inference request. |
| Does one successful API call prove provider portability? | No. It proves only the tested provider/model path. |
| Can one run be used as a latency benchmark? | No. Generation length, reasoning tokens, queue conditions, and normal request variance all affect timing. |

## Continue the story

Next, make the same request through LangChain and compare the application-facing
interface rather than judging which generated sentence sounds better:

[Continue to Experiment 02 — LangChain model wrapper](../02-langchain-model-wrapper/README.md).

## Provider references

- [OpenAI Python SDK](https://github.com/openai/openai-python)
- [Gemini Python quickstart](https://ai.google.dev/gemini-api/docs/get-started)
- [Groq text generation](https://console.groq.com/docs/text-chat)
- [Groq `openai/gpt-oss-20b`](https://console.groq.com/docs/model/openai/gpt-oss-20b)
- [OpenRouter with the OpenAI Python SDK](https://openrouter.ai/docs/guides/community/openai-sdk)

[Back to Models](../../README.md)
