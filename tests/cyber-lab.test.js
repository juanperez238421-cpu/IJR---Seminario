import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';

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
