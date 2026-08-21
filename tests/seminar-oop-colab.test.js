import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

const read=p=>fs.readFileSync(new URL(`../${p}`,import.meta.url),'utf8');
const html=read('t3/oop-logic-01/index.html');
const config=read('t3/oop-logic-01/config.js');
const app=read('t3/oop-logic-01/app.js');
const teacherHtml=read('t3/oop-logic-01/teacher.html');
const teacherJs=read('t3/oop-logic-01/teacher.js');

test('OOP student page is a real Python Colab-style lab',()=>{
  assert.match(html,/pyodide\/v0\.27\.7/);
  assert.match(html,/id="codeEditor"/);
  assert.match(html,/id="runCellButton"/);
  assert.match(html,/Python console/);
  assert.match(app,/loadPyodide/);
  assert.match(app,/runPythonAsync/);
});

test('OOP activity is dedicated and server validated',()=>{
  assert.match(config,/seminar11-oop-colab-01-2026/);
  for(const rpc of ['seminar_oop_colab_start_v1','seminar_oop_colab_resume_v1','seminar_oop_colab_submit_v1','seminar_oop_colab_help_v1','seminar_oop_colab_reveal_v1','seminar_oop_colab_skip_v1']) assert.match(config,new RegExp(rpc));
  for(let i=1;i<=12;i++) assert.match(app,new RegExp(`P${String(i).padStart(2,'0')}:`));
  assert.match(app,/structureCheck/);
});

test('OOP teacher page is an independent live master',()=>{
  assert.match(teacherHtml,/Python OOP Colab · Live Master/);
  assert.match(teacherHtml,/id="exportButton"/);
  assert.match(config,/teacher_seminar_oop_colab_dashboard_v1/);
  assert.match(config,/teacher_seminar_oop_colab_detail_v1/);
  assert.match(teacherJs,/LIVE · 3 s/);
  assert.match(teacherJs,/exportCsv/);
});
