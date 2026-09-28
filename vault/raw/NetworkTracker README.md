# NetworkTracker — Secure Networking Tracker

**Live app → [https://frontend-seven-puce-55.vercel.app](https://frontend-seven-puce-55.vercel.app)**

NetworkTracker is a full-stack web application for keeping track of the people you meet while networking. Each user signs up with an email and password, then builds a private contact list — name, company, role, where you met, notes, and a priority tier — which they can create, view, edit, delete, sort, filter, and search. Contacts persist in Neon Postgres and survive a refresh or a new sign-in. The central design concern is ownership: one user must never see or modify another user's contacts, so isolation is enforced twice over — once in the application layer, where every query is scoped to the authenticated user, and again in the database through Postgres Row Level Security. Built for Berkeley's Agentic AI course, Assignment 1.

> **Try it:** sign up with any email and password (no verification required), or use the demo account
> `browsertest9081@example.com` / `TestPass12345`. To see isolation for yourself, sign up a second
> account in a private window — its contact list will be empty.

**Backend API:** `https://backend-sigma-five-8590c45c6q.vercel.app` · [`/health`](https://backend-sigma-five-8590c45c6q.vercel.app/health)

---

## Contents

[Walkthrough](#walkthrough) · [Features](#features) · [Stack](#technology-stack) · [Architecture](#architecture) · [Local setup](#local-setup) · [Environment variables](#environment-variables) · [Schema](#database-schema) · [Security](#security-authentication-and-rls-ownership) · [Testing](#testing) · [Evidence](#grading-evidence) · [Deployment](#deployment) · [Limitations](#known-limitations-and-what-id-improve-next)

---

## Walkthrough

Every screenshot below was captured by driving the deployed application end to end with a scripted headless Chrome session ([`docs/capture-evidence.mjs`](docs/capture-evidence.mjs)) — none are mockups.

### Sign in and sign out

| Sign-in page | Signed in (empty state) | Signed out again |
|---|---|---|
| ![Sign in](docs/screenshots/01-sign-in.png) | ![Signed in](docs/screenshots/02-signed-in-empty.png) | ![Signed out](docs/screenshots/10-signed-out.png) |

Signing out clears the session and returns to the sign-in screen; protected routes redirect there for anonymous visitors.

### Create, edit, delete, and refresh

| Contact list after creating three | Edit dialog |
|---|---|
| ![Contacts](docs/screenshots/04-contacts-list.png) | ![Edit](docs/screenshots/05-edit-contact.png) |

| Delete confirmation | After delete |
|---|---|
| ![Delete confirm](docs/screenshots/08-delete-confirm.png) | ![After delete](docs/screenshots/09-after-delete.png) |

**Data survives a refresh** — reloading the page re-fetches from Neon Postgres rather than from memory:

![Persists after refresh](docs/screenshots/07-persists-after-refresh.png)

### Sort and filter

Filtering to high priority only:

![Filter](docs/screenshots/06-filter-high-priority.png)

Sorting is available by name, company, priority, or date added, in either direction, and free-text search matches on name, company, and role.

### Invalid input fails safely

Submitting the form with an empty name shows a clear inline message and sends no request. The server independently rejects the same payload with `400 name: Name is required`, so validation does not depend on the client.

![Invalid input](docs/screenshots/03-invalid-input.png)

### Two-account isolation

User A (`ada.lovelace`) created three contacts. User B (`grace.hopper`) then signed up:

| User B sees an empty list | User B adds their own contact | User A is unaffected |
|---|---|---|
| ![B isolated](docs/screenshots/11-user-b-isolated.png) | ![B own contact](docs/screenshots/12-user-b-own-contact.png) | ![A unchanged](docs/screenshots/13-user-a-unchanged.png) |

The capture script asserts this programmatically rather than leaving it to the eye:

```
=== ISOLATION ASSERTIONS ===
  PASS  User B cannot see User A's contacts
  PASS  User A cannot see User B's contact
  PASS  User A still sees own contacts
  PASS  User B sees own contact

ALL PASS: true
```

---

## Features

| Feature | Detail |
|---|---|
| Sign up / sign in / sign out | Email + password via Neon Managed Better Auth |
| Private contact list | Scoped to the signed-in user at both app and database layers |
| Create contact | Name (required), company, role, where met, notes, priority |
| View contacts | Card grid with initials avatar and colour-coded priority badge |
| Edit contact | Full update through a pre-filled modal |
| Delete contact | In-app confirmation dialog naming the contact, with pending state |
| Sort | By name, company, priority, or date added; ascending or descending |
| Filter | By priority tier (high / medium / low) |
| Search | Case-insensitive match across name, company, and role |
| Persistence | Stored in Neon Postgres; survives refresh, sign-out, and new sessions |
| Validation | Client-side and server-side (Zod), with clear inline error messages |
| Protected routes | Anonymous visitors are redirected to sign-in |

---

## Technology Stack

| Layer | Choice | Why |
|---|---|---|
| Frontend | **React 19 + Vite + TypeScript** | Vite gives near-instant builds and a tiny production bundle; TypeScript catches contract drift between the API client and components at compile time. |
| Styling | **Tailwind CSS v4** | The brief requires a design system. Tailwind v4 needs no config file, and utility classes keep spacing and colour consistent without a separate stylesheet to drift. |
| Routing | **React Router v7** | Standard declarative routing; makes the protected-route redirect explicit rather than ad-hoc. |
| HTTP | **Axios** | A single request interceptor attaches the bearer token to every call, so no component handles auth headers. |
| Backend | **Node + Express + TypeScript** | The brief requires a separated backend. Express is minimal enough that the request path stays readable, which matters when the security argument depends on it. |
| Validation | **Zod** | One schema is both the runtime validator and the inferred TypeScript type, so they cannot disagree. |
| Database | **Neon Postgres** (`@neondatabase/serverless`) | Required by the brief. The HTTP driver suits Vercel's serverless model, where a connection pool cannot be held between invocations. |
| Auth | **Neon Managed Better Auth** | Required by the brief. Credentials are handled by the hosted service — the app never sees or stores a password. |
| Testing | **Jest + Supertest** | Fast, zero-config for TypeScript via `ts-jest`. |
| Hosting | **Vercel** | Required by the brief; frontend and backend deploy as two independent projects from one repo. |
| Version control | **Git + GitHub** | Single public repository is the deliverable. |

---

## Architecture

```
                        ┌───────────────────────────┐
                        │  Neon Managed Better Auth │
                        │  (hosted; owns passwords) │
                        └─────────────┬─────────────┘
        1. sign in / sign up          │ 2. writes session row
                        ▲             ▼
┌─────────────────────┐ │  ┌────────────────────────┐
│   React SPA         │─┘  │   Express API          │
│   (Vercel static)   │    │   (Vercel serverless)  │
│                     │───▶│                        │
│  stores token,      │ 3. │  4. resolves token via │
│  sends as Bearer    │    │     neon_auth.session  │
└─────────────────────┘    └───────────┬────────────┘
                                       │ 5. DATABASE_URL (app_user)
                                       ▼
                        ┌──────────────────────────────┐
                        │  Neon Postgres               │
                        │  neon_auth.session / user    │
                        │  contacts  + RLS (enforced)  │
                        └──────────────────────────────┘
```

**Request flow for "list my contacts":**

1. The SPA signs in against Neon Auth directly and receives an opaque session token, which it keeps in `localStorage`.
2. Neon Auth writes a row into `neon_auth.session` in *our* database, linking that token to a user id.
3. The SPA calls `GET /api/contacts` with `Authorization: Bearer <token>` (attached by an Axios interceptor).
4. `requireAuth` middleware joins `neon_auth.session` to `neon_auth."user"`, checks `expiresAt > now()`, and attaches the resolved user to the request. Unknown or expired tokens get `401` and never reach the contacts table.
5. The route opens a transaction, sets `app.current_user_id` for that transaction, and runs a query that is *itself* scoped by `user_id`. RLS independently filters the same rows.

**Frontend** — a static Vite build on Vercel. Auth state lives in a single `AuthProvider` context at the root, so a successful sign-in immediately propagates to the router and every component reads one shared session. On load it restores the session by calling `GET /api/me` with the stored token, which avoids depending on third-party cookies.

**Backend** — an Express app deployed as a Vercel serverless function. It owns validation, token resolution, and ownership scoping. It creates a fresh Neon client per request, since serverless invocations cannot share a pool.

**Database** — one Neon Postgres database holding both `contacts` and Neon Auth's own tables. Because auth data lives alongside application data, verifying a session is a local join rather than a network round-trip.

**Auth** — Neon Managed Better Auth, hosted. It owns password hashing and session issuance; this app never receives a plaintext password.

**Hosting** — two independent Vercel projects from one repository: a static frontend and a serverless backend, wired together by environment variables.

---

## Local Setup

### Prerequisites

- Node.js 18 or newer
- A Neon project with **Managed Better Auth** enabled
- Git

### 1. Clone

```bash
git clone https://github.com/adityasankar98/secure-networking-tracker.git
cd secure-networking-tracker
```

### 2. Create the schema

Open the **Neon SQL Editor** and run [`backend/src/db/schema.sql`](backend/src/db/schema.sql) in full. It creates the `contacts` table, enables **and forces** row level security, adds the four ownership policies, and installs the `updated_at` trigger.

### 3. Create the application role

The backend must **not** connect as `neondb_owner` — see [Security](#the-app_user-role--why-rls-needs-it) for why this is required rather than optional.

```sql
CREATE ROLE app_user LOGIN PASSWORD '<choose-a-strong-password>' NOBYPASSRLS;
GRANT USAGE  ON SCHEMA public, neon_auth              TO app_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON contacts      TO app_user;
GRANT SELECT ON neon_auth.session, neon_auth."user"   TO app_user;
```

### 4. Backend

```bash
cd backend
cp .env.example .env      # fill in DATABASE_URL (app_user) and NEON_AUTH_BASE_URL
npm install
npm run dev               # http://localhost:3001
```

### 5. Frontend

In a second terminal:

```bash
cd frontend
cp .env.example .env      # VITE_BACKEND_URL=http://localhost:3001
npm install
npm run dev               # http://localhost:5173
```

Enable **Allow Localhost** under Auth → Configuration in the Neon console so local sign-in requests are accepted.

---

## Environment Variables

No real values appear anywhere in this repository — both `.env.example` files contain placeholders only, and `.env` is gitignored.

### Backend — `backend/.env` (server-only, never reaches the browser)

| Variable | What it is |
|---|---|
| `DATABASE_URL` | Neon connection string using the **`app_user`** role, not the owner |
| `NEON_AUTH_BASE_URL` | Neon Auth endpoint root (Neon console → Auth → Configuration → Auth URL) |
| `PORT` | Local port; defaults to `3001` |
| `FRONTEND_URL` | Allowed CORS origin for the deployed frontend |

### Frontend — `frontend/.env` (compiled into the browser bundle; public by design)

| Variable | What it is |
|---|---|
| `VITE_BACKEND_URL` | Public URL of the backend API |
| `VITE_NEON_AUTH_URL` | Public Neon Auth endpoint the sign-in form posts to |

Only these two `VITE_` values reach the client. **No database credential is reachable from the browser.**

---

## Database Schema

Every column of the `contacts` table:

| Column | Type | Constraints | Purpose |
|---|---|---|---|
| `id` | `UUID` | `PRIMARY KEY`, default `gen_random_uuid()` | Surrogate key; unguessable, so ids are safe in URLs |
| `user_id` | `TEXT` | `NOT NULL` | **Owner.** Set from the authenticated session, never from the request body |
| `name` | `TEXT` | `NOT NULL` | Contact's full name — the only required field |
| `company` | `TEXT` | nullable | Company or organisation |
| `role` | `TEXT` | nullable | Job title |
| `where_met` | `TEXT` | nullable | Where you met — e.g. "Berkeley career fair" |
| `notes` | `TEXT` | nullable | Free-form follow-up notes |
| `priority` | `TEXT` | `CHECK (priority IN ('high','medium','low'))`, default `'medium'` | Follow-up tier; the CHECK makes an invalid value unstorable |
| `created_at` | `TIMESTAMPTZ` | default `now()` | Creation time; default sort key |
| `updated_at` | `TIMESTAMPTZ` | default `now()` | Last modification, maintained by a `BEFORE UPDATE` trigger |

Full DDL including policies: [`backend/src/db/schema.sql`](backend/src/db/schema.sql).

---

## Security: Authentication and RLS Ownership

### Authentication

Sign-up and sign-in are handled by Neon Managed Better Auth. On success the client receives an opaque session token and sends it as `Authorization: Bearer <token>` on every API request.

The backend resolves that token against `neon_auth.session`, joined to `neon_auth."user"`, checking `expiresAt > now()`. A missing, unknown, or expired token gets `401` and the contacts table is never queried.

> **Why a database lookup rather than the auth server's `/get-session`?**
> Neon's managed Better Auth does not enable Better Auth's bearer plugin, so `/get-session` returns `null` for an `Authorization` header instead of a session — verified directly against the deployed endpoint. The session cookie is not usable either: it is scoped to the `neonauth` domain, making it a third-party cookie from the app's origin. Since Neon Auth writes its session rows into our own database, resolving the token there is both correct and one fewer network hop.

### The ownership rule

**A contact belongs to exactly one user, identified by `contacts.user_id`, and only that user may read or modify it.** `user_id` is written from the authenticated session at insert time and is never accepted from the request body, so a client cannot create a row owned by someone else.

That rule is enforced in two independent places.

**1. Application layer.** Every statement is scoped by `user_id`:

```sql
SELECT * FROM contacts WHERE user_id = $1 ...
UPDATE contacts SET ... WHERE id = $1 AND user_id = $2
DELETE FROM contacts        WHERE id = $1 AND user_id = $2
```

Update and delete match on `id` **and** `user_id`. A request for another user's row therefore affects zero rows and returns `404` — it neither leaks the row nor destroys it.

**2. Database layer (RLS).** The backend opens a transaction and issues `SET LOCAL app.current_user_id = '<id>'` before each query; the policies evaluate against it:

```sql
ALTER TABLE contacts ENABLE ROW LEVEL SECURITY;
ALTER TABLE contacts FORCE  ROW LEVEL SECURITY;

CREATE POLICY contacts_select ON contacts
  FOR SELECT USING (user_id = current_setting('app.current_user_id', true));

CREATE POLICY contacts_insert ON contacts
  FOR INSERT WITH CHECK (user_id = current_setting('app.current_user_id', true));

-- USING blocks reaching another user's row; WITH CHECK blocks reassigning ownership
CREATE POLICY contacts_update ON contacts
  FOR UPDATE
  USING      (user_id = current_setting('app.current_user_id', true))
  WITH CHECK (user_id = current_setting('app.current_user_id', true));

CREATE POLICY contacts_delete ON contacts
  FOR DELETE USING (user_id = current_setting('app.current_user_id', true));
```

The `WITH CHECK` on update is what stops a user handing their row to someone else — `USING` governs which rows can be reached, `WITH CHECK` governs what they may become.

### The `app_user` role — why RLS needs it

Postgres ignores RLS entirely for any role holding the **`BYPASSRLS`** attribute, and Neon's default `neondb_owner` has it. While the backend connected as the owner, all four policies above were **completely inert**: end-to-end testing found that one signed-in user could read *and delete* another user's contacts. `FORCE ROW LEVEL SECURITY` does not help, because `BYPASSRLS` outranks it. Table *owners* also bypass RLS, so the application role must not own `contacts` either.

The backend therefore connects as a dedicated least-privilege role:

| Role | `rolsuper` | `rolbypassrls` | Owns `contacts` | Used by the app |
|---|---|---|---|---|
| `neondb_owner` | false | **true** | yes | no — migrations only |
| `app_user` | false | **false** | no | **yes** |

Enforcement was then verified at the database level, independently of the API:

| Session context | Rows visible |
|---|---|
| none set | **0** — RLS blocks everything |
| set to user A | only user A's rows |
| set to an unknown id | **0** |

### Secrets

`DATABASE_URL` and `NEON_AUTH_BASE_URL` are server-only, are never referenced by any `VITE_` variable, and are set in the Vercel dashboard rather than committed. The repository contains only `.env.example` placeholders, and `.env`, `node_modules/`, `dist/`, and `.vercel/` are gitignored. There is no `DATABASE_URL`, cookie secret, or other credential in the frontend bundle or in Git history.

---

## Testing

```bash
cd backend
npm test
```

### Output

```
PASS tests/frontend-dialogs.test.ts
  Frontend avoids blocking browser dialogs
    ✓ finds frontend source files to scan
    ✓ never calls window.confirm() — blocked in sandboxed/embedded browsers
    ✓ never calls window.alert() — blocked in sandboxed/embedded browsers
    ✓ never calls window.prompt() — blocked in sandboxed/embedded browsers
    ✓ delete flow is gated by in-app state, not a native dialog

PASS tests/contacts.test.ts
  Contact Validation
    ✓ returns 400 when name is missing
    ✓ returns 400 when name is empty string
    ✓ returns 400 when priority is invalid
    ✓ returns 200 with valid contact data
    ✓ applies default priority of medium when not provided

PASS tests/isolation.test.ts
  Cross-user data isolation
    ✓ SELECT is scoped by user_id
    ✓ UPDATE is scoped by user_id, not just id
    ✓ DELETE is scoped by user_id, not just id
    ✓ never deletes or updates by id alone
    ✓ INSERT sets user_id from the authenticated session
    ✓ sort column comes from an allowlist, not raw user input
  Database schema hardening
    ✓ enables row level security
    ✓ forces RLS so the table owner cannot bypass it
    ✓ defines a policy for each of select, insert, update, delete
    ✓ update policy has WITH CHECK so rows cannot be reassigned to another user

Test Suites: 3 passed, 3 total
Tests:       20 passed, 20 total
```

### What the tests verify

**`contacts.test.ts` — input validation.** Exercises the Zod schema behind `POST /api/contacts`: that a missing name and an empty-string name are both rejected with `400 Name is required`, that an out-of-range `priority` is rejected, that a well-formed contact is accepted, and that `priority` defaults to `medium`. This is the required passing validation test.

**`isolation.test.ts` — the ownership invariant.** Asserts that `SELECT`, `UPDATE`, and `DELETE` are all scoped by `user_id`; that no statement matches on `id` alone; that `INSERT` takes `user_id` from the session; that the sort column comes from an allowlist rather than raw input (SQL-injection guard); and that the schema enables *and forces* RLS with four policies and a `WITH CHECK` on update. These exist because this exact leak reached production.

**`frontend-dialogs.test.ts` — no blocking dialogs.** Asserts no frontend source calls `confirm`, `alert`, or `prompt`, and that the delete path is gated by component state. `window.confirm()` returns `false` without prompting in sandboxed and embedded browsers, which silently swallowed every delete.

Each regression test was confirmed to **fail against the pre-fix code** — a test that cannot fail is not evidence.

### End-to-end evidence

[`docs/capture-evidence.mjs`](docs/capture-evidence.mjs) drives the deployed app in headless Chrome — signing up two users, exercising the full CRUD cycle, and asserting cross-user isolation — and produces every screenshot in this README:

```bash
node docs/capture-evidence.mjs
```

It lives outside the Jest suite because it needs the live deployment and creates real accounts.

---

## Deployment

Frontend and backend are two separate Vercel projects from this one repository.

### Backend

```bash
cd backend
vercel deploy --prod
```

Set in the Vercel dashboard for the backend project: `DATABASE_URL` (the `app_user` connection string), `NEON_AUTH_BASE_URL`, and `FRONTEND_URL`.

`vercel.json` routes all traffic to `src/index.ts` via `@vercel/node`. The app skips `app.listen()` when `VERCEL=1`, since the platform supplies the server.

### Frontend

```bash
cd frontend
vercel deploy --prod
```

Set `VITE_BACKEND_URL` and `VITE_NEON_AUTH_URL`. These are compiled in at **build** time, so changing either requires a redeploy, not just a restart. `vercel.json` rewrites all paths to `index.html` so client-side routes survive a hard refresh.

### Neon

Add the deployed frontend origin under **Auth → Configuration → Domains**, otherwise sign-in redirects are rejected as untrusted.

---

## Known Limitations and What I'd Improve Next

- **Email/password only.** Google is enabled on the Neon project but not surfaced in the UI. Adding it is mostly wiring Better Auth's social provider into the sign-in page.
- **No email verification.** Sign-up is immediate so a grader can get in without a real inbox. Neon Auth supports OTP verification; enabling it is a config change plus a "check your email" screen.
- **The isolation matrix is not in CI.** It runs against the live deployment because it needs real auth credentials. The right fix is a Neon branch per CI run, seeded and torn down, so the cross-user assertions run on every push instead of on demand.
- **No pagination.** The contact list is fetched whole. Past a few hundred rows this needs cursor pagination, plus an index on `(user_id, created_at)` and a trigram index for search — currently every query is a sequential scan, which is fine only at this scale.
- **Session tokens live in `localStorage`,** which is readable by any script on the origin. The app has no third-party scripts and a short token lifetime, but an httpOnly first-party cookie set by our own backend would be strictly better.
- **No optimistic UI.** Every mutation waits for the server round-trip. Updating local state first with rollback on failure would make the list feel instant.
- **No rate limiting** on the API. Sign-in throttling is handled by Neon Auth, but the contacts endpoints would accept unlimited requests from a valid session.
- **Tests assert query shape, not runtime behaviour.** The isolation unit tests read the source and check that scoping is present. That catches the regression that actually happened, but a true integration test against a live database would be stronger.

---

## Repository Layout

```
.
├── backend/
│   ├── src/
│   │   ├── db/         client.ts · schema.sql (DDL + RLS policies)
│   │   ├── middleware/ auth.ts   (session-token resolution)
│   │   ├── routes/     contacts.ts (CRUD, ownership-scoped)
│   │   ├── validation/ contact.ts  (Zod schema)
│   │   └── index.ts    Express entry, CORS, /health, /api/me
│   ├── tests/          contacts · isolation · frontend-dialogs
│   └── vercel.json
├── frontend/
│   └── src/
│       ├── api/        client.ts (token interceptor) · contacts.ts · auth.ts
│       ├── components/ ContactCard · ContactForm · Modal · Navbar · PrivateRoute
│       ├── hooks/      useAuth.tsx (root context) · useContacts.ts
│       └── pages/      LoginPage · SignupPage · ContactsPage
└── docs/
    ├── capture-evidence.mjs
    └── screenshots/
```
