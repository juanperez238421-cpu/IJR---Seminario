# Third Period Coding Studio · Python + Java

Interactive course for **Seminario de Programación 11°** based on the complete `Basics T3.zip` guide package.

## Production URLs

The classroom frontend is deployed through **GitHub Pages**. Supabase remains the shared data, session and server-validation backend.

- **T3 course:** https://juanperez238421-cpu.github.io/IJR---Seminario/t3/
- **T3 teacher:** https://juanperez238421-cpu.github.io/IJR---Seminario/t3/teacher.html
- **Python OOP Colab Lab 01:** https://juanperez238421-cpu.github.io/IJR---Seminario/t3/oop-logic-01/
- **Python OOP Colab Lab 01 · master:** https://juanperez238421-cpu.github.io/IJR---Seminario/t3/oop-logic-01/teacher.html
- **Source repository:** https://github.com/juanperez238421-cpu/IJR---Seminario

The GitHub Pages workflow validates the T3 route, Python OOP Colab student/master files, JavaScript syntax and Node contract tests before publishing the repository artifact.

## Routes

Both language routes contain the same 16-topic progression:

- **Basic (8):** environment, variables/types, operators/I-O, conditionals, loops, collections/arrays, functions/methods, classes/objects.
- **Medium (4):** constructors/state/methods, encapsulation, exceptions/debugging, modules/packages.
- **Advanced (4):** inheritance/polymorphism, composition/abstraction, integrative project, final workshop.

The original guide numbers remain traceable. Guides 13 and 14 are intentionally taught before 11 and 12 because the source QA route moves exceptions/debugging and organization to the Medium level.

## Python OOP Colab Lab 01

`t3/oop-logic-01/` is a separate formative activity modeled after the Statistics 11 Colab learning interface. It now combines OOP reasoning with **real Python execution through Pyodide**.

- 12 sequential stages mixing concept questions and Python code cells.
- 36 persistent randomized workstation packs assigned with a least-used random strategy during the classroom window.
- 2–3 participants per session, identified with institutional `@ijr.edu.co` emails.
- Topics: class/object, instance, constructor, `self`, state/behavior, methods, independent objects, references/aliasing, encapsulation, inheritance/overriding, polymorphism and composition.
- Three global help tokens.
- Python syntax/runtime errors do not reduce the grade; only incorrect answers submitted to server-side validation do.
- Reveal closes a stage with 25% credit; skip closes it with 0%.
- Expected answers are validated in Supabase rather than trusted from the browser.
- Dedicated teacher master with live progress, pack number, projected grade, answer evidence, starter/solution code, events and CSV export.

## Student experience

- Python route: real browser execution with Pyodide.
- Java route: source editor + structural analysis + `Main.java` export + real JDK stdout validation.
- Progressive help.
- Retry after incorrect output.
- Reveal solution for partial credit.
- Live projected grade on a 1.00–5.00 scale.

## Teacher

`t3/teacher.html` uses the shared teacher-code session mechanism for the main T3 course. `t3/oop-logic-01/teacher.html` uses the same teacher login but an activity-specific OOP dashboard/detail backend so its 12-stage evidence remains isolated from the 16-module route.

## Data and traceability

- `data/course-index.json`: course route index.
- `data/modules/*.json`: bilingual instructional content for every main T3 module.
- `data/source-map.json`: source-guide traceability.
- `oop-logic-01/`: Python OOP Colab student interface and live master.
- `../qa/SEMINAR_T3_DUAL_LANGUAGE_PLATFORM_QA_2026-08-19.md`: QA rationale and release gates.

## Tests

```bash
npm test
```

The test suite verifies the complete T3 route plus the OOP Colab contract: Pyodide runtime presence, code editor/run controls, 12-stage learning map, dedicated Supabase RPCs and independent live teacher master.
