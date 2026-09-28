# Evidence index

Every file here is actual CLI output; none were hand-edited. Earlier runs are never overwritten, so failures stay next to their fixes. The model for every model run was `mlx-community/gemma-4-e2b-it-4bit` @ `238767527555`, running locally.

## Ask-mode tests (`wiki eval`), in order

| Run | What changed before it | Result |
|---|---|---|
| [`ask/20260922-174330-v1-first-prompt`](ask/20260922-174330-v1-first-prompt/README.md) | first run | Test 1 flagged by my own citation checker (bug: it split "Ms. Pac-Man" into two sentences); **Test 2 false refusal**; Tests 3 and 4 pass |
| [`ask/20260922-174414-v2-balanced-refusal-rule`](ask/20260922-174414-v2-balanced-refusal-rule/README.md) | splitter fixed; refusal rule in `wiki-instructions.md` reworded | Test 2 **still** refuses; rewording the prompt was not enough |
| [`ask/20260922-174553-v3-refusal-double-check`](ask/20260922-174553-v3-refusal-double-check/README.md) | quote-first double-check added | Test 2 still fails, due to a **bug in my quote verifier** (trailing space); the model's quote was actually verbatim |
| [`ask/20260922-174620-v3-refusal-double-check`](ask/20260922-174620-v3-refusal-double-check/README.md) | verifier fixed | all four pass |
| [`ask/20260928-125726-v4-pre-offline`](ask/20260928-125726-v4-pre-offline/README.md) | chat-mode changes only (ask unchanged) | all four pass, identical answers |
| [`ask/20260928-152543-offline`](ask/20260928-152543-offline/README.md) | **Wi-Fi off, fresh processes: the required run** | all four pass; answers identical to v4, so the reviewed assessments are attached |
| [`ask/20260928-160016-final-check`](ask/20260928-160016-final-check/README.md) | after the last re-ingest (concept `sources` de-duplicated) | all four pass, identical answers |

Human assessments for the final answers are in [`../tests/assessments.json`](../tests/assessments.json). They are embedded in any card whose answer text matches exactly.

## Retrieval checked before the model

- [`retrieval/retrieval-v1.md`](retrieval/retrieval-v1.md): BM25 only. Test 3's custom-LLM passage ranked **24th** (missing from the top 5).
- [`retrieval/retrieval-v2`](retrieval/retrieval-v2/README.md): after adding synonym expansion (`retrieval-synonyms.json`), a 3-per-source cap and a 30% relative cut, every expected passage is in the top 5.

## Ingestion

| Log | Notes |
|---|---|
| [`ingest/20260922-175024…`](ingest/20260922-175024-ingest-pac-man-dqn-readme.md), [`…175124…`](ingest/20260922-175124-ingest-networktracker-readme.md), [`…175210…`](ingest/20260922-175210-ingest-custom-llm-readme.md) | first ingest of each source (15 → 17 notes) |
| [`ingest/20260922-184831-ingest-raw`](ingest/20260922-184831-ingest-raw.md) | full re-ingest after fixing concept linking: **0 new files**. ⚠️ Its time (3,370 s) is **not a valid measurement**; the laptop slept on battery during the run. |
| [`ingest/20260922-213025-ingest-raw`](ingest/20260922-213025-ingest-raw.md) | full re-ingest with the 23 review corrections: all applied, **0 new files**. ⚠️ Time (2,460 s) invalid for the same reason. |
| [`ingest/20260928-155828…-ingest-raw`](ingest/20260928-155828-ingest-raw.md) | full re-ingest after de-duplicating concept `sources`: 110 s for all 3 sources, 72 calls, **0 new files** (valid timing) |
| [`ingest/20260928-123727…`](ingest/20260928-123727-ingest-pac-man-dqn-readme.md) + [`perf/ingest-timed.txt`](perf/ingest-timed.txt) | **the valid timing**: 45.5 s, 26 Gemma calls, peak memory footprint 5.08 GB, on AC power, awake |

## Other

- [`perf/`](perf/): `/usr/bin/time -l` output for one ingest and one ask.
- [`runs/`](runs/): individual `--save` runs of ask and search.
- [`chat-dryrun.md`](chat-dryrun.md): online dry run of the chat mode checks; the required offline one is in `offline/`.
- [`chat-saves/`](chat-saves/): a draft saved with `/save`. Saved drafts are kept apart from evidence and never indexed.
- [`screenshots/`](screenshots/): Obsidian screenshots (note, note body with links/sources, index + page list, graph, source-link check).
- [`offline/`](offline/): the offline run: `terminal.txt` recording, Wi-Fi-off screenshot, chat mode checks.
- [`ask/20260928-152543-offline/`](ask/20260928-152543-offline/README.md): **the four required ask-mode evidence cards (offline)**.
