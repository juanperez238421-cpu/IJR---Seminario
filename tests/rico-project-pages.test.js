import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const RICO = path.join(ROOT, 't3/projects/student-workshops/rico-paramo');

function read(rel) {
  return fs.readFileSync(path.join(ROOT, rel), 'utf8');
}

function loadData() {
  const source = fs.readFileSync(path.join(RICO, 'rico-course-data.js'), 'utf8');
  const sandbox = { window: {} };
  vm.createContext(sandbox);
  vm.runInContext(source, sandbox, { filename: 'rico-course-data.js' });
  return sandbox.window.IJR_RICO_PROJECT_DATA;
}

test('Rico project has exactly four classes with dedicated theory and workshop content', () => {
  const data = loadData();
  assert.ok(data);
  assert.equal(data.classes.length, 4);

  for (const [index, cls] of data.classes.entries()) {
    assert.equal(cls.n, index + 1);
    assert.match(cls.title, /.+/);
    assert.ok(Array.isArray(cls.concepts) && cls.concepts.length >= 4);
    assert.ok(Array.isArray(cls.evidence) && cls.evidence.length >= 4);
    assert.ok(Array.isArray(cls.stages) && cls.stages.length === 5);
    assert.ok(cls.uml?.name);
    assert.ok(cls.diagram?.nodes?.length >= 4);

    for (const stage of cls.stages) {
      assert.ok(stage.key);
      assert.ok(Array.isArray(stage.tasks) && stage.tasks.length >= 3);
      assert.ok(stage.command);
      assert.ok(stage.expected);
    }
  }
});

test('Rico Theory and Workshop subpages use the senior Seminar format', () => {
  const theory = fs.readFileSync(path.join(RICO, 'theory.html'), 'utf8');
  const workshop = fs.readFileSync(path.join(RICO, 'workshop.html'), 'utf8');

  assert.match(theory, /oop-uml\/styles\.css/);
  assert.match(theory, /MENTAL MODEL/);
  assert.match(theory, /UML \/ RESPONSIBILITY VIEW/);
  assert.match(theory, /IMPLEMENTATION BRIDGE/);
  assert.match(theory, /MASTERY EVIDENCE/);
  assert.match(theory, /workshop\.html\?class=1/);

  assert.match(workshop, /oop-uml\/workshop-colab\.css/);
  assert.match(workshop, /Real Construction Workshop/);
  assert.match(workshop, /Local terminal/);
  assert.match(workshop, /auditable evidence/);
  assert.match(workshop, /theory\.html\?class=1/);
  assert.match(workshop, /id="workshopStages"/);
});

test('Rico hub exposes exactly four construction classes and no legacy eight-stage roadmap', () => {
  const hub = fs.readFileSync(path.join(RICO, 'index.html'), 'utf8');
  const progress = fs.readFileSync(path.join(RICO, 'hub.js'), 'utf8');

  assert.match(hub, /Build the complete project in four construction classes/);
  assert.match(hub, /4 construction classes · 4 class gates/);
  for (let n = 1; n <= 4; n += 1) {
    assert.match(hub, new RegExp(`id="class-0?${n}"`));
    assert.match(hub, new RegExp(`data-class="${n}"`));
    assert.match(hub, new RegExp(`theory\\.html\\?class=${n}`));
    assert.match(hub, new RegExp(`workshop\\.html\\?class=${n}`));
  }
  assert.doesNotMatch(hub, /8-sprint personal roadmap|8 stages · 4 construction classes|eight engineering stages|data-stage=/i);
  assert.match(hub, /SCOPE \/ SAFETY/);
  assert.match(hub, /No hidden autorun, persistence, control evasion or malware-like behavior/);
  assert.match(progress, /ijr-rico-four-class-progress-v2/);
  assert.match(progress, /All four construction classes are complete/);
  assert.match(progress, /localStorage/);
});

test('Project Decision Center renders the consolidated four-class Rico route', () => {
  const index = read('t3/projects/index.html');
  const js = read('t3/projects/projects.js');

  assert.match(index, /PERSONAL PROJECT BUILD · 4 CONSTRUCTION CLASSES/);
  assert.doesNotMatch(index, /8 STAGES \/ 4 CLASSES|eight-stage build|8-sprint personal roadmap/i);
  for (let n = 1; n <= 4; n += 1) {
    assert.match(index, new RegExp(`rico-paramo/theory\\.html\\?class=${n}`));
    assert.match(index, new RegExp(`rico-paramo/workshop\\.html\\?class=${n}`));
  }

  assert.match(js, /4 CONSTRUCTION CLASSES/);
  assert.match(js, /there is no separate eight-sprint roadmap for this student/);
  assert.match(js, /theory_href/);
  assert.match(js, /workshop_href/);
  assert.match(js, /theory-page-link/);
  assert.match(js, /workshop-page-link/);
});

test('Rico page scripts and all referenced local senior assets exist', () => {
  const required = [
    't3/projects/student-workshops/rico-paramo/theory.html',
    't3/projects/student-workshops/rico-paramo/workshop.html',
    't3/projects/student-workshops/rico-paramo/rico-course-data.js',
    't3/projects/student-workshops/rico-paramo/rico-pages.js',
    't3/projects/student-workshops/rico-paramo/rico-pages.css',
    't3/projects/student-workshops/rico-paramo/hub.js',
    't3/oop-uml/styles.css',
    't3/oop-uml/workshop-colab.css',
    't3/access-gate.js'
  ];

  for (const rel of required) {
    assert.ok(fs.existsSync(path.join(ROOT, rel)), `missing ${rel}`);
  }
});
