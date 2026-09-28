# Search: reward clipping

Mode: **search** (no model, no generated answer) · retrieval: BM25 · scope: raw · 2026-09-28T15:25:55

**[S1] `vault/raw/Pac-Man DQN README.md` lines 303–312 § One limitation** (BM25 7.20, term coverage 1.00)

> The direct cause is in the code: **training rewards are clipped to [−1, +1]**. To the gradient, a
> 10-point pellet and a 1,600-point ghost chain are the same size. The agent is therefore never taught
> that ghosts are worth two orders of magnitude more than pellets — reward clipping stabilises
> training at the cost of making the agent value-blind to exactly the tactic that separates a good
> Ms. Pac-Man player from a mediocre one.
> 
> A second, structural limitation worth naming: **five evaluation games is a very small sample.** The
> same agent scored between 360 and 2,250 on single games during training. Five games with fixed seeds
> makes runs comparable, but it is not a reliable estimate of true skill, and the ±868 gain should be
> read as "clearly improved," not as a precise measurement.

**[S2] `vault/raw/Pac-Man DQN README.md` lines 129–136 § What the agent actually sees, does, and is paid for** (BM25 7.01, term coverage 1.00)

> **Rewards — game points.** The reward is whatever the game's own scoreboard awards: pellets, power
> pellets, eaten ghosts, fruit. Two details matter. For *learning*, rewards are clipped to [−1, +1],
> so a 200-point ghost and a 10-point pellet look the same size to the gradient — this keeps the
> update scale stable across games but means the agent is not taught that ghosts are worth twenty
> pellets. For *reporting*, every score in this README is the raw, unclipped game score.
> 
> The agent is never told the rules. It is not told what a ghost is, that pellets are good, or that
> touching a ghost ends a life. All of that has to be inferred from pixels and points.

**[S3] `vault/raw/Pac-Man DQN README.md` lines 86–92 § My three choices > Learning rate — 0.00025** (BM25 2.70, term coverage 0.50)

> 0.00025 is the rate used in the original DQN work, and is 2.5× the notebook's reference value. The
> argument for the larger step is the update budget: this run performs on the order of 10^5 gradient
> updates, not the 10^7 the method was designed around, so each update has to carry more weight.
> 
> The risk of a larger step is divergence, but the notebook already mitigates it: Huber
> (`smooth_l1_loss`) instead of squared error, gradient-norm clipping at 10.0, a target network synced
> every 1,000 decisions, and an explicit error if the loss ever becomes non-finite.
