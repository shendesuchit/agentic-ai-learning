# 00 — Orientation

[Home](../../README.md) · [LangChain chapters](../README.md) · [Next: Models](../01-models/README.md)

## On this page

- [Why do we need LangChain?](#why-do-we-need-langchain)
- [Model, tool, and agent](#model-tool-and-agent)
- [Where the packages fit](#where-the-packages-fit)
- [When a direct SDK is enough](#when-a-direct-sdk-is-enough)
- [Interview questions](#interview-questions)
- [References](#references)

## Why do we need LangChain?

Say we have a short Python script: send a question to a model and print the answer. A provider's SDK can do that perfectly well. There is no reason to add a framework just for the sake of it.

Now imagine we want the assistant to remember earlier messages, call a tool for fresh information, return a predictable format, and handle a failed call. Our script starts doing more coordination work. LangChain gives us common interfaces and building blocks for some of that work.

The useful question is always: **what did the framework handle, and what does our application still have to handle?** Choosing the right tools, checking an answer, and deciding what a good result looks like still belong to us.

**Interview angle:** If the task is only one model call, explain why a direct SDK can be the clearer choice. If the task has several connected steps, explain which repeated work a framework can help with.

## Model, tool, and agent

These three words often come together, but they do different jobs:

| Part | Its job |
| --- | --- |
| **Model** | Reads the input and produces a response. It may also request a tool call. |
| **Tool** | Performs a specific operation, such as looking up information or running a calculation. |
| **Agent** | Coordinates a loop: ask the model, handle any requested tools, give results back, and decide when to stop. |

Suppose someone asks for the weather in Pune **right now**. A model should not invent live weather. If we make a weather tool available, a possible flow is:

1. The application sends the question and the tool description to the model.
2. The model requests the weather tool with a location.
3. The application (or agent code) runs that tool.
4. The tool result goes back to the model so it can answer.

The important bit: **a request to use a client-side tool is not the same as running it**. We will look at provider-hosted tools separately, because the execution boundary can be different.

An agent can decide whether it needs another tool call. A fixed sequence of known steps may work without an agent at all.

**Interview angle:** When asked whether the model “calls the tool,” distinguish the model's request from the application's execution. Then explain who handles failures and when the loop ends.

## Where the packages fit

The LangChain ecosystem has several names. Here is the simple map:

| Name | What it is for |
| --- | --- |
| Provider SDK | Talks directly to a specific provider's API. |
| `langchain-core` | Shared interfaces, including messages and Runnables. |
| Provider integration | Connects a provider to those interfaces. |
| `langchain` | Higher-level components, including agents. |
| LangGraph | More explicit control over stateful workflows and agent orchestration. LangChain agents use it underneath. |
| LangSmith | Inspecting, tracing, and evaluating application behavior. |
| Deep Agents | Higher-level agent capabilities for more involved tasks. |

We do not need to install the whole list to understand the first model call. Start with the responsibility; choose the package when that responsibility actually comes up.

## When a direct SDK is enough

A direct SDK keeps provider features visible and is easy to understand for one small task. LangChain becomes interesting when a common interface or coordinated pieces make the application simpler. It does add another layer, so we should compare a direct call with a LangChain call before assuming it helps.

That comparison begins in [Models](../01-models/README.md). We will use the same small task on both sides, inspect the actual response, and note where the common interface stops being common.

## Interview questions

| Question | Short answer |
| --- | --- |
| Why use LangChain if I can call a provider directly? | Use it when its interfaces or orchestration remove repeated coordination work. A simple direct call may need nothing more. |
| Is a model the same as an agent? | No. The model generates or requests; the agent manages a loop around those responses. |
| Has a tool already run when the model requests it? | For a client-side tool, no. Application or agent code still runs it and returns the result. |
| Does adding LangChain guarantee a correct answer? | No. The application still needs suitable tools, validation, and a way to assess results. |
| How does LangGraph relate to LangChain agents? | LangChain provides a higher-level agent interface; LangGraph underlies its orchestration and offers more direct control. |

## References

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain model interface](https://docs.langchain.com/oss/python/langchain/models)
- [LangChain installation and integrations](https://docs.langchain.com/oss/python/langchain/install)

[Back to top](README.md) · [Continue to Models](../01-models/README.md)
