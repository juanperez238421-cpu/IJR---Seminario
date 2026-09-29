import http from 'node:http';
import { performance } from 'node:perf_hooks';

const PORT = Number(process.env.PORT || 3000);
const REPORT_COST_MS = Math.max(5, Math.min(100, Number(process.env.REPORT_COST_MS || 35)));
const MAX_BODY_BYTES = 256 * 1024;

const metrics = {
  startedAt: Date.now(),
  total: 0,
  byStatus: {},
  byPath: {},
  recentLatencyMs: []
};

function record(path, status, durationMs) {
  metrics.total += 1;
  metrics.byStatus[status] = (metrics.byStatus[status] || 0) + 1;
  metrics.byPath[path] = (metrics.byPath[path] || 0) + 1;
  metrics.recentLatencyMs.push(durationMs);
  if (metrics.recentLatencyMs.length > 1000) metrics.recentLatencyMs.shift();
}

function percentile95(values) {
  if (!values.length) return 0;
  const copy = [...values].sort((a, b) => a - b);
  const index = Math.min(copy.length - 1, Math.ceil(copy.length * 0.95) - 1);
  return Number(copy[index].toFixed(2));
}

function json(res, status, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(status, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function html(res, status, body) {
  res.writeHead(status, {
    'Content-Type': 'text/html; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store'
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let size = 0;
    const chunks = [];
    req.on('data', chunk => {
      size += chunk.length;
      if (size > MAX_BODY_BYTES) {
        reject(Object.assign(new Error('payload_too_large'), { status: 413 }));
        req.destroy();
        return;
      }
      chunks.push(chunk);
    });
    req.on('end', () => resolve(Buffer.concat(chunks).toString('utf8')));
    req.on('error', reject);
  });
}

function cpuBoundWork(ms) {
  const end = performance.now() + ms;
  let x = 0;
  while (performance.now() < end) {
    x = (x + Math.sqrt((x % 1000) + 1)) % 100000;
  }
  return x;
}

const server = http.createServer(async (req, res) => {
  const started = performance.now();
  const path = new URL(req.url, 'http://lab.local').pathname;
  let status = 500;

  try {
    if (req.method === 'GET' && path === '/') {
      status = 200;
      html(res, status, `<!doctype html>
<html lang="es">
<head><meta charset="utf-8"><title>IJR Web Defense Lab</title></head>
<body>
  <main>
    <h1>IJR Web Defense Lab</h1>
    <p>Aplicación objetivo del laboratorio defensivo.</p>
    <p>Rutas de prueba: <code>/health</code>, <code>/metrics</code>, <code>/api/report</code>, <code>/login</code> y <code>/api/echo</code>.</p>
  </main>
</body>
</html>`);
      return;
    }

    if (req.method === 'GET' && path === '/health') {
      status = 200;
      json(res, status, { ok: true, uptimeSeconds: Math.round(process.uptime()) });
      return;
    }

    if (req.method === 'GET' && path === '/metrics') {
      status = 200;
      json(res, status, {
        uptimeSeconds: Math.round((Date.now() - metrics.startedAt) / 1000),
        requests: metrics.total,
        byStatus: metrics.byStatus,
        byPath: metrics.byPath,
        p95LatencyMs: percentile95(metrics.recentLatencyMs),
        recentSamples: metrics.recentLatencyMs.length
      });
      return;
    }

    if (req.method === 'GET' && path === '/api/report') {
      const checksum = cpuBoundWork(REPORT_COST_MS);
      status = 200;
      json(res, status, {
        report: 'synthetic-school-report',
        generatedAt: new Date().toISOString(),
        checksum: Number(checksum.toFixed(2)),
        costMs: REPORT_COST_MS
      });
      return;
    }

    if (req.method === 'POST' && path === '/login') {
      const raw = await readBody(req);
      let body;
      try {
        body = JSON.parse(raw || '{}');
      } catch {
        status = 400;
        json(res, status, { ok: false, error: 'invalid_json' });
        return;
      }

      const username = typeof body.username === 'string' ? body.username.slice(0, 80) : '';
      const password = typeof body.password === 'string' ? body.password : '';
      const valid = username === 'blue-team' && password === 'lab-only-password';

      status = valid ? 200 : 401;
      json(res, status, valid ? { ok: true, role: 'student' } : { ok: false, error: 'invalid_credentials' });
      return;
    }

    if (req.method === 'POST' && path === '/api/echo') {
      const raw = await readBody(req);
      let parsed;
      try {
        parsed = JSON.parse(raw || '{}');
      } catch {
        status = 400;
        json(res, status, { ok: false, error: 'invalid_json' });
        return;
      }

      status = 200;
      json(res, status, {
        ok: true,
        receivedType: Array.isArray(parsed) ? 'array' : typeof parsed,
        bytes: Buffer.byteLength(raw)
      });
      return;
    }

    status = 404;
    json(res, status, { ok: false, error: 'not_found' });
  } catch (error) {
    status = Number(error?.status || 500);
    if (!res.headersSent) {
      json(res, status, { ok: false, error: status === 413 ? 'payload_too_large' : 'internal_error' });
    } else {
      res.end();
    }
  } finally {
    const durationMs = Number((performance.now() - started).toFixed(2));
    record(path, status, durationMs);
    process.stdout.write(JSON.stringify({
      ts: new Date().toISOString(),
      method: req.method,
      path,
      status,
      durationMs
    }) + '\n');
  }
});

server.listen(PORT, '0.0.0.0', () => {
  process.stdout.write(JSON.stringify({
    ts: new Date().toISOString(),
    event: 'server_started',
    port: PORT,
    reportCostMs: REPORT_COST_MS
  }) + '\n');
});
