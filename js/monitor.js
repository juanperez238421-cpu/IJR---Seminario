const ROSTER_URL = "data/students.json";
const SNAPSHOT_URL = "data/monitor/latest.json";
const BASELINE_ATTENDANCE_URL = "data/attendance/2026-07-28.json";
const ATTENDANCE_STORAGE_KEY = "ijr-seminario-attendance-v2";
const AUTO_REFRESH_MS = 5 * 60 * 1000;

const milestoneLabels = {
  html: "HTML",
  css: "CSS",
  javascript: "JavaScript",
  events: "Eventos",
  dom: "DOM",
  validation: "Validación",
  processing: "Funciones",
  storage: "localStorage",
  readme: "README",
  commits: "Commits"
};

const attendanceLabels = {
  pending: "Sin registrar",
  present: "Presente",
  late: "Llegó tarde",
  absent: "Ausente",
  excused: "Excusa"
};

const elements = {
  refreshButton: document.querySelector("#refreshButton"),
  lastRunLabel: document.querySelector("#lastRunLabel"),
  nextRunLabel: document.querySelector("#nextRunLabel"),
  studentCount: document.querySelector("#studentCount"),
  repositoryCount: document.querySelector("#repositoryCount"),
  updateCount: document.querySelector("#updateCount"),
  attendanceCount: document.querySelector("#attendanceCount"),
  attendanceDateSummary: document.querySelector("#attendanceDateSummary"),
  attendanceDate: document.querySelector("#attendanceDate"),
  markAllPresent: document.querySelector("#markAllPresentButton"),
  exportAttendance: document.querySelector("#exportAttendanceButton"),
  search: document.querySelector("#searchInput"),
  groupFilter: document.querySelector("#groupFilter"),
  repositoryFilter: document.querySelector("#repositoryFilter"),
  studentGrid: document.querySelector("#studentGrid"),
  emptyState: document.querySelector("#emptyState"),
  toast: document.querySelector("#toast")
};

let roster = null;
let snapshot = null;
let baselineAttendance = null;
let attendanceStore = loadAttendanceStore();

function loadAttendanceStore() {
  try {
    const parsed = JSON.parse(localStorage.getItem(ATTENDANCE_STORAGE_KEY));
    return parsed && typeof parsed === "object" ? parsed : {};
  } catch {
    return {};
  }
}

function saveAttendanceStore() {
  localStorage.setItem(ATTENDANCE_STORAGE_KEY, JSON.stringify(attendanceStore));
}

async function fetchJson(url) {
  const separator = url.includes("?") ? "&" : "?";
  const response = await fetch(`${url}${separator}v=${Date.now()}`, { cache: "no-store" });
  if (!response.ok) throw new Error(`No fue posible cargar ${url}`);
  return response.json();
}

function escapeHtml(value = "") {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function formatDateTime(value) {
  if (!value) return "Sin ejecución registrada";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "Fecha no disponible";
  return new Intl.DateTimeFormat("es-CO", {
    dateStyle: "medium",
    timeStyle: "short",
    timeZone: "America/Bogota"
  }).format(date);
}

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "—";
  return new Intl.DateTimeFormat("es-CO", {
    dateStyle: "medium",
    timeZone: "America/Bogota"
  }).format(date);
}

function showToast(message) {
  elements.toast.textContent = message;
  elements.toast.hidden = false;
  window.clearTimeout(showToast.timeoutId);
  showToast.timeoutId = window.setTimeout(() => {
    elements.toast.hidden = true;
  }, 3200);
}

function snapshotByStudentId() {
  return new Map((snapshot?.students || []).map((student) => [student.id, student]));
}

function baselineAttendanceById() {
  const entries = Object.values(baselineAttendance?.groups || {}).flat();
  return new Map(entries.map((entry) => [entry.studentId, entry]));
}

function ensureAttendanceDate(date) {
  if (!attendanceStore[date]) attendanceStore[date] = {};
  const baselineById = baselineAttendanceById();

  for (const student of roster?.students || []) {
    if (!attendanceStore[date][student.id]) {
      const baseline = date === baselineAttendance?.date ? baselineById.get(student.id) : null;
      attendanceStore[date][student.id] = {
        status: baseline?.status || "pending",
        note: baseline?.note || "",
        updatedAt: null
      };
    }
  }

  saveAttendanceStore();
}

function attendanceFor(studentId) {
  const date = elements.attendanceDate.value;
  ensureAttendanceDate(date);
  return attendanceStore[date][studentId];
}

function getFilteredStudents() {
  const query = elements.search.value.trim().toLowerCase();
  const group = elements.groupFilter.value;
  const repositoryFilter = elements.repositoryFilter.value;
  const snapshots = snapshotByStudentId();

  return (roster?.students || []).filter((student) => {
    const monitor = snapshots.get(student.id);
    const searchable = `${student.name} ${student.displayName} ${student.github} ${student.repository} ${student.project}`.toLowerCase();
    const matchesQuery = !query || searchable.includes(query);
    const matchesGroup = group === "all" || student.group === group;
    const matchesRepository = repositoryFilter === "all"
      || (repositoryFilter === "assigned" && Boolean(student.repository))
      || (repositoryFilter === "pending" && !student.repository)
      || (repositoryFilter === "new" && monitor?.changeState === "new");

    return matchesQuery && matchesGroup && matchesRepository;
  });
}

function repositoryStatusLabel(status) {
  if (status === "confirmed") return "Repo confirmado";
  if (status === "provisional") return "Vínculo provisional";
  return "Repo pendiente";
}

function monitorStateLabel(state) {
  if (state === "new") return "Commit nuevo";
  if (state === "unchanged") return "Sin cambio";
  if (state === "baseline") return "Línea base";
  if (state === "error") return "Error de consulta";
  return "Sin repositorio";
}

function renderCommit(student, monitor) {
  if (!student.repository) {
    return `
      <div class="commit-box">
        <strong>Repositorio pendiente</strong>
        <p>Durante la entrevista registra el usuario de GitHub y el proyecto principal.</p>
      </div>
    `;
  }

  if (!monitor?.latestCommit) {
    return `
      <div class="commit-box">
        <strong>${escapeHtml(monitorStateLabel(monitor?.changeState))}</strong>
        <p>${escapeHtml(monitor?.error || "El monitor aún no dispone de una línea base.")}</p>
      </div>
    `;
  }

  const commit = monitor.latestCommit;
  return `
    <div class="commit-box">
      <strong>${escapeHtml(monitorStateLabel(monitor.changeState))}</strong>
      <p><a href="${escapeHtml(commit.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(commit.shortSha)}</a> — ${escapeHtml(commit.message)}</p>
      <div class="commit-meta">
        <span>${escapeHtml(commit.author)}</span>
        <span>${escapeHtml(formatDateTime(commit.date))}</span>
      </div>
    </div>
  `;
}

function renderStudentCard(student) {
  const monitor = snapshotByStudentId().get(student.id);
  const attendance = attendanceFor(student.id);
  const hasUpdate = monitor?.changeState === "new";
  const milestones = (student.milestones || []).map((id) =>
    `<span class="milestone">${escapeHtml(milestoneLabels[id] || id)}</span>`
  ).join("");
  const repositoryLink = student.repository
    ? `<a class="small-button" href="https://github.com/${escapeHtml(student.repository)}" target="_blank" rel="noopener noreferrer">Abrir repo</a>`
    : `<span class="small-button disabled">Repo pendiente</span>`;

  return `
    <article class="student-card ${hasUpdate ? "has-update" : ""}" data-student-id="${escapeHtml(student.id)}">
      <div class="student-top">
        <div>
          <p class="student-number">N.º ${student.rosterNumber} · ${escapeHtml(student.group)}</p>
          <h3 class="student-name">${escapeHtml(student.displayName)}</h3>
          <p class="student-project">${escapeHtml(student.project)}</p>
        </div>
        <div class="chips">
          <span class="chip group">${escapeHtml(student.group)}</span>
          <span class="chip ${student.track === "css" ? "css" : "core"}">${student.track === "css" ? "Especialización CSS" : "Consolidación"}</span>
          <span class="chip ${escapeHtml(student.repositoryStatus)}">${escapeHtml(repositoryStatusLabel(student.repositoryStatus))}</span>
          ${hasUpdate ? '<span class="chip new">Commit nuevo</span>' : ""}
        </div>
      </div>

      <div class="goal-box">
        <strong>Siguiente meta</strong>
        <p>${escapeHtml(student.nextGoal)}</p>
      </div>

      ${renderCommit(student, monitor)}

      <div class="milestone-row" aria-label="Competencias evidenciadas">
        ${milestones || '<span class="milestone">Diagnóstico pendiente</span>'}
      </div>

      <div class="attendance-row">
        <label class="field attendance-select">
          <span>Asistencia</span>
          <select data-attendance-status>
            ${Object.entries(attendanceLabels).map(([value, label]) =>
              `<option value="${value}" ${attendance.status === value ? "selected" : ""}>${label}</option>`
            ).join("")}
          </select>
        </label>
        <label class="field attendance-note">
          <span>Nota breve</span>
          <input data-attendance-note type="text" maxlength="180" value="${escapeHtml(attendance.note)}" placeholder="Opcional">
        </label>
      </div>

      <div class="card-actions">
        ${repositoryLink}
        <a class="small-button" href="progress.html">Evaluar</a>
        ${student.repository ? `<a class="small-button" href="https://github.com/${escapeHtml(student.repository)}/commits" target="_blank" rel="noopener noreferrer">Historial</a>` : ""}
      </div>
    </article>
  `;
}

function renderStudents() {
  const students = getFilteredStudents();
  elements.studentGrid.innerHTML = students.map(renderStudentCard).join("");
  elements.emptyState.hidden = students.length > 0;
  renderAttendanceSummary();
}

function renderSummary() {
  const totalStudents = roster?.students?.length || 0;
  const repositories = roster?.students?.filter((student) => Boolean(student.repository)).length || 0;
  elements.studentCount.textContent = totalStudents;
  elements.repositoryCount.textContent = `${repositories}/${totalStudents}`;
  elements.updateCount.textContent = snapshot?.summary?.updatesDetected ?? 0;
  elements.lastRunLabel.textContent = `Último monitoreo: ${formatDateTime(snapshot?.generatedAt)}`;
  elements.nextRunLabel.textContent = `Frecuencia programada: cada ${snapshot?.intervalHours || 12} horas`;
  renderAttendanceSummary();
}

function renderAttendanceSummary() {
  if (!roster) return;
  const date = elements.attendanceDate.value;
  ensureAttendanceDate(date);
  const records = Object.values(attendanceStore[date] || {});
  const registered = records.filter(({ status }) => status !== "pending").length;
  elements.attendanceCount.textContent = `${registered}/${roster.students.length}`;
  elements.attendanceDateSummary.textContent = formatDate(`${date}T12:00:00Z`);
}

function updateAttendanceFromCard(card) {
  const studentId = card.dataset.studentId;
  const date = elements.attendanceDate.value;
  ensureAttendanceDate(date);
  const status = card.querySelector("[data-attendance-status]").value;
  const note = card.querySelector("[data-attendance-note]").value.trim();
  attendanceStore[date][studentId] = {
    status,
    note,
    updatedAt: new Date().toISOString()
  };
  saveAttendanceStore();
  renderAttendanceSummary();
}

function markVisibleStudentsPresent() {
  const visibleStudents = getFilteredStudents();
  const date = elements.attendanceDate.value;
  ensureAttendanceDate(date);
  visibleStudents.forEach((student) => {
    attendanceStore[date][student.id] = {
      ...attendanceStore[date][student.id],
      status: "present",
      updatedAt: new Date().toISOString()
    };
  });
  saveAttendanceStore();
  renderStudents();
  showToast(`${visibleStudents.length} estudiantes visibles marcados como presentes.`);
}

function exportAttendance() {
  const date = elements.attendanceDate.value;
  ensureAttendanceDate(date);
  const records = roster.students.map((student) => ({
    studentId: student.id,
    rosterNumber: student.rosterNumber,
    name: student.name,
    displayName: student.displayName,
    group: student.group,
    ...attendanceStore[date][student.id]
  }));

  const payload = {
    date,
    subject: roster.course.subject,
    school: roster.course.school,
    exportedAt: new Date().toISOString(),
    records
  };
  const blob = new Blob([JSON.stringify(payload, null, 2)], { type: "application/json" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = `asistencia-seminario-${date}.json`;
  link.click();
  URL.revokeObjectURL(url);
  showToast("Asistencia exportada en formato JSON.");
}

async function loadDashboard({ announce = false } = {}) {
  elements.refreshButton.disabled = true;
  elements.refreshButton.textContent = "Actualizando…";
  try {
    [roster, snapshot, baselineAttendance] = await Promise.all([
      fetchJson(ROSTER_URL),
      fetchJson(SNAPSHOT_URL),
      fetchJson(BASELINE_ATTENDANCE_URL)
    ]);
    ensureAttendanceDate(elements.attendanceDate.value);
    renderSummary();
    renderStudents();
    if (announce) showToast("Tablero actualizado con el último registro automático.");
  } catch (error) {
    console.error(error);
    showToast("No fue posible cargar los datos del monitoreo.");
  } finally {
    elements.refreshButton.disabled = false;
    elements.refreshButton.textContent = "Actualizar tablero";
  }
}

function bindEvents() {
  elements.refreshButton.addEventListener("click", () => loadDashboard({ announce: true }));
  elements.search.addEventListener("input", renderStudents);
  elements.groupFilter.addEventListener("change", renderStudents);
  elements.repositoryFilter.addEventListener("change", renderStudents);
  elements.attendanceDate.addEventListener("change", () => {
    ensureAttendanceDate(elements.attendanceDate.value);
    renderStudents();
  });
  elements.markAllPresent.addEventListener("click", markVisibleStudentsPresent);
  elements.exportAttendance.addEventListener("click", exportAttendance);
  elements.studentGrid.addEventListener("change", (event) => {
    const card = event.target.closest("[data-student-id]");
    if (card && event.target.matches("[data-attendance-status]")) updateAttendanceFromCard(card);
  });
  elements.studentGrid.addEventListener("input", (event) => {
    const card = event.target.closest("[data-student-id]");
    if (card && event.target.matches("[data-attendance-note]")) updateAttendanceFromCard(card);
  });
}

bindEvents();
loadDashboard();
window.setInterval(() => {
  if (document.visibilityState === "visible") loadDashboard();
}, AUTO_REFRESH_MS);
