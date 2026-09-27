# Agentic AI Learning

This is my learning laboratory for understanding how agentic AI systems work.
The aim is to explain each idea clearly, build a small experiment, and understand
what happens when its assumptions fail.

**Current checkpoint:** Orientation and the first Models experiments are ready to
read. A direct Groq SDK call and the same request through LangChain's `ChatGroq`
wrapper have both been run and compared.

**[Explore the learning website](https://shendesuchit.github.io/agentic-ai-learning/)** for chapter navigation and interactive Models diagrams.

## Start here

1. Begin with [00 — Orientation](01-langchain/00-orientation/README.md).
2. Continue with [01 — Models](01-langchain/01-models/README.md) and its [interactive diagrams](https://shendesuchit.github.io/agentic-ai-learning/01-langchain/01-models/visual-guide.html).
3. Read the [direct provider baseline](01-langchain/01-models/experiments/01-provider-specific-baseline/README.md).
4. Compare it with the [LangChain model wrapper experiment](01-langchain/01-models/experiments/02-langchain-model-wrapper/README.md).
5. Use the [LangChain learning map](01-langchain/README.md) to see the topic order.
6. If you are working locally, [SETUP.md](SETUP.md) covers VS Code and GitHub Desktop.

## How we will learn

Problem → Concept → Minimal Experiment → Understand Internals → Compare/Break
→ Apply to Product if Relevant → Move Forward.

At the end of a topic, we consolidate interview questions, record our conclusions,
and make a Git checkpoint. Notes should explain ideas in natural, precise language,
as a teacher would explain them to a learner. Define new terms, use small examples,
and give reasons for decisions.

## What belongs here

Explanations, small experiments, useful failures, comparisons, diagrams,
handwritten notes, selected outputs, references, and tests that answer a real
question. Each topic starts small and grows only when the learning needs it.

The [roadmap](ROADMAP.md) records the wider journey. Only LangChain has folders
at present, and only its first two topics have been created.

## Relationship to the product

The **PV Safety Intelligence & Signal Investigation Platform** will live in a
separate repository. Learning a technology does not mean that we must use it in
the product. We will adopt a concept only when it addresses a clear requirement.
The product repository link will be added when it exists.

## Environment

One root Python environment, managed with uv. Python 3.11 is our agreed starting
version. Provider SDKs and LangChain provider integrations are optional
dependencies; install only what an experiment needs. API credentials remain in
the ignored local `.env` file and are never committed.
