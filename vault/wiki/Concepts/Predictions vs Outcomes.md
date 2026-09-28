---
type: "concept"
description: "Writing down what you expect before an experiment, then reporting where it was wrong."
sources:
  - "[[Pac-Man DQN README]]"
  - "[[Custom LLM README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Predictions vs Outcomes

*Writing down what you expect before an experiment, then reporting where it was wrong.*

The expected modest, noisy improvement in the Pac-Man DQN training was incorrect because the mean went from 492.0 to 1360.0, and every one of the five evaluation games improved, which was stronger evidence than the mean alone ([[Pac-Man DQN README#What I expected, and what actually happened|S1]]). A prediction regarding a new wording regression was wrong because the extra data taught general function-word structure that transferred back to starter templates rather than competing with them for capacity ([[Custom LLM README#2. Where my predictions were wrong|S2]]). In a custom LLM experiment, the coverage went to 48/48 as predicted, and starter patterns improved dramatically because hundreds of sibling sentences taught domain associations ([[Custom LLM README#2. Where my predictions were wrong|S3]]). Another wrong prediction involved scorable accuracy, which rose from 83.3% to 91.7% instead of falling as expected ([[Custom LLM README#2. Where my predictions were wrong|S3]]).

## Where it appears

- [[Custom LLM Training]] — Three confident, specific wrong predictions are more informative than a vague one that cannot fail.
- [[Pac-Man DQN Agent]] — Expected modest improvement, but the actual improvement was significant and consistent across all evaluation games.

## Related notes

- [[Held-Out Evaluation]] — predictions are only meaningful when checked on untouched data

## Sources

- [S1] [[Pac-Man DQN README#What I expected, and what actually happened|Pac-Man DQN README § What I expected, and what actually happened]], lines 140–151
- [S2] [[Custom LLM README#2. Where my predictions were wrong|Custom LLM README § 2. Where my predictions were wrong]], lines 128–136
- [S3] [[Custom LLM README#2. Where my predictions were wrong|Custom LLM README § 2. Where my predictions were wrong]], lines 101–115
- [S4] [[Pac-Man DQN README#What I expected, and what actually happened|Pac-Man DQN README § What I expected, and what actually happened]], lines 239–241
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
