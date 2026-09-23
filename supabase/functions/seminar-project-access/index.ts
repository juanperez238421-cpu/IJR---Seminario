import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const allowedOrigins = new Set([
  "https://rlfxnjbqxbozjdzkbwlz.supabase.co",
  "https://juanperez238421-cpu.github.io",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
]);

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
    const email = normalizeEmail(body?.email);
    if (!email || !email.endsWith("@ijr.edu.co") || email.length < 8) {
      return json(origin, 400, { error: "institutional_email_required" });
    }

    const emailHash = await sha256(email);
    const ipHash = await sha256(ip);

    const identityResult = await admin
      .from("python_hub_student_identities")
      .select("student_registry_id,display_name,institutional_email")
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

    const [projectResult, rosterResult] = await Promise.all([
      admin
        .from("seminar_student_projects")
        .select("group_code,student_name,project_slug,track_slug,project_title,project_summary,objective,stack,safety_scope,sprints,assignment_status,decision_status,decision_note,project_mode,definition_questions,updated_at")
        .eq("student_registry_id", identity.student_registry_id)
        .maybeSingle(),
      admin
        .from("student_registry")
        .select("display_name,group_code,active")
        .eq("id", identity.student_registry_id)
        .maybeSingle(),
    ]);

    if (projectResult.error) throw projectResult.error;
    if (rosterResult.error) throw rosterResult.error;
    const project = projectResult.data;
    const roster = rosterResult.data;

    if (!project || !roster?.active) {
      await admin.from("seminar_project_access_events").insert({
        student_registry_id: identity.student_registry_id,
        success: false,
        email_hash: emailHash,
        ip_hash: ipHash,
        user_agent: userAgent,
      });
      return json(origin, 404, { error: "project_not_assigned" });
    }

    await admin.from("seminar_project_access_events").insert({
      student_registry_id: identity.student_registry_id,
      success: true,
      email_hash: emailHash,
      ip_hash: ipHash,
      user_agent: userAgent,
    });

    return json(origin, 200, {
      ok: true,
      student: {
        name: roster.display_name,
        group_code: roster.group_code,
      },
      project: {
        project_slug: project.project_slug,
        track_slug: project.track_slug,
        project_title: project.project_title,
        project_summary: project.project_summary,
        objective: project.objective,
        stack: project.stack,
        safety_scope: project.safety_scope,
        sprints: project.sprints,
        assignment_status: project.assignment_status,
        decision_status: project.decision_status,
        decision_note: project.decision_note,
        project_mode: project.project_mode,
        definition_questions: project.definition_questions,
        updated_at: project.updated_at,
      },
    });
  } catch (error) {
    console.error(error);
    return json(origin, 400, { error: "invalid_request" });
  }
});