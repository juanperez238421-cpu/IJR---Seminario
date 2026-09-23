import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

test('OOP + UML uses one institutional-email gate and no manual roster fields', async()=>{
  const html=await readFile('t3/oop-uml/index.html','utf8');
  const gate=await readFile('t3/access-gate.js','utf8');
  assert.match(html,/access-gate\.js/);
  assert.doesNotMatch(html,/id="groupCode"/);
  assert.doesNotMatch(html,/id="memberName1"/);
  assert.doesNotMatch(html,/id="registrationMode"/);
  assert.doesNotMatch(html,/id="language"/);
  assert.doesNotMatch(html,/type="password"/);
  assert.match(gate,/type="email"/);
  assert.match(gate,/@ijr\.edu\.co/);
  assert.doesNotMatch(gate,/type="password"/);
});

test('validated email automatically opens the dedicated Supabase OOP + UML session', async()=>{
  const hub=await readFile('t3/oop-uml/hub.js','utf8');
  const store=await readFile('t3/js/course-store.js','utf8');
  assert.match(hub,/IJRSeminarAccess\.ready/);
  assert.match(hub,/startWithEmail/);
  assert.match(store,/seminar_oop_uml_start_email_v8/);
  assert.match(store,/attemptId:data\.attempt_id,token:data\.attempt_token,email/);
});
