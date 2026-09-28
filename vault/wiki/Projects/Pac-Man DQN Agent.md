---
type: "project"
description: "DQN trained from raw pixels on ALE/MsPacman-v5"
source_id: "795c15897638"
source_file: "[[Pac-Man DQN README]]"
source_path: "vault/raw/Pac-Man DQN README.md"
original_filename: "Pac-Man DQN README.md"
origin: "github.com/adityasankar98/pacman-dqn-class3 (README.md)"
sha256: "795c15897638aa468b4b47eb0c79e3ced9393015dc330e1b81cb754ee1c8ad4c"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
generated_at: "2026-09-28T15:57:58"
reviewed: true
visibility: "public"
tags:
  - "projects"
---

# Pac-Man DQN Agent

A DQN was trained from raw pixels on ALE/MsPacman-v5 using the course notebook. The mean score improved from 492.0 untrained to 1360.0 trained across five games. The training involved 342,209 learning updates over 108.5 minutes.

## Key points

### Training a Ms. Pac-Man agent with a Deep Q-Network

Source: [[Pac-Man DQN README|Pac-Man DQN README § Training a Ms. Pac-Man agent with a Deep Q-Network]], lines 3–29

- A DQN was trained from raw pixels on ALE/MsPacman-v5 using the course notebook.
- The mean score improved from 492.0 untrained to 1360.0 trained.
- All five games showed improvement after training.

### How to open and run it

Source: [[Pac-Man DQN README#How to open and run it|Pac-Man DQN README § How to open and run it]], lines 33–50

- In Google Colab, select Runtime → Change runtime type → T4 GPU, then Runtime → Run all.
- Local setup involves cloning a git repository, creating a virtual environment, and installing requirements.
- Selecting a Python 3.11–3.13 kernel and Run All detects CUDA, Apple MPS, and CPU automatically.

### My three choices

Source: [[Pac-Man DQN README#My three choices|Pac-Man DQN README § My three choices]], lines 54–114

- Exploration is constant after 1,000 warm-up decisions.
- 2,000 episodes involve about 1.2M agent decisions.
- The learning rate is 2.5 times the notebook's reference value.

### What the agent actually sees, does, and is paid for

Source: [[Pac-Man DQN README#What the agent actually sees, does, and is paid for|Pac-Man DQN README § What the agent actually sees, does, and is paid for]], lines 118–136

- Observations are four game screens cropped and shrunk to an 84x84 grayscale image.
- Actions are nine discrete joystick movements, including NOOP, UP, RIGHT, LEFT, DOWN, UPRIGHT, UPLEFT, DOWNRIGHT, and DOWNLEFT.
- Rewards are game points, which are clipped to [-1, +1] for learning purposes.

### What I expected, and what actually happened

Source: [[Pac-Man DQN README#What I expected, and what actually happened|Pac-Man DQN README § What I expected, and what actually happened]], lines 140–269

- The mean score improved from 492.0 to 1360.0 across five evaluation games.
- The loss went up during the fastest improvement period; because it is a temporal-difference error whose targets rise as the agent improves, that is not a bad sign.
- The selected checkpoint's held-out mean of 1660.0 is optimistically biased because it is the best of 81 noisy estimates; the reported 1360.0 is unbiased because its seeds were never used to choose.

### The run that produced these numbers

Source: [[Pac-Man DQN README#The run that produced these numbers|Pac-Man DQN README § The run that produced these numbers]], lines 273–291

- The run was completed without interruption.
- Total decisions were 1,369,832, which is approximately 5.5M emulator frames.
- The training involved 342,209 learning updates over 108.5 minutes.

### One limitation

Source: [[Pac-Man DQN README#One limitation|Pac-Man DQN README § One limitation]], lines 295–312

- The agent learned to eat pellets and avoid ghosts reactively.
- Training rewards are clipped to [−1, +1], making a 10-point pellet and a 1,600-point ghost chain the same size to the gradient.
- Five evaluation games is a very small sample, and the gain should be read as clearly improved.

### My next experiment

Source: [[Pac-Man DQN README#My next experiment|Pac-Man DQN README § My next experiment]], lines 316–329

- The proposed next experiment anneals exploration from 1.0 to 0.05 over the first ~200,000 decisions instead of fixing it at 0.10.
- A constant 0.10 is a compromise that is wrong at both ends of training.
- The README predicts the change would show up as a higher ceiling rather than faster early progress.

### Reproducing this exact run

Source: [[Pac-Man DQN README#Reproducing this exact run|Pac-Man DQN README § Reproducing this exact run]], lines 334–338

- Actual run parameters and hardware are in results/config.json.
- The per-episode log is in results/training.csv.
- Exact reproduction is not guaranteed due to non-deterministic floating-point scheduling.

### Where the large files are

Source: [[Pac-Man DQN README#Where the large files are|Pac-Man DQN README § Where the large files are]], lines 342–345

- Model checkpoints are not committed to keep the repository small.
- Checkpoints are kept locally in the run's ZIP archive with the pacman_runs/(timestamp)/ folder.
- Everything needed for grading is in the results/ folder.

## Related notes

- [[Apple Silicon Training]] — The run completed with 2,000 episodes, using Apple M4 hardware and MPS for training.
- [[Deep Q-Network]] — The loss went up during the fastest improvement period; because it is a temporal-difference error whose targets rise as the agent improves, that is not a bad sign, not distance from ground truth.
- [[Experience Replay]] — The replay buffer was increased from 5,000 to 50,000 transitions to break correlation.
- [[Exploration Rate]] — Exploration was held constant at 0.10; the proposed next experiment anneals it from 1.0 to 0.05 over ~200,000 decisions.
- [[Held-Out Evaluation]] — The held-out figure of 1660.0 is optimistically biased, while the reported 1360.0 is not, because its evaluation seeds were never used to choose the checkpoint.
- [[Predictions vs Outcomes]] — Expected modest improvement, but the actual improvement was significant and consistent across all evaluation games.
- [[Reward Clipping]] — Rewards are clipped to [-1, +1] for learning, while reporting uses the raw, unclipped game score.

## Sources

- Original: [[Pac-Man DQN README]] (`vault/raw/Pac-Man DQN README.md`, sha256 `795c15897638`)
- Catalog entry: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
