const slug = document.body.dataset.track;
const dataUrl = '../../data/studio-index.json';
const learningUrl = '../../data/track-learning.json';
const TOKEN_KEY = 'ijr-seminario-studio-edit-token-v1';
const API = 'https://rlfxnjbqxbozjdzkbwlz.supabase.co/functions/v1/seminar-studio-student';
const KEY = 'sb_publishable_rmVOQ3Orx49KpW_4uMqYew_c2HpcA87';
const BANK = '2026-09-05-v3';
const $ = id => document.getElementById(id);
const esc = (v = '') => String(v ?? '').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));

let profile = null;
let track = null;
let learningTrack = null;
let diagnostic = null;
let questions = [];

async function studioApi(action, payload = {}) {
  const edit_token = localStorage.getItem(TOKEN_KEY);
  if (!edit_token) throw new Error('studio_profile_required');
  const r = await fetch(API, {
    method: 'POST',
    headers: {'Content-Type':'application/json','apikey':KEY},
    body: JSON.stringify({action, edit_token, ...payload})
  });
  let data = null;
  try { data = await r.json(); } catch {}
  if (!r.ok) throw new Error(data?.error || `HTTP ${r.status}`);
  return data;
}

async function loadProfile() {
  try {
    const data = await studioApi('load');
    return data?.profile || null;
  } catch {
    return null;
  }
}

function insertAdaptiveSections() {
  const sprintSection = document.querySelector('.sprints')?.closest('section');
  if (!sprintSection) throw new Error('Track layout incomplete');
  const wrap = document.createElement('div');
  wrap.innerHTML = `
    <section id="diagnosticPanel" class="panel diagnostic-panel">
      <div class="adaptive-head">
        <div>
          <div class="kicker">PERSONALIZED ENTRY DIAGNOSTIC</div>
          <h2>What do you already know?</h2>
          <p id="diagnosticIntro" class="muted">Loading personalized diagnostic…</p>
        </div>
        <div id="diagnosticActions" class="actions"></div>
      </div>
      <div id="diagnosticBody"></div>
    </section>
    <section id="learningPanel" class="panel">
      <div class="adaptive-head">
        <div>
          <div class="kicker">THEORY + WORKSHOP PATH</div>
          <h2>Your personalized learning stages</h2>
          <p id="learningSummary" class="muted">Complete the diagnostic to calculate your starting stage.</p>
        </div>
      </div>
      <div id="learningStages" class="learning-stages"></div>
    </section>`;
  const nodes = [...wrap.children];
  nodes.reverse().forEach(node => sprintSection.parentNode.insertBefore(node, sprintSection));
}

function renderTrackHeader() {
  document.title = `${track.title} · Software Engineering Studio`;
  $('trackTitle').textContent = track.title;
  $('projectTitle').textContent = track.project;
  $('stack').innerHTML = track.stack.map(x => `<span>${esc(x)}</span>`).join('');
  $('examples').innerHTML = track.examples.map(x => `<li>${esc(x)}</li>`).join('');
  const current = profile && profile.track_slug === slug ? Number(profile.sprint_current || 1) : 0;
  $('personal').textContent = profile
    ? profile.track_slug === slug
      ? `${profile.full_name} · Sprint ${profile.sprint_current}/8 · ${profile.progress_percent}%`
      : `${profile.full_name} · tu ruta oficial es ${profile.first_choice}. Este diagnóstico de ${track.title} queda guardado como exploración individual.`
    : 'Explora el syllabus. Regístrate en My Studio para activar diagnóstico y ruta personalizada.';
  $('sprints').innerHTML = track.sprints.map(s => `
    <article class="sprint ${s.n === current ? 'current' : ''}">
      <div class="n">S${s.n}</div>
      <div><strong>${esc(s.title)}</strong><p>${esc(s.goal)}</p></div>
      <div><span class="kicker">DELIVERABLE</span><p>${esc(s.deliverable)}</p></div>
    </article>`).join('');
}

function stageStatus(stageNo) {
  if (!diagnostic || diagnostic.status !== 'completed') return 'locked';
  const highest = Number(diagnostic.highest_mastered_stage || 0);
  const recommended = Number(diagnostic.recommended_stage || 1);
  if (stageNo <= highest) return 'mastered';
  if (stageNo === recommended) return 'current';
  return 'locked';
}

function renderLearningPath() {
  const box = $('learningStages');
  if (!learningTrack || !box) return;
  if (learningTrack.safety) {
    $('learningSummary').innerHTML = `<strong>Safety boundary:</strong> ${esc(learningTrack.safety)}`;
  } else if (diagnostic?.status === 'completed') {
    const h = Number(diagnostic.highest_mastered_stage || 0);
    $('learningSummary').textContent = h >= 4
      ? 'All four conceptual stages were credited. Keep them available for review and move into project execution.'
      : `Stages 1–${h || 0} are credited. Stage ${diagnostic.recommended_stage} is your active Theory + Workshop starting point.`;
  } else {
    $('learningSummary').textContent = 'Complete the diagnostic to calculate the highest contiguous stage you already master.';
  }

  box.innerHTML = learningTrack.stages.map(s => {
    const state = stageStatus(s.n);
    const accessible = state !== 'locked';
    const score = diagnostic?.stage_scores?.[String(s.n)];
    const scoreText = score ? `${score.score}/${score.max} · ${score.percent}%` : 'Not evaluated';
    const badge = state === 'mastered' ? 'MASTERED · REVIEW AVAILABLE'
      : state === 'current' ? 'ACTIVE LEARNING STAGE'
      : 'LOCKED UNTIL PRIOR STAGE';
    const theory = accessible ? `
      <details class="stage-detail">
        <summary>Theory</summary>
        <div class="detail-body">
          <p><strong>${esc(s.focus)}</strong></p>
          <ul>${s.theory.map(x => `<li>${esc(x)}</li>`).join('')}</ul>
        </div>
      </details>` : '';
    const workshop = accessible ? `
      <details class="stage-detail">
        <summary>Workshop</summary>
        <div class="detail-body">
          <ol>${s.workshop.map(x => `<li>${esc(x)}</li>`).join('')}</ol>
          <p class="evidence"><strong>Evidence:</strong> ${esc(s.evidence)}</p>
        </div>
      </details>` : '';
    return `
      <article class="learning-stage ${state}">
        <div class="stage-top">
          <div><span class="stage-number">STAGE ${s.n}</span><h3>${esc(s.title)}</h3></div>
          <div class="stage-result"><span class="stage-badge">${badge}</span><span>${scoreText}</span></div>
        </div>
        <p>${esc(s.focus)}</p>
        ${accessible ? theory + workshop : '<div class="locked-note">Complete the active stage before moving forward.</div>'}
      </article>`;
  }).join('');
}

function resultLabel(level) {
  return ({foundation:'Foundation',developing:'Developing',proficient:'Proficient',advanced:'Advanced'})[level] || level || '—';
}

function renderDiagnosticStatus() {
  const intro = $('diagnosticIntro');
  const actions = $('diagnosticActions');
  const body = $('diagnosticBody');
  if (!profile) {
    intro.textContent = 'A private Studio profile is required so the result belongs to the correct student.';
    actions.innerHTML = '<a class="button" href="../../studio/">Register in My Studio</a>';
    body.innerHTML = '<div class="notice">The diagnostic does not accept anonymous mastery claims. Register first, then return to this project page.</div>';
    renderLearningPath();
    return;
  }

  if (diagnostic?.status === 'completed') {
    const h = Number(diagnostic.highest_mastered_stage || 0);
    const next = Number(diagnostic.recommended_stage || 1);
    intro.textContent = `Personalized result for ${profile.full_name}. Mastery is computed on the server; later stages stay locked until prerequisite knowledge is demonstrated.`;
    actions.innerHTML = '<button id="retakeDiagnostic" class="secondary" type="button">Retake diagnostic</button>';
    $('retakeDiagnostic').addEventListener('click', startDiagnostic);
    const safety = ['cybersecurity','robotics'].includes(slug)
      ? '<div class="safety-gate">Critical safety/authorization questions are mandatory gates. A high total score cannot bypass a failed critical gate.</div>'
      : '';
    body.innerHTML = `
      <div class="diag-metrics">
        <div><span>Knowledge</span><strong>${Number(diagnostic.knowledge_percent || 0).toFixed(1)}%</strong></div>
        <div><span>Level</span><strong>${esc(resultLabel(diagnostic.level))}</strong></div>
        <div><span>Mastered</span><strong>${h}/4 stages</strong></div>
        <div><span>Start here</span><strong>Stage ${next}</strong></div>
      </div>
      ${safety}
      <p class="muted small">Rule: only consecutive mastered stages receive prior-knowledge credit. The first unmet stage becomes the active Theory + Workshop stage; later stages remain locked.</p>`;
    renderLearningPath();
    return;
  }

  intro.textContent = '15 questions · 12 knowledge checks + 3 self-profile items · one result for this student and this project track.';
  actions.innerHTML = '<button id="startDiagnostic" type="button">Start diagnostic</button>';
  $('startDiagnostic').addEventListener('click', startDiagnostic);
  body.innerHTML = `<div class="diag-empty">No completed ${esc(track.title)} diagnostic is stored for this student yet.</div>`;
  renderLearningPath();
}

async function loadDiagnosticStatus() {
  if (!profile) {
    diagnostic = null;
    renderDiagnosticStatus();
    return;
  }
  try {
    diagnostic = await studioApi('diagnostic-status', {track_slug: slug});
  } catch (e) {
    diagnostic = null;
    $('diagnosticIntro').textContent = 'Diagnostic backend unavailable.';
    $('diagnosticActions').innerHTML = '';
    $('diagnosticBody').innerHTML = `<div class="notice">Could not load personalized diagnostic: ${esc(e.message)}</div>`;
    renderLearningPath();
    return;
  }
  renderDiagnosticStatus();
}

function questionCard(q, index) {
  const stage = q.stage_no ? learningTrack.stages.find(s => s.n === Number(q.stage_no)) : null;
  const section = stage ? `Stage ${stage.n} · ${stage.title}` : 'Self profile';
  return `
    <fieldset class="diag-question" data-question="${esc(q.id)}">
      <legend><span>${index + 1}. ${esc(q.prompt)}</span><small>${esc(section)}</small></legend>
      <div class="diag-options">
        ${(Array.isArray(q.options) ? q.options : []).map((opt, i) => `
          <label>
            <input type="radio" name="${esc(q.id)}" value="${i}" required>
            <span>${esc(opt)}</span>
          </label>`).join('')}
      </div>
    </fieldset>`;
}

async function startDiagnostic() {
  if (!profile) return;
  const actions = $('diagnosticActions');
  const body = $('diagnosticBody');
  actions.innerHTML = '';
  $('diagnosticIntro').textContent = 'Loading the current project-specific question bank…';
  body.innerHTML = '<div class="diag-empty">Preparing diagnostic…</div>';
  try {
    const [qs, attempt] = await Promise.all([
      studioApi('diagnostic-questions', {track_slug:slug, bank_version:BANK}),
      studioApi('diagnostic-start', {track_slug:slug, bank_version:BANK})
    ]);
    if (!Array.isArray(qs) || qs.length !== 15) throw new Error('question_bank_incomplete');
    questions = qs;
    $('diagnosticIntro').textContent = `Diagnostic in progress · ${profile.full_name} · answer all 15 items. No answer key is sent to the browser.`;
    body.innerHTML = `
      ${learningTrack.safety ? `<div class="safety-gate">${esc(learningTrack.safety)}</div>` : ''}
      <form id="diagnosticForm">
        <div class="diag-question-list">${questions.map(questionCard).join('')}</div>
        <div class="diag-submit">
          <button id="submitDiagnostic" type="submit">Submit and calculate my path</button>
          <span id="diagnosticFormStatus" class="status"></span>
        </div>
      </form>`;
    $('diagnosticForm').addEventListener('submit', async e => {
      e.preventDefault();
      const answers = {};
      for (const q of questions) {
        const selected = document.querySelector(`input[name="${CSS.escape(q.id)}"]:checked`);
        if (!selected) {
          $('diagnosticFormStatus').textContent = 'Answer every item before submitting.';
          return;
        }
        answers[q.id] = Number(selected.value);
      }
      $('submitDiagnostic').disabled = true;
      $('diagnosticFormStatus').textContent = 'Calculating stage mastery on the server…';
      try {
        diagnostic = await studioApi('diagnostic-submit', {
          attempt_id: attempt.attempt_id,
          answers
        });
        renderDiagnosticStatus();
        $('diagnosticPanel').scrollIntoView({behavior:'smooth', block:'start'});
      } catch (err) {
        $('submitDiagnostic').disabled = false;
        $('diagnosticFormStatus').textContent = `Could not submit: ${err.message}`;
      }
    });
  } catch (e) {
    $('diagnosticIntro').textContent = 'Could not start the diagnostic.';
    body.innerHTML = `<div class="notice">${esc(e.message)}</div>`;
    actions.innerHTML = '<button id="retryDiagnostic" class="secondary" type="button">Try again</button>';
    $('retryDiagnostic').addEventListener('click', startDiagnostic);
  }
}

Promise.all([
  fetch(dataUrl).then(r => {
    if (!r.ok) throw new Error('Studio manifest unavailable');
    return r.json();
  }),
  fetch(learningUrl).then(r => {
    if (!r.ok) throw new Error('Learning-stage manifest unavailable');
    return r.json();
  }),
  loadProfile()
]).then(([root, learning, loadedProfile]) => {
  const studio = root.studio;
  track = studio.tracks.find(t => t.slug === slug);
  learningTrack = learning.tracks.find(t => t.slug === slug);
  profile = loadedProfile;
  if (!track || !learningTrack) throw new Error('Track not found');
  if (learning.version !== BANK || Number(learning.stageCount) !== 4) throw new Error('Learning policy version mismatch');
  renderTrackHeader();
  insertAdaptiveSections();
  renderLearningPath();
  return loadDiagnosticStatus();
}).catch(err => {
  if ($('personal')) $('personal').textContent = `No fue posible cargar el track: ${err.message}`;
});
