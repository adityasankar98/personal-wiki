# test-4: What grade did I receive for the Pac-Man assignment?

| | |
|---|---|
| Mode | **ask** (standalone: no chat history, no persona) |
| Execution | **local** — offline-capable local model |
| Model | `mlx-community/gemma-4-e2b-it-4bit` @ `238767527555` (4-bit (MLX)) |
| Runtime | mlx-vlm 0.7.2, mlx 0.32.2, Python 3.12.14, macOS 15.6.1, Apple M4, 16 GB |
| Time | 2026-09-28T15:25:54 |
| Evidence gate | passed |
| Latency / memory | 1.02 s generation, 1263 prompt tokens, 20 generated tokens, peak MLX memory 4.32 GB |

**Question:** What grade did I receive for the Pac-Man assignment?

## Retrieved passages

**[S1] `vault/raw/Custom LLM README.md` lines 128–136 § 2. Where my predictions were wrong** (BM25 8.32, term coverage 0.40)

> **Wrong #3 — I predicted a `new_wording` regression** from extension material consuming ~49% of
> training batches and halving classroom exposure. Instead `new_wording` went 4/8 → 8/8. The
> extra data appears to have taught general function-word structure that transferred back to the
> starter templates, rather than competing with them for capacity.
> 
> I am reporting these because the assignment grades prediction against observation, and three
> confident, specific, wrong predictions are more informative than a vague one that cannot fail.
> 
> ---

**[S2] `vault/raw/Pac-Man DQN README.md` lines 342–345 § Where the large files are** (BM25 8.13, term coverage 0.60)

> Model checkpoints (`untrained.pt`, `episode_*.pt`, `trained.pt`, ~6.8 MB each) are **not** committed,
> to keep the repository small. They are kept locally in the run's ZIP archive alongside the
> `pacman_runs/<timestamp>/` folder produced by the notebook. Everything needed to grade the
> experiment — settings, logs, plots, GIFs, and all evaluation scores — is in [`results/`](results/).

**[S3] `vault/raw/Pac-Man DQN README.md` lines 153–159 § What I expected, and what actually happened** (BM25 5.84, term coverage 0.60)

> And the loss went **up**, not down — from about 0.03 early to a plateau around 0.15 — during exactly
> the period when play was improving fastest. This is the assignment's warning made concrete. The loss
> here is a *temporal-difference error*, not a distance from ground truth. As the agent learns to
> survive and collect more, the true value of its states genuinely rises, the target network keeps
> being refreshed to a stronger network, and so the quantity being minimised is itself growing. A
> falling loss in this setup could just as easily have meant the agent had settled into a dull,
> predictable policy. **The loss panel is the least informative of the three.**

**[S4] `vault/raw/Pac-Man DQN README.md` lines 3–16 § Training a Ms. Pac-Man agent with a Deep Q-Network** (BM25 5.40, term coverage 0.60)

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

**[S5] `vault/raw/Custom LLM README.md` lines 719–725 § 9. Reproducing this** (BM25 3.81, term coverage 0.20)

> **Scoring rules** (unchanged from the supplied runner): the model sees only the prompt — never
> the four choices, never the answer key. It scores 1 when the correct word receives the highest
> next-token probability among the four choices, 0 otherwise. Ties score 0. Cases with any
> unknown prompt or choice word, or an over-long context, are `out_of_vocabulary` /
> `context_too_long`, score 0 in the all-case rate, and are excluded from scorable accuracy and
> coverage. A free continuation is generated and saved separately for every case and is **not**
> what the score measures.

## Gemma's answer (verbatim)

> Insufficient evidence: the passages do not state what grade was received for the Pac-Man assignment.

## Citation check (automatic)

- Status: **PASS (insufficient-evidence reply; no citations needed)**

## Expected (from tests/questions.json, written before the run)

- Expected behaviour: an explicit insufficient-evidence statement

## Automatic assessment

- Retrieval: **PASS**
- Answer: **PASS** — expected an insufficient-evidence reply: got one

## Human assessment (I opened each cited passage)

**PASS: correct refusal.** None of the five retrieved passages mentions a grade received. S1 contains the word “grades” in a different sense (“the assignment grades prediction against observation”), a plausible trap for keyword matching, and the model was not misled. The evidence gate did not block this question, because “Pac-Man assignment” matches real passages (as predicted), so the refusal came from the model following rule 4 of `wiki-instructions.md`. My prediction that this test would fail first time was wrong.
