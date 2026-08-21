import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import {fileURLToPath} from 'node:url';

const here=path.dirname(fileURLToPath(import.meta.url));
const root=path.join(here,'..');
const read=rel=>fs.readFileSync(path.join(root,rel),'utf8');
const config=read('t3/oop-logic-01/config.js');
const student=read('t3/oop-logic-01/index.html');
const app=read('t3/oop-logic-01/app.js');
const teacher=read('t3/oop-logic-01/teacher.js');
const migration=read('supabase/migrations/20260821142615_seminar_oop_logic_01_question_lab.sql');

test('OOP Logic Lab exposes the 12-question / 36-pack contract',()=>{
  assert.match(config,/questionCount:\s*12/);
  assert.match(config,/variantBankSize:\s*36/);
  assert.match(config,/helpTokenLimit:\s*3/);
  assert.match(student,/12 QUESTIONS/);
  assert.match(student,/36 packs/);
  assert.match(student,/1 estudiante/);
  assert.match(student,/3 estudiantes/);
});

test('student flow is server-validated and contains no embedded answer bank',()=>{
  for(const rpc of ['seminar_oop_start_team_v1','seminar_oop_resume_v1','seminar_oop_submit_v1','seminar_oop_use_help_v1','seminar_oop_reveal_v1','seminar_oop_skip_v1']) assert.match(config,new RegExp(rpc));
  assert.match(app,/cfg\.rpc\.submit/);
  assert.match(app,/cfg\.rpc\.reveal/);
  assert.doesNotMatch(app,/expected_text\s*:/i);
});

test('migration seeds 36 persistent packs across all 12 checkpoints',()=>{
  assert.match(migration,/generate_series\(1,36\)/);
  for(let i=1;i<=12;i++) assert.match(migration,new RegExp(`'Q${String(i).padStart(2,'0')}'`));
  assert.match(migration,/least_used_random_4h/);
  assert.match(migration,/learning_activity_attempt_variant_pack/);
});

test('teacher dashboard uses activity-specific protected RPCs',()=>{
  assert.match(config,/teacher_seminar_oop_dashboard_v1/);
  assert.match(config,/teacher_seminar_oop_detail_v1/);
  assert.match(teacher,/cfg\.rpc\.teacherDashboard/);
  assert.match(teacher,/cfg\.rpc\.teacherDetail/);
  assert.match(teacher,/teacherLogin/);
});
