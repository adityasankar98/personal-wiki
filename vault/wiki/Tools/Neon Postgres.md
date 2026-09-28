---
type: "concept"
description: "Serverless Postgres that stored the contacts and the auth sessions."
sources:
  - "[[NetworkTracker README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "tools"
---

# Neon Postgres

*Serverless Postgres that stored the contacts and the auth sessions.*

Neon Postgres is used for the database layer ([[NetworkTracker README#Technology Stack|S2]]). It is required by the brief ([[NetworkTracker README#Technology Stack|S2]]).

## Where it appears

- [[NetworkTracker App]] — Postgres ignores Row Level Security for roles holding the BYPASSRLS attribute, requiring a dedicated least-privilege role for application usage.

## Related notes

- [[Row Level Security]] — enforced inside this database
- [[Vercel Deployment]] — the serverless backend that connects to it

## Sources

- [S1] [[NetworkTracker README#Security Authentication and RLS Ownership|NetworkTracker README § Security: Authentication and RLS Ownership]], lines 317–332
- [S2] [[NetworkTracker README#Technology Stack|NetworkTracker README § Technology Stack]], lines 104–114
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
