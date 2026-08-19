# Third Period Coding Studio · Python + Java

Interactive course for **Seminario de Programación 11°** based on the complete `Basics T3.zip` guide package.

## Production URLs

The canonical classroom deployment is currently served by the shared academic Supabase project because GitHub Pages is not enabled for `IJR---Seminario`.

- **Student course:** https://rlfxnjbqxbozjdzkbwlz.supabase.co/functions/v1/seminar-t3-host/
- **Teacher / master gradebook:** https://rlfxnjbqxbozjdzkbwlz.supabase.co/functions/v1/seminar-t3-host/teacher.html
- **Source repository:** https://github.com/juanperez238421-cpu/IJR---Seminario

The Supabase production workflow smoke-tests the student HTML, teacher HTML and `data/course-index.json` before reporting `SEMINAR T3 HOST READY`. Do not distribute the legacy `github.io/IJR---Seminario/...` URLs unless GitHub Pages is explicitly enabled and its deployment is independently verified.

## Routes

Both language routes contain the same 16-topic progression:

- **Basic (8):** environment, variables/types, operators/I-O, conditionals, loops, collections/arrays, functions/methods, classes/objects.
- **Medium (4):** constructors/state/methods, encapsulation, exceptions/debugging, modules/packages.
- **Advanced (4):** inheritance/polymorphism, composition/abstraction, integrative project, final workshop.

The original guide numbers remain traceable. Guides 13 and 14 are intentionally taught before 11 and 12 because the source QA route moves exceptions/debugging and organization to the Medium level.

## Student experience

- 1–3 students per attempt.
- Python: real browser execution with Pyodide.
- Java: source editor + structural analysis + `Main.java` export + real JDK stdout validation.
- 3 progressive hints per module.
- Retry after incorrect output.
- Reveal solution for 25% module credit.
- Continue without solving for 0%.
- Syntax/runtime/structural errors do not reduce the grade.
- Live projected grade on a 1.00–5.00 scale.
- Fullscreen-guided mode with observable exit telemetry.
- LocalStorage fallback if the backend is not reachable.

## Teacher

`t3/teacher.html` uses the shared teacher-code session mechanism and the Seminar T3 dashboard RPC. The production Supabase backend contains the course RPC layer and the teacher page reads the live team/module records through that authenticated teacher session.

## Data and traceability

- `data/course-index.json`: course route index.
- `data/modules/*.json`: complete bilingual instructional content for every module.
- `data/source-map.json`: maps every interactive module back to its Python and Java source PDF in the uploaded package.
- `../qa/SEMINAR_T3_DUAL_LANGUAGE_PLATFORM_QA_2026-08-19.md`: QA rationale and release gates.

## Tests

```bash
npm test
```

The course test verifies complete 16-module coverage, both language variants, progressive hints, starter/solution separation, scoring and Java structural QA.
