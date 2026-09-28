# Message roles and conversation history

[Messages](../../README.md) · [Previous chapter: Models](../../../01-models/README.md) · [LangChain chapters](../../../README.md)

## Learning question

**Does conversational continuity come from the model automatically remembering
our previous Python call, or from the context our application supplies?**

We answer that with three small parts:

1. send explicit `SystemMessage` and `HumanMessage` objects;
2. append the returned `AIMessage` and make a contextual follow-up;
3. make an isolated invocation without the earlier history.

## Classes used

```python
from langchain.messages import (
    AIMessage,
    HumanMessage,
    SystemMessage,
)
from langchain_groq import ChatGroq
```

| Class | Role in this experiment |
| --- | --- |
| `ChatGroq` | LangChain provider integration used to call the model. |
| `SystemMessage` | Supplies the teacher-style instruction. |
| `HumanMessage` | Represents each user turn. |
| `AIMessage` | Represents the model response that we append back into history. |

`ToolMessage` is part of the Messages model, but this experiment does not execute
a tool. We will test it when tool calling becomes the learning objective.

## Run it

From the repository root:

```powershell
uv run --extra groq --env-file .env python 01-langchain/02-messages/experiments/01-message-history/main.py
```

The experiment uses:

```text
provider: Groq
model: openai/gpt-oss-20b
```

## Part 1 — explicit message roles

Input:

```python
messages = [
    SystemMessage(
        "You are a patient teacher. "
        "Answer in one simple sentence."
    ),
    HumanMessage(
        "Explain what an API is."
    ),
]
```

Observed:

```text
Response type: AIMessage
Is AIMessage: True
Answer: An API is a set of rules that lets different software programs talk to each other.
```

### What this establishes

- explicit Message objects can be supplied directly to `model.invoke(...)`;
- the returned object is an `AIMessage`;
- the system instruction and user request are represented as different roles.

The result is one run, not proof that every model will obey every system
instruction perfectly.

## Part 2 — build explicit history

We append the actual returned `AIMessage`:

```python
messages.append(response)
```

Then add a contextual follow-up:

```python
messages.append(
    HumanMessage(
        "Now explain the same concept using a restaurant analogy."
    )
)
```

Before the second call, the program printed:

```text
1. SystemMessage: You are a patient teacher. Answer in one simple sentence.
2. HumanMessage: Explain what an API is.
3. AIMessage: An API is a set of rules that lets different software programs talk to each other.
4. HumanMessage: Now explain the same concept using a restaurant analogy.
```

The next call was:

```python
follow_up = model.invoke(messages)
```

Observed:

```text
Response type: AIMessage
Answer: Just like a menu tells a waiter what dishes you can order and how to get them, an API lists the functions a program can use and how to call them.
```

The interesting phrase is:

```text
"the same concept"
```

The follow-up message alone does not name APIs. The request worked because the
earlier turns were included in the `messages` list supplied to this invocation.

## Part 3 — remove the history

The isolated call supplied only:

```python
HumanMessage(
    "What concept were we discussing, "
    "and what analogy did you use?"
)
```

Observed:

```text
Response type: AIMessage
Answer: I’m not sure which conversation you’re referring to. Could you give me a little more context or remind me of the topic and the analogy we used? That way I can give you the exact answer you’re looking for.
```

This creates a clean comparison:

| Call | Earlier turns supplied? | Observed behavior |
| --- | --- | --- |
| Follow-up with `messages` | Yes | The model connected "the same concept" to the earlier API discussion. |
| Isolated invocation | No | The model said it lacked enough conversational context. |

## What this experiment proves

For the tested LangChain + Groq path:

- explicit System and Human messages were accepted;
- `model.invoke(messages)` returned `AIMessage`;
- our Python list stored the ordered conversation;
- resending the list provided continuity for the follow-up;
- omitting the earlier list removed that conversational context from the
  isolated request.

## What it does not prove

- It does not test every model or provider.
- It does not test provider-managed conversation/session APIs outside this code.
- It does not test tool calls or `ToolMessage`.
- It does not test multimodal content blocks.
- It does not test streaming or `AIMessageChunk`.
- It does not prove that every prior message should always be resent.

The final point is important: sending every old message forever creates its own
cost, context-window, relevance, privacy, and security problems.

## Useful failure / negative case

Part 3 is intentionally a useful negative case.

Instead of documenting only the successful multi-turn conversation, we removed
the required context and saw the model ask for more information.

That turns the idea:

> "the application supplies conversation context"

into an observed behavior rather than a statement we simply copied from
documentation.

## Interview questions

| Question | Short answer |
| --- | --- |
| Why use explicit messages instead of strings? | To represent roles and ordered conversational context clearly. |
| What did `model.invoke(messages)` return? | An `AIMessage`. |
| Who appended the AI response to history? | Our application did, with `messages.append(response)`. |
| Why could the model understand "the same concept"? | The earlier Human and AI messages were resent in the current request. |
| What did the isolated call demonstrate? | When the earlier turns were not supplied, the model no longer had that conversation context. |
| Does reusing the same `ChatGroq` Python object automatically send previous turns? | Not in this experiment; only the Messages supplied to each invocation were sent by our code. |
| Should we resend every message forever? | No. Context must eventually be selected, trimmed, summarized, or otherwise managed. |

## Continue the story

[Back to the Messages chapter](../../README.md) to connect this experiment to
context-window pressure, privacy/security risks, content blocks, tool messages,
and the five interactive visual explanations.

[Back to Messages](../../README.md)
