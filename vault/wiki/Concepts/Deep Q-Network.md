---
type: "concept"
description: "A neural network that estimates the future reward of each action from game screens."
sources:
  - "[[Pac-Man DQN README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Deep Q-Network

*A neural network that estimates the future reward of each action from game screens.*

The loss went up during the period when play was improving fastest, which is the assignment's warning made concrete ([[Pac-Man DQN README#What I expected, and what actually happened|S1]]). The loss is a temporal-difference error, not a distance from ground truth ([[Pac-Man DQN README#What I expected, and what actually happened|S1]]). A falling loss could also mean the agent settled into a dull, predictable policy ([[Pac-Man DQN README#What I expected, and what actually happened|S1]]). The loss panel is the least informative of the three ([[Pac-Man DQN README#What I expected, and what actually happened|S1]]). The learning rate used is 0.00025, which is 2.5 times the notebook's reference value ([[Pac-Man DQN README#My three choices|S2]]). This larger step is justified because the run performs on the order of 10^5 gradient updates, not the 10^7 the method was designed around, requiring each update to carry more weight ([[Pac-Man DQN README#My three choices|S2]]).

## Where it appears

- [[Pac-Man DQN Agent]] — The loss went up during the fastest improvement period; because it is a temporal-difference error whose targets rise as the agent improves, that is not a bad sign, not distance from ground truth.

## Related notes

- [[Experience Replay]] — the buffer a DQN learns from
- [[Reward Clipping]] — how game points are rescaled before a DQN learns from them
- [[Exploration Rate]] — how often a DQN acts randomly instead of greedily

## Sources

- [S1] [[Pac-Man DQN README#What I expected, and what actually happened|Pac-Man DQN README § What I expected, and what actually happened]], lines 153–159
- [S2] [[Pac-Man DQN README#My three choices|Pac-Man DQN README § My three choices]], lines 86–92
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
