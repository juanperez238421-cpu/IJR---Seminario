import "jsr:@supabase/functions-js/edge-runtime.d.ts";
import { createClient } from "npm:@supabase/supabase-js@2";

const allowedOrigins = new Set([
  "https://juanperez238421-cpu.github.io",
  "http://localhost:8000",
  "http://127.0.0.1:8000",
]);

function cors(origin: string | null) {
  return {
    "Access-Control-Allow-Origin": origin && allowedOrigins.has(origin) ? origin : "null",
    "Access-Control-Allow-Headers": "content-type, apikey, authorization, x-client-info",
    "Access-Control-Allow-Methods": "POST, OPTIONS",
    "Content-Type": "application/json; charset=utf-8",
    "Cache-Control": "no-store",
    "Vary": "Origin",
  };
}
function json(origin: string | null, status: number, body: unknown) {
  return new Response(JSON.stringify(body), { status, headers: cors(origin) });
}
function text(v: unknown, max: number) {
  return typeof v === "string" ? v.trim().slice(0, max) : "";
}
function normalize(value: string) {
  return value.normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, " ")
    .trim();
}
function identityKey(value: string) {
  return normalize(value).split(/\s+/).filter(Boolean).sort().join(" ");
}
async function sha256(value: string) {
  const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(value));
  return Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
}

Deno.serve(async (req: Request) => {
  const origin = req.headers.get("Origin");
  if (req.method === "OPTIONS") {
    if (!origin || !allowedOrigins.has(origin)) return json(origin, 403, { error: "origin_denied" });
    return new Response(null, { status: 204, headers: cors(origin) });
  }
  if (req.method !== "POST") return json(origin, 405, { error: "method_not_allowed" });
  if (!origin || !allowedOrigins.has(origin)) return json(origin, 404, { error: "not_found" });

  const url = Deno.env.get("SUPABASE_URL") ?? "";
  const serviceRoleKey = Deno.env.get("SUPABASE_SERVICE_ROLE_KEY") ?? "";
  if (!url || !serviceRoleKey) return json(origin, 503, { error: "backend_unavailable" });

  try {
    const body = await req.json();
    const editToken = text(body?.edit_token, 160);
    if (!/^[a-f0-9]{48,128}$/i.test(editToken)) return json(origin, 400, { error: "invalid_edit_token" });

    const admin = createClient(url, serviceRoleKey, {
      auth: { persistSession: false, autoRefreshToken: false },
    });
    const tokenHash = await sha256(editToken);
    const { data: profile, error: profileError } = await admin
      .from("seminar_studio_profiles")
      .select("student_registry_id,full_name,group_code")
      .eq("edit_token_hash", tokenHash)
      .maybeSingle();
    if (profileError) throw profileError;
    if (!profile) return json(origin, 404, { error: "profile_not_found" });

    let assignment: any = null;
    if (profile.student_registry_id) {
      const direct = await admin
        .from("seminar_student_projects")
        .select("*")
        .eq("student_registry_id", profile.student_registry_id)
        .maybeSingle();
      if (direct.error) throw direct.error;
      assignment = direct.data;
    }

    if (!assignment) {
      const groupCode = String(profile.group_code ?? "").replace(/-/g, "");
      const candidates = await admin
        .from("seminar_student_projects")
        .select("*")
        .eq("group_code", groupCode)
        .limit(100);
      if (candidates.error) throw candidates.error;
      const key = identityKey(String(profile.full_name ?? ""));
      assignment = (candidates.data ?? []).find((row: any) =>
        identityKey(String(row.student_name ?? "")) === key
      ) ?? null;
    }

    return json(origin, 200, { ok: true, assignment });
  } catch (error) {
    console.error(error);
    return json(origin, 400, { error: "invalid_request" });
  }
});