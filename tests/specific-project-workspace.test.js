import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const read=p=>fs.readFileSync(p,'utf8');

test('specific project workspace uses central institutional identity and tracked backend',()=>{
  const hub=read('t3/projects/workspace/index.html');
  const unit=read('t3/projects/workspace/unit.html');
  const js=read('t3/projects/workspace/workspace.js');
  assert.match(hub,/Specific Project Workspace/);
  assert.match(unit,/Project Unit/);
  assert.doesNotMatch(hub,/id="institutionalEmail"/);
  assert.doesNotMatch(unit,/id="institutionalEmail"/);
  assert.match(js,/IJRSeminarAccess/);
  assert.match(js,/action:'load'/);
  assert.match(js,/action:'save_progress'/);
  assert.match(js,/project_gate_requirements_missing/);
  assert.match(js,/previous_project_unit_incomplete/);
});

test('workspace renders actual project units and four auditable gate checks',()=>{
  const js=read('t3/projects/workspace/workspace.js');
  const unit=read('t3/projects/workspace/unit.html');
  for(const key of ['defined','built','tested','evidence']) assert.match(unit,new RegExp('data-check="'+key+'"'));
  assert.match(js,/state\.project\.sprints/);
  assert.match(js,/progress_percent/);
  assert.match(js,/gate_passed/);
  assert.match(js,/evidence_note/);
  assert.match(js,/repo_ref/);
});

test('backend source constrains and persists project progress',()=>{
  const edge=read('supabase/functions/seminar-project-access/index.ts');
  const migration=read('supabase/migrations/20260930134500_seminar_specific_project_workspace_v1.sql');
  assert.match(edge,/save_progress/);
  assert.match(edge,/WORKSPACE_CHECKS/);
  assert.match(edge,/previous_project_unit_incomplete/);
  assert.match(edge,/seminar_project_unit_progress/);
  assert.match(migration,/create table if not exists public\.seminar_project_unit_progress/);
  assert.match(migration,/seminar_master_dashboard_v4/);
  assert.match(migration,/gate_passed/);
});

test('teacher master exposes project units and gates',()=>{
  const master=read('t3/js/teacher.js');
  const html=read('t3/teacher.html');
  assert.match(master,/specific_project/);
  assert.match(master,/completed_units/);
  assert.match(master,/Unit .*gates/);
  assert.match(html,/Specific Project Workspace/);
});

test('Seminar home routes hour 2 to the specific project workspace',()=>{
  const html=read('t3/index.html');
  assert.match(html,/projects\/workspace/);
  assert.match(html,/Abrir mi Proyecto Específico/);
});

test('coding projects expose a persistent interactive source workspace',()=>{
  const unit=read('t3/projects/workspace/unit.html');
  const js=read('t3/projects/workspace/workspace.js');
  assert.match(unit,/id="codeLabPanel"/);
  assert.match(unit,/id="projectCodeEditor"/);
  assert.match(unit,/id="runCode"/);
  assert.match(unit,/id="webPreview"/);
  assert.match(js,/save_code_file/);
  assert.match(js,/record_code_run/);
  assert.match(js,/loadPyodide/);
  assert.match(js,/buildWebSrcdoc/);
  assert.match(js,/TODO_BUILD/);
  assert.match(js,/scheduleCodeSave/);
});

test('live code backend persists files, runtime state and gate snapshots',()=>{
  const edge=read('supabase/functions/seminar-project-access/index.ts');
  const migration=read('supabase/migrations/20260930153000_seminar_specific_project_live_code_v2.sql');
  for(const table of ['seminar_project_code_files','seminar_project_code_runtime','seminar_project_code_snapshots']) {
    assert.match(migration,new RegExp('create table if not exists public\\.'+table));
    assert.match(edge,new RegExp(table));
  }
  assert.match(edge,/project_code_run_required/);
  assert.match(edge,/project_code_incomplete/);
  assert.match(edge,/last_run_ok/);
  assert.match(migration,/seminar_master_dashboard_v5/);
});

test('teacher master surfaces saved project code and runtime status',()=>{
  const master=read('t3/js/teacher.js');
  assert.match(master,/sp\.code/);
  assert.match(master,/Code workspaces/);
  assert.match(master,/runtime PASS/);
  assert.match(master,/snapshot_count/);
});
