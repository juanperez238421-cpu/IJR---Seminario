const STORAGE_KEY = "ijr-seminario-progress-v1";
const ROSTER_URL = "data/students.json";
const SNAPSHOT_URL = "data/monitor/latest.json";
const milestoneIds = [
  "html",
  "css",
  "javascript",
  "events",
  "dom",
  "validation",
  "processing",
  "storage",
  "readme",
  "commits"
];
const criterionIds = ["functionality", "technical", "explanation", "liveChange", "gitDocs"];

async function fetchJson(url) {
  const response = await fetch(`${url}?v=${Date.now()}`, { cache: "no-store" });
  if (!response.ok) throw new Error(`No fue posible cargar ${url}`);
  return response.json();
}

function emptyCriteria() {
  return Object.fromEntries(criterionIds.map((id) => [id, null]));
}

function milestoneObject(completed = []) {
  const completedSet = new Set(completed);
  return Object.fromEntries(milestoneIds.map((id) => [id, completedSet.has(id)]));
}

function readStoredState() {
  try {
    const parsed = JSON.parse(localStorage.getItem(STORAGE_KEY));
    return parsed?.students ? parsed : { students: [] };
  } catch {
    return { students: [] };
  }
}

function findPreviousStudent(students, rosterStudent) {
  return students.find((student) =>
    student.id === rosterStudent.id
    || (rosterStudent.repository && student.repository === rosterStudent.repository)
    || student.name?.toLocaleLowerCase("es") === rosterStudent.displayName.toLocaleLowerCase("es")
  );
}

async function initializeRoster() {
  try {
    const [roster, snapshot] = await Promise.all([
      fetchJson(ROSTER_URL),
      fetchJson(SNAPSHOT_URL)
    ]);
    const previousState = readStoredState();
    const snapshotById = new Map((snapshot.students || []).map((student) => [student.id, student]));

    const students = roster.students.map((rosterStudent) => {
      const previous = findPreviousStudent(previousState.students || [], rosterStudent);
      const monitor = snapshotById.get(rosterStudent.id);
      return {
        id: rosterStudent.id,
        name: rosterStudent.displayName,
        group: rosterStudent.group,
        github: rosterStudent.github,
        repository: rosterStudent.repository,
        project: rosterStudent.project,
        track: rosterStudent.track === "css" ? "css" : "core",
        status: previous?.status || "active",
        criteria: { ...emptyCriteria(), ...(previous?.criteria || {}) },
        milestones: { ...milestoneObject(rosterStudent.milestones), ...(previous?.milestones || {}) },
        nextGoal: previous?.nextGoal || rosterStudent.nextGoal,
        notes: previous?.notes || (rosterStudent.repositoryStatus === "provisional"
          ? "Vínculo de repositorio provisional: confirmar durante la entrevista."
          : ""),
        latestCommit: monitor?.latestCommit
          ? {
              sha: monitor.latestCommit.sha,
              message: monitor.latestCommit.message,
              date: monitor.latestCommit.date,
              author: monitor.latestCommit.author,
              url: monitor.latestCommit.url,
              syncedAt: monitor.checkedAt
            }
          : previous?.latestCommit || null,
        lastReviewedSha: previous?.lastReviewedSha || null,
        updatedAt: previous?.updatedAt || new Date().toISOString()
      };
    });

    const localOnlyStudents = (previousState.students || []).filter((student) =>
      !students.some((current) => current.id === student.id || (current.repository && current.repository === student.repository))
    );

    localStorage.setItem(STORAGE_KEY, JSON.stringify({
      version: 2,
      updatedAt: new Date().toISOString(),
      students: [...students, ...localOnlyStudents]
    }));
  } catch (error) {
    console.warn("No fue posible sincronizar el listado oficial antes de abrir la evaluación.", error);
  }

  await import("./progress.js");
}

initializeRoster();
