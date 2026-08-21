# Third Period Coding Studio · Python + Java

Interactive course for **Seminario de Programación 11°** based on the complete `Basics T3.zip` guide package.

## Production / source routing

`IJR---Seminario` is the canonical **source repository**. Repository-level GitHub Pages is not currently enabled there, so this repository validates the static source but does not publish a `github.io/IJR---Seminario/...` classroom site.

The **Python OOP Colab Lab 01** is published through the already-enabled institutional GitHub Pages repository `ijr-estadistica-11-2026`, while Supabase remains the data/session/server-validation backend:

- **Python OOP Colab Lab 01 · student:** https://juanperez238421-cpu.github.io/ijr-estadistica-11-2026/seminario-oop-colab-01/
- **Python OOP Colab Lab 01 · teacher master:** https://juanperez238421-cpu.github.io/ijr-estadistica-11-2026/seminario-oop-colab-01/teacher.html
- **Source repository:** https://github.com/juanperez238421-cpu/IJR---Seminario

Both OOP GitHub Pages routes were independently HTTP-smoke-tested after deployment and returned `200` with the expected student/master HTML. The versioned CSS/JS/config remain sourced from the merged Seminar repository code.

## Routes

Both main language routes contain the same 16-topic progression:

- **Basic (8):** environment, variables/types, operators/I-O, conditionals, loops, collections/arrays, functions/methods, classes/objects.
- **Medium (4):** constructors/state/methods, encapsulation, exceptions/debugging, modules/packages.
- **Advanced (4):** inheritance/polymorphism, composition/abstraction, integrative project, final workshop.

The original guide numbers remain traceable. Guides 13 and 14 are intentionally taught before 11 and 12 because the source QA route moves exceptions/debugging and organization to the Medium level.

## Python OOP Colab Lab 01

`t3/oop-logic-01/` is a separate formative activity modeled after the Statistics 11 Colab learning interface. It combines OOP reasoning with **real Python execution through Pyodide**.

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

- Python OOP: real browser execution with Pyodide in a Colab-style notebook surface.
- Main Python route: real browser execution with Pyodide.
- Java route: source editor + structural analysis + `Main.java` export + real JDK stdout validation.
- Progressive help, retry, reveal, skip and live projected grade on a 1.00–5.00 scale.

## Teacher

The OOP master uses the existing teacher-code session mechanism but activity-specific dashboard/detail/delete RPCs, keeping its 12-stage evidence isolated from the main 16-module route.

## Data and traceability

- `data/course-index.json`: main course route index.
- `data/modules/*.json`: bilingual instructional content for every main T3 module.
- `data/source-map.json`: source-guide traceability.
- `oop-logic-01/`: canonical Python OOP Colab source and master source.
- `../qa/SEMINAR_T3_DUAL_LANGUAGE_PLATFORM_QA_2026-08-19.md`: QA rationale and release gates.

## Tests

```bash
npm test
```

The test suite verifies the complete T3 route plus the OOP Colab contract: Pyodide runtime presence, code editor/run controls, 12-stage learning map, dedicated Supabase RPCs and independent live teacher master.
