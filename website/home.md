# Agentic AI Learning

Understanding an AI system becomes much easier when we can follow what happens inside it. Start with one model call, look at its response, and then add the next piece.

These chapters explain the concepts through small examples and interactive diagrams. Start with Orientation, or go straight to Models if the basics are familiar.

## Start with LangChain

| Chapter | What it explains |
| --- | --- |
| [00 — Orientation](01-langchain/00-orientation/README.md) | Where LangChain fits, and how a model, a tool, and an agent differ. |
| [01 — Models](01-langchain/01-models/README.md) | Calling a model, receiving its response, and understanding the interface around it. |

## Explore Models visually

Follow the request from the application to the provider. Then compare how a complete response, streamed chunks, and multiple requests arrive.

- [The request journey](01-langchain/01-models/visual-guide.md#the-request-journey)
- [Invoke, stream, and batch](01-langchain/01-models/visual-guide.md#invoke-stream-and-batch)
- [Inside an AIMessage](01-langchain/01-models/visual-guide.md#inside-an-aimessage)

The diagrams illustrate the concepts. They are not live model calls or performance measurements.

## Try one model call

[Direct provider call](01-langchain/01-models/experiments/01-provider-specific-baseline/README.md) shows the same small request with OpenAI, Gemini, Groq, or OpenRouter. Choose the provider you can access, then look at the response before adding LangChain.
