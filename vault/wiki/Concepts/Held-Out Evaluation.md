---
type: "concept"
description: "Keeping test data separate from anything used to train, tune or choose a model."
sources:
  - "[[Custom LLM README]]"
  - "[[Pac-Man DQN README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Held-Out Evaluation

*Keeping test data separate from anything used to train, tune or choose a model.*

The eval suite is the exam, and the corpus is the study material ([[Custom LLM README#5. Keeping the exam out of the textbook|S2]]). Four independent checks keep the eval prompts out of the training corpus ([[Custom LLM README#5. Keeping the exam out of the textbook|S2]]). The suite is a development benchmark that guided the corpus design, so no numbers support a claim about unseen generalization ([[Custom LLM README#5. Keeping the exam out of the textbook|S1]]).

## Where it appears

- [[Custom LLM Training]] — The suite is a development benchmark that guided corpus design, so numbers do not support claims about unseen generalization.
- [[Pac-Man DQN Agent]] — The held-out figure of 1660.0 is optimistically biased, while the reported 1360.0 is not, because its evaluation seeds were never used to choose the checkpoint.

## Related notes

- [[Predictions vs Outcomes]] — an honest test is what makes a prediction checkable

## Sources

- [S1] [[Custom LLM README#5. Keeping the exam out of the textbook|Custom LLM README § 5. Keeping the exam out of the textbook]], lines 314–325
- [S2] [[Custom LLM README#5. Keeping the exam out of the textbook|Custom LLM README § 5. Keeping the exam out of the textbook]], lines 298–312
- [S3] [[Pac-Man DQN README#What I expected, and what actually happened|Pac-Man DQN README § What I expected, and what actually happened]], lines 245–261
- [S4] [[Pac-Man DQN README#What I expected, and what actually happened|Pac-Man DQN README § What I expected, and what actually happened]], lines 263–269
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
