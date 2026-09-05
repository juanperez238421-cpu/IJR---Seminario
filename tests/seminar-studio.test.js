import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
const read=p=>fs.readFileSync(new URL(`../${p}`,import.meta.url),'utf8');

const TRACKS=['web','data-science','cybersecurity','3d-programming','robotics'];

test('Studio manifest has one common core and exactly five tracks',()=>{
  const x=JSON.parse(read('t3/data/studio-index.json')).studio;
  assert.equal(x.commonCore.length,10);
  assert.deepEqual(x.tracks.map(t=>t.slug),TRACKS);
  x.tracks.forEach(t=>assert.equal(t.sprints.length,8));
});

test('Personalized project learning manifest has four Theory + Workshop stages per track',()=>{
  const x=JSON.parse(read('t3/data/track-learning.json'));
  assert.equal(x.version,'2026-09-05-v3');
  assert.equal(x.stageCount,4);
  assert.deepEqual(x.tracks.map(t=>t.slug),TRACKS);
  x.tracks.forEach(t=>{
    assert.equal(t.stages.length,4);
    assert.deepEqual(t.stages.map(s=>s.n),[1,2,3,4]);
    t.stages.forEach(s=>{
      assert.ok(s.title.length>3);
      assert.ok(s.focus.length>8);
      assert.ok(s.theory.length>=3);
      assert.ok(s.workshop.length>=3);
      assert.ok(s.evidence.length>5);
    });
  });
});

test('Every project page is wired to the shared adaptive track runtime with fresh assets',()=>{
  TRACKS.forEach(slug=>{
    const html=read(`t3/tracks/${slug}/index.html`);
    assert.match(html,new RegExp(`data-track=["']${slug}["']`));
    assert.match(html,/track\.js\?v=20260905-1/);
    assert.match(html,/track\.css\?v=20260905-1/);
  });
});

test('Track runtime requires Studio identity and uses Edge-gateway diagnostic actions',()=>{
  const js=read('t3/tracks/track.js');
  assert.match(js,/ijr-seminario-studio-edit-token-v1/);
  assert.match(js,/seminar-studio-student/);
  assert.match(js,/2026-09-05-v3/);
  assert.match(js,/diagnostic-status/);
  assert.match(js,/diagnostic-questions/);
  assert.match(js,/diagnostic-start/);
  assert.match(js,/diagnostic-submit/);
  assert.match(js,/qs\.length !== 15/);
  assert.match(js,/stageCount\) !== 4/);
  assert.match(js,/ACTIVE LEARNING STAGE/);
  assert.match(js,/LOCKED UNTIL PRIOR STAGE/);
  assert.doesNotMatch(js,/rest\/v1\/rpc/);
  assert.doesNotMatch(js,/correct_option/);
});

test('Student Edge gateway enforces origin + token and is sole browser route for diagnostics',()=>{
  const edge=read('supabase/functions/seminar-studio-student/index.ts');
  assert.match(edge,/DIAGNOSTIC_BANK = "2026-09-05-v3"/);
  assert.match(edge,/allowedOrigins/);
  assert.match(edge,/validToken/);
  assert.match(edge,/profile_not_found/);
  assert.match(edge,/diagnostic-status/);
  assert.match(edge,/diagnostic-questions/);
  assert.match(edge,/diagnostic-start/);
  assert.match(edge,/diagnostic-submit/);
  assert.match(edge,/admin\.rpc\("seminar_track_diagnostic_status"/);
  assert.match(edge,/admin\.rpc\("seminar_track_diagnostic_submit"/);
  assert.match(edge,/sprint_not_released/);
  assert.doesNotMatch(edge,/correct_option/);
});

test('Defensive cybersecurity track preserves authorized-only scope and critical gating',()=>{
  const html=read('t3/tracks/cybersecurity/index.html');
  const learning=read('t3/data/track-learning.json');
  const migration=read('supabase/migrations/20260905130000_seminar_track_personalized_diagnostics_v3.sql');
  assert.match(html,/AUTHORIZED DEFENSIVE SCOPE/);
  assert.match(html,/No external target exploitation/);
  assert.match(learning,/Authorized defensive scope only/);
  assert.match(learning,/sandboxed or explicitly authorized systems/);
  assert.match(migration,/cybersecurity.+position in \(2,6,9,10,11\)/s);
  assert.match(migration,/cybersecurity-s1-authorized-scope/);
});

test('Robotics track emphasizes simulation, fail-safe reasoning and hardware limits',()=>{
  const learning=read('t3/data/track-learning.json');
  const migration=read('supabase/migrations/20260905130000_seminar_track_personalized_diagnostics_v3.sql');
  assert.match(learning,/Simulate first/);
  assert.match(learning,/State machines, validation & fail-safe/);
  assert.match(learning,/voltage\/current\/polarity/);
  assert.match(migration,/robotics.+position in \(5,6,9,11\)/s);
});

test('Diagnostic migration binds attempts to private Studio profiles and computes mastery only on server',()=>{
  const sql=read('supabase/migrations/20260905130000_seminar_track_personalized_diagnostics_v3.sql');
  assert.match(sql,/studio_profile_id uuid/);
  assert.match(sql,/stage_scores jsonb/);
  assert.match(sql,/highest_mastered_stage/);
  assert.match(sql,/recommended_stage/);
  assert.match(sql,/critical_gates/);
  assert.match(sql,/seminar_track_diagnostic_status/);
  assert.match(sql,/v_stage_percent >= 66\.7/);
  assert.match(sql,/security definer/);
  assert.match(sql,/set search_path=''/);
  assert.match(sql,/revoke all on table public\.seminar_track_diagnostic_questions from anon, authenticated/);
});

test('Diagnostic RPCs are hardened behind service-role Edge gateway',()=>{
  const sql=read('supabase/migrations/20260905140000_seminar_track_diagnostic_edge_gateway_hardening.sql');
  for(const fn of ['get_questions','start','submit','snapshot','status']){
    assert.match(sql,new RegExp(`seminar_track_diagnostic_${fn}`));
  }
  assert.match(sql,/from public, anon, authenticated/);
  assert.match(sql,/to service_role/);
});

test('Public T3 navigation exposes Studio but not private Studio teacher route',()=>{
  const html=read('t3/index.html');
  assert.match(html,/studio\//);
  assert.doesNotMatch(html,/studio\/teacher\.html/);
});

test('Student Studio uses one constrained Edge Function and first-choice routing',()=>{
  const js=read('t3/studio/app.js');
  assert.match(js,/seminar-studio-student/);
  assert.match(js,/first_choice/);
  assert.match(js,/track_slug/);
});

test('Private teacher view uses MFA gateway and exposes diagnostic summaries without answer keys',()=>{
  const html=read('t3/studio/teacher.html');
  const js=read('t3/studio/teacher.js');
  assert.match(html,/<th>Diagnostic<\/th>/);
  assert.match(js,/teacher-auth-gateway/);
  assert.match(js,/seminar_studio_dashboard/);
  assert.match(js,/getAuthenticatorAssuranceLevel/);
  assert.match(js,/highest_mastered_stage/);
  assert.match(js,/critical_gates/);
  assert.doesNotMatch(js,/from\(['"]seminar_studio_profiles/);
  assert.doesNotMatch(js,/correct_option/);
});
