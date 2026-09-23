import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

test('OOP + UML registration contains exactly one student credential field: institutional email', async()=>{
  const html=await readFile('t3/oop-uml/index.html','utf8');
  const panel=html.split('<section id="registrationPanel"')[1].split('<main id="hubPanel"')[0];

  assert.match(panel,/id="institutionalEmail"/);
  assert.match(panel,/type="email"/);
  assert.match(panel,/@ijr\.edu\.co/);
  assert.equal((panel.match(/<input\b/g)||[]).length,1);
  assert.equal((panel.match(/<select\b/g)||[]).length,0);

  assert.doesNotMatch(panel,/id="groupCode"/);
  assert.doesNotMatch(panel,/id="memberName1"/);
  assert.doesNotMatch(panel,/id="registrationMode"/);
  assert.doesNotMatch(panel,/id="language"/);
  assert.doesNotMatch(panel,/type="password"/);
  assert.doesNotMatch(panel,/Full name/);
});

test('OOP + UML email is resolved through the dedicated Supabase roster RPC', async()=>{
  const hub=await readFile('t3/oop-uml/hub.js','utf8');
  const store=await readFile('t3/js/course-store.js','utf8');

  assert.match(hub,/ensureEmailOnlyRegistration/);
  assert.match(hub,/startWithEmail\(\{email,language:'python'\}\)/);
  assert.doesNotMatch(hub,/store\.start\(\{language,group,names/);
  assert.match(store,/seminar_oop_uml_start_email_v8/);
  assert.match(store,/attemptId:data\.attempt_id,token:data\.attempt_token,email/);
});
