import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

test('OOP + UML registration asks for institutional email only', async()=>{
  const html=await readFile('t3/oop-uml/index.html','utf8');
  assert.match(html,/id="institutionalEmail"/);
  assert.match(html,/type="email"/);
  assert.doesNotMatch(html,/id="groupCode"/);
  assert.doesNotMatch(html,/id="memberName1"/);
  assert.doesNotMatch(html,/id="registrationMode"/);
  assert.doesNotMatch(html,/type="password"/);
});

test('OOP + UML email registration uses the dedicated Supabase RPC', async()=>{
  const hub=await readFile('t3/oop-uml/hub.js','utf8');
  const store=await readFile('t3/js/course-store.js','utf8');
  assert.match(hub,/startWithEmail/);
  assert.match(store,/seminar_oop_uml_start_email_v8/);
});
