import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { execFileSync } from 'node:child_process';

const read = p => fs.readFileSync(new URL(`../${p}`, import.meta.url), 'utf8');

test('cyber lab binds the web target to localhost and uses an internal Docker network', () => {
  const compose = read('t3/tracks/cybersecurity/lab/docker-compose.yml');
  assert.match(compose, /127\.0\.0\.1:8080:80/);
  assert.match(compose, /internal:\s*true/);
});

test('controlled traffic runner has a fixed internal target and no arbitrary target input', () => {
  const runner = read('t3/tracks/cybersecurity/lab/attack-runner/runner.py');
  assert.match(runner, /TARGET = "http:\/\/proxy"/);
  assert.doesNotMatch(runner, /TARGET_URL/);
  assert.doesNotMatch(runner, /sys\.argv/);
  assert.doesNotMatch(runner, /input\(/);
  assert.match(runner, /ALLOWED_PROFILES/);
});

test('cyber lab documentation explicitly prohibits external targets', () => {
  const readme = read('t3/tracks/cybersecurity/lab/README.md');
  assert.match(readme, /does not accept arbitrary domains, public IP addresses, or target URLs/);
  assert.match(readme, /Do not redirect, rewrite, proxy, or adapt the traffic runner to public websites/);
});


test('project center exposes four guided real defensive cyber cases', () => {
  const html = read('t3/projects/index.html');
  assert.match(html, /CASE 01/);
  assert.match(html, /HTTP Flood/);
  assert.match(html, /Credential Abuse/);
  assert.match(html, /Broken Access Control/);
  assert.match(html, /Stored HTML \/ XSS Defense/);
});

test('real cyber cases keep executable examples on localhost or internal Docker services', () => {
  const caseFiles = [
    't3/projects/cyber-cases/case-01-http-flood.html',
    't3/projects/cyber-cases/case-02-auth-abuse.html',
    't3/projects/cyber-cases/case-03-broken-access-control.html',
    't3/projects/cyber-cases/case-04-stored-xss.html'
  ];
  for (const file of caseFiles) {
    const html = read(file);
    assert.doesNotMatch(html, /https?:\/\/(?!127\.0\.0\.1|github\.com|proxy(?:\/|<|\s))/);
  }
});

test('target app contains only synthetic access-control records and local board case', () => {
  const app = read('t3/tracks/cybersecurity/lab/app/server.js');
  assert.match(app, /Synthetic record A/);
  assert.match(app, /\/api\/records/);
  assert.match(app, /\/board/);
  assert.match(app, /INTENTIONAL LAB STARTING POINT/);
});


test('target lab server passes Node syntax validation', () => {
  const serverPath = new URL('../t3/tracks/cybersecurity/lab/app/server.js', import.meta.url);
  execFileSync(process.execPath, ['--check', serverPath.pathname], { stdio: 'pipe' });
});
