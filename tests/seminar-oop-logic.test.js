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
const legacyMigration=read('supabase/migrations/20260821142615_seminar_oop_logic_01_question_lab.sql');

test('Python OOP Colab exposes the 12-stage / 36-pack contract',()=>{
  assert.match(config,/questionCount:\s*12/);
  assert.match(config,/variantBankSize:\s*36/);
  assert.match(config,/helpTokenLimit:\s*3/);
  assert.match(student,/12 stages/i);
  assert.match(student,/36 equivalent workstation packs/i);
  assert.match(student,/2 students/);
  assert.match(student,/3 students/);
  assert.match(student,/Google Colab-style workspace/i);
});

test('student flow uses dedicated server validation plus real Python execution',()=>{
  for(const rpc of ['seminar_oop_colab_start_v1','seminar_oop_colab_resume_v1','seminar_oop_colab_submit_v1','seminar_oop_colab_help_v1','seminar_oop_colab_reveal_v1','seminar_oop_colab_skip_v1']) assert.match(config,new RegExp(rpc));
  assert.match(app,/cfg\.rpc\.submit/);
  assert.match(app,/cfg\.rpc\.reveal/);
  assert.match(app,/runPythonAsync/);
  assert.match(app,/structureCheck/);
  assert.doesNotMatch(app,/expected_text\s*:/i);
});

test('legacy OOP migration retains randomized-pack infrastructure for backwards compatibility',()=>{
  assert.match(legacyMigration,/generate_series\(1,36\)/);
  assert.match(legacyMigration,/least_used_random_4h/);
  assert.match(legacyMigration,/learning_activity_attempt_variant_pack/);
});

test('teacher dashboard uses protected OOP RPCs through institutional MFA gateway',()=>{
  assert.match(config,/teacher_seminar_oop_colab_dashboard_v1/);
  assert.match(config,/teacher_seminar_oop_colab_detail_v1/);
  assert.match(config,/teacher_seminar_oop_colab_delete_v1/);
  assert.match(teacher,/cfg\.rpc\.teacherDashboard/);
  assert.match(teacher,/cfg\.rpc\.teacherDetail/);
  assert.match(teacher,/cfg\.rpc\.teacherDelete/);
  assert.match(teacher,/teacher-auth-gateway/);
  assert.match(teacher,/getAuthenticatorAssuranceLevel/);
  assert.match(teacher,/currentLevel==='aal2'/);
  assert.match(teacher,/signInWithPassword/);
  assert.doesNotMatch(teacher,/teacher_code_login/);
});
