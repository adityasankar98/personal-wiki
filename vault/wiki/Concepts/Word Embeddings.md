---
type: "concept"
description: "Learned vectors for each token; similar words end up with nearby vectors."
sources:
  - "[[Custom LLM README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Word Embeddings

*Learned vectors for each token; similar words end up with nearby vectors.*

Each word ID indexes a row of a 64-number embedding table that moves only through training ([[Custom LLM README#7. How it learns — traced through actual numbers|S1]]). After training, customer's nearest neighbours were exactly the role nouns it shares frames with (client, buyer, shopper, subscriber, consumer, cosine > 0.96), because those words appear in the same slots ([[Custom LLM README#7. How it learns — traced through actual numbers|S1]]). In the 4-layer model, hot's nearest neighbour changed from slot-mates such as rough and smooth to its antonym cold ([[Custom LLM README#7. How it learns — traced through actual numbers|S2]]).

## Where it appears

- [[Custom LLM Training]] — Embedding neighbors moved toward role nouns after training, showing that words appearing in the same slots cluster together.

## Related notes

- [[Model Capacity]] — a deeper model grouped antonyms together

## Sources

- [S1] [[Custom LLM README#7. How it learns — traced through actual numbers|Custom LLM README § 7. How it learns — traced through actual numbers]], lines 503–517
- [S2] [[Custom LLM README#7. How it learns — traced through actual numbers|Custom LLM README § 7. How it learns — traced through actual numbers]], lines 533–544
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
