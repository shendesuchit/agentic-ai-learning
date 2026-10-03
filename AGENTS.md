# Agentic AI Learning Project

## Purpose

This repository is primarily a learning repository.

The goal is not to generate large amounts of content or code as quickly as possible.
The goal is to deeply understand Agentic AI concepts through small runnable experiments, observations, comparisons, diagrams, explanations, and interview preparation.

Learning quality takes priority over repository expansion.

## Learning Workflow

Follow this sequence for every topic:

1. Understand the concept first.
2. Connect it to the previous experiment/topic.
3. Build or inspect a small runnable experiment where applicable. For conceptual topics, a reasoned comparison or other appropriate learning exercise is acceptable, consistent with LEARNING_METHOD.md.
4. Run the experiment or carry out the chosen learning exercise.
5. Observe the actual output or findings.
6. Explain why the output occurred or what supports the findings.
7. Compare it with the previous approach where relevant.
8. Discuss important classes, interfaces, abstractions, and design decisions.
9. Discuss useful interview questions; save them only when artifact generation is authorized.
10. Only after the learner acknowledges understanding and separately authorizes artifact generation, package the topic.

Do not skip directly to artifact generation.

## Learning Gate

For a new learning topic, do NOT create topic artifacts merely because the user asks to "prepare", "start", "build", or "work on" the topic.

There are two distinct gates.

### Gate 1: Learning acknowledgement

The user saying either of the following, or equivalent, means only that the learner considers the conceptual learning checkpoint complete:

- "concept understood"
- "learning complete"

This acknowledgement does NOT authorize artifact generation. An explanation provided by the agent must never be treated as evidence that the learner understands the topic.

### Gate 2: Artifact authorization

After the learning checkpoint, artifact generation requires a separate explicit instruction for the named or clearly identified active topic, such as:

- "generate repo artifacts"
- "package this topic"
- "create the artifacts"

Remain in learning mode until both gates are satisfied. Do not infer either gate from a request to move to another topic.

### Learning mode

In learning mode you may:

- inspect existing repository content,
- explain concepts,
- propose experiments,
- discuss expected behavior,
- answer questions,
- suggest the next learning step.

Without artifact authorization, do not create or modify repository artifacts for the learning topic, including:

- topic directories
- topic README files
- parent README/navigation
- diagrams
- saved outputs
- website content/integration
- roadmap/progress markers
- dependency/configuration files
- unrelated repository files

Exception: A specific experimental file may be created or modified when the user explicitly requests it as part of the active learning exercise. Create only the parent directories needed for that file, if missing. This exception does not authorize packaging the topic or creating accompanying artifacts.

Inspecting existing code and running an authorized experiment must respect these write boundaries. Discuss results in the conversation rather than saving outputs without authorization.

LEARNING_METHOD.md's README-first packaging convention applies when artifact generation has been authorized; it does not override the Learning Gate.

These gates govern learning-topic work. A separate explicit maintenance request, such as editing AGENTS.md, authorizes only its stated changes and does not authorize topic artifacts.

Requests such as "start Prompts", "let's do Prompts", "prepare Prompts", or "move to the next topic" must NOT by themselves be interpreted as approval to generate the complete repository artifacts.

### Artifact mode

Artifact authorization applies only to the explicitly named or clearly identified active topic and integration changes necessary to package that topic.

It does not authorize subsequent topics, unrelated cleanup, broad refactoring, dependency upgrades, or redesign of unrelated website areas. It does not override safety or Git approval boundaries.

Artifact authorization expires after that topic's packaging task is completed. Later packaging work requires its own authorization.

## Sequencing and Progress Authority

AGENTS.md defines how Codex works, not the current completion status of topics.

ROADMAP.md is authoritative for module order and module progress. Within a module, its README defines topic/experiment order and progress.

Stale progress or status markers do not invalidate sequencing authority. Report discrepancies without automatically correcting them. Do not maintain a detailed completion snapshot in AGENTS.md.

Do not skip ahead or change the learning sequence unless explicitly instructed. Permission to move ahead does not mark the previous topic complete or authorize artifacts for the next topic.

## Provider Coverage

Where provider-specific behavior is relevant, consider examples or references for:

- OpenAI
- Groq
- Google Gemini
- OpenRouter

Do not force every provider into every experiment when it adds no learning value.

Prefer LangChain abstractions when the topic is about LangChain, while still explaining what provider-specific SDK behavior exists underneath.

## Repository Artifact Standard

When packaging an authorized learning topic, the repository should tell the complete story supported by actual learning and observations.

Where applicable, a completed topic should include:

- topic navigation
- conceptual explanation
- runnable code
- commands used to run the experiment
- actual observed output or observations
- comparison with the previous experiment
- relevant classes/interfaces
- diagrams or visual explanations
- interview questions within useful subsections
- consolidated interview questions at topic README level
- links between explanation, code, diagrams, and website
- parent README/navigation updates
- website integration

Include only artifacts that add learning value. This list is not permission to create files before both gates are satisfied.

## Python Environment

The project uses:

- Python 3.11 as the agreed baseline (pyproject.toml permits Python >=3.11)
- uv
- pyproject.toml
- uv.lock
- .venv

Use the existing uv-based workflow as the standard for learning experiments.

The existing website tooling currently uses website/requirements.txt and pip. Preserve that existing website setup unless explicitly asked to migrate it.

Do not introduce another package manager or environment-management approach unless explicitly requested.

Before adding a dependency, check whether it already exists in pyproject.toml or the appropriate optional dependency group.

Keep dependency changes within explicitly authorized scope. Topic packaging alone does not authorize dependency upgrades.

## Safety and Change Rules

Within the user's requested scope and the Learning Gate, you may:

- inspect repository files
- search the codebase
- explain code
- create or modify project files
- run safe project-local commands
- run Python examples
- run tests
- run website validation/build commands
- inspect Git status and diffs

Preserve existing tracked and untracked user work. Never overwrite, delete, reset, clean, or discard user-authored work unless explicitly authorized. Permission to edit a file covers the requested changes, not discarding unrelated content.

Established build tooling may regenerate only its designated generated output directories when running an explicitly requested build/validation task. This exception does not authorize cleanup elsewhere.

Never expose secrets, API keys, tokens, .env contents, or credentials in terminal output reproduced to the user, documentation, artifacts, or logs intentionally saved to the repository. Avoid commands that print secrets.

Do NOT without explicit approval:

- overwrite, delete, or discard user-authored work
- modify .env files or credentials
- perform destructive Git operations
- force reset branches
- rewrite Git history
- install system-level software
- git commit
- push to GitHub
- merge branches
- create or merge pull requests
- publish releases
- deploy, publish, manually dispatch a publishing workflow, or otherwise trigger GitHub Pages publication

## Git Workflow

The human user controls Git commit, push, and merge. Perform these actions only when explicitly requested.

Before considering a topic complete:

1. show the relevant changes,
2. run appropriate validations,
3. explain what changed,
4. allow the user to review,
5. leave commit/push under user control unless explicitly requested.

A clean logical checkpoint should normally be offered for human review after each completed learning topic. References to commits, tags, or publishing in LEARNING_METHOD.md describe human-controlled checkpoints, not automatic authorization for the agent.

## Website

The repository includes an MkDocs-based learning website.

When completing a topic, verify where applicable:

- MkDocs navigation
- internal links
- diagram links
- code links
- website build
- GitHub Pages compatibility

Website validation/build is different from publication/deployment. Use the established commands and conventions for an explicitly requested build/validation task:

- python website/build.py build
- existing MkDocs configuration
- hook-generated navigation
- .website-build generated output

If a build/validation task has not been requested, report that validation remains pending rather than treating packaging authorization as permission to regenerate build output.

Preserve the website's pip and website/requirements.txt tooling. Do not replace hook-generated navigation with an unrelated navigation system.

Do not deploy, publish, manually dispatch a publishing workflow, or otherwise trigger GitHub Pages publication without explicit authorization. A local build does not grant that authorization; the existing workflow can publish from main after a push or manual dispatch.

Do not redesign unrelated parts of the website while working on a learning topic.

## Diagrams

Diagrams should simplify complex concepts and support learning.

Prefer a clear visual story over decorative complexity.

When Archify or the repository's existing visualization approach is being used, preserve existing conventions. Propose changes with a clear reason; do not migrate diagram tooling without explicit authorization.

## Working Style

Make small, reviewable changes.

Do not refactor unrelated code while implementing a learning experiment.

Do not silently fix unrelated issues discovered during a task.
Report them separately.

If repository documentation conflicts with the actual repository state, point out the discrepancy before changing it.

## Completion Principle

A topic's learning checkpoint is complete only when the learner acknowledges understanding. Its authorized packaging task is complete when the repository accurately captures that understanding and applicable validation and review requirements are satisfied. Report any pending validation or human Git checkpoint separately; do not perform it autonomously to declare completion.

More files do not mean more learning.
