# 02 — Messages

[Home](../../README.md) · [LangChain chapters](../README.md) · [Previous: Models](../01-models/README.md)

## On this page

- [Why Messages come after Models](#why-messages-come-after-models)
- [What is a LangChain Message?](#what-is-a-langchain-message)
- [The four core message roles](#the-four-core-message-roles)
- [String prompt vs explicit HumanMessage](#string-prompt-vs-explicit-humanmessage)
- [Conversation history is application data](#conversation-history-is-application-data)
- [What our experiment proved](#what-our-experiment-proved)
- [What happens when history grows forever?](#what-happens-when-history-grows-forever)
- [Content, metadata, tools, and chunks](#content-metadata-tools-and-chunks)
- [Five interactive diagrams](#five-interactive-diagrams)
- [Interview questions](#interview-questions)
- [References](#references)

## Why Messages come after Models

In the Models chapter we called Groq through LangChain:

```python
response = model.invoke(
    "Explain what an API is in one simple sentence."
)
```

The response type was:

```text
AIMessage
```

That immediately creates a useful question:

> If the model returns an `AIMessage`, what exactly are Messages and how do they
> represent a conversation?

This chapter answers that question before we move to prompt templates.

## What is a LangChain Message?

Messages are LangChain's standard units of model context. A message carries:

- a **role** — who or what the message represents,
- **content** — the payload sent to or returned from the model,
- optional **metadata** — IDs, token usage, provider response information, and
  other structured fields.

A list of Messages is therefore more than a list of strings. It represents an
ordered conversation with explicit roles.

A useful mental model is:

```text
role + content + optional metadata
              |
              v
           Message
```

The model sees the Messages supplied in the **current invocation**.

## The four core message roles

### `SystemMessage`

Represents instructions or context that guide model behavior.

```python
SystemMessage(
    "You are a patient teacher. Answer in one simple sentence."
)
```

In our run, the model followed that instruction and returned a short one-sentence
explanation.

A system message is an instruction role, not a guarantee that unsafe or
conflicting instructions can never influence a model. We will treat instruction
priority and prompt-injection defenses as later safety topics.

### `HumanMessage`

Represents user input.

```python
HumanMessage("Explain what an API is.")
```

A human message can carry more than plain text; LangChain also supports message
content for multimodal data when the selected model/provider supports it.

### `AIMessage`

Represents model output.

Our model returned:

```text
AIMessage
```

An `AIMessage` is not merely a Python string. Depending on the model and
integration, it can expose information such as:

```python
response.content
response.id
response.usage_metadata
response.response_metadata
response.tool_calls
```

We already observed `content`, `usage_metadata`, and `response_metadata` in the
Models chapter.

### `ToolMessage`

Represents the result of one tool execution sent back to the model.

The important direction is:

```text
AIMessage asks for a tool
        |
        v
application executes the tool
        |
        v
ToolMessage carries the result back
```

We introduce the role here, but we will execute and inspect real tool messages in
the Tools chapter rather than pretending that this Messages experiment tested
them.

## String prompt vs explicit HumanMessage

For a simple standalone request, LangChain allows:

```python
model.invoke("Explain what an API is.")
```

A string is a convenience form for a single user/human input.

When roles or conversation history matter, explicit message objects make the
structure visible:

```python
messages = [
    SystemMessage("You are a patient teacher."),
    HumanMessage("Explain what an API is."),
]

response = model.invoke(messages)
```

The second form is easier to reason about when the conversation grows.

## Conversation history is application data

Our most important lesson in this chapter is:

> **Conversation continuity comes from supplying relevant earlier Messages again.**

The application created:

```python
messages = [
    SystemMessage(...),
    HumanMessage(...),
]
```

The model returned an `AIMessage`, and our code explicitly appended it:

```python
messages.append(response)
```

Then we appended the next user turn:

```python
messages.append(
    HumanMessage(
        "Now explain the same concept using a restaurant analogy."
    )
)
```

The next invocation received the ordered history:

```text
SystemMessage
HumanMessage
AIMessage
HumanMessage
```

That history gave the model enough context to understand what **"the same
concept"** referred to.

The application owns the Python list. The model does not receive an old turn
merely because the same `ChatGroq` object is being reused.

## What our experiment proved

[Read Experiment 01 — Message roles and history](experiments/01-message-history/README.md).

We used Groq with:

```text
openai/gpt-oss-20b
```

### Part 1 — explicit roles

The request contained:

```text
SystemMessage
HumanMessage
```

Observed:

```text
Response type: AIMessage
Is AIMessage: True
Answer: An API is a set of rules that lets different software programs talk to each other.
```

### Part 2 — explicit history

Before the follow-up call, the history printed:

```text
1. SystemMessage: You are a patient teacher. Answer in one simple sentence.
2. HumanMessage: Explain what an API is.
3. AIMessage: An API is a set of rules that lets different software programs talk to each other.
4. HumanMessage: Now explain the same concept using a restaurant analogy.
```

The model then answered:

```text
Just like a menu tells a waiter what dishes you can order and how to get them,
an API lists the functions a program can use and how to call them.
```

The important observation is not the restaurant wording itself. The model could
resolve **"the same concept"** because earlier turns were supplied again.

### Part 3 — isolated invocation

We deliberately sent only:

```text
HumanMessage:
"What concept were we discussing, and what analogy did you use?"
```

without the earlier history.

Observed:

```text
Response type: AIMessage
Answer: I’m not sure which conversation you’re referring to. Could you give me
a little more context or remind me of the topic and the analogy we used? ...
```

This is a clean contrast:

```text
with relevant history     -> conversational continuity
isolated current message  -> previous turns absent from this request
```

We should describe the architecture precisely: the earlier Messages were not
supplied in the isolated invocation. We do not need to make stronger claims about
what a provider might offer through other stateful APIs or products.

## What happens when history grows forever?

A naive application could keep doing:

```python
messages.append(...)
messages.append(...)
messages.append(...)
```

and resend the whole list on every turn.

That eventually creates several problems.

### Cost and latency

Longer histories usually mean more input tokens. That can increase API cost and
the amount of work required to process a request.

One call is not a benchmark, and latency depends on the provider, model,
generation length, queueing, caching, and other factors. The safe conclusion is
simply that unnecessary context is unnecessary work.

### Relevance and stale information

More context is not automatically better context.

Old messages can:

- distract from the current task,
- contain superseded decisions,
- conflict with newer information,
- repeat an earlier model mistake and make it look authoritative.

A previous `AIMessage` is conversation data, not automatically verified truth.

### Privacy and security

Blindly replaying history can repeatedly expose data that the current request
does not need.

History may contain:

- personal or confidential information,
- secrets accidentally returned by a tool,
- untrusted retrieved text,
- malicious prompt-injection instructions.

If that material is stored and resent, its influence can persist across later
model calls.

Useful principles are:

- minimize data sent to the model,
- do not place credentials or secrets in model context,
- distinguish trusted instructions from untrusted external content,
- keep retention and redaction policies explicit.

### Context-window pressure

The current request may need to fit:

```text
system instructions
+ conversation history
+ tool results
+ retrieved documents
+ current question
+ room for the answer
```

A finite context window means we cannot simply append everything forever.

### Operational and environmental efficiency

Large histories also mean larger request payloads, logs, traces, and storage.
At scale, unnecessary tokens mean unnecessary inference work and infrastructure
usage. The exact environmental impact depends on the model, hardware, datacenter,
energy mix, utilization, and serving architecture, so we do not equate one token
with a fixed environmental cost.

The practical lesson is broader:

> **Good context is relevant context, not maximum context.**

Later Context Engineering and Short-Term Memory chapters will study how systems
select, trim, summarize, retrieve, and persist context.

## Content, metadata, tools, and chunks

Messages are richer than this first experiment.

### Content blocks and multimodality

Message content can be a simple string or structured content. LangChain also
offers standard content blocks for text, reasoning, images, audio, files, and
other supported content.

Provider support still matters. A LangChain content type does not guarantee that
every model accepts every modality.

We have **not** run a multimodal Messages experiment yet.

### Metadata

`AIMessage` can carry common usage information and provider/model response
metadata. We observed both in the previous Models experiment.

`HumanMessage` can also carry optional identifiers such as a name or message ID.
Provider handling of optional fields can vary.

### Tool messages

An AI message can request tool calls. A `ToolMessage` represents the execution
result associated with a tool-call ID.

We intentionally defer real tool execution to the Tools chapter.

### Streaming chunks

When streaming a chat model, LangChain yields `AIMessageChunk` objects that can
be combined into a complete message.

We intentionally defer the runnable streaming experiment to the Streaming topic.
The Messages chapter needs to recognize the type without mixing two learning
objectives into one experiment.

## Five interactive diagrams

After rendering the bundled Archify sources, the website visual guide contains:

1. **The four message roles** — where System, Human, AI, and Tool messages fit.
2. **String shortcut vs explicit messages** — when a plain string is enough and
   when roles should be explicit.
3. **Building conversation history** — how the application appends model output
   and resends ordered context.
4. **With history vs isolated call** — the exact contrast tested in Part 3.
5. **Risks of unbounded history** — cost, latency, relevance, privacy/security,
   context limits, and resource efficiency.

The diagrams are conceptual learning aids. They do not call the model or report
measured performance.

## Interview questions

| Question | Short answer |
| --- | --- |
| What is a LangChain Message? | A standard unit of model context containing a role, content, and optional metadata. |
| What are the main message roles? | System, Human, AI, and Tool. |
| What does `SystemMessage` represent? | Instructions/context intended to guide model behavior. |
| What does `HumanMessage` represent? | User input supplied to the model. |
| What does `AIMessage` represent? | Model output, including content and potentially metadata or tool-call requests. |
| What does `ToolMessage` represent? | The result of a tool execution sent back to the model and associated with a tool-call ID. |
| Is `model.invoke("hello")` always wrong? | No. A string is convenient for a standalone human/user input. Explicit messages are clearer when roles/history matter. |
| Who maintained history in our experiment? | Our Python application maintained the `messages` list and supplied it again. |
| Why did "the same concept" work in Part 2? | The request included the earlier Human and AI messages, so the reference had context. |
| What happened in the isolated call? | Earlier turns were not supplied, and the model asked for more context. |
| Does more history always improve answers? | No. Irrelevant, stale, conflicting, unsafe, or sensitive history can make the request worse. |
| Why not send the entire transcript forever? | It consumes context and can increase cost, latency, noise, privacy/security exposure, and operational load. |
| Is a previous `AIMessage` verified truth? | No. It is previous model output and may contain mistakes. |
| What is the difference between conversation history and memory? | History is the ordered conversation data; memory is the broader strategy/system for retaining and supplying useful past information. |
| What is an `AIMessageChunk`? | A partial model message returned during streaming; chunks can be combined into a complete message. |
| Does LangChain make every provider's message behavior identical? | No. The message abstraction is common, while provider capabilities and treatment of optional fields can still differ. |

## Our conclusion

Models taught us how to call an LLM through a common interface.

Messages teach us **what context crosses that interface**.

The key boundary is:

```text
application chooses and orders context
                |
                v
          model invocation
                |
                v
            AIMessage
```

That boundary will matter repeatedly when we reach Prompts, Tools, Context
Engineering, Memory, and Agents.

## References

- [LangChain Messages](https://docs.langchain.com/oss/python/langchain/messages)
- [LangChain Models](https://docs.langchain.com/oss/python/langchain/models)
- [LangChain Groq integration](https://docs.langchain.com/oss/python/integrations/chat/groq)
- [Archify](https://github.com/tt-a1i/archify)

[Back to top](README.md) · Next chapter: Prompts
