# test-2: Why was one signed-in user of my networking app initially able to see and delete another person's contacts?

| | |
|---|---|
| Mode | **ask** (standalone: no chat history, no persona) |
| Execution | **local** — offline-capable local model |
| Model | `mlx-community/gemma-4-e2b-it-4bit` @ `238767527555` (4-bit (MLX)) |
| Runtime | mlx-vlm 0.7.2, mlx 0.32.2, Python 3.12.14, macOS 15.6.1, Apple M4, 16 GB |
| Time | 2026-09-22T17:43:36 |
| Evidence gate | passed |
| Latency / memory | 1.39 s generation, 1157 prompt tokens, 38 generated tokens, peak MLX memory 4.24 GB |

**Question:** Why was one signed-in user of my networking app initially able to see and delete another person's contacts?

## Retrieved passages

**[S1] `vault/raw/NetworkTracker README.md` lines 3–13 § NetworkTracker — Secure Networking Tracker** (BM25 27.77, term coverage 0.75)

> **Live app → [https://frontend-seven-puce-55.vercel.app](https://frontend-seven-puce-55.vercel.app)**
> 
> NetworkTracker is a full-stack web application for keeping track of the people you meet while networking. Each user signs up with an email and password, then builds a private contact list — name, company, role, where you met, notes, and a priority tier — which they can create, view, edit, delete, sort, filter, and search. Contacts persist in Neon Postgres and survive a refresh or a new sign-in. The central design concern is ownership: one user must never see or modify another user's contacts, so isolation is enforced twice over — once in the application layer, where every query is scoped to the authenticated user, and again in the database through Postgres Row Level Security. Built for Berkeley's Agentic AI course, Assignment 1.
> 
> > **Try it:** sign up with any email and password (no verification required), or use the demo account
> > `browsertest9081@example.com` / `TestPass12345`. To see isolation for yourself, sign up a second
> > account in a private window — its contact list will be empty.
> 
> **Backend API:** `https://backend-sigma-five-8590c45c6q.vercel.app` · [`/health`](https://backend-sigma-five-8590c45c6q.vercel.app/health)
> 
> ---

**[S2] `vault/raw/NetworkTracker README.md` lines 317–332 § Security: Authentication and RLS Ownership > The `app_user` role — why RLS needs it** (BM25 22.80, term coverage 0.58)

> Postgres ignores RLS entirely for any role holding the **`BYPASSRLS`** attribute, and Neon's default `neondb_owner` has it. While the backend connected as the owner, all four policies above were **completely inert**: end-to-end testing found that one signed-in user could read *and delete* another user's contacts. `FORCE ROW LEVEL SECURITY` does not help, because `BYPASSRLS` outranks it. Table *owners* also bypass RLS, so the application role must not own `contacts` either.
> 
> The backend therefore connects as a dedicated least-privilege role:
> 
> | Role | `rolsuper` | `rolbypassrls` | Owns `contacts` | Used by the app |
> |---|---|---|---|---|
> | `neondb_owner` | false | **true** | yes | no — migrations only |
> | `app_user` | false | **false** | no | **yes** |
> 
> Enforcement was then verified at the database level, independently of the API:
> 
> | Session context | Rows visible |
> |---|---|
> | none set | **0** — RLS blocks everything |
> | set to user A | only user A's rows |
> | set to an unknown id | **0** |

**[S3] `vault/raw/NetworkTracker README.md` lines 186–193 § Local Setup > 3. Create the application role** (BM25 20.76, term coverage 0.42)

> The backend must **not** connect as `neondb_owner` — see [Security](#the-app_user-role--why-rls-needs-it) for why this is required rather than optional.
> 
> ```sql
> CREATE ROLE app_user LOGIN PASSWORD '<choose-a-strong-password>' NOBYPASSRLS;
> GRANT USAGE  ON SCHEMA public, neon_auth              TO app_user;
> GRANT SELECT, INSERT, UPDATE, DELETE ON contacts      TO app_user;
> GRANT SELECT ON neon_auth.session, neon_auth."user"   TO app_user;
> ```

## Gemma's answer (verbatim)

> Insufficient evidence: The provided passages describe issues where users could read and delete another user's contacts, but they do not specify why this was initially possible for a signed-in user.

## Citation check (automatic)

- Status: **PASS (insufficient-evidence reply; no citations needed)**

## Expected (from tests/questions.json, written before the run)

- `vault/raw/NetworkTracker README.md` containing “Postgres ignores RLS entirely for any role holding the” → **found at rank 2**
- Expected facts in answer: BYPASSRLS

## Automatic assessment

- Retrieval: **PASS**
- Answer: **FAIL** — model refused although the evidence was retrieved; missing expected facts: ['BYPASSRLS']; citation check: PASS (insufficient-evidence reply; no citations needed)

## Human assessment (I opened each cited passage)

_Not yet reviewed for this exact answer (answer hash `a5204d9f96ac`)._
