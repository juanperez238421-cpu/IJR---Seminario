# Seminar 11 · Class 03 · Constructors & Valid State

Dedicated render package for the Common Core OOP + UML Session 3.

## Curriculum lock

Ground truth is the repository's current Session 3 contract:

- OOP: Constructors
- UML: Initialization
- Technical module: `m09`
- Required evidence: `3 valid objects`

The lesson uses `Measurement(value, unit)` as the central thread and prepares students for both Python (`__init__`, `self`) and Java (constructor named after the class, `this`). Encapsulation, inheritance, polymorphism and relationships are not taught as Class 03 content.

## Scene

`Seminar11Class03ConstructorsValidState`

## Render protocol

Target environment: ManimCE 0.20.1, 1920×1080, 30 fps, white background.

Preview:

```bash
LESSON_TIME_SCALE=0.12 manim -pql Seminar11_Class03_Constructors_ValidState.py Seminar11Class03ConstructorsValidState --disable_caching
```

Final:

```bash
LESSON_TIME_SCALE=0.80 manim -pqh Seminar11_Class03_Constructors_ValidState.py Seminar11Class03ConstructorsValidState --fps 30 --disable_caching
```

Expected final file:

`Seminar11_Class03_Constructors_ValidState_FINAL_pqh.mp4`

The GitHub Actions workflow assembles the scene chunks, then performs `py_compile`, static curriculum/style QA, strict ffprobe verification, full FFmpeg decode, representative-frame extraction, SHA-256 generation, artifact upload, and publication to a direct-download delivery branch.
