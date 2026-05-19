// Cloudflare Pages Function — proxies /audit on cascadelocalseo.com
// to the Supabase self-audit edge function. Preserves URL in browser.
//
// GET  /audit               → renders the self-audit form
// POST /audit               → submits the self-audit (handled by Supabase)
// GET  /audit?prospect=N    → form with prefill data from prospect_audits.id=N

const SUPABASE_URL = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/self-audit";

export async function onRequest(context) {
  const incoming = new URL(context.request.url);
  const targetUrl = `${SUPABASE_URL}${incoming.search}`;

  const headers = new Headers(context.request.headers);
  headers.delete("host");
  headers.delete("cf-connecting-ip");
  headers.delete("cf-ray");
  headers.delete("cf-visitor");
  headers.set("x-forwarded-host", incoming.host);
  headers.set("x-forwarded-proto", "https");

  const init = {
    method: context.request.method,
    headers,
    redirect: "manual",
  };

  if (context.request.method !== "GET" && context.request.method !== "HEAD") {
    init.body = await context.request.arrayBuffer();
  }

  const upstream = await fetch(targetUrl, init);
  const responseHeaders = new Headers(upstream.headers);
  responseHeaders.delete("content-security-policy");

  return new Response(upstream.body, {
    status: upstream.status,
    headers: responseHeaders,
  });
}
