(() => {
  const KEY = 'ijr-rico-portable-build-progress-v1';
  const stages = [...document.querySelectorAll('.build-stage')];
  const inputs = [...document.querySelectorAll('input[data-check]')];
  const progressText = document.getElementById('progressText');
  const progressBar = document.getElementById('progressBar');
  const nextStageText = document.getElementById('nextStageText');
  const reset = document.getElementById('resetProgress');

  function readState() {
    try { return JSON.parse(localStorage.getItem(KEY) || '{}') || {}; }
    catch { return {}; }
  }

  function writeState(state) {
    try { localStorage.setItem(KEY, JSON.stringify(state)); } catch {}
  }

  function stageComplete(stage) {
    const boxes = [...stage.querySelectorAll('input[data-check]')];
    return boxes.length > 0 && boxes.every(box => box.checked);
  }

  function update() {
    const complete = stages.filter(stageComplete);
    stages.forEach(stage => {
      const done = stageComplete(stage);
      stage.classList.toggle('is-complete', done);
      const status = stage.querySelector('.build-status');
      if (status) status.textContent = done ? 'COMPLETE' : 'NOT COMPLETE';
    });

    const count = complete.length;
    progressText.textContent = `${count} / ${stages.length} stages`;
    progressBar.style.width = `${(count / stages.length) * 100}%`;

    const next = stages.find(stage => !stageComplete(stage));
    nextStageText.textContent = next
      ? `Next: Stage ${String(next.dataset.stage).padStart(2,'0')} · ${next.querySelector('h2')?.textContent || 'continue building'}.`
      : 'All eight stages are complete. Prepare the final live defense.';
  }

  const state = readState();
  inputs.forEach(input => {
    input.checked = Boolean(state[input.dataset.check]);
    input.addEventListener('change', () => {
      const current = readState();
      current[input.dataset.check] = input.checked;
      writeState(current);
      update();
    });
  });

  reset?.addEventListener('click', () => {
    if (!window.confirm('Reset only the progress marks stored in this browser?')) return;
    try { localStorage.removeItem(KEY); } catch {}
    inputs.forEach(input => { input.checked = false; });
    update();
  });

  update();
})();