import {
  MILESTONES,
  RUBRIC_CRITERIA,
  TRACKS,
  calculateProgress,
  calculateWeightedGrade,
  createStudent,
  getCommitReviewState,
  getStudentStatus,
  normalizeRepository,
} from "./progress-core.js";

const STORAGE_KEY = "ijr-seminario-progress-v1";
const AUTO_SYNC_MS = 10 * 60 * 1000;

const defaultStudents = [
  createStudent({
    id: "jrod917",
    name: "JRod",
    group: "11°",
    github: "jrod917",
    repository: "jrod917/Carrito",
    project: "Carrito de restaurante",
    track: "css",
    milestones: {
      html: true,
      css: true,
      javascript: true,
      events: true,
      dom: true,
      validation: false,
      processing: true,
      storage: false,
      readme: false,
      commits: false,
    },
    nextGoal: "Finalizar recibo y dedicar la siguiente mejora a CSS responsive, estados visuales y componentes reutilizables.",
    notes: "Proyecto de referencia entre los estudiantes: mayor integración actual de HTML, CSS y JavaScript.",
  }),
  createStudent({
    id: "jp0705git",
    name: "JP",
    group: "11°",
    github: "jp0705git",
    repository: "jp0705git/SeminarioProgramacion2",
    project: "Sistema de pedidos Delivery",
    track: "core",
    milestones: {
      html: true,
      css: false,
      javascript: true,
      events: false,
      dom: true,
      validation: false,
      processing: true,
      storage: true,
      readme: false,
      commits: false,
    },
    nextGoal: "Convertir Delivery en una interfaz HTML con eventos, validaciones y resultados visibles sin depender de prompt().",
  }),
  createStudent({
    id: "pablo-jaramillo",
    name: "Pablo Jaramillo Palacio",
    group: "11°B",
    github: "pablitojarita2008-oss",
    repository: "pablitojarita2008-oss/pablitoSeminario",
    project: "Registro de actividades — interfaz",
    track: "core",
    milestones: {
      html: true,
      css: false,
      javascript: true,
      events: true,
      dom: true,
      validation: false,
      processing: false,
      storage: true,
      readme: false,
      commits: false,
    },
    nextGoal: "Ampliar el formulario, agregar validaciones y dejar evidencia individual mediante commits propios.",
    notes: "Repositorio compartido con Samuel. La calificación debe separar autoría y defensa individual.",
  }),
  createStudent({
    id: "samuel-velasquez",
    name: "Samuel Velásquez",
    group: "11°C",
    github: "pablitojarita2008-oss",
    repository: "pablitojarita2008-oss/pablitoSeminario",
    project: "Registro de actividades — lógica",
    track: "core",
    milestones: {
      html: true,
      css: false,
      javascript: true,
      events: true,
      dom: true,
      validation: false,
      processing: false,
      storage: true,
      readme: false,
      commits: false,
    },
    nextGoal: "Implementar resumen editable, validaciones y un commit identificable desde su propia cuenta.",
    notes: "Repositorio compartido con Pablo. Verificar contribución mediante modificación en vivo.",
  }),
  createStudent({
    id: "pedropae07",
    name: "Pedro",
    group: "11°",
    github: "Pedropae07",
    repository: "Pedropae07/practice_seminario",
    project: "Cajero automático didáctico",
    track: "core",
    milestones: {
      html: true,
      css: false,
      javascript: true,
      events: false,
      dom: false,
      validation: false,
      processing: false,
      storage: false,
      readme: false,
      commits: false,
    },
    nextGoal: "Corregir autenticación y completar un solo flujo funcional: ingreso, consulta de saldo y retiro validado.",
  }),
];

const elements = {
  studentList: document.querySelector("#studentList"),
  emptyState: document.querySelector("#emptyStudentState"),
  search: document.querySelector("#studentSearch"),
  groupFilter: document.querySelector("#groupFilter"),
  statusFilter: document.querySelector("#statusFilter"),
  syncAll: document.querySelector("#syncAllButton"),
  syncMessage: document.querySelector("#syncMessage"),
  exportButton: document.querySelector("#exportButton"),
  importInput: document.querySelector("#importInput"),
  resetButton: document.querySelector("#resetDataButton"),
  addButton: document.querySelector("#addStudentButton"),
  addDialog: document.querySelector("#addStudentDialog"),
  addForm: document.querySelector("#addStudentForm"),
  closeDialog: document.querySelector("#closeStudentDialog"),
  evaluationPanel: document.querySelector("#evaluationPanel"),
  evaluationForm: document.querySelector("#evaluationForm"),
  selectedName: document.querySelector("#selectedStudentName"),
  selectedMeta: document.querySelector("#selectedStudentMeta"),
  selectedTrack: document.querySelector("#selectedTrack"),
  selectedRepo: document.querySelector("#selectedRepoLink"),
  selectedCommit: document.querySelector("#selectedCommit"),
  criteriaFields: document.querySelector("#criteriaFields"),
  milestoneFields: document.querySelector("#milestoneFields"),
  nextGoal: document.querySelector("#nextGoalInput"),
  notes: document.querySelector("#notesInput"),
  studentStatus: document.querySelector("#studentStatusInput"),
  saveEvaluation: document.querySelector("#saveEvaluationButton"),
  markReviewed: document.querySelector("#markReviewedButton"),
  deleteStudent: document.querySelector("#deleteStudentButton"),
  summaryStudents: document.querySelector("#summaryStudents"),
  summaryNewCommits: document.querySelector("#summaryNewCommits"),
  summaryAverage: document.querySelector("#summaryAverage"),
  summaryMilestones: document.querySelector("#summaryMilestones"),
  lastUpdated: document.querySelector("#lastUpdated"),
  toast: document.querySelector("#progressToast"),
};

let state = loadState();
let selectedStudentId = state.students[0]?.id || null;
let syncTimer = null;

function loadState() {
  try {
    const stored = JSON.parse(localStorage.getItem(STORAGE_KEY));
    if (stored?.students?.length) {
      return {
        version: 1,
        updatedAt: stored.updatedAt || new Date().toISOString(),
        students: stored.students.map((student) => createStudent(student)),
      };
    }
  } catch (error) {
    console.warn("No fue posible recuperar el seguimiento guardado.", error);
  }

  return {
    version: 1,
    updatedAt: new Date().toISOString(),
    students: defaultStudents,
  };
}

function saveState() {
  state.updatedAt = new Date().toISOString();
  localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
  renderLastUpdated();
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDate(value) {
  if (!value) return "Sin sincronizar";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Fecha no disponible";
  return new Intl.DateTimeFormat("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
  }).format(date);
}

function shortSha(sha = "") {
  return sha ? sha.slice(0, 7) : "—";
}

function getStatusCopy(status) {
  const labels = {
    starting: "Inicio",
    developing: "En desarrollo",
    advanced: "Avanzado",
    complete: "Completo",
    "new-commit": "Commit nuevo",
    paused: "En pausa",
  };
  return labels[status] || "Sin estado";
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.hidden = false;
  window.clearTimeout(showToast.timeoutId);
  showToast.timeoutId = window.setTimeout(() => {
    elements.toast.hidden = true;
  }, 3200);
}

function renderCriteriaFields(student) {
  elements.criteriaFields.innerHTML = RUBRIC_CRITERIA.map((criterion) => {
    const value = student.criteria[criterion.id];
    return `
      <label class="score-field" for="criterion-${criterion.id}">
        <span>
          <strong>${escapeHtml(criterion.label)}</strong>
          <small>Peso ${criterion.weight}%</small>
        </span>
        <input
          id="criterion-${criterion.id}"
          name="${criterion.id}"
          type="number"
          min="0"
          max="5"
          step="0.1"
          inputmode="decimal"
          value="${value === null ? "" : escapeHtml(value)}"
          placeholder="0–5"
        >
      </label>
    `;
  }).join("");
}

function renderMilestoneFields(student) {
  elements.milestoneFields.innerHTML = MILESTONES.map((milestone) => `
    <label class="milestone-check">
      <input
        type="checkbox"
        name="milestone-${milestone.id}"
        ${student.milestones[milestone.id] ? "checked" : ""}
      >
      <span>${escapeHtml(milestone.label)}</span>
    </label>
  `).join("");
}

function renderEvaluationPanel() {
  const student = state.students.find(({ id }) => id === selectedStudentId);
  if (!student) {
    elements.evaluationPanel.hidden = true;
    return;
  }

  elements.evaluationPanel.hidden = false;
  elements.selectedName.textContent = student.name;
  elements.selectedMeta.textContent = `${student.group} · ${student.project}`;
  elements.selectedTrack.textContent = TRACKS[student.track]?.label || TRACKS.core.label;
  elements.selectedTrack.dataset.track = student.track;
  elements.selectedRepo.href = `https://github.com/${student.repository}`;
  elements.selectedRepo.textContent = student.repository;
  elements.selectedCommit.textContent = student.latestCommit
    ? `${shortSha(student.latestCommit.sha)} · ${student.latestCommit.message} · ${formatDate(student.latestCommit.date)}`
    : "Aún no se ha sincronizado el último commit.";
  elements.nextGoal.value = student.nextGoal;
  elements.notes.value = student.notes;
  elements.studentStatus.value = student.status;
  elements.markReviewed.disabled = !student.latestCommit?.sha;
  renderCriteriaFields(student);
  renderMilestoneFields(student);
}

function renderGroupOptions() {
  const currentValue = elements.groupFilter.value;
  const groups = [...new Set(state.students.map(({ group }) => group).filter(Boolean))].sort();
  elements.groupFilter.innerHTML = `<option value="all">Todos los grupos</option>${groups
    .map((group) => `<option value="${escapeHtml(group)}">${escapeHtml(group)}</option>`)
    .join("")}`;
  elements.groupFilter.value = groups.includes(currentValue) ? currentValue : "all";
}

function getFilteredStudents() {
  const query = elements.search.value.trim().toLowerCase();
  const group = elements.groupFilter.value;
  const status = elements.statusFilter.value;

  return state.students.filter((student) => {
    const searchable = `${student.name} ${student.github} ${student.repository} ${student.project}`.toLowerCase();
    const matchesQuery = !query || searchable.includes(query);
    const matchesGroup = group === "all" || student.group === group;
    const matchesStatus = status === "all" || getStudentStatus(student) === status;
    return matchesQuery && matchesGroup && matchesStatus;
  });
}

function renderStudentCard(student) {
  const progress = calculateProgress(student.milestones);
  const grade = calculateWeightedGrade(student.criteria);
  const status = getStudentStatus(student);
  const commitState = getCommitReviewState(student.latestCommit?.sha, student.lastReviewedSha);
  const isSelected = student.id === selectedStudentId;

  return `
    <article class="student-card ${isSelected ? "is-selected" : ""}" data-student-id="${escapeHtml(student.id)}">
      <button class="student-card-select" type="button" data-action="select" aria-label="Evaluar a ${escapeHtml(student.name)}"></button>
      <div class="student-card-top">
        <div>
          <p class="student-group">${escapeHtml(student.group)}</p>
          <h3>${escapeHtml(student.name)}</h3>
          <p class="student-project">${escapeHtml(student.project)}</p>
        </div>
        <span class="status-chip status-${status}">${getStatusCopy(status)}</span>
      </div>

      <div class="track-line">
        <span class="track-chip track-${student.track}">${escapeHtml(TRACKS[student.track]?.label || TRACKS.core.label)}</span>
        <span class="grade-value">${grade === null ? "Pendiente" : grade.toFixed(2)}</span>
      </div>

      <div class="progress-row" aria-label="${progress.completed} de ${progress.total} metas completadas">
        <div class="progress-track"><span style="width: ${progress.percentage}%"></span></div>
        <strong>${progress.percentage}%</strong>
      </div>

      <p class="next-goal"><strong>Siguiente meta:</strong> ${escapeHtml(student.nextGoal)}</p>

      <div class="commit-box commit-${commitState}">
        <div>
          <span class="commit-label">Último commit</span>
          <strong>${student.latestCommit ? escapeHtml(shortSha(student.latestCommit.sha)) : "Sin sincronizar"}</strong>
        </div>
        <p>${student.latestCommit ? escapeHtml(student.latestCommit.message) : "Pulsa sincronizar para consultar GitHub."}</p>
        <small>${student.latestCommit ? escapeHtml(formatDate(student.latestCommit.date)) : ""}</small>
      </div>

      <div class="student-actions">
        <a class="small-button" href="https://github.com/${escapeHtml(student.repository)}" target="_blank" rel="noopener noreferrer">Abrir repo</a>
        <button class="small-button" type="button" data-action="sync">Sincronizar</button>
        <button class="small-button primary" type="button" data-action="select">Evaluar</button>
      </div>
    </article>
  `;
}

function renderStudents() {
  const students = getFilteredStudents();
  elements.studentList.innerHTML = students.map(renderStudentCard).join("");
  elements.emptyState.hidden = students.length > 0;
}

function renderSummary() {
  const grades = state.students
    .map(({ criteria }) => calculateWeightedGrade(criteria))
    .filter((grade) => grade !== null);
  const newCommits = state.students.filter((student) =>
    getCommitReviewState(student.latestCommit?.sha, student.lastReviewedSha) === "new"
  ).length;
  const milestoneTotals = state.students.reduce(
    (accumulator, student) => {
      const progress = calculateProgress(student.milestones);
      accumulator.completed += progress.completed;
      accumulator.total += progress.total;
      return accumulator;
    },
    { completed: 0, total: 0 }
  );

  elements.summaryStudents.textContent = state.students.length;
  elements.summaryNewCommits.textContent = newCommits;
  elements.summaryAverage.textContent = grades.length
    ? (grades.reduce((sum, grade) => sum + grade, 0) / grades.length).toFixed(2)
    : "—";
  elements.summaryMilestones.textContent = milestoneTotals.total
    ? `${Math.round((milestoneTotals.completed / milestoneTotals.total) * 100)}%`
    : "0%";
}

function renderLastUpdated() {
  elements.lastUpdated.textContent = `Datos locales: ${formatDate(state.updatedAt)}`;
}

function renderAll() {
  renderGroupOptions();
  renderSummary();
  renderStudents();
  renderEvaluationPanel();
  renderLastUpdated();
}

async function fetchLatestCommit(student) {
  const repository = normalizeRepository(student.repository);
  if (!repository.includes("/")) throw new Error("Repositorio inválido");

  const response = await fetch(`https://api.github.com/repos/${repository}/commits?per_page=1`, {
    headers: { Accept: "application/vnd.github+json" },
  });

  if (!response.ok) {
    if (response.status === 403) throw new Error("Límite temporal de GitHub alcanzado");
    if (response.status === 404) throw new Error("Repositorio no encontrado o no público");
    throw new Error(`GitHub respondió ${response.status}`);
  }

  const commits = await response.json();
  const commit = commits[0];
  if (!commit) throw new Error("El repositorio no tiene commits");

  return {
    sha: commit.sha,
    message: commit.commit?.message?.split("\n")[0] || "Commit sin mensaje",
    date: commit.commit?.committer?.date || commit.commit?.author?.date || null,
    author: commit.author?.login || commit.commit?.author?.name || "Autor no identificado",
    url: commit.html_url,
    syncedAt: new Date().toISOString(),
  };
}

async function syncStudent(studentId, { silent = false } = {}) {
  const student = state.students.find(({ id }) => id === studentId);
  if (!student) return;

  const card = elements.studentList.querySelector(`[data-student-id="${CSS.escape(studentId)}"]`);
  card?.classList.add("is-syncing");

  try {
    student.latestCommit = await fetchLatestCommit(student);
    student.updatedAt = new Date().toISOString();
    saveState();
    if (!silent) showToast(`${student.name}: commit actualizado.`);
  } catch (error) {
    if (!silent) showToast(`${student.name}: ${error.message}.`);
    console.warn(`No se pudo sincronizar ${student.repository}`, error);
  } finally {
    card?.classList.remove("is-syncing");
    renderSummary();
    renderStudents();
    renderEvaluationPanel();
  }
}

async function syncAllStudents({ silent = false } = {}) {
  elements.syncAll.disabled = true;
  elements.syncMessage.textContent = "Consultando repositorios públicos de GitHub…";

  const results = await Promise.allSettled(
    state.students.map(async (student) => {
      student.latestCommit = await fetchLatestCommit(student);
      student.updatedAt = new Date().toISOString();
    })
  );

  const successCount = results.filter(({ status }) => status === "fulfilled").length;
  const errorCount = results.length - successCount;
  saveState();
  renderAll();
  elements.syncAll.disabled = false;
  elements.syncMessage.textContent = errorCount
    ? `${successCount} repositorios actualizados; ${errorCount} no pudieron consultarse.`
    : `${successCount} repositorios actualizados correctamente.`;

  if (!silent) showToast(elements.syncMessage.textContent);
}

function saveEvaluation(event) {
  event.preventDefault();
  const student = state.students.find(({ id }) => id === selectedStudentId);
  if (!student) return;

  const formData = new FormData(elements.evaluationForm);
  RUBRIC_CRITERIA.forEach(({ id }) => {
    const rawValue = formData.get(id);
    student.criteria[id] = rawValue === "" ? null : Number(rawValue);
  });
  MILESTONES.forEach(({ id }) => {
    student.milestones[id] = formData.has(`milestone-${id}`);
  });
  student.nextGoal = elements.nextGoal.value.trim() || "Definir la siguiente meta verificable.";
  student.notes = elements.notes.value.trim();
  student.status = elements.studentStatus.value;
  student.updatedAt = new Date().toISOString();
  saveState();
  renderAll();
  showToast(`Evaluación de ${student.name} guardada localmente.`);
}

function markCurrentCommitReviewed() {
  const student = state.students.find(({ id }) => id === selectedStudentId);
  if (!student?.latestCommit?.sha) return;
  student.lastReviewedSha = student.latestCommit.sha;
  student.updatedAt = new Date().toISOString();
  saveState();
  renderAll();
  showToast(`Commit ${shortSha(student.lastReviewedSha)} marcado como revisado.`);
}

function deleteSelectedStudent() {
  const student = state.students.find(({ id }) => id === selectedStudentId);
  if (!student) return;
  if (!window.confirm(`¿Eliminar a ${student.name} del tablero local?`)) return;

  state.students = state.students.filter(({ id }) => id !== selectedStudentId);
  selectedStudentId = state.students[0]?.id || null;
  saveState();
  renderAll();
  showToast("Registro eliminado del tablero local.");
}

function addStudent(event) {
  event.preventDefault();
  const formData = new FormData(elements.addForm);
  const repository = normalizeRepository(formData.get("repository"));

  if (!repository.includes("/")) {
    showToast("Escribe el repositorio como usuario/proyecto.");
    return;
  }

  const student = createStudent({
    name: formData.get("name"),
    group: formData.get("group"),
    repository,
    project: formData.get("project"),
    track: formData.get("track"),
  });

  state.students.push(student);
  selectedStudentId = student.id;
  saveState();
  elements.addForm.reset();
  elements.addDialog.close();
  renderAll();
  showToast(`${student.name} fue agregado al seguimiento.`);
  syncStudent(student.id, { silent: true });
}

function exportData() {
  const blob = new Blob([JSON.stringify(state, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `seminario-progreso-${new Date().toISOString().slice(0, 10)}.json`;
  link.click();
  URL.revokeObjectURL(url);
  showToast("Copia de seguimiento exportada.");
}

async function importData(event) {
  const [file] = event.target.files;
  if (!file) return;

  try {
    const imported = JSON.parse(await file.text());
    if (!Array.isArray(imported.students)) throw new Error("Formato inválido");
    state = {
      version: 1,
      updatedAt: new Date().toISOString(),
      students: imported.students.map((student) => createStudent(student)),
    };
    selectedStudentId = state.students[0]?.id || null;
    saveState();
    renderAll();
    showToast("Seguimiento importado correctamente.");
  } catch (error) {
    showToast("No fue posible importar ese archivo JSON.");
    console.warn(error);
  } finally {
    event.target.value = "";
  }
}

function resetData() {
  if (!window.confirm("¿Restablecer el tablero con los estudiantes y metas iniciales?")) return;
  state = {
    version: 1,
    updatedAt: new Date().toISOString(),
    students: defaultStudents.map((student) => createStudent(JSON.parse(JSON.stringify(student)))),
  };
  selectedStudentId = state.students[0]?.id || null;
  saveState();
  renderAll();
  showToast("Datos de referencia restablecidos.");
}

function handleStudentListClick(event) {
  const card = event.target.closest("[data-student-id]");
  const actionElement = event.target.closest("[data-action]");
  if (!card || !actionElement) return;

  const studentId = card.dataset.studentId;
  const action = actionElement.dataset.action;
  if (action === "select") {
    selectedStudentId = studentId;
    renderStudents();
    renderEvaluationPanel();
    elements.evaluationPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  if (action === "sync") syncStudent(studentId);
}

function startAutoSync() {
  window.clearInterval(syncTimer);
  syncTimer = window.setInterval(() => {
    if (document.visibilityState === "visible") syncAllStudents({ silent: true });
  }, AUTO_SYNC_MS);
}

function bindEvents() {
  elements.search.addEventListener("input", renderStudents);
  elements.groupFilter.addEventListener("change", renderStudents);
  elements.statusFilter.addEventListener("change", renderStudents);
  elements.studentList.addEventListener("click", handleStudentListClick);
  elements.syncAll.addEventListener("click", () => syncAllStudents());
  elements.evaluationForm.addEventListener("submit", saveEvaluation);
  elements.markReviewed.addEventListener("click", markCurrentCommitReviewed);
  elements.deleteStudent.addEventListener("click", deleteSelectedStudent);
  elements.exportButton.addEventListener("click", exportData);
  elements.importInput.addEventListener("change", importData);
  elements.resetButton.addEventListener("click", resetData);
  elements.addButton.addEventListener("click", () => elements.addDialog.showModal());
  elements.closeDialog.addEventListener("click", () => elements.addDialog.close());
  elements.addForm.addEventListener("submit", addStudent);
}

renderAll();
bindEvents();
startAutoSync();
syncAllStudents({ silent: true });
