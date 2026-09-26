# 00 — Orientation

**Status:** introductory reading prepared; learner review and checkpoint pending.

## 1. The problem

Imagine starting with a script that sends a question to one model provider.
That script may be quite sufficient. As the application grows, however, you may
need message history, tool calls, validated responses, streaming, and a loop that
decides whether more work is needed. Each addition creates coordination work.

LangChain offers common interfaces and an agent framework to help with that
work. We should understand each responsibility before handing it to an abstraction.

**Interview insight:** Why might a direct provider SDK be the right starting point?

It exposes the provider's behavior directly and keeps a small experiment easy to
inspect. It also gives us a baseline for judging what a framework changes.
Follow-up: when would repeated coordination code justify a higher-level interface?

## 2. A working mental model

A model generates a response. A tool is an operation the application can make
available. An agent combines model decisions with a loop that can execute tools
and continue until it can respond or must stop.

The framework helps coordinate these parts. It does not make the model infallible
or decide whether the application's requirements have been satisfied.

**Interview insight:** Does a model's request to call a tool mean the tool ran?

For a client-side tool, no. Application or agent code must execute the request
and return the result. Keep that distinction in mind when we reach tool calling.
Provider-hosted tools require a separate discussion of where execution occurs.

## 3. Read the ecosystem by responsibility

| Component | Responsibility to understand |
|---|---|
| Provider SDK | Direct access to a provider's API and features |
| `langchain-core` | Shared abstractions, including messages and Runnables |
| Provider integration package | Connects a provider to LangChain interfaces |
| `langchain` | Higher-level building blocks and agent APIs |
| LangGraph | Stateful workflow and agent orchestration underneath LangChain agents |
| LangSmith | Tools for inspecting and evaluating application behavior |
| Deep Agents | A higher-level agent framework with capabilities for more involved tasks |

These are related tools, not interchangeable names. Our immediate job is to
understand the boundaries; we do not need to install or master every component.

**Interview insight:** Why study a manual loop before `create_agent`?

Writing the loop makes message updates, tool execution, failures, and stopping
conditions visible. We can then explain which responsibilities the framework
takes over. This is our teaching sequence, not a prerequisite imposed by the API.

## 4. A comparison exercise

Consider two hypothetical tasks:

1. A script asks one model to rewrite a sentence.
2. An assistant may look up several records, inspect results, and decide whether
   another lookup is necessary.

For each, explain what coordination code you would need. Which task benefits
more from an agent loop? What would still need checking even with a framework?
No code is needed for this exercise.

## 5. Common misconceptions

- Installing a framework does not create an agent by itself.
- A shared model interface does not guarantee identical provider behavior.
- LangChain and LangGraph have different scopes even when they work together.
- A convincing response is not evidence that the system behaved correctly.

## 6. Consolidated interview questions

Try each answer aloud, then use the guidance to check the reasoning.

| Question | Answer guidance | Revisit |
|---|---|---|
| Why use a framework for model applications? | Explain the recurring coordination work and the cost of an abstraction. | Sections 1 and 2 |
| When is a provider SDK sufficient? | Use the single-call example; explain simplicity and direct feature access. | Sections 1 and 4 |
| How do a model, tool, and agent differ? | Separate generation, executable operations, and the control loop. | Section 2 |
| Has a requested client-side tool already run? | No; distinguish a request from application execution and its returned result. | Section 2 |
| Why are provider integrations separate? | Separate common interfaces from provider-specific implementation. | Section 3 |
| How do LangChain and LangGraph relate? | Describe abstraction level and underlying orchestration. | Section 3 |
| Does switching an interface guarantee portability? | Discuss feature support, response details, and behavior that must be checked. | Section 5 |
| What does a framework still leave to the developer? | Requirements, tool design, validation, failure handling, and assessment of results. | Sections 2 and 4 |

## 7. Product relevance

**Decision: Maybe later.** The PV platform may need structured extraction and
evidence tools. Orientation helps us choose responsibilities sensibly; it does
not yet establish that any particular framework is required.

## 8. Completion check

- [ ] Explain the ecosystem table without reading its descriptions.
- [ ] Discuss the two comparison tasks and justify the level of abstraction.
- [ ] Answer the interview questions and record any corrections in this README.
- [ ] Confirm or revise the product-relevance reasoning.
- [ ] Update the module status and commit: `learn(langchain): complete orientation`.
- [ ] Push the checkpoint through GitHub Desktop.

## 9. References

- [LangChain overview](https://docs.langchain.com/oss/python/langchain/overview)
- [Package installation and integrations](https://docs.langchain.com/oss/python/langchain/install)
- [LangChain model interface](https://docs.langchain.com/oss/python/langchain/models)

These are starting references. We will inspect exact APIs when the corresponding
experiment begins.

## 10. Next

[01 — Models](../01-models/README.md): establish a direct provider baseline,
then compare it with LangChain's model abstraction.
