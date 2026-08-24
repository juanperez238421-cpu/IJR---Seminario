# IJR — Seminario de Programación 11° · 2026

Official source for the Grade 11 Programming Seminar at Instituto Jorge Robledo.

## Current architecture

The third-period course is organized as a **Software Engineering Studio**:

- Hour 1: **Object-Oriented Programming + UML** for everyone.
- Hour 2: **Specialized Project Studio**.
- Tracks: Web Development, Python & Data Science, Defensive Cybersecurity, 3D Design + Programming, and Robotics & Automation.
- Common workflow: **design → model → implement → test → document → defend**.

The complete 16-module Python/Java route and the Python OOP Colab Lab remain available as technical libraries and guided practice. They were not replaced.

## Student routes

- Main T3 course: `t3/`
- Common Core OOP + UML: `t3/common/`
- Project selection/profile: `t3/studio/`
- Track catalog: `t3/tracks/`

Teacher/admin routes are intentionally not linked from public student navigation.

## Privacy and security baseline

Public rosters, attendance artifacts, answer keys and teacher-dashboard navigation were removed on 2026-08-24. Teacher access uses institutional Supabase Auth + TOTP MFA (AAL2) through the audited `teacher-auth-gateway`.

Student Studio records are private database rows. Public clients have no direct `SELECT/INSERT/UPDATE/DELETE` access. Registration and self-update use a constrained Edge Function plus a private edit token; teacher reads/updates require the MFA gateway.

## Project assessment

| Criterion | Weight |
|---|---:|
| Common OOP + UML | 30% |
| Functional project | 40% |
| Git + documentation | 15% |
| Individual live defense / modification | 15% |

## Development

```bash
python -m http.server 8000
npm test
```

GitHub Pages CI validates privacy baseline files, the preserved T3 course, OOP Colab, Studio manifest, five track pages and JavaScript syntax before deployment.
