# Ask: Did my Pac-Man agent win a class prize?

| | |
|---|---|
| Mode | **ask** (standalone: no chat history, no persona) |
| Execution | **local** — offline-capable local model |
| Model | `mlx-community/gemma-4-e2b-it-4bit` @ `238767527555` (4-bit (MLX)) |
| Runtime | mlx-vlm 0.7.2, mlx 0.32.2, Python 3.12.14, macOS 15.6.1, Apple M4, 16 GB |
| Time | 2026-09-28T15:26:17 |
| Evidence gate | passed |
| Latency / memory | 1.66 s generation, 1798 prompt tokens, 20 generated tokens, peak MLX memory 4.34 GB |

**Question:** Did my Pac-Man agent win a class prize?

## Retrieved passages

**[S1] `vault/raw/Pac-Man DQN README.md` lines 3–16 § Training a Ms. Pac-Man agent with a Deep Q-Network** (BM25 6.93, term coverage 0.67)

> Class 3 assignment. A DQN is trained from raw pixels on `ALE/MsPacman-v5` using the course
> notebook, and evaluated against an untrained network on five fixed seeds under identical settings.
> 
> - **Notebook (executed, with outputs):** [`pacman_dqn.ipynb`](pacman_dqn.ipynb)
> - **Evidence:** [`results/`](results/)
> 
> > **A note for the grader on viewing gameplay in the notebook.** The notebook's own gameplay clips
> > are stored as `image/gif` outputs, and **GitHub's static notebook viewer does not render that MIME
> > type** — it prints `<IPython.core.display.Image object>` instead. I verified this is not a problem
> > with the saved file: the GIF data is present in the `.ipynb`, and `nbconvert --to html` drops it
> > the same way, so it affects any run of this notebook rather than this one specifically. The
> > **scores, the training dashboard, and every printed result do render on GitHub.** All 82 gameplay
> > GIFs are additionally saved as files under [`results/demos/`](results/demos/) and embedded
> > throughout this README, where they display correctly.

**[S2] `vault/raw/Pac-Man DQN README.md` lines 18–29 § Training a Ms. Pac-Man agent with a Deep Q-Network** (BM25 6.03, term coverage 0.50)

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

**[S3] `vault/raw/Pac-Man DQN README.md` lines 303–312 § One limitation** (BM25 6.01, term coverage 0.50)

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

**[S4] `vault/raw/Custom LLM README.md` lines 3–21 § Building a Custom LLM — Class 4** (BM25 2.31, term coverage 0.17)

> Training Karpathy's nanoGPT from scratch on a word-token corpus, measuring it with a fixed
> 48-case language eval suite before and after training across five experiments, and talking to
> the result through a terminal chat interface.
> 
> **The best model here has 230k parameters, a 48-token context, and trained for 38 seconds on
> synthetic sentences.** It is not a chat assistant. It continues sentences in the shapes it was shown.
> Everything below reports what it actually did, including where it failed and where my
> predictions were wrong.
> 
> | | |
> |---|---|
> | Executed notebook, experiment 1 | [`custom_llm_experiment1_starter.ipynb`](custom_llm_experiment1_starter.ipynb) |
> | Executed notebook, experiment 2 | [`custom_llm_experiment2_extended.ipynb`](custom_llm_experiment2_extended.ipynb) |
> | Executed notebook, experiment 3 | [`custom_llm_experiment3_targeted.ipynb`](custom_llm_experiment3_targeted.ipynb) |
> | Executed notebook, experiment 5 | [`custom_llm_experiment5_capacity.ipynb`](custom_llm_experiment5_capacity.ipynb) |
> | Eval suite (unchanged) | [`evals/language_evals.json`](evals/language_evals.json) |
> | Chat evidence | [screenshot](results/chat-screenshot.png) · [session recording](results/chat-session-recording.txt) · [transcript](results/chat-experiment5.json) |
> 
> ---

**[S5] `vault/raw/NetworkTracker README.md` lines 104–114 § Technology Stack** (BM25 2.20, term coverage 0.17)

> | Layer | Choice | Why |
> |---|---|---|
> | Frontend | **React 19 + Vite + TypeScript** | Vite gives near-instant builds and a tiny production bundle; TypeScript catches contract drift between the API client and components at compile time. |
> | Styling | **Tailwind CSS v4** | The brief requires a design system. Tailwind v4 needs no config file, and utility classes keep spacing and colour consistent without a separate stylesheet to drift. |
> | Routing | **React Router v7** | Standard declarative routing; makes the protected-route redirect explicit rather than ad-hoc. |
> | HTTP | **Axios** | A single request interceptor attaches the bearer token to every call, so no component handles auth headers. |
> | Backend | **Node + Express + TypeScript** | The brief requires a separated backend. Express is minimal enough that the request path stays readable, which matters when the security argument depends on it. |
> | Validation | **Zod** | One schema is both the runtime validator and the inferred TypeScript type, so they cannot disagree. |
> | Database | **Neon Postgres** (`@neondatabase/serverless`) | Required by the brief. The HTTP driver suits Vercel's serverless model, where a connection pool cannot be held between invocations. |
> | Auth | **Neon Managed Better Auth** | Required by the brief. Credentials are handled by the hosted service — the app never sees or stores a password. |
> | Testing | **Jest + Supertest** | Fast, zero-config for TypeScript via `ts-jest`. |

## Gemma's answer (verbatim)

> Insufficient evidence: no information is provided regarding whether the Pac-Man agent won a class prize.

## Citation check (automatic)

- Status: **PASS (insufficient-evidence reply; no citations needed)**
