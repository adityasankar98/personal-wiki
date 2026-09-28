# test-3: What hardware and device did I use to train the Pac-Man agent and the custom language model?

| | |
|---|---|
| Mode | **ask** (standalone: no chat history, no persona) |
| Execution | **local** — offline-capable local model |
| Model | `mlx-community/gemma-4-e2b-it-4bit` @ `238767527555` (4-bit (MLX)) |
| Runtime | mlx-vlm 0.7.2, mlx 0.32.2, Python 3.12.14, macOS 15.6.1, Apple M4, 16 GB |
| Time | 2026-09-22T17:43:38 |
| Evidence gate | passed |
| Latency / memory | 2.84 s generation, 2018 prompt tokens, 84 generated tokens, peak MLX memory 4.3 GB |

**Question:** What hardware and device did I use to train the Pac-Man agent and the custom language model?

## Retrieved passages

**[S1] `vault/raw/Pac-Man DQN README.md` lines 273–291 § The run that produced these numbers** (BM25 20.25, term coverage 0.56)

> | | |
> |---|---|
> | Status | completed (not interrupted) |
> | Completed episodes | **2,000 / 2,000** |
> | Total decisions | **1,369,832** (~5.5M emulator frames) |
> | Learning updates | **342,209** |
> | Elapsed training time | **108.5 min** (6,512 s, including periodic demos) |
> | Total notebook wall-clock | 114.0 min (includes baseline eval, 81-checkpoint selection, final eval) |
> | Hardware | Apple M4, 10 cores, 16 GB, macOS 15.6.1 |
> | Device | **MPS** (Apple Silicon GPU) |
> | Python | 3.12.14 |
> | Key packages | torch 2.14.0, gymnasium 1.3.0, ale-py 0.11.2, numpy 2.5.3 |
> 
> Evidence: [`results/training_summary.json`](results/training_summary.json) ·
> [`results/training.csv`](results/training.csv) (one row per episode) ·
> [`results/config.json`](results/config.json) ·
> [`results/comparison.json`](results/comparison.json) ·
> [`results/baseline.json`](results/baseline.json) ·
> [`results/demo_scores.json`](results/demo_scores.json)

**[S2] `vault/raw/Pac-Man DQN README.md` lines 334–338 § Reproducing this exact run** (BM25 12.08, term coverage 0.44)

> Actual run parameters and hardware are in [`results/config.json`](results/config.json); the
> per-episode log is in [`results/training.csv`](results/training.csv).
> 
> Note that exact reproduction is not guaranteed even with the fixed seed: MPS and CUDA kernels
> schedule floating-point work non-deterministically, so a rerun will land near, not on, these numbers.

**[S3] `vault/raw/Custom LLM README.md` lines 182–198 § 3. The experiments > Experiments 3–5 — the follow-ups** (BM25 11.40, term coverage 0.33)

> | | E4 (2 layers) | E5 (4 layers) |
> |---|---|---|
> | Unique passages | 9,704 (train 8,733 / val 971) | 10,520 (train 9,468 / val 1,052) |
> | Vocabulary | 433 | 433 |
> | Parameters | 130,880 | **230,848** |
> | Steps / elapsed | 3,000 / 12 s | 6,000 / 38 s |
> | Unknown-token rate | training 0.0%, held-out 0.009% | training 0.0%, held-out 0.009% |
> | Score | 44/48 | **47/48** |
> 
> E4 was run from the script rather than the notebook, since it is an isolation control; its full
> artifacts (config, corpus, both eval result sets, weights) are in its run folder exactly as for
> the others. E1, E2, E3 and E5 each have an executed notebook.
> 
> Hardware: macOS 15.6.1, Apple Silicon, CPU only. Python 3.12.14, PyTorch 2.14.0. **No run was
> interrupted; every run completed its full step budget** —
> [E1 training_summary.json](llm_runs/20260921T220602_231016Z/training_summary.json) ·
> [E2 training_summary.json](llm_runs/20260921T220633_918630Z/training_summary.json).

**[S4] `vault/raw/Custom LLM README.md` lines 729–750 § 9. Reproducing this > Layout** (BM25 10.73, term coverage 0.44)

> | Path | |
> |---|---|
> | `custom_llm.py` | notebook source; `build_notebook.py` compiles it to `.ipynb` |
> | `build_corpus.py` | generates the extension corpus with the leakage filter |
> | `verify_corpus.py` | read-only pre-flight check (this is the important one) |
> | `corpus/` | teaching material only |
> | `evals/` | the fixed 48-case suite — never a training input |
> | `llm_runs/` | per-run artifacts, weights, eval results, ZIPs |
> | `results/` | standalone eval reruns and chat evidence |
> 
> `run_evals.py`, `chat.py`, `nanogpt_model.py` and `evals/language_evals.json` are supplied and
> **unmodified** — the notebook verifies all four against pinned SHA-256 hashes on every run and
> refuses to start if any byte changed.
> 
> **Attribution.** The transformer is Karpathy's nanoGPT at commit `3adf61e`, used under its MIT
> license, retained verbatim in [`NANOGPT_LICENSE`](NANOGPT_LICENSE). The notebook scaffold, eval
> suite, runner and chat interface come from the course
> [starter repository](https://github.com/pepealonso95/custom-llm). My own contributions are
> `build_corpus.py`, `verify_corpus.py`, the nine files in `corpus/`, the prediction and choices
> in section 1 of the notebook, and this README.
> 
> ---

**[S5] `vault/raw/Custom LLM README.md` lines 3–21 § Building a Custom LLM — Class 4** (BM25 10.34, term coverage 0.44)

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

## Gemma's answer (verbatim)

> Hardware for the Pac-Man agent training was Apple M4 with 10 cores and 16 GB of memory on macOS 15.6.1 [S1]. The device used for the Pac-Man agent was MPS (Apple Silicon GPU) [S1]. For the custom language model experiments, hardware included macOS 15.6.1 and Apple Silicon CPU only [S3].

## Citation check (automatic)

- Status: **PASS**
- Cited: S1 → `vault/raw/Pac-Man DQN README.md:273-291 § The run that produced these numbers`, S3 → `vault/raw/Custom LLM README.md:182-198 § 3. The experiments > Experiments 3–5 — the follow-ups`

## Expected (from tests/questions.json, written before the run)

- `vault/raw/Pac-Man DQN README.md` containing “Apple M4, 10 cores, 16 GB” → **found at rank 1**
- `vault/raw/Custom LLM README.md` containing “Hardware: macOS 15.6.1, Apple Silicon, CPU only” → **found at rank 3**
- Expected facts in answer: M4, CPU

## Automatic assessment

- Retrieval: **PASS**
- Answer: **PASS** — expected facts present, citations valid

## Human assessment (I opened each cited passage)

_Not yet reviewed for this exact answer (answer hash `c08064083dc8`)._
