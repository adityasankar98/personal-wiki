# Ask: What mean score did the trained Ms. Pac-Man agent get on the five evaluation seeds, compared with the untrained agent?

| | |
|---|---|
| Mode | **ask** (standalone: no chat history, no persona) |
| Execution | **local** — offline-capable local model |
| Model | `mlx-community/gemma-4-e2b-it-4bit` @ `238767527555` (4-bit (MLX)) |
| Runtime | mlx-vlm 0.7.2, mlx 0.32.2, Python 3.12.14, macOS 15.6.1, Apple M4, 16 GB |
| Time | 2026-09-28T12:36:28 |
| Evidence gate | passed |
| Latency / memory | 1.94 s generation, 1106 prompt tokens, 51 generated tokens, peak MLX memory 4.2 GB |

**Question:** What mean score did the trained Ms. Pac-Man agent get on the five evaluation seeds, compared with the untrained agent?

## Retrieved passages

**[S1] `vault/raw/Pac-Man DQN README.md` lines 18–29 § Training a Ms. Pac-Man agent with a Deep Q-Network** (BM25 32.67, term coverage 0.92)

> **Result: mean score over five fixed evaluation seeds went from 492.0 (untrained) to 1360.0
> (trained) — a gain of +868.0, or +176%. All five games improved.**
> 
> | | Untrained | Trained |
> |---|---|---|
> | Mean over 5 seeds | 492.0 | **1360.0** |
> 
> | Untrained agent | Best trained game |
> |---|---|
> | ![untrained gameplay](results/demos/episode_0000.gif) | ![trained gameplay](results/demos/final_best.gif) |
> 
> *Both clips are the first 20 seconds of game time at 4× playback.*

**[S2] `vault/raw/Pac-Man DQN README.md` lines 163–176 § What I expected, and what actually happened > All five evaluation scores** (BM25 23.78, term coverage 0.83)

> Same five seeds, 5% exploration, same 3,000-decision cap, before and after. The baseline is an
> untrained network, not a random-action agent. Full data: [`results/comparison.json`](results/comparison.json).
> 
> | Game | Seed | Before (untrained) | After (trained) | Change |
> |---|---|---|---|---|
> | 1 | 101 | 350 | **1400** | +1050 |
> | 2 | 202 | 500 | **1740** | +1240 |
> | 3 | 303 | 320 | **1240** | +920 |
> | 4 | 404 | 800 | **1510** | +710 |
> | 5 | 505 | 490 | **910** | +420 |
> | **Mean** | | **492.0** | **1360.0** | **+868.0** |
> 
> The agent also survived longer: mean game length rose from 589 to 764 decisions. No game hit the
> 3,000-decision time limit in either condition, so every score is a real game-over, not a truncation.

**[S3] `vault/raw/Pac-Man DQN README.md` lines 303–312 § One limitation** (BM25 19.16, term coverage 0.67)

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

## Gemma's answer (verbatim)

> The mean score for the trained Ms. Pac-Man agent was 1360.0, which was an improvement of +868.0 over the untrained score of 492.0 [S1][S2].

## Citation check (automatic)

- Status: **PASS**
- Cited: S1 → `vault/raw/Pac-Man DQN README.md:18-29 § Training a Ms. Pac-Man agent with a Deep Q-Network`, S2 → `vault/raw/Pac-Man DQN README.md:163-176 § What I expected, and what actually happened > All five evaluation scores`
