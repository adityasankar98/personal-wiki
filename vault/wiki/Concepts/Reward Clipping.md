---
type: "concept"
description: "Squashing rewards to [-1, +1] for stable learning, at the cost of their relative size."
sources:
  - "[[Pac-Man DQN README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Reward Clipping

*Squashing rewards to [-1, +1] for stable learning, at the cost of their relative size.*

Rewards are game points. For learning, rewards are clipped to [-1, +1], which means a 200-point ghost and a 10-point pellet look the same size to the gradient ([[Pac-Man DQN README#What the agent actually sees, does, and is paid for|S1]]). This clipping keeps the update scale stable across games but means the agent is not taught that ghosts are worth twenty pellets ([[Pac-Man DQN README#One limitation|S2]]).

## Where it appears

- [[Pac-Man DQN Agent]] — Rewards are clipped to [-1, +1] for learning, while reporting uses the raw, unclipped game score.

## Related notes

- [[Deep Q-Network]] — clipping changes what the network is taught to value

## Sources

- [S1] [[Pac-Man DQN README#What the agent actually sees, does, and is paid for|Pac-Man DQN README § What the agent actually sees, does, and is paid for]], lines 129–136
- [S2] [[Pac-Man DQN README#One limitation|Pac-Man DQN README § One limitation]], lines 303–312
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
