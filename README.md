# Agentic AI Learning

This is my learning laboratory for understanding how agentic AI systems work.
The aim is to explain each idea clearly, build a small experiment, and understand
what happens when its assumptions fail.

**Current checkpoint:** repository starter prepared; local setup and learning
completion still need to be confirmed. Begin with LangChain orientation.

## Start here

1. Follow [SETUP.md](SETUP.md) to open this project in VS Code and configure GitHub Desktop.
2. Read the [learning method and repository conventions](LEARNING_METHOD.md).
3. Open the [LangChain learning map](01-langchain/README.md).
4. Begin [00 — Orientation](01-langchain/00-orientation/README.md).

## How we will learn

Problem → Concept → Minimal Experiment → Understand Internals → Compare/Break
→ Apply to Product if Relevant → Move Forward.

At the end of a topic, we will consolidate interview questions, record our
conclusions, and make a Git checkpoint. Notes should explain ideas in natural,
precise language, as a teacher would explain them to a learner. Define new terms,
use small examples, and give reasons for decisions.

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
version. Dependencies will be added when the first experiment needs them.
This starter includes no LangChain code, provider choice, or API credentials.
