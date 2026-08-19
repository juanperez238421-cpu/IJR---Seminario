# Seminario T3 · Dual-language interactive course — QA review

**Date:** 2026-08-19  
**Repository target:** `juanperez238421-cpu/IJR---Seminario`  
**Source package:** `Basics T3.zip`

## 1. Source coverage

The uploaded package contains **34 PDFs**:

- 1 Python learning-route document + 16 Python guides.
- 1 Java learning-route document + 16 Java guides.

No thematic guide is omitted. The application preserves the source guide numbers while using the QA route order defined by the route documents.

### Route represented in the platform

| Route order | Source guide | Level | Topic |
|---:|---:|---|---|
| 1 | 01 | Basic | Environment and first program |
| 2 | 02 | Basic | Variables and data types |
| 3 | 03 | Basic | Operators, input and output |
| 4 | 04 | Basic | Conditionals |
| 5 | 05 | Basic | Loops |
| 6 | 06 | Basic | Collections / arrays |
| 7 | 07 | Basic | Functions / methods |
| 8 | 08 | Basic | Classes and objects |
| 9 | 09 | Medium | Constructors, state and methods |
| 10 | 10 | Medium | Encapsulation |
| 11 | 13 | Medium | Exceptions and debugging |
| 12 | 14 | Medium | Modules / packages and organization |
| 13 | 11 | Advanced | Inheritance and polymorphism |
| 14 | 12 | Advanced | Composition + abstraction / interfaces + abstract classes |
| 15 | 15 | Advanced | Integrative project |
| 16 | 16 | Advanced | Final workshop |

The route documents explicitly justify keeping source numbers 13 and 14 while moving them to the Medium level.

## 2. Source pedagogy retained

The course implements the route rule from the attached documents:

1. Read the objective before code.
2. Predict the result.
3. Execute or validate.
4. Change a condition or datum.
5. Explain what changed and why.
6. Complete the guided exercise.
7. Complete the challenge without copying.
8. Show evidence: code + test + explanation.

The platform also preserves the source mastery rule: executing a program alone is not enough. The learner must explain flow/state, justify the chosen structure and make a short live modification.

## 3. Interactive architecture

### Python
- Real Python runtime in the browser with Pyodide.
- Editable source cell.
- Shared Python console.
- stdout/stderr shown in a terminal-style pane.
- `WRITE_HERE` scaffolding prevents the initial cell from revealing the target expression.
- Runtime/syntax errors are treated as learning feedback, not as scoring errors.

### Java
- The source guides explicitly use JDK / VS Code / `javac` / `java`.
- The browser therefore does **not** pretend that a JavaScript structural checker is `javac`.
- The platform provides:
  - editable Java source;
  - structural checks (markers, balanced delimiters, expected constructs);
  - `Main.java` download;
  - explicit JDK commands;
  - a field for the real stdout produced by `java Main`;
  - output validation after the learner runs the program with the JDK.

This is intentionally honest runtime labeling rather than simulated compiler output.

## 4. Scaffolding and scoring

Every Python and Java module includes exactly **three progressive hints** derived from that guide's concepts.

Per module:
- solved with no help/wrong validation: 100%;
- each help: -20 percentage points of that module's potential;
- each validated wrong output: -10 percentage points, capped at three penalties;
- correctly solved modules have a 25% floor;
- reveal correct solution: 25%;
- continue without solving: 0%;
- syntax/runtime/structural errors: no penalty.

Course grade:
`1 + 4 × (awarded internal points / 16)`.

The projected grade starts from 5.00 and falls as help/errors/reveals/skips are registered. It converges with the final grade after all sixteen modules are completed.

## 5. Team model

- A course attempt can represent **1, 2 or 3 students**.
- One group and one language route are selected for that attempt.
- The team shares code, progress and grade.
- Free-name registration is supported.
- Local browser persistence keeps the course usable if the backend cannot be reached.
- When the Supabase RPC layer is available, the same attempt is synchronized to the live teacher dashboard.

## 6. Teacher dashboard

The T3 teacher page is designed to expose:
- group;
- team members;
- Python/Java route;
- active/finalized state;
- completed / 16;
- projected/final grade;
- help count;
- validated wrong outputs;
- revealed solutions;
- skipped modules;
- fullscreen/visibility events;
- last activity.

It refreshes approximately every five seconds when the Supabase backend is available.

## 7. Fullscreen integrity

During an active lab:
- leaving fullscreen pauses work;
- fullscreen exits are recorded when the backend is available;
- visibility changes are recorded;
- the browser cannot physically disable OS-level Alt+Tab/Esc, so the platform blocks work until fullscreen is restored instead of claiming impossible browser control.

## 8. Timing

The manifest uses a progressive workload rather than forcing every topic into one 40-minute session.

- Basic modules: ~25–40 min each.
- Medium modules: ~40 min each.
- Advanced conceptual modules: ~45 min.
- Integrative project: ~60 min.
- Final workshop: ~70 min.
- Total planned guided practice: **635 minutes** (~10 h 35 min).

This is a complete third-period foundation path, not a single class activity.

## 9. Automated acceptance checks

`tests/seminar-t3-course.test.js` verifies:
- exactly 16 thematic modules;
- QA route order;
- 8 Basic / 4 Medium / 4 Advanced;
- both Python and Java variants for every topic;
- source objectives/concepts/steps/questions/criteria exist;
- exactly 3 hints per variant;
- starter code contains `WRITE_HERE`;
- solution code does not contain `WRITE_HERE`;
- scoring math;
- every Java solution passes the structural analyzer while every starter remains incomplete.

The Pages workflow additionally checks JSON validity and JavaScript syntax before deployment.

## 10. Backend design

Migration: `20260819190000_seminar_t3_dual_language_course.sql`.

Tables:
- `seminar_course_attempts`
- `seminar_course_attempt_members`
- `seminar_course_module_records`
- `seminar_course_events`

RLS is enabled and direct anonymous/authenticated table access is revoked. Student traffic uses token-checked `SECURITY DEFINER` RPCs; the teacher dashboard uses the existing teacher-code session helper already used by the shared academic backend.

### Important grading limitation

This is a **formative learning course**, not a secure examination. The browser necessarily contains the instructional content and records a solved/revealed/skipped outcome. The teacher should still use the source package's mastery rule—explain, modify and defend the code live—for any high-stakes grade.

## 11. Release gates

- [x] Manifest source coverage: 34 PDFs / 32 thematic language guides.
- [x] Local Node course tests pass.
- [x] JS syntax checks pass.
- [x] JSON course index and all 16 module files parse.
- [x] Python and Java routes render from one source manifest.
- [x] Local fallback persistence implemented.
- [x] Supabase migration prepared.
- [x] Backend deployment workflow prepared.
- [ ] GitHub PR merged.
- [ ] Main CI passes.
- [ ] Supabase migration workflow passes with repository secrets.
- [ ] One classroom smoke test per language.

**Release recommendation:** merge after PR diff inspection. Frontend remains usable in local mode even if the backend deployment is temporarily unavailable.
