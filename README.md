# cascadelocalseo.com

Static landing page + Cloudflare Pages Functions that proxy audit pages from Supabase.

## Routes

- `/` — static landing page (`index.html`)
- `/audit` — proxies to Supabase `self-audit` edge function (form GET + POST)
- `/audits/<id>` — proxies to Supabase `render-audit` edge function for a specific audit

## Deploy

Pushed via git → Cloudflare Pages auto-builds on push. Custom domain `cascadelocalseo.com` configured in CF dashboard.

The Supabase edge functions live in the [Supabase project](https://ijpgsoeajxyeyqkjivhi.supabase.co) and are managed separately (not in this repo).
