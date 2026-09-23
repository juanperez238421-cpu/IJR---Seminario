import test from 'node:test';
import assert from 'node:assert/strict';
import {readFile} from 'node:fs/promises';

const studentPages = [
  't3/index.html',
  't3/lab.html',
  't3/common/index.html',
  't3/oop-logic-01/index.html',
  't3/oop-uml/index.html',
  't3/oop-uml/theory.html',
  't3/oop-uml/workshop.html',
  't3/projects/index.html',
  't3/studio/index.html',
  't3/studio/projects/index.html',
  't3/tracks/index.html',
  't3/tracks/3d-programming/index.html',
  't3/tracks/cybersecurity/index.html',
  't3/tracks/data-science/index.html',
  't3/tracks/robotics/index.html',
  't3/tracks/web/index.html'
];

test('all student-facing Seminar T3 pages require institutional email access', async () => {
  for (const page of studentPages) {
    const html = await readFile(page, 'utf8');
    if (page === 't3/oop-uml/index.html') {
      assert.match(html, /id="institutionalEmail"/, page + ' must expose the direct institutional email field');
      assert.match(html, /type="email"/, page + ' must use an email input');
      assert.doesNotMatch(html, /id="memberName1"|id="groupCode"|id="registrationMode"/, page + ' must not expose legacy manual identity fields');
    } else {
      assert.match(html, /access-gate\.js/, page + ' must load access-gate.js');
    }
  }
});

test('gate requests only institutional email and validates through Supabase', async () => {
  const source = await readFile('t3/access-gate.js', 'utf8');
  assert.match(source, /seminar_email_access_v1/);
  assert.match(source, /@ijr\.edu\.co/);
  assert.match(source, /type="email"/);
  assert.doesNotMatch(source, /type="password"/);
  assert.doesNotMatch(source, /studentName1|groupCode/);
});
