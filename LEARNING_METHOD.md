# How we will use this repository

## The learning cycle

Begin with a problem. Explain the concept that addresses it. Build the smallest
experiment that makes its behavior visible. Inspect the result and relevant
internals. Change an assumption, compare an alternative, or provoke a failure.
Then explain what you learned and decide whether it has a use in the PV product.

Keep explanations natural and specific. A good note tells the reader what
happened, why it happened, and what evidence supports the conclusion. Avoid
claiming that an experiment worked before it has actually been run.

## Where things belong

| Level | Responsibility |
|---|---|
| Root README | Purpose, starting point, current module, product relationship |
| ROADMAP.md | Progress across major modules |
| This file | Shared learning, naming, interview, and checkpoint conventions |
| Module README | Ordered topic map, topic progress, module-wide conclusions |
| Topic README | Explanation, experiments, findings, interview consolidation |
| Experiment folder | Code and evidence for one focused question |

Keep the roadmap as text until a topic is needed. Do not add empty directories
or placeholder files for every future subject.

## Let each topic grow naturally

Every topic begins with `README.md`. Add `experiments/01-descriptive-name/main.py`
when there is something to run. A short experiment can be explained entirely in
the topic README. Give it its own README only when setup or findings need space.

| Artifact | Place it here, only when needed |
|---|---|
| Topic diagram | Inline Mermaid, or `diagrams/` with editable source |
| Experiment diagram | Beside that experiment's code |
| Handwritten topic notes | `notes/handwritten/YYYY-MM-DD-subject-page-01.jpg` |
| References | Topic README; move a long collection to `references.md` |
| One useful output | Experiment's `output.md` |
| Several useful outputs | Experiment's `outputs/` |
| Focused tests | Experiment's `tests/` |
| Interactive notebook | Relevant experiment folder |
| Module-wide diagram | Module's `diagrams/`, when it serves several topics |
| Repository-wide diagram | `docs/diagrams/`, if eventually useful |

Do not create all these folders together. Preserve curated outputs that explain
a result; ignore raw logs and scratch data. Record the command, model, relevant
settings, and package versions when they affect reproduction. Remove credentials
and private data before saving outputs. Use public or synthetic learning data.

Default to Python scripts. Use notebooks when interactive inspection adds value.
Keep important conclusions in the README even when handwritten notes exist.

## Naming and execution

- Number module, topic, and experiment folders with `NN-kebab-case`; experiment
  numbers restart at `01` within each topic.
- Keep established paths stable. If an extra prerequisite appears, document
  reading order in the README instead of renumbering the entire repository.
- Use `snake_case.py`, such as `main.py`, `compare.py`, or `inspect_response.py`.
  Avoid filenames such as `inspect.py`, `json.py`, or `typing.py`: they can shadow
  Python's standard-library modules.
- Numbered folders organize learning; they are not importable Python packages.
  Run scripts by path from the repository root. Do not add package scaffolding
  simply to make every topic importable.
- Use dates for notes or dated investigations, not routine experiment names.
- Keep one root `pyproject.toml` and lockfile. Add dependencies when needed.

Some duplication helps a learner read an experiment independently. Consider
module-level `_shared/` only when repeated setup becomes distracting, often
around the third or fourth repetition. Do not extract the concept being taught.

## Topic README guide

Use the following headings when they help. Combine or omit sections that add
no value; do not fill them just to satisfy a template.

1. Problem
2. Concept and mental model
3. Experiments: question, link or command, status, result
4. What I observed
5. How it works internally
6. Compare / break
7. Common mistakes and misconceptions
8. Interview questions
9. Product relevance
10. Key takeaways
11. References
12. Next topic

For an unrun experiment, write **Planned**. Record findings after observing them.
For a retired approach, write **Superseded** and link to the newer explanation.
Keep educational failures. Git history is our archive; no general archive folder
is needed. Tag meaningful milestones before dependency upgrades when useful.
Add module-level `VERSION_NOTES.md` only when API changes warrant an explanation.
The current lockfile describes the current environment; an older commit and its
lockfile are needed to reproduce an older environment.

## Interview questions at two levels

Within a concept section or an experiment's explanation, add an **Interview
insight**: one relevant question, a concise answer, and a useful follow-up.
For a tiny experiment, this can live in the topic README beside its findings.

At the end of the topic, consolidate the important questions under **Interview
questions**. Group them by fundamentals, practical use, internals, comparisons,
failure cases, or scenarios where those categories help. Do not create empty
categories. Link back to the relevant explanation to avoid copying long answers.

Answer aloud before revealing the guidance. A useful answer explains a mechanism
or a trade-off and refers to an experiment. Definitions alone are insufficient.
Distinguish deterministic tests from evaluations of probabilistic model behavior.

## Topic completion and Git checkpoint

- [ ] I can explain the problem and concept in my own words.
- [ ] I ran the applicable experiments and recorded useful results.
- [ ] I inspected the relevant internals and compared or broke an assumption.
- [ ] The README and links reflect what I actually learned.
- [ ] Section-level interview insights and a consolidated question set are ready.
- [ ] I recorded a product-relevance decision with a reason.
- [ ] I reviewed the changed files in GitHub Desktop and committed them.
- [ ] I published or pushed the checkpoint to GitHub.

For a conceptual topic, a reasoned comparison can replace code. Small intermediate
commits are welcome; the topic-completion commit is the main milestone.

Suggested summaries:

```text
chore: establish agentic ai learning foundation
learn(langchain): complete orientation
learn(langchain): complete model fundamentals
experiment(langchain-models): compare provider and langchain interfaces
docs(langchain-models): record streaming observations
```

Keep `main` as the simple starting workflow. Update topic status in the module
README in the same completion commit. Git history records its commit hash, so
there is no need to maintain a duplicate commit log manually.

## Product relevance

Record **Relevant**, **Maybe later**, or **Not now**, then explain the product
problem, how the concept could help, and the remaining uncertainty. A learning
example belongs here; a production integration belongs in the separate product
repository. Never mark an integration complete just because it seems promising.

## Keeping the repository manageable

Navigate root → module → topic → experiment. Split an oversized topic by concept
when its experiment index becomes difficult to use. Avoid a second global
experiment catalogue. Add a separate environment only for an actual dependency
conflict, not a hypothetical one.

Before adding anything, ask: **Will this make the concept easier to understand,
reproduce, compare, or remember?**
