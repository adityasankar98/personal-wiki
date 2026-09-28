---
type: "concept"
description: "The share of random actions (epsilon) an agent takes while it learns."
sources:
  - "[[Pac-Man DQN README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Exploration Rate

*The share of random actions (epsilon) an agent takes while it learns.*

The proposed next experiment would make exploration decay instead of holding it constant, annealing epsilon from 1.0 to 0.05 over the first ~200,000 decisions instead of fixing it at 0.10 ([[Pac-Man DQN README#My next experiment|S1]]). Exploration in this notebook is constant after 1,000 warm-up decisions, so at the default of 0.20 one move in five stays random for the whole run ([[Pac-Man DQN README#My three choices|S2]]). Halving exploration to 0.10 keeps enough randomness to reach states the greedy policy would never visit while letting the learned policy express itself in the collected experience and training score ([[Pac-Man DQN README#My three choices|S2]]).

## Where it appears

- [[Pac-Man DQN Agent]] — Exploration was held constant at 0.10; the proposed next experiment anneals it from 1.0 to 0.05 over ~200,000 decisions.

## Related notes

- [[Deep Q-Network]] — the agent whose actions are randomised
- [[Experience Replay]] — random actions shape the stored experience

## Sources

- [S1] [[Pac-Man DQN README#My next experiment|Pac-Man DQN README § My next experiment]], lines 316–329
- [S2] [[Pac-Man DQN README#My three choices|Pac-Man DQN README § My three choices]], lines 62–71
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
