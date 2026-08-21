# Python OOP Colab Lab 01 · Seminario 11

Google-Colab-style formative laboratory for learning object-oriented programming by reasoning about objects **and executing real Python in the browser**.

## Scope

- 12 sequential OOP stages mixing concept checks and Python cells.
- Real Python execution with Pyodide.
- 36 persistent randomized workstation packs (12 × 36 = 432 backend variants).
- Teams of 2–3 students in 11A / 11B / 11C using institutional `@ijr.edu.co` emails.
- Class/object, instance, constructor, `self`, state/behavior, methods, independent objects, aliasing/references, encapsulation, inheritance/overriding, polymorphism and composition.
- Three global help tokens.
- Python syntax/runtime errors do **not** reduce the grade; only incorrect answers sent to server-side validation do.
- Reveal = 25% stage credit; skip = 0%.
- Supabase session persistence, server validation and 36-pack allocation.
- Separate live teacher master with search/group filters, projected grades, detailed stage inspection, evidence events, CSV export and cleanup of invalid registrations.

## Canonical production routes

The source is maintained in `IJR---Seminario`. Its repository-level GitHub Pages site is not enabled, so the classroom HTML is deliberately published through the already-enabled institutional Pages repository `ijr-estadistica-11-2026`. Supabase remains the data/validation backend, not the classroom frontend.

- Student: `https://juanperez238421-cpu.github.io/ijr-estadistica-11-2026/seminario-oop-colab-01/`
- Teacher master: `https://juanperez238421-cpu.github.io/ijr-estadistica-11-2026/seminario-oop-colab-01/teacher.html`

The two canonical URLs were HTTP-smoke-tested after deployment and returned `200` with the expected OOP student/master HTML.

## Backend activity

`seminar11-oop-colab-01-2026`

Backend QA contract:

- 12 checkpoints.
- 432 variant records.
- least-used randomized pack allocation over the active classroom window.
- token-validated student RPCs.
- teacher-code-protected master RPCs.
- internal pack/snapshot helpers not executable by browser client roles.
