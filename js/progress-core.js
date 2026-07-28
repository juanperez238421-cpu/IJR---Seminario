export const RUBRIC_CRITERIA = [
  { id: "functionality", label: "Estado funcional del proyecto", weight: 30 },
  { id: "technical", label: "Competencias visibles en el código", weight: 25 },
  { id: "explanation", label: "Explicación individual", weight: 20 },
  { id: "liveChange", label: "Modificación en vivo", weight: 15 },
  { id: "gitDocs", label: "Git y documentación", weight: 10 },
];

export const MILESTONES = [
  { id: "html", label: "Estructura HTML visible y semántica" },
  { id: "css", label: "CSS conectado y organizado" },
  { id: "javascript", label: "JavaScript conectado correctamente" },
  { id: "events", label: "Eventos conectados a la interfaz" },
  { id: "dom", label: "Resultados renderizados con DOM" },
  { id: "validation", label: "Validación real de entradas" },
  { id: "processing", label: "Funciones de procesamiento reutilizables" },
  { id: "storage", label: "Persistencia o navegación con localStorage" },
  { id: "readme", label: "README con propósito e instrucciones" },
  { id: "commits", label: "Commits pequeños y descriptivos" },
];

export const TRACKS = {
  core: {
    label: "Consolidación funcional",
    description: "Completar una aplicación integrada antes de ampliar el alcance.",
  },
  css: {
    label: "Especialización CSS",
    description: "Mejorar jerarquía visual, responsive, accesibilidad y componentes reutilizables.",
  },
};

export function createEmptyCriteria() {
  return Object.fromEntries(RUBRIC_CRITERIA.map(({ id }) => [id, null]));
}

export function createEmptyMilestones() {
  return Object.fromEntries(MILESTONES.map(({ id }) => [id, false]));
}

export function clampScore(value) {
  if (value === "" || value === null || value === undefined) return null;
  const numericValue = Number(value);
  if (!Number.isFinite(numericValue)) return null;
  return Math.min(5, Math.max(0, Math.round(numericValue * 10) / 10));
}

export function isRubricComplete(criteria = {}) {
  return RUBRIC_CRITERIA.every(({ id }) => clampScore(criteria[id]) !== null);
}

export function calculateWeightedGrade(criteria = {}) {
  if (!isRubricComplete(criteria)) return null;

  const total = RUBRIC_CRITERIA.reduce((sum, criterion) => {
    const score = clampScore(criteria[criterion.id]);
    return sum + score * (criterion.weight / 100);
  }, 0);

  return Math.round(total * 100) / 100;
}

export function calculateProgress(milestones = {}) {
  const completed = MILESTONES.filter(({ id }) => Boolean(milestones[id])).length;
  const total = MILESTONES.length;
  return {
    completed,
    total,
    percentage: Math.round((completed / total) * 100),
  };
}

export function normalizeRepository(value = "") {
  return String(value)
    .trim()
    .replace(/^https?:\/\/github\.com\//i, "")
    .replace(/\.git$/i, "")
    .replace(/^\/+|\/+$/g, "");
}

export function getCommitReviewState(latestSha, reviewedSha) {
  if (!latestSha) return "unknown";
  if (!reviewedSha) return "unreviewed";
  return latestSha === reviewedSha ? "reviewed" : "new";
}

export function getStudentStatus(student) {
  const grade = calculateWeightedGrade(student.criteria);
  const progress = calculateProgress(student.milestones);

  if (student.status === "paused") return "paused";
  if (grade !== null && grade >= 4.5 && progress.percentage === 100) return "complete";
  if (getCommitReviewState(student.latestCommit?.sha, student.lastReviewedSha) === "new") return "new-commit";
  if (progress.percentage >= 70) return "advanced";
  if (progress.percentage >= 40) return "developing";
  return "starting";
}

export function createStudent(input = {}) {
  const repository = normalizeRepository(input.repository);
  const fallbackId = `${repository || input.name || "student"}-${Date.now()}`
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");

  return {
    id: input.id || fallbackId,
    name: String(input.name || "Estudiante sin nombre").trim(),
    group: String(input.group || "11°").trim(),
    github: String(input.github || repository.split("/")[0] || "").trim(),
    repository,
    project: String(input.project || "Proyecto por consolidar").trim(),
    track: input.track === "css" ? "css" : "core",
    status: input.status || "active",
    criteria: { ...createEmptyCriteria(), ...(input.criteria || {}) },
    milestones: { ...createEmptyMilestones(), ...(input.milestones || {}) },
    nextGoal: String(input.nextGoal || "Definir la siguiente meta verificable.").trim(),
    notes: String(input.notes || "").trim(),
    latestCommit: input.latestCommit || null,
    lastReviewedSha: input.lastReviewedSha || null,
    updatedAt: input.updatedAt || new Date().toISOString(),
  };
}
