---
type: "concept"
description: "Hosting the frontend and serverless backend as two Vercel projects."
sources:
  - "[[NetworkTracker README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "tools"
---

# Vercel Deployment

*Hosting the frontend and serverless backend as two Vercel projects.*

The backend is an Express app deployed as a Vercel serverless function ([[NetworkTracker README#Architecture|S1]]). This component handles validation, token resolution, and ownership scoping, creating a fresh Neon client per request ([[NetworkTracker README#Architecture|S1]]). Deployment involves running vercel deploy --prod in the backend directory ([[NetworkTracker README#Deployment|S2]]). Environment variables like DATABASE_URL, NEON_AUTH_BASE_URL, and FRONTEND_URL are set in the Vercel dashboard for the backend project ([[NetworkTracker README#Deployment|S2]]).

## Where it appears

- [[NetworkTracker App]] — Deployment involves using vercel deploy for the backend project and setting DATABASE_URL, NEON_AUTH_BASE_URL, and FRONTEND_URL in the dashboard.

## Related notes

- [[Neon Postgres]] — the database the deployed backend talks to

## Sources

- [S1] [[NetworkTracker README#Architecture|NetworkTracker README § Architecture]], lines 155–163
- [S2] [[NetworkTracker README#Deployment|NetworkTracker README § Deployment]], lines 412–419
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
