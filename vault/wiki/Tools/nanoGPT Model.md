---
type: "concept"
description: "Karpathy's minimal GPT transformer, trained from scratch on a word-token corpus."
sources:
  - "[[Custom LLM README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "tools"
---

# nanoGPT Model

*Karpathy's minimal GPT transformer, trained from scratch on a word-token corpus.*

The project involves training Karpathy's nanoGPT from scratch on a word-token corpus ([[Custom LLM README#Building a Custom LLM — Class 4|S2]]). The best model has 230k parameters, a 48-token context, and was trained for 38 seconds on synthetic sentences ([[Custom LLM README#Building a Custom LLM — Class 4|S2]]). The model continues sentences in the shapes it was shown and is not a chat assistant ([[Custom LLM README#Building a Custom LLM — Class 4|S2]]).

## Where it appears

- [[Custom LLM Training]] — The transformer is Karpathy's nanoGPT at commit 3adf61e, used under its MIT license.

## Related notes

- [[Model Capacity]] — its layer count was the capacity experiment
- [[Word Embeddings]] — its embedding table is what the neighbour analysis inspects

## Sources

- [S1] [[Custom LLM README#9. Reproducing this|Custom LLM README § 9. Reproducing this]], lines 729–750
- [S2] [[Custom LLM README#Building a Custom LLM — Class 4|Custom LLM README § Building a Custom LLM — Class 4]], lines 3–21
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
