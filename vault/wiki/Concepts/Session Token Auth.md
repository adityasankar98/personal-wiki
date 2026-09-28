---
type: "concept"
description: "Signing users in and resolving an opaque bearer token to a user on every request."
sources:
  - "[[NetworkTracker README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Session Token Auth

*Signing users in and resolving an opaque bearer token to a user on every request.*

Sign-up and sign-in are handled by Neon Managed Better Auth. The client receives an opaque session token and sends it as Authorization: Bearer (token) on every API request ([[NetworkTracker README#Security Authentication and RLS Ownership|S1]]). The backend resolves that token against neon_auth.session joined to neon_auth."user", checking expiresAt > now(), and a missing, unknown, or expired token gets 401 and the contacts table is never queried ([[NetworkTracker README#Security Authentication and RLS Ownership|S1]]). The session cookie is scoped to the neonauth domain, making it a third-party cookie from the app's origin ([[NetworkTracker README#Security Authentication and RLS Ownership|S1]]).

## Where it appears

- [[NetworkTracker App]] — Sign-up and sign-in use Neon Managed Better Auth, where the token is resolved against the database.

## Related notes

- [[Row Level Security]] — the resolved user id is what the database policies check

## Sources

- [S1] [[NetworkTracker README#Security Authentication and RLS Ownership|NetworkTracker README § Security: Authentication and RLS Ownership]], lines 268–273
- [S2] [[NetworkTracker README#Architecture|NetworkTracker README § Architecture]], lines 147–153
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
