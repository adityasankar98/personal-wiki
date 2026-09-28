---
type: "concept"
description: "Storing past transitions and training on random samples of them."
sources:
  - "[[Pac-Man DQN README]]"
  - "[[Custom LLM README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Experience Replay

*Storing past transitions and training on random samples of them.*

The replay capacity was changed from 5,000 to 50,000 ([[Pac-Man DQN README#My three choices|S1]]). This change resulted in a difference in sample time, with 50,000 taking 0.53 ms versus 0.19 ms at 5,000, which is about one extra minute per 100,000 updates ([[Pac-Man DQN README#My three choices|S1]]). The shipped 5,000-transition buffer held only about eight games, so sampled batches came from a handful of highly correlated recent episodes; 50,000 holds about 80 games ([[Pac-Man DQN README#My three choices|S1]]).

## Where it appears

- [[Pac-Man DQN Agent]] — The replay buffer was increased from 5,000 to 50,000 transitions to break correlation.

## Related notes

- [[Deep Q-Network]] — the learner that samples from the buffer
- [[Exploration Rate]] — exploration decides what kind of experience fills the buffer

## Sources

- [S1] [[Pac-Man DQN README#My three choices|Pac-Man DQN README § My three choices]], lines 96–111
- [S2] [[Pac-Man DQN README#My next experiment|Pac-Man DQN README § My next experiment]], lines 316–329
- [S3] [[Custom LLM README#7. How it learns — traced through actual numbers|Custom LLM README § 7. How it learns — traced through actual numbers]], lines 533–544
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
