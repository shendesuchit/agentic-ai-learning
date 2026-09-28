# Agentic AI Learning

Understanding an AI system becomes much easier when we can follow what happens
inside it. Start with one model call, look at its response, then follow the
context that is sent on the next turn.

These chapters explain concepts through small experiments and interactive
diagrams.

## Start with LangChain

| Chapter | What it explains |
| --- | --- |
| [00 — Orientation](01-langchain/00-orientation/README.md) | Where LangChain fits, and how a model, a tool, and an agent differ. |
| [01 — Models](01-langchain/01-models/README.md) | Calling a model, comparing a provider SDK with a LangChain wrapper, and understanding the response abstraction. |
| [02 — Messages](01-langchain/02-messages/README.md) | Roles, ordered conversation context, application-managed history, and why unlimited replay becomes a problem. |

## Explore Models visually

Follow the request from the application to the provider and inspect the
`AIMessage` returned by LangChain.

- [The request journey](01-langchain/01-models/visual-guide.md#the-request-journey)
- [Invoke, stream, and batch](01-langchain/01-models/visual-guide.md#invoke-stream-and-batch)
- [Inside an AIMessage](01-langchain/01-models/visual-guide.md#inside-an-aimessage)

## Explore Messages visually

Follow five related questions:

- [The four message roles](01-langchain/02-messages/visual-guide.md#the-four-message-roles)
- [String shortcut vs explicit messages](01-langchain/02-messages/visual-guide.md#string-shortcut-vs-explicit-messages)
- [Building conversation history](01-langchain/02-messages/visual-guide.md#building-conversation-history)
- [With history vs isolated invocation](01-langchain/02-messages/visual-guide.md#with-history-vs-isolated-invocation)
- [Risks of unbounded history](01-langchain/02-messages/visual-guide.md#risks-of-unbounded-history)

The diagrams are conceptual learning aids. They do not call a model or report
measured performance.

## Follow the experiments

1. [Direct provider call](01-langchain/01-models/experiments/01-provider-specific-baseline/README.md) — establish the provider-SDK baseline.
2. [LangChain model wrapper](01-langchain/01-models/experiments/02-langchain-model-wrapper/README.md) — repeat the request through `ChatGroq` and inspect `AIMessage`.
3. [Message roles and history](01-langchain/02-messages/experiments/01-message-history/README.md) — build a multi-turn message list, then remove the history and observe the negative case.

The recorded model experiments currently use Groq with `openai/gpt-oss-20b`.
Other provider paths remain references until we execute them ourselves.
