# Ask-mode eval run 20260922-174414 (v2-balanced-refusal-rule)

| Test | Kind | Retrieval: expected passage found? | Answer check | Human assessment |
|---|---|---|---|---|
| [test-1](test-1.md) | direct, one source | PASS — ranks 1 | PASS: expected facts present, citations valid | pending |
| [test-2](test-2.md) | reworded vs the source | PASS — ranks 2 | FAIL: model refused although the evidence was retrieved; missing expected facts: ['BYPASSRLS']; citation check: PASS (insufficient-evidence reply; no citations needed) | pending |
| [test-3](test-3.md) | connects two sources | PASS — ranks 1, 3 | PASS: expected facts present, citations valid | pending |
| [test-4](test-4.md) | unsupported (answer not in the wiki) | n/a (no source should contain the answer) | PASS: expected an insufficient-evidence reply: got one | pending |

Model: `mlx-community/gemma-4-e2b-it-4bit` @ `238767527555` · mlx-vlm 0.7.2, mlx 0.32.2 · macOS 15.6.1 · Apple M4 · 16 GB · execution: local
