import { mkdir, readFile, writeFile, appendFile } from "node:fs/promises";
import process from "node:process";

const ROSTER_PATH = new URL("../data/students.json", import.meta.url);
const MONITOR_DIR = new URL("../data/monitor/", import.meta.url);
const LATEST_PATH = new URL("../data/monitor/latest.json", import.meta.url);
const HISTORY_PATH = new URL("../data/monitor/history.json", import.meta.url);
const SUMMARY_PATH = new URL("../data/monitor/summary.md", import.meta.url);
const token = process.env.GITHUB_TOKEN || "";

async function readJson(path, fallback) {
  try {
    return JSON.parse(await readFile(path, "utf8"));
  } catch {
    return fallback;
  }
}

function firstLine(value = "") {
  return String(value).split(/\r?\n/, 1)[0].trim() || "Commit sin mensaje";
}

function shortSha(value = "") {
  return value ? value.slice(0, 7) : "—";
}

function githubHeaders() {
  const headers = {
    Accept: "application/vnd.github+json",
    "User-Agent": "IJR-Seminario-Student-Monitor",
    "X-GitHub-Api-Version": "2022-11-28"
  };
  if (token) headers.Authorization = `Bearer ${token}`;
  return headers;
}

async function fetchLatestCommit(repository) {
  const response = await fetch(`https://api.github.com/repos/${repository}/commits?per_page=1`, {
    headers: githubHeaders()
  });

  if (!response.ok) {
    const rateRemaining = response.headers.get("x-ratelimit-remaining");
    const suffix = rateRemaining === "0" ? " (límite de API alcanzado)" : "";
    throw new Error(`GitHub respondió ${response.status}${suffix}`);
  }

  const commits = await response.json();
  const commit = commits[0];
  if (!commit) throw new Error("El repositorio no tiene commits");

  return {
    sha: commit.sha,
    shortSha: shortSha(commit.sha),
    message: firstLine(commit.commit?.message),
    author: commit.author?.login || commit.commit?.author?.name || "Autor no identificado",
    date: commit.commit?.committer?.date || commit.commit?.author?.date || null,
    url: commit.html_url || `https://github.com/${repository}/commit/${commit.sha}`
  };
}

function buildSummaryMarkdown(snapshot) {
  const rows = snapshot.students.map((student) => {
    const state = student.changeState === "new"
      ? "🟠 Commit nuevo"
      : student.changeState === "unchanged"
        ? "🟢 Sin cambio"
        : student.changeState === "baseline"
          ? "🔵 Línea base"
          : student.changeState === "pending"
            ? "⚪ Falta repositorio"
            : "🔴 Error";

    const commit = student.latestCommit
      ? `[${student.latestCommit.shortSha}](${student.latestCommit.url}) — ${student.latestCommit.message}`
      : student.error || "Sin datos";

    return `| ${student.group} | ${student.rosterNumber} | ${student.displayName} | ${state} | ${commit} |`;
  });

  return `# Monitoreo automático de Seminario\n\n` +
    `- **Última ejecución:** ${snapshot.generatedAt}\n` +
    `- **Frecuencia:** cada ${snapshot.intervalHours} horas\n` +
    `- **Repositorios asignados:** ${snapshot.summary.repositoriesAssigned}/${snapshot.summary.totalStudents}\n` +
    `- **Actualizaciones detectadas:** ${snapshot.summary.updatesDetected}\n` +
    `- **Errores:** ${snapshot.summary.errors}\n\n` +
    `| Grupo | N.º | Estudiante | Estado | Último commit |\n` +
    `|---|---:|---|---|---|\n` +
    `${rows.join("\n")}\n`;
}

const roster = await readJson(ROSTER_PATH, null);
if (!roster?.students?.length) {
  throw new Error("No fue posible cargar data/students.json");
}

await mkdir(MONITOR_DIR, { recursive: true });
const previousSnapshot = await readJson(LATEST_PATH, { students: [] });
const previousById = new Map((previousSnapshot.students || []).map((student) => [student.id, student]));
const previousHistory = await readJson(HISTORY_PATH, { version: 1, events: [] });
const generatedAt = new Date().toISOString();
const students = [];
const newEvents = [];

for (const student of roster.students) {
  const previous = previousById.get(student.id);
  const base = {
    id: student.id,
    rosterNumber: student.rosterNumber,
    name: student.name,
    displayName: student.displayName,
    group: student.group,
    github: student.github,
    repository: student.repository,
    repositoryStatus: student.repositoryStatus,
    project: student.project,
    track: student.track,
    nextGoal: student.nextGoal,
    checkedAt: generatedAt,
    previousSha: previous?.latestCommit?.sha || null,
    latestCommit: null,
    changeState: "pending",
    error: null
  };

  if (!student.repository) {
    students.push(base);
    continue;
  }

  try {
    const latestCommit = await fetchLatestCommit(student.repository);
    const previousSha = previous?.latestCommit?.sha || null;
    const changeState = previousSha
      ? (previousSha === latestCommit.sha ? "unchanged" : "new")
      : "baseline";

    const record = { ...base, latestCommit, changeState };
    students.push(record);

    if (changeState === "new") {
      newEvents.push({
        detectedAt: generatedAt,
        studentId: student.id,
        rosterNumber: student.rosterNumber,
        name: student.name,
        displayName: student.displayName,
        group: student.group,
        repository: student.repository,
        previousSha,
        currentSha: latestCommit.sha,
        message: latestCommit.message,
        author: latestCommit.author,
        commitDate: latestCommit.date,
        url: latestCommit.url
      });
    }
  } catch (error) {
    students.push({
      ...base,
      changeState: "error",
      error: error instanceof Error ? error.message : String(error)
    });
  }
}

const summary = {
  totalStudents: students.length,
  repositoriesAssigned: students.filter((student) => Boolean(student.repository)).length,
  repositoriesPending: students.filter((student) => !student.repository).length,
  repositoriesChecked: students.filter((student) => Boolean(student.latestCommit)).length,
  updatesDetected: students.filter((student) => student.changeState === "new").length,
  errors: students.filter((student) => student.changeState === "error").length
};

const snapshot = {
  version: 1,
  generatedAt,
  intervalHours: roster.course?.monitorIntervalHours || 12,
  timezone: roster.course?.timezone || "America/Bogota",
  summary,
  students
};

const history = {
  version: 1,
  updatedAt: generatedAt,
  events: [...newEvents, ...(previousHistory.events || [])].slice(0, 1000)
};

await writeFile(LATEST_PATH, `${JSON.stringify(snapshot, null, 2)}\n`, "utf8");
await writeFile(HISTORY_PATH, `${JSON.stringify(history, null, 2)}\n`, "utf8");
await writeFile(SUMMARY_PATH, buildSummaryMarkdown(snapshot), "utf8");

if (process.env.GITHUB_OUTPUT) {
  await appendFile(process.env.GITHUB_OUTPUT, `updates=${summary.updatesDetected}\n`, "utf8");
  await appendFile(process.env.GITHUB_OUTPUT, `checked=${summary.repositoriesChecked}\n`, "utf8");
  await appendFile(process.env.GITHUB_OUTPUT, `errors=${summary.errors}\n`, "utf8");
}

console.log(`Monitoreo completado: ${summary.repositoriesChecked} repositorios, ${summary.updatesDetected} cambios, ${summary.errors} errores.`);
