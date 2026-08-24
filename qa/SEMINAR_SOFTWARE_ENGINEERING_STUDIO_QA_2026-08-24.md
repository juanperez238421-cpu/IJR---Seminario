# Seminar 11 Software Engineering Studio · Senior QA

Date: 2026-08-24

## Architecture decision

The existing 16-module Python/Java T3 course is preserved. It becomes the technical library. The classroom flow is a 10-session OOP+UML common core plus five synchronized eight-sprint project tracks.

## Student selection

One canonical survey replaces the two legacy mechanisms. Required data: name, group, one-or-more interests, first choice, modality, partner when applicable, optional project idea. First choice maps deterministically to one of five track slugs.

## Privacy

- Legacy survey direct inserts are revoked.
- Studio tables have RLS enabled and no anon/authenticated table privileges.
- Student register/load/update runs through a constrained Edge Function with exact-origin CORS and a high-entropy private edit token.
- Teacher dashboard/update runs only after Auth + MFA AAL2 + active teacher/admin profile through `teacher-auth-gateway`.
- Teacher Studio route is intentionally absent from public navigation and deployment summaries.
- Teacher notes never return through the student Edge Function.

## Curriculum contract

Hour 1: class/object, state/behavior, constructors, encapsulation, relationships, inheritance, polymorphism/abstraction, architecture, debugging/refactoring, defense.

Hour 2: Web, Data Science, Defensive Cybersecurity, 3D Programming, Robotics. Every track follows the same eight-sprint engineering progression and ends with UML + repository + MVP + live defense.

## Release gates

- [x] Five track manifest.
- [x] Ten Common Core sessions.
- [x] Eight sprints per track.
- [x] Existing T3 modules preserved.
- [x] Single survey frontend.
- [x] Private Studio database schema.
- [x] Student Edge Function deployed.
- [x] MFA gateway extended for Studio.
- [x] Public teacher links omitted.
- [x] CI updated to the 2026-08-24 privacy baseline.
- [ ] PR CI green.
- [ ] Classroom smoke test with one disposable student profile.
