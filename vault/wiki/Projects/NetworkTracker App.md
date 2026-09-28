---
type: "project"
description: "NetworkTracker is a full-stack web application for tracking people met during networking"
source_id: "a05da27bc262"
source_file: "[[NetworkTracker README]]"
source_path: "vault/raw/NetworkTracker README.md"
original_filename: "NetworkTracker README.md"
origin: "github.com/adityasankar98/secure-networking-tracker (README.md)"
sha256: "a05da27bc2625ef9df62b39d2475493e8b2c9a6bddf466aac721dcb36fec73bc"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
generated_at: "2026-09-28T15:57:35"
reviewed: true
visibility: "public"
tags:
  - "projects"
---

# NetworkTracker App

NetworkTracker is a full-stack web application for tracking people met during networking. It manages private contact lists with details like name, company, role, and priority tier. Contact persistence is handled in Neon Postgres with ownership enforced via application layer and database row level security.

## Key points

### NetworkTracker — Secure Networking Tracker

Source: [[NetworkTracker README|NetworkTracker README § NetworkTracker — Secure Networking Tracker]], lines 3–13

- NetworkTracker is a full-stack web application for tracking people met during networking.
- Users build a private contact list including name, company, role, where met, notes, and a priority tier.
- Contact persistence is handled in Neon Postgres with ownership enforced via application layer and database row level security.

### Walkthrough

Source: [[NetworkTracker README#Walkthrough|NetworkTracker README § Walkthrough]], lines 23–81

- Screenshots were captured using a scripted headless Chrome session.
- Signing out clears the session and redirects anonymous visitors to the sign-in screen.
- Data survives a refresh by re-fetching from Neon Postgres.

### Features

Source: [[NetworkTracker README#Features|NetworkTracker README § Features]], lines 85–100

- Sign up, sign in, and sign out use Email and password via Neon Managed Better Auth.
- Private contact list is scoped to the signed-in user at both app and database layers.
- Contact creation includes fields for Name, company, role, where met, notes, and priority.

### Technology Stack

Source: [[NetworkTracker README#Technology Stack|NetworkTracker README § Technology Stack]], lines 104–118

- Frontend uses React 19, Vite, and TypeScript for builds and contract checking.
- Styling utilizes Tailwind CSS v4 to maintain consistent spacing and color utilities.
- Backend is built with Node, Express, and TypeScript for readable request paths.

### Architecture

Source: [[NetworkTracker README#Architecture|NetworkTracker README § Architecture]], lines 122–163

- The React SPA signs in directly against Neon Auth, then calls the Express API with the session token as a bearer token.
- The process involves writing a session row in Neon Auth and resolving the token for access.
- The database contains contacts and Neon Auth session data, enforced by Row Level Security.

### Local Setup

Source: [[NetworkTracker README#Local Setup|NetworkTracker README § Local Setup]], lines 169–217

- Prerequisites include Node.js 18 or newer, a Neon project with Managed Better Auth enabled, and Git.
- Cloning involves git clone https://github.com/adityasankar98/secure-networking-tracker.git and changing directory.
- Creating the schema involves running backend/src/db/schema.sql to create the contacts table and security policies.

### Environment Variables

Source: [[NetworkTracker README#Environment Variables|NetworkTracker README § Environment Variables]], lines 221–241

- Backend environment variables are server-only and do not reach the browser.
- Backend variables include DATABASE_URL, NEON_AUTH_BASE_URL, PORT, and FRONTEND_URL.
- Frontend environment variables are compiled into the browser bundle and include VITE_BACKEND_URL and VITE_NEON_AUTH_URL.

### Database Schema

Source: [[NetworkTracker README#Database Schema|NetworkTracker README § Database Schema]], lines 245–262

- The contacts table has a column named id which is a UUID and is the PRIMARY KEY with a default of gen_random_uuid().
- The user_id column is TEXT and is NOT NULL, set from the authenticated session.
- The priority column has a CHECK constraint limiting values to 'high', 'medium', or 'low', defaulting to 'medium'.

### Security: Authentication and RLS Ownership

Source: [[NetworkTracker README#Security Authentication and RLS Ownership|NetworkTracker README § Security: Authentication and RLS Ownership]], lines 268–338

- Sign-up and sign-in use Neon Managed Better Auth; the client then sends the opaque session token as a bearer token on every API request.
- A contact belongs to exactly one user, enforced by scoping statements on the application layer and Row Level Security policies on the database layer.
- The backend connects as a dedicated `app_user` role without `BYPASSRLS` that does not own the contacts table, because the default `neondb_owner` bypassed RLS and left the policies inert.

### Testing

Source: [[NetworkTracker README#Testing|NetworkTracker README § Testing]], lines 342–404

- Tests confirm input validation for contacts, rejecting missing names and invalid priorities.
- Isolation tests verify that every select, update and delete is scoped by user_id and never matches rows on id alone.
- Frontend tests ensure no blocking browser dialogs are called and that delete flow is state-gated.

### Deployment

Source: [[NetworkTracker README#Deployment|NetworkTracker README § Deployment]], lines 408–434

- Frontend and backend are separate Vercel projects from the repository.
- Backend deployment requires setting DATABASE_URL, NEON_AUTH_BASE_URL, and FRONTEND_URL in the Vercel dashboard.
- Frontend deployment requires setting VITE_BACKEND_URL and VITE_NEON_AUTH_URL, and routes are rewritten in vercel.json.

### Known Limitations and What I'd Improve Next

Source: [[NetworkTracker README#Known Limitations and What I'd Improve Next|NetworkTracker README § Known Limitations and What I'd Improve Next]], lines 438–447

- Email and password are the only authentication methods implemented.
- No email verification exists; enabling OTP verification requires configuration changes.
- The isolation matrix runs against live deployment because it requires real authentication credentials.

### Repository Layout

Source: [[NetworkTracker README#Repository Layout|NetworkTracker README § Repository Layout]], lines 451–471

- The backend directory contains source code for database client, schema, authentication middleware, contact routes, validation schemas, and an index file.
- The backend tests directory includes tests for contacts, isolation, and frontend dialogs.
- The frontend directory includes API clients, components, hooks, and pages for authentication and contact functionality.

## Related notes

- [[Neon Postgres]] — Postgres ignores Row Level Security for roles holding the BYPASSRLS attribute, requiring a dedicated least-privilege role for application usage.
- [[Row Level Security]] — Row level security policies control select insert update and delete operations on the contacts table based on the current user ID.
- [[Session Token Auth]] — Sign-up and sign-in use Neon Managed Better Auth, where the token is resolved against the database.
- [[Vercel Deployment]] — Deployment involves using vercel deploy for the backend project and setting DATABASE_URL, NEON_AUTH_BASE_URL, and FRONTEND_URL in the dashboard.

## Sources

- Original: [[NetworkTracker README]] (`vault/raw/NetworkTracker README.md`, sha256 `a05da27bc262`)
- Catalog entry: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
