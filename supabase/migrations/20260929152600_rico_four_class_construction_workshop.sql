-- Rico four-class construction workshop
-- Mirrors the production change applied on 2026-09-29.
-- Transitional rule: existing projects may still use 8 roadmap steps while migrated projects use 4.

alter table public.seminar_student_projects
  drop constraint if exists seminar_student_projects_sprints_array;

alter table public.seminar_student_projects
  add constraint seminar_student_projects_sprints_array
  check (
    jsonb_typeof(sprints) = 'array'
    and jsonb_array_length(sprints) in (4, 8)
  );

update public.seminar_student_projects
set
  sprints = $json$
[
  {
    "n": 1,
    "phase": "CLASS 1 · FOUNDATION + ARCHITECTURE",
    "title": "Project contract + animation architecture",
    "goal": "Convert the visual idea into a measurable engineering contract and finish the class with a real Pygame baseline plus a responsibility architecture.",
    "theory": "Animation as a time-dependent system; Pygame vs Manim; App, Scene, Effect, Config and Launcher responsibilities.",
    "workshop": "Create the repository, storyboard, acceptance criteria, UML/responsibility map and a main.py that opens, animates and closes cleanly.",
    "deliverable": "Storyboard + 5 acceptance criteria + UML + runnable baseline + first Git commit",
    "gate": "The Python window must run a visible animation and close cleanly; the student must explain the final product contract and architecture.",
    "href": "student-workshops/rico-paramo/theory.html?class=1",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=1",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=1",
    "diagram": {
      "kicker": "CLASS FLOW",
      "title": "Idea to executable baseline",
      "nodes": ["Visual idea", "Acceptance criteria", "Architecture", "Runnable baseline"],
      "note": "The class does not end at planning: the architecture must already exist as executable Python."
    }
  },
  {
    "n": 2,
    "phase": "CLASS 2 · PROCEDURAL ENGINE",
    "title": "Animation engine + reusable effects",
    "goal": "Turn the baseline into a frame-rate-independent procedural engine with reusable effect classes and parameter-driven behavior.",
    "theory": "Delta time, procedural equations, deterministic seeds, scene graph and stable update/draw interfaces.",
    "workshop": "Implement App + Scene plus OrbitEffect, PulseEffect and ParticleField; test parameters, FPS invariance and reproducibility.",
    "deliverable": "Runnable scene + 3 reusable effects + parameter comparison + FPS/seed verification",
    "gate": "The same effect class must be reusable with different parameters and motion must remain approximately consistent across frame-rate changes.",
    "href": "student-workshops/rico-paramo/theory.html?class=2",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=2",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=2",
    "diagram": {
      "kicker": "FRAME PIPELINE",
      "title": "Real-time animation loop",
      "nodes": ["Poll events", "Measure dt", "Update state", "Draw scene", "Flip frame"],
      "note": "State evolves from elapsed time rather than from a fixed amount per frame."
    }
  },
  {
    "n": 3,
    "phase": "CLASS 3 · PORTABLE BUILD",
    "title": "Relative paths + portable build + launcher",
    "goal": "Remove development-computer assumptions, externalize parameters and package the visual show so it survives a folder move and offline execution.",
    "theory": "Relative resource paths, JSON configuration, packaged runtime paths, PyInstaller and explicit/manual launching.",
    "workshop": "Create config.json, resource_path(), fallback behavior, PortableVisualShow.exe, launch.bat and a PORTABLE_BUILD folder; test from a renamed clean path without internet.",
    "deliverable": "Portable build + config + visible launcher + clean-path test + offline test",
    "gate": "The copied/renamed build must launch manually with the network disconnected and without absolute developer paths.",
    "href": "student-workshops/rico-paramo/theory.html?class=3",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=3",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=3",
    "diagram": {
      "kicker": "PORTABILITY",
      "title": "Source to offline runtime",
      "nodes": ["Source project", "PyInstaller", "Portable folder", "USB / clean path", "Offline run"],
      "note": "Packaging alone is not evidence of portability; the moved build must actually execute."
    }
  },
  {
    "n": 4,
    "phase": "CLASS 4 · QA + LIVE DEFENSE",
    "title": "Offline QA + live project defense",
    "goal": "Treat the visual show as a product: inject controlled faults, fix observed failures, document evidence and defend the architecture through a live parameter change.",
    "theory": "Claim-evidence testing, fault injection, regression testing, performance observation and reproducible technical defense.",
    "workshop": "Execute the 8-case QA matrix, repair defects, finalize README/UML/evidence, launch from portable media or a clean folder and change one visual parameter live.",
    "deliverable": "QA matrix + fixes + final portable demo + UML + README + live parameter defense",
    "gate": "The build must pass the documented offline/portable tests and the student must predict, execute and explain a live parameter change.",
    "href": "student-workshops/rico-paramo/theory.html?class=4",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=4",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=4",
    "diagram": {
      "kicker": "QA LOOP",
      "title": "Evidence-driven hardening",
      "nodes": ["Inject condition", "Observe", "Diagnose", "Fix", "Retest"],
      "note": "A failure is only closed when the same condition is repeated and the new evidence demonstrates the fix."
    }
  }
]
$json$::jsonb,
  content_sections = $json$
[
  {
    "class": 1,
    "kicker": "CLASS 1 · THEORY + WORKSHOP",
    "title": "Project contract + animation architecture",
    "body": "The first class converts the idea into an executable engineering baseline. Planning and coding happen in the same session.",
    "theory_intro": "Understand the minimum architecture needed before visual complexity is added.",
    "theory": [
      "Animation is state that changes as a function of elapsed time; a frame is only one sample of that state.",
      "Pygame is selected for the reference implementation because the final product needs real-time rendering, a launcher and live parameter changes.",
      "Separate App, Scene, Effect, Config and Launcher responsibilities so later effects do not collapse into one monolithic script.",
      "Acceptance criteria must be observable and testable, not aesthetic intentions such as 'make it cool'."
    ],
    "workshop_intro": "Produce the first real project increment before leaving class.",
    "workshop": [
      "Create the project folder, virtual environment and Git repository.",
      "Write a 6–10 panel storyboard and five acceptance criteria.",
      "Create the App/Scene/Effect/Config/Launcher responsibility diagram.",
      "Install Pygame and build main.py with a visible time-based animation loop.",
      "Run the program, close it cleanly and commit the working baseline."
    ],
    "diagram": {
      "kicker": "ARCHITECTURE",
      "title": "Portable visual show responsibility flow",
      "nodes": ["Launcher", "App", "Scene", "Effects", "Surface"],
      "note": "Config remains external data read by the runtime; effects expose behavior through parameters instead of duplicated code."
    },
    "evidence": ["storyboard", "5 acceptance criteria", "UML/responsibility map", "running main.py", "first Git commit"],
    "gate": "Do not advance unless the window opens, animates and closes cleanly and the student can explain each responsibility.",
    "href": "student-workshops/rico-paramo/theory.html?class=1",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=1",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=1"
  },
  {
    "class": 2,
    "kicker": "CLASS 2 · THEORY + WORKSHOP",
    "title": "Procedural animation engine",
    "body": "The second class transforms the baseline into a small reusable engine rather than a collection of copied drawing commands.",
    "theory_intro": "Model motion mathematically and separate update from draw.",
    "theory": [
      "Use delta time so motion is expressed in units per second rather than units per frame.",
      "Procedural animation computes visual state from equations, parameters and time instead of replaying a pre-made asset.",
      "A stable update(dt)/draw(surface) contract lets one Scene coordinate heterogeneous effects.",
      "A deterministic random seed makes particle initialization reproducible for debugging and testing."
    ],
    "workshop_intro": "Implement and experimentally verify reusable effects.",
    "workshop": [
      "Refactor the baseline into App and VisualScene classes.",
      "Implement OrbitEffect using polar motion.",
      "Implement PulseEffect using periodic sine-based variation.",
      "Implement ParticleField with a fixed seed and many generated elements.",
      "Run tests at different FPS and parameter values and record the observed differences."
    ],
    "diagram": {
      "kicker": "FRAME PIPELINE",
      "title": "One deterministic real-time iteration",
      "nodes": ["Poll events", "Measure dt", "Update effects", "Draw scene", "Flip display"],
      "note": "The update phase owns simulation state; the draw phase visualizes that state without redefining the motion law."
    },
    "evidence": ["App + Scene", "OrbitEffect", "PulseEffect", "ParticleField", "FPS comparison", "parameter test"],
    "gate": "The student must reuse one effect class with different parameters and explain why delta time makes the motion approximately frame-rate independent.",
    "href": "student-workshops/rico-paramo/theory.html?class=2",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=2",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=2"
  },
  {
    "class": 3,
    "kicker": "CLASS 3 · THEORY + WORKSHOP",
    "title": "Portability, configuration and packaging",
    "body": "The third class turns the working animation into a portable product that no longer depends on the developer's machine or path.",
    "theory_intro": "Distinguish a program that runs locally from a product that survives relocation.",
    "theory": [
      "Absolute paths are machine-specific dependencies and therefore portability defects.",
      "Configuration should be data in JSON so visual parameters can change without rewriting algorithms.",
      "PyInstaller changes runtime assumptions; resource lookup must work in source and packaged modes.",
      "A portable build still requires an actual moved-folder/offline execution test."
    ],
    "workshop_intro": "Package, move and prove the build.",
    "workshop": [
      "Move visual parameters into config.json and implement defaults/fallbacks.",
      "Implement resource_path() with pathlib and packaged-runtime support.",
      "Build PortableVisualShow.exe with PyInstaller.",
      "Create a visible manual launch.bat and README.",
      "Copy/rename the folder, disconnect the network and execute the product again."
    ],
    "diagram": {
      "kicker": "PORTABILITY",
      "title": "Development source to offline runtime",
      "nodes": ["Python source", "PyInstaller", "PORTABLE_BUILD", "Moved/USB path", "Offline execution"],
      "note": "Portability is verified at the destination, not inferred from a successful build command."
    },
    "evidence": ["config.json", "relative paths", "PortableVisualShow.exe", "launch.bat", "clean-path run", "offline run"],
    "gate": "The renamed/copy build must launch with no internet and no reference to the original development path.",
    "href": "student-workshops/rico-paramo/theory.html?class=3",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=3",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=3"
  },
  {
    "class": 4,
    "kicker": "CLASS 4 · THEORY + WORKSHOP",
    "title": "QA hardening + live technical defense",
    "body": "The final class validates the project as a product and prepares an evidence-based defense instead of a scripted presentation.",
    "theory_intro": "Testing is a reproducible claim-evidence process.",
    "theory": [
      "A test defines condition, action, expected result and observed evidence.",
      "Fault injection intentionally creates realistic failures while there is still time to fix them.",
      "Regression testing repeats the same condition after a fix to verify that the defect is actually closed.",
      "Live defense demonstrates architectural ownership by predicting the effect of a parameter change before relaunch."
    ],
    "workshop_intro": "Run the complete final validation and defend the result.",
    "workshop": [
      "Execute QA-01 through QA-08 and capture PASS/FAIL evidence.",
      "Diagnose and fix any path, config, asset, shutdown or performance defect.",
      "Finalize architecture diagram, README, QA matrix and evidence folder.",
      "Launch from USB/removable media or a clean folder.",
      "Change a documented visual parameter live, predict the result, relaunch and verify it."
    ],
    "diagram": {
      "kicker": "QA FEEDBACK LOOP",
      "title": "Evidence-driven hardening",
      "nodes": ["Inject condition", "Observe", "Diagnose", "Fix", "Repeat same test"],
      "note": "The cycle ends with evidence that the original failure condition now passes."
    },
    "evidence": ["8-case QA matrix", "fixed defect", "offline/USB run", "final UML", "README", "live parameter change"],
    "gate": "The project is complete only when the portable build passes the documented tests and the student can explain architecture and live behavior.",
    "href": "student-workshops/rico-paramo/theory.html?class=4",
    "theory_href": "student-workshops/rico-paramo/theory.html?class=4",
    "workshop_href": "student-workshops/rico-paramo/workshop.html?class=4"
  }
]
$json$::jsonb,
  definition_questions = $json$
[
  "Class 1: What measurable behavior proves the visual show has started correctly?",
  "Class 2: Which three visual effects are reusable classes and which parameters control them?",
  "Class 3: How will you prove there is no dependency on the original computer path or network?",
  "Class 4: Which QA failure did you reproduce, fix and retest with evidence?"
]
$json$::jsonb,
  decision_note = 'Proyecto específico: exactamente 4 clases. Cada clase tiene subpágina Theory y subpágina Workshop, construcción sobre el proyecto real, ejecución verificable, evidencia y gate obligatorio.',
  updated_at = now()
where upper(trim(student_name)) = 'RICO PARAMO ALEJANDRO'
  and group_code = '11B'
  and project_title = 'Portable Python Visual Show — USB Launcher & Procedural Animation';
