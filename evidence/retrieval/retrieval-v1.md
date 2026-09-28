# Retrieval check v1 — BM25 only, no synonyms, no per-source cap

Run before ask mode existed. EXPECTED marks the passage named in tests/questions.json.

## test-1: What mean score did the trained Ms. Pac-Man agent get on the five evaluation seeds, compared with the untrained agent?

| rank | score | coverage | expected? | passage |
|---|---|---|---|---|
| 1 | 31.48 | 0.92 | **yes** | `vault/raw/Pac-Man DQN README.md:18-29 § Training a Ms. Pac-Man agent with a Deep Q-Network` |
| 2 | 23.37 | 0.83 |  | `vault/raw/Pac-Man DQN README.md:163-176 § What I expected, and what actually happened > All five evaluation scores` |
| 3 | 20.10 | 0.67 |  | `vault/raw/Pac-Man DQN README.md:303-312 § One limitation` |
| 4 | 17.30 | 0.75 |  | `vault/raw/Pac-Man DQN README.md:3-16 § Training a Ms. Pac-Man agent with a Deep Q-Network` |
| 5 | 15.50 | 0.58 |  | `vault/raw/Pac-Man DQN README.md:140-151 § What I expected, and what actually happened` |
| 6 | 14.82 | 0.67 |  | `vault/raw/Pac-Man DQN README.md:201-216 § What I expected, and what actually happened > Gameplay through training` |
| 7 | 14.76 | 0.67 |  | `vault/raw/Pac-Man DQN README.md:62-71 § My three choices > Exploration — 0.10` |
| 8 | 13.06 | 0.50 |  | `vault/raw/Pac-Man DQN README.md:245-261 § What I expected, and what actually happened > Which network was reported, and why` |

## test-2: Why was one signed-in user of my networking app initially able to see and delete another person's contacts?

| rank | score | coverage | expected? | passage |
|---|---|---|---|---|
| 1 | 23.25 | 0.75 |  | `vault/raw/NetworkTracker README.md:3-13 § NetworkTracker — Secure Networking Tracker` |
| 2 | 17.93 | 0.50 |  | `vault/raw/NetworkTracker README.md:293-313 § Security: Authentication and RLS Ownership > The ownership rule` |
| 3 | 17.89 | 0.58 | **yes** | `vault/raw/NetworkTracker README.md:317-332 § Security: Authentication and RLS Ownership > The `app_user` role — why RLS needs it` |
| 4 | 15.98 | 0.42 |  | `vault/raw/NetworkTracker README.md:63-81 § Walkthrough > Two-account isolation` |
| 5 | 15.90 | 0.50 |  | `vault/raw/NetworkTracker README.md:277-291 § Security: Authentication and RLS Ownership > The ownership rule` |
| 6 | 15.46 | 0.42 |  | `vault/raw/NetworkTracker README.md:186-193 § Local Setup > 3. Create the application role` |
| 7 | 14.24 | 0.42 |  | `vault/raw/NetworkTracker README.md:85-100 § Features` |
| 8 | 13.30 | 0.42 |  | `vault/raw/NetworkTracker README.md:349-382 § Testing > Output` |

## test-3: What hardware and device did I use to train the Pac-Man agent and the custom language model?

| rank | score | coverage | expected? | passage |
|---|---|---|---|---|
| 1 | 10.13 | 0.56 | **yes** | `vault/raw/Pac-Man DQN README.md:273-291 § The run that produced these numbers` |
| 2 | 9.85 | 0.44 |  | `vault/raw/Pac-Man DQN README.md:334-338 § Reproducing this exact run` |
| 3 | 9.80 | 0.44 |  | `vault/raw/Pac-Man DQN README.md:18-29 § Training a Ms. Pac-Man agent with a Deep Q-Network` |
| 4 | 9.51 | 0.44 |  | `vault/raw/Pac-Man DQN README.md:303-312 § One limitation` |
| 5 | 8.05 | 0.44 |  | `vault/raw/Custom LLM README.md:3-21 § Building a Custom LLM — Class 4` |
| 6 | 7.49 | 0.33 |  | `vault/raw/Pac-Man DQN README.md:113-114 § My three choices > One further change, declared: replay capacity 5,000 → 50,000` |
| 7 | 7.37 | 0.44 |  | `vault/raw/Pac-Man DQN README.md:118-127 § What the agent actually sees, does, and is paid for` |
| 8 | 7.29 | 0.44 |  | `vault/raw/Pac-Man DQN README.md:3-16 § Training a Ms. Pac-Man agent with a Deep Q-Network` |

## test-4: What grade did I receive for the Pac-Man assignment?

| rank | score | coverage | expected? | passage |
|---|---|---|---|---|
| 1 | 8.71 | 0.60 |  | `vault/raw/Pac-Man DQN README.md:342-345 § Where the large files are` |
| 2 | 7.81 | 0.40 |  | `vault/raw/Custom LLM README.md:128-136 § 2. Where my predictions were wrong` |
| 3 | 6.50 | 0.60 |  | `vault/raw/Pac-Man DQN README.md:153-159 § What I expected, and what actually happened` |
| 4 | 6.36 | 0.60 |  | `vault/raw/Pac-Man DQN README.md:3-16 § Training a Ms. Pac-Man agent with a Deep Q-Network` |
| 5 | 4.61 | 0.40 |  | `vault/raw/Pac-Man DQN README.md:18-29 § Training a Ms. Pac-Man agent with a Deep Q-Network` |
| 6 | 4.52 | 0.40 |  | `vault/raw/Pac-Man DQN README.md:54-58 § My three choices` |
| 7 | 4.39 | 0.60 |  | `vault/raw/Pac-Man DQN README.md:96-111 § My three choices > One further change, declared: replay capacity 5,000 → 50,000` |
| 8 | 4.35 | 0.40 |  | `vault/raw/Pac-Man DQN README.md:113-114 § My three choices > One further change, declared: replay capacity 5,000 → 50,000` |

## Outcome

- test-1: expected passage at rank 1 (predicted rank 1).
- test-2: expected passage at rank 3 (predicted top-5 but not rank 1).
- test-3: Pac-Man hardware passage at rank 1; **custom-LLM hardware passage absent from the top 8 (rank 24 overall)**. Cause: vocabulary mismatch (question: "custom language model", "hardware", "device"; source: "LLM", "Apple Silicon, CPU only") and one source crowding out the other. Retrieval failure, so the model was not blamed.
- test-4: no source contains a grade; top hits are loosely related Pac-Man passages, so the score gate will not fire (as predicted).
