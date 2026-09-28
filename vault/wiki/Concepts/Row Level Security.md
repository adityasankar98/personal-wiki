---
type: "concept"
description: "Postgres policies that restrict which rows each user can read or change."
sources:
  - "[[NetworkTracker README]]"
generated_by: "mlx-community/gemma-4-e2b-it-4bit@2387675"
reviewed: true
visibility: "public"
tags:
  - "concepts"
---

# Row Level Security

*Postgres policies that restrict which rows each user can read or change.*

Row Level Security policies are defined on tables like contacts ([[NetworkTracker README#Security Authentication and RLS Ownership|S1]]). Policies such as contacts_select, contacts_insert, contacts_update, and contacts_delete govern access based on the current user ID ([[NetworkTracker README#Security Authentication and RLS Ownership|S1]]). The WITH CHECK on update stops a user from handing their row to someone else, while USING governs which rows can be reached, and WITH CHECK governs what they may become ([[NetworkTracker README#Security Authentication and RLS Ownership|S1]]). The app_user role is used because Postgres ignores Row Level Security for roles holding the BYPASSRLS attribute, and the default neondb_owner has this attribute, rendering the policies inert ([[NetworkTracker README#Security Authentication and RLS Ownership|S2]]).

## Where it appears

- [[NetworkTracker App]] — Row level security policies control select insert update and delete operations on the contacts table based on the current user ID.

## Related notes

- [[Session Token Auth]] — the policies compare rows against the user id that token authentication resolved
- [[Neon Postgres]] — the database that enforces the policies

## Sources

- [S1] [[NetworkTracker README#Security Authentication and RLS Ownership|NetworkTracker README § Security: Authentication and RLS Ownership]], lines 293–313
- [S2] [[NetworkTracker README#Security Authentication and RLS Ownership|NetworkTracker README § Security: Authentication and RLS Ownership]], lines 317–332
- Catalog: [[sources]] · Start page: [[index]]

## Notes (manual)

_Anything written below this heading survives re-ingestion._
