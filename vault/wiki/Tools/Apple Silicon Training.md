---
type: "concept"
description: "Training on an Apple M4 laptop: MPS GPU for the DQN, CPU for the tiny LLM."
sources:
  - "[[Pac-Man DQN README]]"
  - "[[Custom LLM README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "tools"
---

# Apple Silicon Training

*Training on an Apple M4 laptop: MPS GPU for the DQN, CPU for the tiny LLM.*

The run produced 2,000 completed episodes out of 2,000 episodes ([[Pac-Man DQN README#The run that produced these numbers|S1]]). The training involved 1,369,832 total decisions and 342,209 learning updates ([[Pac-Man DQN README#The run that produced these numbers|S1]]). This training utilized hardware including Apple M4, 10 cores, 16 GB, and macOS 15.6.1, with the MPS (Apple Silicon GPU) being the device ([[Pac-Man DQN README#The run that produced these numbers|S1]]).

## Where it appears

- [[Custom LLM Training]] — Apple Silicon CPU only hardware was used for the experiments.
- [[Pac-Man DQN Agent]] — The run completed with 2,000 episodes, using Apple M4 hardware and MPS for training.

## Related notes

- [[Deep Q-Network]] — the model trained on the M4's GPU
- [[nanoGPT Model]] — the model trained on the M4's CPU

## Sources

- [S1] [[Pac-Man DQN README#The run that produced these numbers|Pac-Man DQN README § The run that produced these numbers]], lines 273–291
- [S2] [[Custom LLM README#3. The experiments|Custom LLM README § 3. The experiments]], lines 182–198
- [S3] [[Pac-Man DQN README#How to open and run it|Pac-Man DQN README § How to open and run it]], lines 33–50
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
