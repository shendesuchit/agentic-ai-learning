# LangChain

## Why we are learning this

We want to understand what a framework does for us and what responsibilities
remain in our application. We compare a direct provider call with a model
abstraction, then work towards a manual tool loop and a framework-managed agent.

The important question is: **Which work did this abstraction take over, and what
did it leave in our hands?**

## Agreed learning sequence

This is the sequence agreed on 26 September 2026.

| Topic | Learning focus | Status |
|---|---|---|
| [00-orientation](00-orientation/README.md) | Why the framework exists; packages, ecosystem, and boundaries | Explanation available |
| [01-models](01-models/README.md) | Provider baseline; model interface, configuration, invocation, and responses | Direct SDK and LangChain wrapper compared with Groq |
| [02-messages](02-messages/README.md) | Roles, content, metadata, tool-message boundary, history, and chunks | Core roles + explicit history experiment completed with Groq |
| `03-prompts` | Static instructions, templates, dynamic inputs, and message placeholders | Next |
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

- Orientation and Models explanations are available, with [interactive Models diagrams](https://shendesuchit.github.io/agentic-ai-learning/01-langchain/01-models/visual-guide.html).
- The [direct SDK experiment](01-models/experiments/01-provider-specific-baseline/README.md) was run with Groq and `openai/gpt-oss-20b`.
- The [LangChain model wrapper experiment](01-models/experiments/02-langchain-model-wrapper/README.md) repeated the same prompt and model through `ChatGroq`.
- We observed `ChatCompletion` in the provider SDK path and `AIMessage` in the LangChain wrapper path.
- The [Messages experiment](02-messages/experiments/01-message-history/README.md) then tested explicit roles, application-managed history, and an isolated request without the earlier turns.
- Five Messages visual sources explain roles, syntax, history construction, the isolation comparison, and unbounded-history risks.
- The next topic is Prompts.

## Important boundary learned in Messages

The model receives the context supplied for the current invocation.

Our application chose and ordered:

```text
SystemMessage
HumanMessage
AIMessage
HumanMessage
```

and resent that list for the contextual follow-up.

This is the foundation for later Context Engineering and Short-Term Memory work.
Those later chapters will decide **which** history should be retained or supplied;
the Messages chapter establishes the representation and the input boundary.

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

## Product relevance

Potential applications include structured extraction from synthetic narratives
and tools for evidence retrieval. These are possibilities to investigate, not
approved product architecture. Record concrete decisions within each topic.

## References and next step

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
- [LangChain Messages](https://docs.langchain.com/oss/python/langchain/messages)
- [Repository conventions](../LEARNING_METHOD.md)
- [Begin orientation](00-orientation/README.md)
- [Models](01-models/README.md)
- [Messages](02-messages/README.md)

Update this page when a topic is completed, using the agreed Git checkpoint
convention. Preserve useful misconceptions and conclusions in the topic that
explains them rather than duplicating every finding here.
