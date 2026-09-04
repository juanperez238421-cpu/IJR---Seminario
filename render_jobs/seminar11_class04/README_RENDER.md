# Seminar 11 · Class 04 · Encapsulation & Visibility

This render job implements the **real Common Core Session 4** defined by the repository curriculum.

## Curriculum ground truth

- `t3/common/index.html` → Week 4: **Encapsulation**, UML **Visibility + / -**, existing lab **m10**, evidence **Protected state**.
- `t3/oop-uml/course-data.js` → `Encapsulation & Visibility`: protect state behind a controlled interface; use `+`, `-`, `#`; validation belongs close to the state it protects.
- `t3/data/modules/m10.json` → Python `_atributo`, `@property`, setter validation, zero-absolute rule; Java `private`, `public`, `protected`, purposeful getters/setters.

## Full scene

`Seminar11Class04EncapsulationVisibility`

The scene contains:
1. Direct state mutation problem.
2. Encapsulation mental model.
3. UML visibility `+ / - / #`.
4. Python `_valor` convention.
5. Python `@property` read interface.
6. Python validated setter with `-273.15 °C` invariant.
7. Java `private/public/protected` and validation.
8. Why getters/setters should not be generated mechanically.
9. Request → validate → update → valid-state pipeline.
10. Transfer to the five Seminar project tracks.
11. m10 evidence checklist.
12. Exit check.

## Render contract

- ManimCE 0.20.1
- 1920 × 1080
- 30 fps
- white background / monochrome classroom style
- literal full-scene `-pql` QA before final `-pqh`
- ffprobe + full FFmpeg decode + representative frames + SHA-256
- verified MP4 published to a delivery branch for direct download

Expected final file:

`Seminar11_Class04_Encapsulation_Visibility_FINAL_pqh.mp4`
