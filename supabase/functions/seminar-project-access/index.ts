import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2.95.0";

const allowedOrigins = new Set([
  "https://rlfxnjbqxbozjdzkbwlz.supabase.co",
  "https://juanperez238421-cpu.github.io",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
]);

type ProjectRow = Record<string, any>;
type Option = {
  key: string;
  label: string;
  title: string;
  summary: string;
  objective: string;
  stack: string[];
  track_slug?: string;
  kind: "teacher" | "curated" | "custom";
};

function cors(origin: string | null) {
  return {
    "Access-Control-Allow-Origin": origin && allowedOrigins.has(origin) ? origin : "null",
    "Access-Control-Allow-Headers": "content-type, apikey, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Vary": "Origin",
  };
}
function json(origin: string | null, status: number, body: unknown) {
  return new Response(JSON.stringify(body), { status, headers: cors(origin) });
}
function normalizeEmail(value: unknown) {
  return typeof value === "string" ? value.trim().toLowerCase().slice(0, 254) : "";
}
function cleanText(value: unknown, max: number) {
  return typeof value === "string" ? value.trim().slice(0, max) : "";
}
function normalizeStudentCode(value: unknown) {
  return typeof value === "string" ? value.trim().toUpperCase().slice(0, 64) : "";
}
async function sha256(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}
function getDefaultKey(envName: string) {
  const raw = Deno.env.get(envName) ?? "";
  if (!raw) return "";
  try {
    const parsed = JSON.parse(raw);
    return typeof parsed?.default === "string" ? parsed.default : "";
  } catch {
    return "";
  }
}
function proposalOption(project: ProjectRow): Option {
  return {
    key: "teacher-proposal",
    label: "Propuesta inicial",
    title: project.initial_project_title || project.project_title || "",
    summary: project.initial_project_summary || project.project_summary || "",
    objective: project.initial_objective || project.objective || "",
    stack: Array.isArray(project.initial_stack) ? project.initial_stack : (project.stack || []),
    track_slug: String(project.track_slug || ""),
    kind: "teacher",
  };
}
function curatedOptions(track: string): Option[] {
  const map: Record<string, Option[]> = {
    web: [
      {
        key: "web-project-tracker",
        label: "Opción A · Web",
        title: "Project Tracker — Organizador de tareas y evidencias",
        summary: "Aplicación web para crear, editar, priorizar y filtrar tareas de un proyecto, conservar el estado y visualizar el avance.",
        objective: "Construir y publicar una aplicación web con datos estructurados, persistencia local y una interacción completa de crear, editar, filtrar y consultar información.",
        stack: ["HTML", "CSS", "JavaScript", "JSON", "localStorage", "GitHub Pages"],
        kind: "curated",
      },
      {
        key: "web-smart-catalog",
        label: "Opción B · Web",
        title: "Smart Catalog — Catálogo con búsqueda, filtros y favoritos",
        summary: "Catálogo temático elegido por el estudiante con tarjetas, detalle, búsqueda, filtros combinables y favoritos persistentes.",
        objective: "Modelar datos de una temática real y convertirlos en una interfaz web usable, responsiva y publicable con búsqueda, filtros y estado persistente.",
        stack: ["HTML", "CSS", "JavaScript", "JSON", "localStorage", "Git"],
        kind: "curated",
      },
      {
        key: "web-community-tool",
        label: "Opción C · Web",
        title: "Community Utility — Herramienta web para una necesidad concreta",
        summary: "Herramienta web para resolver una necesidad no sensible del colegio o de la comunidad, por ejemplo agenda, inventario simulado, guía de recursos o tablero informativo.",
        objective: "Definir un usuario y un problema concreto, construir un MVP funcional y demostrar con pruebas que la aplicación resuelve el flujo principal.",
        stack: ["HTML", "CSS", "JavaScript", "JSON or API", "localStorage", "Git"],
        kind: "curated",
      },
    ],
    "data-science": [
      {
        key: "data-sports-analysis",
        label: "Opción A · Datos",
        title: "Sports Performance Explorer — Análisis de rendimiento",
        summary: "Análisis reproducible de un dataset público o simulado de rendimiento deportivo para comparar variables, detectar patrones y comunicar hallazgos.",
        objective: "Cargar, limpiar, explorar y visualizar datos deportivos en Python y producir conclusiones respaldadas por estadísticas descriptivas y gráficos.",
        stack: ["Python", "Pandas", "NumPy", "Matplotlib", "Jupyter or Colab"],
        kind: "curated",
      },
      {
        key: "data-mobility-analysis",
        label: "Opción B · Datos",
        title: "Urban Mobility Explorer — Análisis de movilidad",
        summary: "Proyecto de análisis de datos abiertos o simulados sobre movilidad, transporte, tiempos de viaje o comportamiento del tráfico.",
        objective: "Formular una pregunta medible, preparar el dataset y construir un análisis reproducible con indicadores, comparaciones y visualizaciones.",
        stack: ["Python", "Pandas", "Matplotlib", "CSV", "Jupyter or Colab"],
        kind: "curated",
      },
      {
        key: "data-gaming-media",
        label: "Opción C · Datos",
        title: "Gaming & Media Data Lab — Tendencias de videojuegos o entretenimiento",
        summary: "Análisis de un dataset público sobre videojuegos, películas, música u otra temática de entretenimiento para explorar popularidad, categorías y relaciones entre variables.",
        objective: "Transformar una pregunta de interés personal en un análisis de datos documentado, con limpieza, estadísticas descriptivas, gráficos y conclusiones.",
        stack: ["Python", "Pandas", "NumPy", "Matplotlib", "optional scikit-learn"],
        kind: "curated",
      },
    ],
    cybersecurity: [
      {
        key: "cyber-secure-login",
        label: "Opción A · Ciberseguridad",
        title: "Secure Login Lab — Autenticación y control de acceso",
        summary: "Laboratorio local y defensivo para construir un flujo de autenticación, validación, límites de intentos y registro de eventos sin atacar servicios externos.",
        objective: "Implementar y probar controles defensivos de autenticación en un entorno propio o sandbox, documentando amenazas, mitigaciones y evidencias.",
        stack: ["Python or Web", "authentication", "rate limiting", "logging", "input validation"],
        kind: "curated",
      },
      {
        key: "cyber-log-dashboard",
        label: "Opción B · Ciberseguridad",
        title: "Security Log Dashboard — Detección de eventos anómalos",
        summary: "Generador o dataset de logs simulados y un dashboard que clasifica eventos, identifica patrones sospechosos y explica reglas de detección.",
        objective: "Diseñar un flujo defensivo de monitoreo con datos sintéticos o propios, reglas transparentes y visualización de alertas sin interactuar con sistemas ajenos.",
        stack: ["Python", "Pandas", "logging", "rule-based detection", "Matplotlib or Web"],
        kind: "curated",
      },
      {
        key: "cyber-input-hardening",
        label: "Opción C · Ciberseguridad",
        title: "Input Hardening Lab — Validación y sanitización segura",
        summary: "Aplicación local con formularios y casos de prueba controlados para demostrar validación, sanitización, mensajes seguros y registro de entradas inválidas.",
        objective: "Construir una aplicación de laboratorio que resista entradas malformadas mediante controles defensivos y demuestre el resultado con pruebas reproducibles.",
        stack: ["HTML", "JavaScript or Python", "input validation", "sanitization", "testing", "logging"],
        kind: "curated",
      },
    ],
    "3d-programming": [
      {
        key: "3d-parametric-stand",
        label: "Opción A · 3D",
        title: "Parametric Stand — Soporte funcional ajustable",
        summary: "Diseño paramétrico de un soporte para celular, tableta u objeto definido por el estudiante, con dimensiones y tolerancias modificables.",
        objective: "Modelar una pieza funcional parametrizada, validar medidas, exportar STL y documentar al menos una iteración de mejora.",
        stack: ["OpenSCAD or FreeCAD", "parametric CAD", "STL", "slicer", "3D printing"],
        kind: "curated",
      },
      {
        key: "3d-functional-organizer",
        label: "Opción B · 3D",
        title: "Functional Organizer — Organizador modular",
        summary: "Organizador funcional para escritorio, herramientas o componentes, diseñado a partir de restricciones reales de tamaño y uso.",
        objective: "Convertir requisitos medibles en geometría paramétrica, comprobar encajes y producir un prototipo imprimible con evidencia de iteración.",
        stack: ["OpenSCAD or FreeCAD", "parametric design", "measurement", "STL", "slicer"],
        kind: "curated",
      },
      {
        key: "3d-custom-adapter",
        label: "Opción C · 3D",
        title: "Custom Adapter — Adaptador o bracket paramétrico",
        summary: "Pieza de unión o adaptación para dos elementos físicos definidos por el estudiante, con énfasis en dimensiones, tolerancias y resistencia geométrica básica.",
        objective: "Diseñar una solución geométrica reproducible para un problema físico concreto y verificar sus dimensiones antes y después del prototipo.",
        stack: ["CAD", "parametric constraints", "STL", "slicer", "3D printing"],
        kind: "curated",
      },
    ],
    robotics: [
      {
        key: "robot-obstacle-rover",
        label: "Opción A · Robótica",
        title: "Obstacle Rover — Robot móvil con evasión",
        summary: "Robot o simulación que detecta obstáculos, decide entre estados y controla actuadores para desplazarse de manera segura.",
        objective: "Implementar el ciclo Sensor → Controller → Actuator con una máquina de estados, pruebas de escenarios y comportamiento seguro ante fallos.",
        stack: ["Arduino or MicroPython", "sensors", "motors", "state machine", "simulation"],
        kind: "curated",
      },
      {
        key: "robot-environment-monitor",
        label: "Opción B · Robótica",
        title: "Environment Monitor — Monitor ambiental con alertas",
        summary: "Sistema que mide una o más variables ambientales, procesa umbrales y activa indicadores o alertas con registro de lecturas.",
        objective: "Integrar sensores, lógica de decisión y salida visible, calibrar lecturas y validar el sistema con casos de prueba reproducibles.",
        stack: ["Arduino or MicroPython", "sensors", "display or LEDs", "logging", "state machine"],
        kind: "curated",
      },
      {
        key: "robot-automatic-control",
        label: "Opción C · Robótica",
        title: "Automatic Control System — Automatización de una tarea",
        summary: "Sistema automatizado para una tarea concreta elegida por el estudiante, con entradas, estados, actuadores y condiciones de seguridad.",
        objective: "Diseñar y prototipar un sistema automático con estados explícitos, manejo de fallos y pruebas que demuestren el comportamiento esperado.",
        stack: ["Arduino or MicroPython", "sensors", "actuators", "state machine", "simulation"],
        kind: "curated",
      },
    ],
  };
  return (map[track] || []).map((option) => ({ ...option, track_slug: track }));
}

const TRACKS = ["web", "data-science", "cybersecurity", "3d-programming", "robotics"] as const;
function validTrack(value: string) {
  return (TRACKS as readonly string[]).includes(value);
}
function customOption(track = ""): Option {
  return {
    key: "custom",
    label: "Mi propia idea",
    title: "",
    summary: "",
    objective: "",
    stack: [],
    track_slug: track,
    kind: "custom",
  };
}
function buildOptions(project: ProjectRow | null, preferredTrack = ""): Option[] {
  if (project) {
    const track = String(project.track_slug || "");
    return [
      proposalOption(project),
      ...curatedOptions(track),
      customOption(track),
    ];
  }

  const orderedTracks = validTrack(preferredTrack)
    ? [preferredTrack, ...TRACKS.filter((track) => track !== preferredTrack)]
    : [...TRACKS];

  return [
    ...orderedTracks.flatMap((track) => curatedOptions(track)),
    customOption(validTrack(preferredTrack) ? preferredTrack : ""),
  ];
}
function virtualProject(roster: Record<string, any>, preferredTrack = ""): ProjectRow {
  return {
    project_slug: null,
    track_slug: validTrack(preferredTrack) ? preferredTrack : "",
    project_title: "Aún no tienes un proyecto definido",
    project_summary: "Selecciona una de las opciones disponibles o plantea tu propia idea. Después concreta título, producto, objetivo, ruta técnica y herramientas antes de confirmar.",
    objective: "",
    stack: [],
    safety_scope: null,
    content_sections: [],
    sprints: [],
    assignment_status: "unassigned",
    decision_status: "proposed",
    decision_note: "No tienes un proyecto final definido todavía. Elige una base y conviértela en una propuesta concreta y verificable.",
    project_mode: "guided_definition",
    definition_questions: [
      "¿Quién usará o se beneficiará del producto?",
      "¿Qué problema concreto resolverá?",
      "¿Cuál es el producto mínimo funcional que puedes demostrar?",
      "¿Qué evidencia mostrará que el proyecto realmente funciona?"
    ],
    student_choice_key: null,
    student_decision_note: null,
    student_decided_at: null,
    student_revision_count: 0,
    updated_at: null,
    group_code: roster?.group_code || "",
    student_name: roster?.display_name || "",
  };
}
function projectPayload(project: ProjectRow) {
  return {
    is_defined: Boolean(project.project_slug),
    project_slug: project.project_slug,
    track_slug: project.track_slug,
    project_title: project.project_title,
    project_summary: project.project_summary,
    objective: project.objective,
    stack: project.stack,
    safety_scope: project.safety_scope,
    content_sections: project.content_sections,
    sprints: project.sprints,
    assignment_status: project.assignment_status,
    decision_status: project.decision_status,
    decision_note: project.decision_note,
    project_mode: project.project_mode,
    definition_questions: project.definition_questions,
    student_choice_key: project.student_choice_key,
    student_decision_note: project.student_decision_note,
    student_decided_at: project.student_decided_at,
    student_revision_count: project.student_revision_count,
    updated_at: project.updated_at,
  };
}

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("Origin");
  if (req.method === "OPTIONS") {
    if (!origin || !allowedOrigins.has(origin)) return json(origin, 403, { error: "origin_denied" });
    return new Response(null, { status: 204, headers: cors(origin) });
  }
  if (req.method !== "POST") return json(origin, 405, { error: "method_not_allowed" });
  if (!origin || !allowedOrigins.has(origin)) return json(origin, 404, { error: "not_found" });

  const suppliedApiKey = req.headers.get("apikey") ?? "";
  const publishable = getDefaultKey("SUPABASE_PUBLISHABLE_KEYS");
  const legacyAnon = Deno.env.get("SUPABASE_ANON_KEY") ?? "";
  if (!suppliedApiKey || (suppliedApiKey !== publishable && suppliedApiKey !== legacyAnon)) {
    return json(origin, 401, { error: "invalid_client" });
  }

  const url = Deno.env.get("SUPABASE_URL") ?? "";
  const secret = getDefaultKey("SUPABASE_SECRET_KEYS") || Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") || "";
  if (!url || !secret) return json(origin, 503, { error: "backend_unavailable" });

  const admin = createClient(url, secret, { auth: { persistSession: false, autoRefreshToken: false } });
  const ip = (req.headers.get("x-forwarded-for") ?? "").split(",")[0].trim();
  const userAgent = (req.headers.get("user-agent") ?? "").slice(0, 1000);

  try {
    const body = await req.json();
    const action = cleanText(body?.action, 32) || "load";
    const email = normalizeEmail(body?.email);
    if (!email || !email.endsWith("@ijr.edu.co") || email.length < 8) {
      return json(origin, 400, { error: "institutional_email_required" });
    }

    const emailHash = await sha256(email);
    const ipHash = await sha256(ip);

    const identityResult = await admin
      .from("python_hub_student_identities")
      .select("student_registry_id,display_name,institutional_email,user_code")
      .eq("institutional_email", email)
      .limit(1)
      .maybeSingle();

    if (identityResult.error) throw identityResult.error;
    const identity = identityResult.data;

    if (!identity?.student_registry_id) {
      await admin.from("seminar_project_access_events").insert({
        student_registry_id: null,
        success: false,
        email_hash: emailHash,
        ip_hash: ipHash,
        user_agent: userAgent,
      });
      return json(origin, 404, { error: "project_access_denied" });
    }

    const projectSelect = "group_code,student_name,project_slug,track_slug,project_title,project_summary,objective,stack,initial_project_title,initial_project_summary,initial_objective,initial_stack,safety_scope,content_sections,sprints,assignment_status,decision_status,decision_note,project_mode,definition_questions,student_choice_key,student_decision_note,student_decided_at,student_revision_count,updated_at";
    const [projectResult, rosterResult, studioResult] = await Promise.all([
      admin.from("seminar_student_projects").select(projectSelect).eq("student_registry_id", identity.student_registry_id).maybeSingle(),
      admin.from("student_registry").select("display_name,group_code,active").eq("id", identity.student_registry_id).maybeSingle(),
      admin.from("seminar_studio_profiles")
        .select("track_slug")
        .eq("student_registry_id", identity.student_registry_id)
        .order("updated_at", { ascending: false })
        .limit(1)
        .maybeSingle(),
    ]);

    if (projectResult.error) throw projectResult.error;
    if (rosterResult.error) throw rosterResult.error;
    if (studioResult.error) throw studioResult.error;
    let project = projectResult.data as ProjectRow | null;
    const roster = rosterResult.data;
    const preferredTrack = validTrack(String(studioResult.data?.track_slug || ""))
      ? String(studioResult.data?.track_slug)
      : "";

    if (!roster?.active || !["11A", "11B", "11C"].includes(String(roster.group_code || ""))) {
      await admin.from("seminar_project_access_events").insert({
        student_registry_id: identity.student_registry_id,
        success: false,
        email_hash: emailHash,
        ip_hash: ipHash,
        user_agent: userAgent,
      });
      return json(origin, 404, { error: "project_access_denied" });
    }

    if (action === "save_decision") {
      let authorized = false;
      const editToken = cleanText(body?.edit_token, 160);
      if (/^[a-f0-9]{48,128}$/i.test(editToken)) {
        const tokenHash = await sha256(editToken);
        const tokenMatch = await admin
          .from("seminar_studio_profiles")
          .select("id")
          .eq("edit_token_hash", tokenHash)
          .eq("student_registry_id", identity.student_registry_id)
          .limit(1)
          .maybeSingle();
        if (tokenMatch.error) throw tokenMatch.error;
        authorized = Boolean(tokenMatch.data);
      }

      if (!authorized) {
        const suppliedCode = normalizeStudentCode(body?.student_code);
        const storedCode = normalizeStudentCode(identity.user_code);
        authorized = Boolean(suppliedCode && storedCode && suppliedCode === storedCode);
      }

      if (!authorized) {
        return json(origin, 403, { error: "write_authorization_required" });
      }

      const choiceKey = cleanText(body?.choice_key, 80);
      const requestedTrack = cleanText(body?.track_slug, 40);
      const options = buildOptions(project, preferredTrack);
      const selectedOption = options.find((option) => option.key === choiceKey);
      if (!selectedOption) {
        return json(origin, 400, { error: "invalid_choice" });
      }
      if (!validTrack(requestedTrack)) {
        return json(origin, 400, { error: "track_required" });
      }
      if (project && requestedTrack !== String(project.track_slug || "")) {
        return json(origin, 409, { error: "track_change_not_allowed" });
      }
      if (selectedOption.kind !== "custom" && selectedOption.track_slug !== requestedTrack) {
        return json(origin, 400, { error: "invalid_track_choice" });
      }

      const title = cleanText(body?.project_title, 180);
      const summary = cleanText(body?.project_summary, 1600);
      const objective = cleanText(body?.objective, 1200);
      const studentNote = cleanText(body?.student_note, 1200);
      const stack = Array.isArray(body?.stack)
        ? body.stack.map((x: unknown) => cleanText(x, 80)).filter(Boolean).slice(0, 12)
        : [];

      if (title.length < 3 || summary.length < 10 || objective.length < 10) {
        return json(origin, 400, { error: "project_fields_required" });
      }

      const saved = await admin.rpc("seminar_student_project_save_decision_v2", {
        p_student_registry_id: identity.student_registry_id,
        p_track_slug: requestedTrack,
        p_choice_key: choiceKey,
        p_project_title: title,
        p_project_summary: summary,
        p_objective: objective,
        p_stack: stack,
        p_student_note: studentNote || null,
        p_ip_hash: ipHash,
        p_user_agent: userAgent,
      });
      if (saved.error) throw saved.error;

      const refreshed = await admin
        .from("seminar_student_projects")
        .select(projectSelect)
        .eq("student_registry_id", identity.student_registry_id)
        .single();
      if (refreshed.error) throw refreshed.error;
      project = refreshed.data as ProjectRow;

      return json(origin, 200, {
        ok: true,
        saved: true,
        student: { name: roster.display_name, group_code: roster.group_code, institutional_email: identity.institutional_email },
        project: projectPayload(project),
        options: buildOptions(project, preferredTrack),
      });
    }

    if (action !== "load") return json(origin, 404, { error: "not_found" });

    await admin.from("seminar_project_access_events").insert({
      student_registry_id: identity.student_registry_id,
      success: true,
      email_hash: emailHash,
      ip_hash: ipHash,
      user_agent: userAgent,
    });

    return json(origin, 200, {
      ok: true,
      student: { name: roster.display_name, group_code: roster.group_code, institutional_email: identity.institutional_email },
      project: projectPayload(project ?? virtualProject(roster, preferredTrack)),
      options: buildOptions(project, preferredTrack),
    });
  } catch (error) {
    console.error(error);
    return json(origin, 400, { error: "invalid_request" });
  }
});
