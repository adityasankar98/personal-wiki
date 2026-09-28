# Test expectations — written before building retrieval or ask mode

Kept outside `vault/` so the answer key is never retrievable. The machine-readable version is
[`questions.json`](questions.json). Outcomes are reported in the README's evaluation section and
compared against every prediction below.

## Choices made before testing

- **Data:** three READMEs I wrote for earlier classes (full-stack app, Pac-Man DQN, custom LLM).
  The wiki should answer "what did I build, what did I choose, what happened, and why".
- **Model:** Gemma 4 E2B instruction-tuned, 4-bit MLX (`mlx-community/gemma-4-e2b-it-4bit`).
- **Retrieval:** BM25 keyword search over heading-aware passages of the *original* sources.
  No embeddings, so nothing extra to download and search works without the model.

## The four ask-mode tests

| # | Question | Expected evidence | Expected answer |
|---|---|---|---|
| 1 | What mean score did the trained Ms. Pac-Man agent get on the five evaluation seeds, compared with the untrained agent? | `Pac-Man DQN README.md`, opening result line + "All five evaluation scores" table | 1360.0 trained vs 492.0 untrained (+868, +176%) |
| 2 | Why was one signed-in user of my networking app initially able to see and delete another person's contacts? | `NetworkTracker README.md` § "The `app_user` role — why RLS needs it" | The backend connected as `neondb_owner`, which has `BYPASSRLS`, so the RLS policies were inert; fixed with a least-privilege `app_user` role |
| 3 | What hardware and device did I use to train the Pac-Man agent and the custom language model? | `Pac-Man DQN README.md` § "The run that produced these numbers"; `Custom LLM README.md` § "Experiments 3–5" hardware line | Apple M4 (10 cores, 16 GB) on MPS for Pac-Man; Apple Silicon, CPU only for the custom LLM |
| 4 | What grade did I receive for the Pac-Man assignment? | none — no source mentions a grade | An explicit insufficient-evidence statement |

## Predictions

1. **Test 1 will pass easily.** The question shares "mean", "score", "evaluation", "seeds",
   "untrained" with the source. I expect the correct passage at rank 1.
2. **Test 2 is the retrieval risk.** The question says "networking app", "see", "person"; the
   source says "NetworkTracker", "read", "user". Words like "user" and "contacts" occur in almost
   every section of that README, so BM25 may rank the general ownership-rule section above the
   `BYPASSRLS` passage. I predict the right passage lands in the top 5 but not at rank 1.
3. **Test 3 is the model risk.** The Pac-Man hardware line is a table row that retrieval should
   find, but the custom LLM's hardware is a single sentence inside a long section, so I expect it
   to rank lower. Even with both retrieved, I expect E2B may blur the two (e.g. say both used MPS).
4. **Test 4 will not be caught by the retrieval gate**, because "Pac-Man assignment" matches
   plenty of real passages. It depends entirely on the model following the "insufficient
   evidence" rule. I expect a small model to be tempted to answer from nearby numbers (the score),
   so this is the test most likely to fail on the first run.

## Mode checks (interface behaviour, not research questions)

| Check | Expected |
|---|---|
| chat: "what can we do?" / "what can you help me with?" | Describes real capabilities and commands; no notes search, no citations, no refusal |
| chat: "draft a 3-step plan to study for my next class" → "make that shorter" | Second reply shortens the first, using conversation history only |
| `wiki search "reward clipping"` | Original passages + paths + sections, no generated text, model never loaded |
| chat claim → ask | Tell chat "my Pac-Man agent won a class prize"; then `wiki ask "Did my Pac-Man agent win a class prize?"` must report insufficient evidence |
