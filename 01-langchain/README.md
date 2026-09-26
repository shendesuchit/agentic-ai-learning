# LangChain

## Why we are learning this

We want to understand what a framework does for us and what responsibilities
remain in our application. We will compare a direct provider call with a model
abstraction, then work towards a manual tool loop and a framework-managed agent.

The important question is: **Which work did this abstraction take over, and what
did it leave in our hands?**

## Agreed learning sequence

This is the sequence agreed on 26 September 2026. Only orientation and models
have folders so far. The remaining entries describe future work.

| Topic | Learning focus | Status |
|---|---|---|
| [00-orientation](00-orientation/README.md) | Why the framework exists; packages, ecosystem, and boundaries | Reading prepared; not completed |
| [01-models](01-models/README.md) | Provider baseline; model interface, configuration, invocation, and responses | Experiments planned; not started |
| `02-messages` | Roles, content blocks, metadata, tool messages, history, and chunks | Planned |
| `03-prompts` | Static instructions, templates, dynamic inputs, and message placeholders | Planned |
| `04-runnables-and-composition` | Runnable interface, sequences, parallel composition, configuration, retries | Planned |
| `05-structured-output` | Schemas, validation, native and tool-based approaches, parsing failures | Planned |
| `06-tools-and-tool-calling` | Functions, descriptions, schemas, binding, requests, execution, responses | Planned |
| `07-manual-agent-loop` | Implement the loop; multiple calls, tool failures, limits, and termination | Planned |
| `08-langchain-agents` | create_agent; compare its behavior and responsibilities with our manual loop | Planned |
| `09-agent-state-and-runtime` | State, runtime context, dependencies, configuration, and their lifetimes | Planned |
| `10-middleware` | Model and tool hooks, dynamic behavior, retries, policies, and summarization | Planned |
| `11-context-engineering` | Select instructions, messages, tools, and information for each model call | Planned |
| `12-short-term-memory` | Conversation threads, history, trimming, summarization, persistence boundary | Planned |
| `13-streaming-and-events` | Tokens, chunks, agent updates, tool progress, custom events, async streams | Planned |
| `14-reliability-and-failure-modes` | Timeouts, invalid output, retries, rate limits, tool loops, context limits | Planned |
| `15-provider-portability` | Compare providers and discover where shared interfaces stop helping | Planned |
| `16-testing-and-debugging` | Deterministic helpers, fake tools, schemas, failure paths, trace inspection | Planned |
| `17-internals-and-boundaries` | Package architecture, Runnable inheritance, delegation, API evolution | Planned |
| `18-mini-capstones` | Combine concepts in a small extraction, research, or resilient tool assistant | Planned |

## Current checkpoint

- Starter prepared; setup and foundation commit await local confirmation.
- Next learning task: read orientation and answer its review questions.
- No experiments have been run and no topic has been marked complete.

## Boundaries

LangChain agents use LangGraph underneath. We will understand that relationship
here, then study graph orchestration in its own module. Likewise, full RAG,
embedding theory, MCP internals, evaluation methodology, observability, safety,
human approval, and multi-agent architecture have their own later modules.

Runnables and composition remain part of our foundations. We will learn them
before agents so that execution and data flow are easier to reason about.

## Interview preparation

Each topic includes questions beside the relevant concepts and a consolidated
set at the end. As topics are completed, their READMEs become the revision index.
We do not need another question-bank file yet.

## Product relevance

Potential applications include structured extraction from synthetic narratives
and tools for evidence retrieval. These are possibilities to investigate, not
approved product architecture. Record concrete decisions within each topic.

## References and next step

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
- [Repository conventions](../LEARNING_METHOD.md)
- [Begin orientation](00-orientation/README.md)

Update this page when a topic is completed, using the agreed Git checkpoint
convention. Preserve useful misconceptions and conclusions in the topic that
explains them rather than duplicating every finding here.
