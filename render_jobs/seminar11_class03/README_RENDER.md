# Seminar 11 · Class 03 · Constructors & Valid State · Senior Robot Continuity

Dedicated ManimCE render package for the Common Core OOP + UML Session 3.

## Continuity contract

This revision continues directly from the previous Class 1–2 animation and preserves its `Robot` / Atlas visual narrative. The bridge is explicit:

- Previous: **MODEL THE WORLD. GIVE EACH OBJECT A RESPONSIBILITY.**
- Class 03 question: **HOW DOES AN OBJECT BEGIN ITS LIFE?**

The lesson does **not** restart OOP from zero and does not teach the dedicated Class 04 topic.

## Curriculum lock

Source-of-truth Session 3:

- OOP: Constructors
- UML: Initialization
- Technical module: `m09`
- Evidence: three valid objects, justified constructor parameters, UML/code consistency, one rejected invalid initial state, and `self.valor` vs `factor` explanation

Primary narrative:

`ARGUMENTS → CONSTRUCTOR → INITIALIZATION / VALIDATION → VALID OBJECT → BEHAVIOR`

Python requirements represented:

- `__init__`
- instance attributes through `self`
- parameter vs object-state distinction
- methods that receive parameters and return values
- early rejection of impossible initial state

Class 04 content is intentionally deferred: no `@property`, getters/setters, or visibility lesson.

## Scene

`Seminar11Class03ConstructorsValidState`

Main chapters:

00. Opening continuity
01. Remember Atlas
02. Empty-object problem
03. Constructor mental model
04. Python `__init__`
05. `self` = this object
06. One class → three valid objects
07. Valid initial state / validation gate
08. Constructor vs method
09. UML synchronization
10. `Medicion` transfer to m09
11. Empty object + patch later anti-pattern
12. Exit check
13. Final synthesis + classroom evidence + Class 04 teaser

## Render protocol

Target environment: **ManimCE 0.20.1**, **1920×1080**, **30 fps**, white background.

Preview QA:

```bash
LESSON_TIME_SCALE=0.16 manim -pql Seminar11_Class03_Constructors_ValidState.py Seminar11Class03ConstructorsValidState --disable_caching
```

Final:

```bash
LESSON_TIME_SCALE=1.00 manim -pqh Seminar11_Class03_Constructors_ValidState.py Seminar11Class03ConstructorsValidState --fps 30 --disable_caching
```

Expected final file:

`Seminar11_Class03_Constructors_Valid_State_SENIOR_FINAL_pqh.mp4`

Target instructional duration: approximately **4:30–5:30**.

The GitHub Actions workflow reconstructs the canonical executable Python source from the repository render payload, performs `py_compile`, static curriculum/style QA, literal full-scene PQL and PQH renders, strict ffprobe checks, full FFmpeg decode, representative-frame extraction, SHA-256 generation, artifact upload, and publication to a direct-download delivery branch.
