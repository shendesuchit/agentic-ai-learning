# LangChain model wrapper

[Models](../../README.md) · [Previous: Direct provider call](../01-provider-specific-baseline/README.md) · [LangChain chapters](../../../README.md)

## Learning question

**What changes when our application stops calling a provider SDK directly and
calls the same model through a LangChain chat-model wrapper?**

This experiment deliberately keeps the important variables fixed:

- same provider: Groq
- same requested model: `openai/gpt-oss-20b`
- same prompt: `Explain what an API is in one simple sentence.`

That lets us focus on the software abstraction instead of comparing model quality.

## Before and after

The baseline route was:

```text
Application
    |
    v
Groq SDK
    |
    v
Groq API
    |
    v
openai/gpt-oss-20b
    |
    v
ChatCompletion
```

This experiment inserts LangChain:

```text
Application
    |
    v
ChatGroq
    |
    v
langchain-groq integration
    |
    v
Groq API
    |
    v
openai/gpt-oss-20b
    |
    v
AIMessage
```

[Explore the existing request-journey diagram](https://shendesuchit.github.io/agentic-ai-learning/01-langchain/01-models/visual-guide.html#the-request-journey).

## The classes and interfaces in this experiment

### `ChatGroq`

```python
from langchain_groq import ChatGroq
```

`ChatGroq` is a **LangChain provider integration**. Creating it does not run the
LLM inside Python. It creates an object that knows how to communicate with the
selected model through Groq while exposing LangChain's chat-model interface.

```python
model = ChatGroq(model="openai/gpt-oss-20b")
```

Provider-specific initialization has not disappeared. We still selected a Groq
integration and a Groq API key.

### `invoke`

The application-facing call is now:

```python
response = model.invoke(PROMPT)
```

Compare that with the direct SDK baseline:

```python
response = client.chat.completions.create(
    model=model_name,
    messages=[{"role": "user", "content": PROMPT}],
)
```

This is the first abstraction we wanted to experience rather than merely read
about.

### `AIMessage`

`invoke` returned:

```text
AIMessage
```

not the provider SDK's `ChatCompletion`.

The visible answer is available through:

```python
response.content
```

The message also exposes other useful information, including:

```python
response.usage_metadata
response.response_metadata
```

[Explore the existing AIMessage diagram](https://shendesuchit.github.io/agentic-ai-learning/01-langchain/01-models/visual-guide.html#inside-an-aimessage).

## Provider references in the code

The helper keeps the provider boundary visible:

| Provider | LangChain class | Integration package | Tested here? |
| --- | --- | --- | --- |
| OpenAI | `ChatOpenAI` | `langchain-openai` | No |
| Gemini | `ChatGoogleGenerativeAI` | `langchain-google-genai` | No |
| Groq | `ChatGroq` | `langchain-groq` | **Yes** |
| OpenRouter | `ChatOpenRouter` | `langchain-openrouter` | No |

The shared `model.invoke(...)` call is the lesson. The table is **not** a claim
that all four providers have identical capabilities or that the untested paths
are already validated.

## Install the tested integration

The Groq optional dependency group needs the LangChain integration as well as the
direct SDK:

```powershell
uv add --optional groq langchain-groq
```

This updates `pyproject.toml` and `uv.lock`.

API keys stay in the ignored local `.env` file. Never commit them.

## Run the experiment

From the repository root:

```powershell
uv run --extra groq --env-file .env python 01-langchain/01-models/experiments/02-langchain-model-wrapper/main.py --provider groq --model openai/gpt-oss-20b
```

## Recorded run — Groq through LangChain

Recorded on 27 September 2026.

Observed output:

```text
Provider: groq
Requested model: openai/gpt-oss-20b
LangChain wrapper: ChatGroq
Response type: AIMessage
Answer: An API is a set of rules that lets one software program ask another program for information or services.
```

Observed normalized usage metadata:

```python
{
    "input_tokens": 81,
    "output_tokens": 67,
    "total_tokens": 148,
    "output_token_details": {
        "reasoning": 38
    }
}
```

Selected response metadata included:

```python
{
    "model_name": "openai/gpt-oss-20b",
    "service_tier": "on_demand",
    "finish_reason": "stop",
    "model_provider": "groq"
}
```

The complete runtime output also contained provider token-usage timing/details.
We record the fields that help explain the abstraction rather than treating one
request as a benchmark.

## Compare with the direct SDK run

| Observation | Direct Groq SDK | LangChain `ChatGroq` |
| --- | --- | --- |
| Requested model | `openai/gpt-oss-20b` | `openai/gpt-oss-20b` |
| Prompt | Same | Same |
| Input tokens | 81 | 81 |
| Response type | `ChatCompletion` | `AIMessage` |
| Call from our code | `client.chat.completions.create(...)` | `model.invoke(...)` |
| Text access | `response.choices[0].message.content` | `response.content` |
| Usage access | `response.usage` | `response.usage_metadata` |
| Provider details | SDK response | `response.response_metadata` |

The two generated sentences were similar but not identical. The direct request
reported 91 completion tokens with 63 reasoning tokens; the LangChain request
reported 67 output tokens with 38 reasoning tokens.

That variation does **not** mean the wrapper changed the intelligence of the
model. They were separate generations.

## What LangChain actually abstracted

The useful change is:

```text
Provider-shaped application call
        |
        v
Common model operation: invoke()
        |
        v
LangChain message abstraction
```

After the provider-specific model object exists, higher-level application code
can work with a more consistent operation and response shape.

For example:

```python
response = model.invoke(PROMPT)
print(response.content)
```

The application does not need to traverse Groq's `choices[0].message.content`
shape for this common task.

## What LangChain did not abstract away

We still care about:

- provider credentials,
- provider integration packages,
- supported model IDs,
- pricing and rate limits,
- provider/model capabilities,
- provider-specific parameters,
- some provider-specific response metadata.

That is why this statement is more accurate than "LangChain makes every provider
the same":

> LangChain provides a common model interface over provider-specific integrations.

## Why keep both normalized and provider metadata?

Our run showed both:

```python
response.usage_metadata
```

and:

```python
response.response_metadata
```

This is useful design.

`usage_metadata` gives application code a normalized place to look for common
token information when supplied by the integration.

`response_metadata` preserves details that may still matter for debugging,
observability, model/provider analysis, or provider-specific behavior.

The abstraction is therefore not "throw provider information away." It is
"normalize the common path without blocking access to useful details."

## What `finish_reason: stop` told us

The observed response metadata contained:

```text
finish_reason: stop
```

For this request, that indicates a normal completion. We will study other finish
conditions only when an experiment produces or requires them.

## What this experiment proves

- `ChatGroq` successfully called the same Groq-hosted model.
- `model.invoke(...)` returned a LangChain `AIMessage`.
- `response.content` exposed the visible answer.
- `usage_metadata` exposed normalized token information.
- `response_metadata` preserved provider/model details.
- A common interface reduces provider-shaped code in the higher application layer.

## What this experiment does not prove

- It does not prove every provider branch works; only Groq was run.
- It does not prove providers are feature-equivalent.
- It does not prove LangChain is faster or slower than the direct SDK.
- It does not prove identical prompts produce identical text.
- It does not yet explain the full LangChain Messages model.

That last gap gives us the next topic naturally.

## Interview questions

| Question | Short answer |
| --- | --- |
| What is `ChatGroq`? | A LangChain chat-model integration for communicating with models served through Groq. |
| What changed compared with the direct Groq SDK? | Our application used `model.invoke(...)` and received an `AIMessage` instead of calling Groq's chat-completions method and receiving `ChatCompletion`. |
| Does LangChain remove provider-specific initialization? | No. We still choose an integration, model, credentials, and provider-specific features. |
| Why is `AIMessage` useful compared with returning only a string? | It can carry content plus structured information such as usage, metadata, and later tool-call requests. |
| What is the difference between `usage_metadata` and `response_metadata`? | Usage metadata provides a normalized view of common usage information; response metadata preserves useful model/provider details. |
| Why did the two experiments produce different token counts? | They were separate model generations. Reasoning/output length varied even though the prompt and requested model were the same. |
| Can we conclude LangChain adds no overhead because provider time was lower in this run? | No. One pair of requests with different generations is not a benchmark. |
| Does `openai/gpt-oss-20b` mean OpenAI was the API provider in our experiment? | No. Groq was the inference provider serving that model. |
| What does "program to an interface" mean in this context? | Higher-level code depends on common model operations such as `invoke` instead of embedding provider-specific response traversal everywhere. |
| Why do provider integrations still exist if LangChain has a common interface? | Something still has to translate the common interface into the provider's API behavior and features. |

## Our conclusion

The direct SDK baseline taught us what provider-shaped application code looks
like. This experiment showed the first practical value of LangChain: the
higher-level application can work with a common model operation and a common
message abstraction while still retaining provider-specific details when needed.

The next question is now unavoidable:

**What exactly is an `AIMessage`, and how do System, Human, AI, and Tool messages
represent a conversation?**

That is the next learning topic.

## References

- [LangChain models](https://docs.langchain.com/oss/python/langchain/models)
- [LangChain messages](https://docs.langchain.com/oss/python/langchain/messages)
- [LangChain Groq integration](https://docs.langchain.com/oss/python/integrations/chat/groq)
- [Groq `openai/gpt-oss-20b`](https://console.groq.com/docs/model/openai/gpt-oss-20b)

[Back to Models](../../README.md) · Previous: [Direct provider call](../01-provider-specific-baseline/README.md)
