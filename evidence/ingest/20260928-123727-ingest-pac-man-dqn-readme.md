# Ingest run

```

== vault/raw/Pac-Man DQN README.md  (2996 words; sha256 795c15897638)
   section “Training a Ms. Pac-Man agent with a Deep Q-Network”: 3 point(s)
   section “How to open and run it”: 3 point(s)
   section “My three choices”: 3 point(s)
   section “What the agent actually sees, does, and is paid for”: 3 point(s)
   section “What I expected, and what actually happened”: 3 point(s)
   section “The run that produced these numbers”: 3 point(s)
   section “One limitation”: 3 point(s)
   section “My next experiment”: 3 point(s)
   section “Reproducing this exact run”: 3 point(s)
   section “Where the large files are”: 3 point(s)
   linked concepts: Deep Q-Network, Experience Replay, Reward Clipping, Exploration Rate, Held-Out Evaluation, Predictions vs Outcomes, Apple Silicon Training
   applied review correction: misleading: bias comes from choosing the max of 81 noisy estimates, not from held-out seeds (source lines 263-266)
   applied review correction: misleading: the source says the loss IS a temporal-difference error, which is why a rising loss is not a bad sign (lines 153-159)
   applied review correction: garbled menu path (lines 36-37)
   applied review correction: the proposal is an annealing schedule, stated as a next experiment (lines 316-317)
   applied review correction: it is the README's prediction, not a test result (lines 326-329)
   applied review correction: the next experiment is a proposal, not something that was done (lines 316-317)
   applied review correction: vague: which seeds (lines 265-266)
   -> updated: vault/wiki/Projects/Pac-Man DQN Agent.md

== concept notes
   applied review correction: misleading: the source says the loss IS a temporal-difference error, which is why a rising loss is not a bad sign (lines 153-159)
   -> unchanged: vault/wiki/Concepts/Deep Q-Network.md
   applied review correction: off-topic: these two sentences are about exploration, not replay (they belong to Exploration Rate)
   -> unchanged: vault/wiki/Concepts/Experience Replay.md
   -> unchanged: vault/wiki/Concepts/Reward Clipping.md
   applied review correction: the next experiment is a proposal, not something that was done (lines 316-317)
   applied review correction: states a proposed experiment as if done; garbled clause about the 0.20 default (lines 62-67, 316-317)
   applied review correction: garbled clause about the 0.20 default (lines 62-65)
   -> unchanged: vault/wiki/Concepts/Exploration Rate.md
   applied review correction: vague: which seeds (lines 265-266)
   applied review correction: the checks keep eval prompts out of the corpus; the suite does not 'include' them (lines 298-312)
   -> unchanged: vault/wiki/Concepts/Held-Out Evaluation.md
   -> unchanged: vault/wiki/Concepts/Predictions vs Outcomes.md
   -> unchanged: vault/wiki/Tools/Apple Silicon Training.md

ingest done in 45.2 s · 26 Gemma calls (40.6 s generating) · notes: {'created': 0, 'updated': 1, 'unchanged': 7} · new files: 0 · wiki notes before/after: 17/17 · index: 253 passages · peak memory 2.41 GB RSS
```
