---
type: "concept"
description: "How much a model can represent, set by its layers and parameters."
sources:
  - "[[Custom LLM README]]"
  - "[[Pac-Man DQN README]]"
  - "[[NetworkTracker README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Model Capacity

*How much a model can represent, set by its layers and parameters.*

After E2, the README hypothesised that the model used a single copy mechanism for two incompatible jobs: copying a name across a clause boundary correctly while copying a category across the same frame incorrectly ([[Custom LLM README#10. Limitation and next experiment|S1]]). Fixing the issue at two layers cost three cases elsewhere, indicating that the ceiling was capacity ([[Custom LLM README#1. Headline results|S2]]). Doubling the depth cleared the issue to 47/48 and unexpectedly changed the embedding geometry ([[Custom LLM README#10. Limitation and next experiment|S1]]).

## Where it appears

- [[Custom LLM Training]] — The immediate cause of a language error was a missing frame, not capacity, but fixing it at two layers cost cases, indicating a capacity ceiling.

## Related notes

- [[Word Embeddings]] — extra capacity changed the embedding geometry, not just the score
- [[nanoGPT Model]] — the architecture whose depth was varied

## Sources

- [S1] [[Custom LLM README#10. Limitation and next experiment|Custom LLM README § 10. Limitation and next experiment]], lines 754–765
- [S2] [[Custom LLM README#1. Headline results|Custom LLM README § 1. Headline results]], lines 47–57
- [S3] [[Pac-Man DQN README#My next experiment|Pac-Man DQN README § My next experiment]], lines 316–329
- [S4] [[NetworkTracker README#Security Authentication and RLS Ownership|NetworkTracker README § Security: Authentication and RLS Ownership]], lines 277–291
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
