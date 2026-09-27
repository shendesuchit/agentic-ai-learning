# Agentic AI Learning

Understanding an AI system becomes much easier when we can follow what happens
inside it. Start with one model call, look at its response, and then add the next
piece.

These chapters explain the concepts through small examples and interactive
diagrams. Start with Orientation, or go straight to Models if the basics are
familiar.

## Start with LangChain

| Chapter | What it explains |
| --- | --- |
| [00 — Orientation](01-langchain/00-orientation/README.md) | Where LangChain fits, and how a model, a tool, and an agent differ. |
| [01 — Models](01-langchain/01-models/README.md) | Calling a model, comparing a provider SDK with a LangChain wrapper, and understanding the response abstraction. |

## Explore Models visually

Follow the request from the application to the provider. Then look inside the
message returned by LangChain.

- [The request journey](01-langchain/01-models/visual-guide.md#the-request-journey)
- [Invoke, stream, and batch](01-langchain/01-models/visual-guide.md#invoke-stream-and-batch)
- [Inside an AIMessage](01-langchain/01-models/visual-guide.md#inside-an-aimessage)

The diagrams illustrate the concepts. They are not live model calls or performance
measurements.

## Follow the first two experiments

1. [Direct provider call](01-langchain/01-models/experiments/01-provider-specific-baseline/README.md) — establish the provider-SDK baseline.
2. [LangChain model wrapper](01-langchain/01-models/experiments/02-langchain-model-wrapper/README.md) — make the same request through `ChatGroq` and inspect the `AIMessage`.

The recorded comparison uses Groq with `openai/gpt-oss-20b`. Other providers are
kept as reference paths until we run them ourselves.
