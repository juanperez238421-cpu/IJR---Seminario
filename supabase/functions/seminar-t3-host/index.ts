const FUNCTION_NAME = "seminar-t3-host";
const UPSTREAM_BASE = "https://raw.githubusercontent.com/juanperez238421-cpu/IJR---Seminario/main/t3/";
const REPO_HOME = "https://github.com/juanperez238421-cpu/IJR---Seminario";
const OOP_UML_EMAIL_BUILD = "20260923-email-v11";
const OOP_UML_REGISTRATION_PANEL = `  <section id="registrationPanel" class="registration-screen">
    <div class="registration-card">
      <p class="eyebrow">SOFTWARE ENGINEERING STUDIO · COMMON CORE</p>
      <h1>Sign in with your institutional email.</h1>
      <p class="registration-lead">Enter only your <strong>@ijr.edu.co institutional email</strong>. Supabase resolves your official name and Grade 11 group automatically. No password, student name, group, language, registration mode or team field is requested.</p>

      <div class="sequence-rule">
        <strong>10-session progression</strong>
        <span>Objects → State → Constructors → Encapsulation → Relationships → Inheritance → Polymorphism → Architecture → Refactoring → Defense</span>
        <small>Every session has a dedicated Theory page and Workshop. Python opens automatically for this Common Core route.</small>
      </div>

      <form id="registrationForm" class="hub-registration-form" novalidate>
        <div class="registration-grid">
          <label>Institutional email <small>· Correo institucional</small>
            <input id="institutionalEmail" name="institutionalEmail" type="email" inputmode="email"
                   autocomplete="email" placeholder="nombre.apellido@ijr.edu.co" required>
          </label>
        </div>

        <div class="sequence-rule">
          <strong>Automatic identity resolution</strong>
          <span>Your email is matched server-side against the official Grade 11 Seminar roster.</span>
          <small>After validation, your official name and group are attached to the tracked OOP + UML session automatically.</small>
        </div>

        <div class="registration-actions">
          <div><strong>Common Core rule</strong><span>predict → model → implement → test → explain. A program that only runs is not sufficient evidence of mastery.</span></div>
          <button id="registerButton" class="button button-dark" type="submit">Enter OOP + UML Hub</button>
        </div>
        <p id="registrationStatus" class="inline-status" role="status" aria-live="polite"></p>
      </form>
    </div>
  </section>`;

const MIME: Record<string, string> = {
  html: "text/html; charset=utf-8",
  css: "text/css; charset=utf-8",
  js: "text/javascript; charset=utf-8",
  mjs: "text/javascript; charset=utf-8",
  json: "application/json; charset=utf-8",
  txt: "text/plain; charset=utf-8",
  svg: "image/svg+xml",
  png: "image/png",
  jpg: "image/jpeg",
  jpeg: "image/jpeg",
  ico: "image/x-icon",
  webp: "image/webp",
};

function headersFor(path: string): Headers {
  const ext = path.split(".").pop()?.toLowerCase() ?? "";
  return new Headers({
    "Content-Type": MIME[ext] ?? "application/octet-stream",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Access-Control-Allow-Origin": "*",
    "Cache-Control": ext === "html" ? "no-store, max-age=0" : "public, max-age=60",
  });
}

function safeRelativePath(url: URL): { path?: string; redirect?: string; error?: string } {
  const pathname = decodeURIComponent(url.pathname);
  const markers = [`/functions/v1/${FUNCTION_NAME}`, `/${FUNCTION_NAME}`];
  let suffix: string | null = null;

  for (const marker of markers) {
    if (pathname === marker) {
      return { redirect: `${url.origin}${pathname}/${url.search}` };
    }
    if (pathname.startsWith(`${marker}/`)) {
      suffix = pathname.slice(marker.length + 1);
      break;
    }
  }

  // Supabase Edge Runtime may expose the path after the function name only,
  // e.g. "/", "/teacher.html" or "/data/course-index.json".
  if (suffix === null) suffix = pathname.replace(/^\/+/, "");

  let path = suffix || "index.html";
  if (path.endsWith("/")) path += "index.html";

  if (path.includes("..") || path.includes("\\") || path.startsWith("/")) {
    return { error: "Unsafe path" };
  }
  if (!/^[A-Za-z0-9_./-]+$/.test(path)) return { error: "Unsupported path" };
  return { path };
}

function rewriteHtml(html: string): string {
  return html
    .replaceAll('href="../monitor.html"', `href="${REPO_HOME}/blob/main/monitor.html"`)
    .replaceAll('href="../progress.html"', `href="${REPO_HOME}/blob/main/progress.html"`)
    .replaceAll('href="../"', `href="${REPO_HOME}"`);
}

function rewriteOopUmlHtml(html: string): string {
  const startMarker = '<section id="registrationPanel"';
  const endMarker = '<main id="hubPanel"';
  const start = html.indexOf(startMarker);
  const end = start >= 0 ? html.indexOf(endMarker, start) : -1;

  if (start >= 0 && end > start) {
    html = html.slice(0, start) + OOP_UML_REGISTRATION_PANEL + "\n\n  " + html.slice(end);
  }

  html = html
    .replace(/<script src="\.\.\/access-gate\.js[^"]*"><\/script>\s*/g, "")
    .replace(/hub\.js\?v=[^"]+/g, `hub.js?v=${OOP_UML_EMAIL_BUILD}`);

  if (!html.includes('data-oop-uml-build=')) {
    html = html.replace("<body>", `<body data-oop-uml-build="${OOP_UML_EMAIL_BUILD}">`);
  }

  const legacyOopUmlFields = /id="(?:memberName1|groupCode|registrationMode|language)"/;
  if (
    !html.includes('id="institutionalEmail"') ||
    !html.includes('type="email"') ||
    legacyOopUmlFields.test(html) ||
    html.includes("Register the student or exact classroom team")
  ) {
    throw new Error("oop_uml_email_only_rewrite_failed");
  }

  return html;
}

Deno.serve(async (req: Request) => {
  if (req.method === "OPTIONS") {
    return new Response(null, {
      status: 204,
      headers: {
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Allow-Methods": "GET, HEAD, OPTIONS",
        "Access-Control-Allow-Headers": "content-type",
      },
    });
  }

  if (req.method !== "GET" && req.method !== "HEAD") {
    return new Response("Method not allowed", { status: 405, headers: { Allow: "GET, HEAD, OPTIONS" } });
  }

  const url = new URL(req.url);
  const route = safeRelativePath(url);
  if (route.redirect) return Response.redirect(route.redirect, 308);
  if (route.error || !route.path) return new Response(route.error ?? "Bad request", { status: 400 });

  const upstreamUrl = new URL(`${UPSTREAM_BASE}${route.path}`);
  if (route.path === "oop-uml/index.html" || route.path === "oop-uml/hub.js") {
    upstreamUrl.searchParams.set("_ijr_build", OOP_UML_EMAIL_BUILD);
    upstreamUrl.searchParams.set("_ijr_now", Date.now().toString());
  }

  const upstream = await fetch(upstreamUrl, {
    cache: "no-store",
    headers: {
      "User-Agent": "IJR-Seminar-T3-Static-Host/1.3",
      "Cache-Control": "no-cache, no-store, max-age=0",
      "Pragma": "no-cache",
    },
  });

  if (!upstream.ok) {
    return new Response("Not found", {
      status: upstream.status === 404 ? 404 : 502,
      headers: { "Content-Type": "text/plain; charset=utf-8", "Cache-Control": "no-store" },
    });
  }

  const headers = headersFor(route.path);
  headers.set("X-IJR-Source", "GitHub-main:t3");

  const isOopUmlIndex = route.path === "oop-uml/index.html";
  const isOopUmlHubJs = route.path === "oop-uml/hub.js";
  if (isOopUmlIndex || isOopUmlHubJs) {
    headers.set("Cache-Control", "no-store, no-cache, must-revalidate, max-age=0");
    headers.set("Pragma", "no-cache");
    headers.set("Expires", "0");
    headers.set("X-IJR-Build", OOP_UML_EMAIL_BUILD);
  }

  if (req.method === "HEAD") return new Response(null, { status: 200, headers });

  const ext = route.path.split(".").pop()?.toLowerCase();
  if (ext === "html") {
    let html = rewriteHtml(await upstream.text());
    if (isOopUmlIndex) html = rewriteOopUmlHtml(html);
    return new Response(html, { status: 200, headers });
  }

  return new Response(upstream.body, { status: 200, headers });
});
