// Cloudflare Pages Function — proxies /audits/<id> on cascadelocalseo.com
// to the Supabase render-audit function. Preserves the URL in the browser.

const SUPABASE_URL = "https://ijpgsoeajxyeyqkjivhi.supabase.co/functions/v1/render-audit";

export const onRequestGet: PagesFunction<unknown, "id"> = async (context) => {
  const { id } = context.params;
  if (!id || Array.isArray(id) || !/^\d+$/.test(id)) {
    return new Response("Invalid audit ID", { status: 400 });
  }

  const targetUrl = `${SUPABASE_URL}?id=${encodeURIComponent(id)}`;
  const upstream = await fetch(targetUrl);
  const responseHeaders = new Headers(upstream.headers);
  responseHeaders.delete("content-security-policy");

  return new Response(upstream.body, {
    status: upstream.status,
    headers: responseHeaders,
  });
};
