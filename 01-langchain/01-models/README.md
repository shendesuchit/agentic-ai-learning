# 01 — Models

**Status:** experiment plan prepared; implementation and observations pending.

## 1. The question we will investigate

What changes when we place a common model interface between our application
and a provider? We will keep the first task small so that input, configuration,
and response differences remain visible.

## 2. Starting concept

A model interface gives application code a consistent way to request a response.
The provider still determines the available models, capabilities, and service
behavior. Our experiments should reveal both the shared interface and its limits.

**Interview insight:** Does a shared interface make providers interchangeable?

Not completely. Matching method names does not guarantee matching features,
configuration, output details, or behavior. We will support this answer with a
concrete comparison rather than leaving it as a general claim.

## 3. Planned experiments, in order

The paths below are reserved names, not existing folders. Create each when we
are ready to implement it. No provider or model has been chosen yet.

| # | Future folder under `experiments/` | Question | Status |
|---|---|---|---|
| 01 | `01-provider-specific-baseline` | What do request and response look like with the provider SDK? | Planned |
| 02 | `02-langchain-model-abstraction` | What changes through the LangChain interface? | Planned |
| 03 | `03-provider-swap` | Which parts stay stable when the provider changes? | Planned; second provider access needed |
| 04 | `04-model-configuration` | Which settings affect behavior, and which depend on the provider? | Planned |
| 05 | `05-invoke-vs-stream` | How does receiving chunks change response handling? | Planned |
| 06 | `06-batch-and-async` | How do multiple inputs and asynchronous calls change execution? | Planned |
| 07 | `07-inspect-model-response` | What is present beyond the visible answer text? | Planned |

Use `main.py` for a simple experiment. Put its question, command, and findings
here unless the experiment needs a longer explanation of its own.

For each comparison, record the provider, model, relevant settings, input,
package versions, and what actually happened. A model-name change alone is not
enough to explain a behavioral difference. If second-provider access is missing,
record that limitation rather than claiming portability was tested.

## 4. What we will inspect

Start with basic invocation. Then inspect response type, content, available usage
metadata, and streaming chunks. More advanced capabilities—multimodal content,
reasoning blocks, model profiles—can be explored when supported and useful.
Message semantics get their own treatment in the following topic.

There are no observed results yet. Add them after running the experiments.

## 5. Compare and break

Try a configuration the selected provider does not support. Compare its failure
with an application input error. Check whether metadata is present before relying
on it. Explain why a streamed partial response needs different handling from a
complete one. Record actual behavior rather than predicting exact exceptions.

## 6. Consolidated interview questions

These are initial study prompts. Expand their answers with experimental evidence.

| Category | Question | A useful answer should address |
|---|---|---|
| Fundamentals | What does a model abstraction standardize? | Invocation and response interfaces; provider-specific limits |
| Comparison | What changed between the SDK and LangChain versions? | A concrete input, configuration, and output comparison |
| Practical | When would you use streaming? | Incremental delivery and the added handling of chunks or interruptions |
| Internals | Is an AI response just a string? | Inspect the actual response object, content, and available metadata |
| Failure | What if a provider does not support a setting? | Locate the source of rejection and document the observed failure |
| Scenario | A provider swap breaks structured responses; why? | Capability and schema support need verification beyond method names |
| Follow-up | How do batch and async differ? | Multiple inputs versus non-blocking execution; inspect concurrency behavior |

Add short interview insights beside individual experiment findings. Keep the
consolidated questions here so revision does not require opening every script.

## 7. Product relevance

**Decision: Maybe later.** A stable invocation boundary could help the PV product
compare models for synthetic narrative extraction. Adoption requires evidence
about extraction quality, capabilities, operational needs, and cost.

## 8. Completion check

- [ ] Run and explain the planned experiments, documenting any access limitation.
- [ ] Record useful outputs, internals, comparisons, and failure observations.
- [ ] Answer the interview questions with examples from those experiments.
- [ ] Write key takeaways and revisit the product-relevance decision.
- [ ] Update the module status and commit: `learn(langchain): complete model fundamentals`.
- [ ] Push the checkpoint through GitHub Desktop.

## 9. References and next topic

- [LangChain models](https://docs.langchain.com/oss/python/langchain/models)
- [LangChain installation](https://docs.langchain.com/oss/python/langchain/install)
- Add the selected provider's official SDK documentation when it is chosen.

Next: `02-messages`. Create that topic when model fundamentals are complete.
