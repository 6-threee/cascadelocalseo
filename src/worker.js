// cascadelocalseo.com Worker
// - /audit and /audit?prospect=N  → proxies to Supabase self-audit function
// - /audits/<id>                   → proxies to Supabase render-audit function
// - everything else                → static assets from ./public via env.ASSETS

const SUPABASE_SELF_AUDIT = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/self-audit";
const SUPABASE_AI_READINESS = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/ai-readiness";
const SUPABASE_RENDER_AUDIT = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/render-audit";
const SUPABASE_APPROVE_AUDIT = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/approve-audit";
const SUPABASE_DASHBOARD = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/dashboard";
const SUPABASE_RENDER_BLOG = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/render-blog";
const SUPABASE_RENDER_LEADERBOARD = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/render-leaderboard";
const SUPABASE_CLIENT_DASHBOARD = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/render-client-dashboard";
const SUPABASE_GENERATE_SCHEMA = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/generate-schema";

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

// /ai-readiness (+ /ai-check alias) → free "is AI recommending you?" instant-score lead magnet,
// proxied to the Supabase ai-readiness function. GET renders the form/score; POST captures email.
async function proxyAiReadiness(request, url) {
  const target = `${SUPABASE_AI_READINESS}${url.search}`;
  const headers = new Headers(request.headers);
  headers.delete("host");
  headers.delete("cf-connecting-ip");
  headers.delete("cf-ray");
  headers.delete("cf-visitor");
  headers.set("x-forwarded-host", url.host);
  headers.set("x-forwarded-proto", "https");
  const init = { method: request.method, headers, redirect: "manual" };
  if (request.method !== "GET" && request.method !== "HEAD") {
    init.body = await request.arrayBuffer();
  }
  const upstream = await fetch(target, init);
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: { "content-type": "text/html; charset=utf-8", "cache-control": "no-store" },
  });
}

async function proxyRenderAudit(id, url) {
  const flyer = url && url.searchParams.get("flyer") === "1" ? "&flyer=1" : "";
  const target = `${SUPABASE_RENDER_AUDIT}?id=${encodeURIComponent(id)}${flyer}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store, no-cache, must-revalidate",
    },
  });
}

async function proxyApproveAudit(url) {
  const target = `${SUPABASE_APPROVE_AUDIT}${url.search}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
    },
  });
}

async function proxyDashboard(url) {
  const target = `${SUPABASE_DASHBOARD}${url.search}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow",
    },
  });
}

// /client/<token> → a retainer client's private, token-gated live results dashboard, proxied to
// the Supabase render-client-dashboard function. The unguessable token IS the key; the function
// 404s on a bad/missing one. no-store + noindex so these private pages are never cached or crawled.
async function proxyClientDashboard(path) {
  const token = path.slice("/client/".length).split("/")[0];
  const target = `${SUPABASE_CLIENT_DASHBOARD}?token=${encodeURIComponent(token)}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow",
    },
  });
}

async function proxyRenderBlog(path, url) {
  let target;
  if (path === "/blog") target = `${SUPABASE_RENDER_BLOG}?mode=index`;
  else if (path === "/blog/sitemap.xml") target = `${SUPABASE_RENDER_BLOG}?mode=sitemap`;
  else if (path === "/blog/approve") target = `${SUPABASE_RENDER_BLOG}?mode=approve&${url.searchParams.toString()}`;
  else if (path.startsWith("/blog/preview/")) target = `${SUPABASE_RENDER_BLOG}?mode=post&preview=1&slug=${encodeURIComponent(path.slice("/blog/preview/".length))}`;
  else target = `${SUPABASE_RENDER_BLOG}?mode=post&slug=${encodeURIComponent(path.slice("/blog/".length))}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  const isXml = path === "/blog/sitemap.xml";
  const noCache = path === "/blog/approve" || path.startsWith("/blog/preview/");
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": isXml ? "application/xml; charset=utf-8" : "text/html; charset=utf-8",
      "cache-control": noCache ? "no-store" : "public, max-age=300",
    },
  });
}

// /leaderboards, /leaderboards/<slug>, /leaderboards/sitemap.xml → public "Google Maps Power
// Rankings" boards, proxied to the Supabase render-leaderboard function. (Renamed from /rankings;
// the old paths 301-redirect here, see the router below.)
async function proxyRenderLeaderboard(path, url) {
  let target;
  if (path === "/leaderboards") target = `${SUPABASE_RENDER_LEADERBOARD}?mode=index`;
  else if (path === "/leaderboards/sitemap.xml") target = `${SUPABASE_RENDER_LEADERBOARD}?mode=sitemap`;
  else target = `${SUPABASE_RENDER_LEADERBOARD}?mode=board&slug=${encodeURIComponent(path.slice("/leaderboards/".length))}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  const isXml = path === "/leaderboards/sitemap.xml";
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": isXml ? "application/xml; charset=utf-8" : "text/html; charset=utf-8",
      "cache-control": "public, max-age=600",
    },
  });
}

// /schema?prospect_id=N (or ?client_id / direct params) → the AI-Ready Schema
// Package deliverable. Forces format=html and serves it under the brand domain so
// the audit's "Preview your structured data" link is on-brand (and renders for
// everyone, including HTTPS-inspected machines that mangle raw supabase.co HTML).
async function proxySchema(url) {
  const params = new URLSearchParams(url.search);
  params.set("format", "html");
  const target = `${SUPABASE_GENERATE_SCHEMA}?${params.toString()}`;
  const upstream = await fetch(target);
  const body = await upstream.text();
  return new Response(body, {
    status: upstream.status,
    headers: {
      "content-type": "text/html; charset=utf-8",
      "cache-control": "no-store",
      "x-robots-tag": "noindex, nofollow",
    },
  });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/\/+$/, "") || "/";

    // /gbp was the standalone $299 GBP Optimization Pass LP. That offer folded into the
    // $199 AI-Ready Foundations on-ramp (2026-06-04), so funnel the old paid path to it
    // instead of serving a page whose Stripe link is now deactivated. (/gbp-thanks, the
    // post-checkout success page, is a different path and is intentionally not caught.)
    if (path === "/gbp") {
      return Response.redirect(`${url.origin}/#foundations`, 302);
    }

    if (path === "/schema") {
      return proxySchema(url);
    }

    if (path === "/audit") {
      return proxySelfAudit(request, url);
    }

    if (path === "/ai-readiness" || path === "/ai-check") {
      return proxyAiReadiness(request, url);
    }

    if (path === "/approve") {
      return proxyApproveAudit(url);
    }

    if (path === "/dashboard") {
      return proxyDashboard(url);
    }

    if (path.startsWith("/client/")) {
      return proxyClientDashboard(path);
    }

    // /exec-dashboard → token-walled executive dashboard (static shell in ./public, live ops data
    // fetched client-side from the exec-dashboard-data edge fn). The .html form would hit ASSETS'
    // html_handling redirect and drop ?token, so redirect it ourselves preserving the query; gate
    // the extensionless path (ASSETS serves the .html content there directly, 200). The
    // /exec-dashboard.css and .js assets are intentionally NOT gated (no secret data) so styling/
    // scripts load for an authorized viewer. Gate = SHA-256(token) vs a baked-in hash, so no Worker
    // secret is needed (deploy.py replaces bindings on every PUT, which would wipe a secret); only
    // the hash lives in source and the 40-hex-char token is not recoverable from it. The same token
    // value is stored in config.exec_dashboard_token for the data fn.
    if (path === "/exec-dashboard.html") {
      return Response.redirect(`${url.origin}/exec-dashboard${url.search}`, 301);
    }
    if (path === "/exec-dashboard") {
      const EXEC_TOKEN_SHA256 = "9f1c37b7e6131334705cf2e96a3fdc427e0a70a5320604332b8e22d61580afd7";
      const supplied = url.searchParams.get("token") || "";
      const digest = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(supplied));
      const hex = Array.from(new Uint8Array(digest)).map((b) => b.toString(16).padStart(2, "0")).join("");
      if (hex !== EXEC_TOKEN_SHA256) {
        return new Response("Not found", { status: 404 });
      }
      return env.ASSETS.fetch(request);
    }

    // Google Search Console verification. Served straight from the Worker so the
    // exact .html path returns 200 — static-asset html_handling would otherwise
    // redirect /<file>.html → /<file>, which Google's file verifier rejects.
    if (path === "/google9fa7c234c0ae307a.html") {
      return new Response("google-site-verification: google9fa7c234c0ae307a.html", {
        headers: { "content-type": "text/html; charset=utf-8" },
      });
    }

    if (path === "/blog" || path.startsWith("/blog/")) {
      return proxyRenderBlog(path, url);
    }

    // Renamed /rankings to /leaderboards; 301 the old paths so indexed URLs migrate cleanly.
    if (path === "/rankings" || path.startsWith("/rankings/")) {
      return Response.redirect(`${url.origin}/leaderboards${path.slice("/rankings".length)}${url.search}`, 301);
    }
    if (path === "/leaderboards" || path.startsWith("/leaderboards/")) {
      return proxyRenderLeaderboard(path, url);
    }

    const auditMatch = path.match(/^\/audits\/(\d+)$/);
    if (auditMatch) {
      return proxyRenderAudit(auditMatch[1], url);
    }

    if (env.ASSETS && typeof env.ASSETS.fetch === "function") {
      return env.ASSETS.fetch(request);
    }
    return new Response("Not found", { status: 404 });
  },
};
