// cascadelocalseo.com Worker
// - /audit and /audit?prospect=N  → proxies to Supabase self-audit function
// - /audits/<id>                   → proxies to Supabase render-audit function
// - everything else                → static assets from ./public via env.ASSETS

const SUPABASE_SELF_AUDIT = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/self-audit";
const SUPABASE_RENDER_AUDIT = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/render-audit";

async function proxySelfAudit(request, url) {
  const target = `${SUPABASE_SELF_AUDIT}${url.search}`;
  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("cf-connecting-ip");
  headers.delete("cf-ray");
  headers.delete("cf-visitor");
  headers.set("x-forwarded-host", url.host);
  headers.set("x-forwarded-proto", "https");

  const init = {
    method: request.method,
    headers,
    redirect: "manual",
  };

  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = await request.arrayBuffer();
  }

  const upstream = await fetch(target, init);
  // Read body as text so we can control the content-type explicitly
  // (the streaming proxy was downgrading text/html → text/plain somewhere in the chain).
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

async function proxyRenderAudit(id) {
  const target = `${SUPABASE_RENDER_AUDIT}?id=${encodeURIComponent(id)}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "public, max-age=300",
    },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";

    if (path === "/audit") {
      return proxySelfAudit(request, url);
    }

    const auditMatch = path.match(/^\/audits\/(\d+)$/);
    if (auditMatch) {
      return proxyRenderAudit(auditMatch[1]);
    }

    if (env.ASSETS && typeof env.ASSETS.fetch === "function") {
      return env.ASSETS.fetch(request);
    }
    return new Response("Not found", { status: 404 });
  },
};
