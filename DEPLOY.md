# Deploying cascadelocalseo.com

## Once-only setup (one evening, ~30 minutes total)

### 1. Buy the domain (Cloudflare Registrar)

1. Sign in at https://dash.cloudflare.com
2. **Registrar → Register Domains**
3. Search `cascadelocalseo.com` → buy (~$10/year, wholesale)
4. After purchase, the domain auto-lands in your Cloudflare DNS

### 2. Deploy this folder to Cloudflare Pages

**Option A — drag & drop (fastest, no GitHub):**
1. Cloudflare dashboard → **Workers & Pages → Create application → Pages → Upload assets**
2. Project name: `cascadelocalseo`
3. Drag the `cascadelocalseo` folder (containing `index.html`) into the uploader
4. Click **Deploy**. Pages assigns a `cascadelocalseo.pages.dev` URL — visit to verify

**Option B — Git-based (for iteration):**
1. Push this folder to a new GitHub repo
2. Pages → Create → **Connect to Git** → pick the repo
3. Framework preset: **None**. Build command: leave blank. Output: `/`
4. Deploy

### 3. Wire your custom domain

In the Pages project settings:
1. **Custom domains → Set up a custom domain**
2. Enter `cascadelocalseo.com`
3. Cloudflare auto-creates the CNAME/A records. SSL is auto. Done.

Visit `https://cascadelocalseo.com` — should load the page within a few minutes.

### 4. Verify Resend domain (for sending audits FROM your domain)

1. Sign in to Resend → **Domains → Add Domain**
2. Enter `cascadelocalseo.com`
3. Resend gives you ~3 DNS records (SPF TXT, DKIM CNAME, optionally an MX)
4. In Cloudflare DNS, **add each record** as Resend specifies
5. **Critical:** Set the proxy status to **"DNS only" (gray cloud)** for SPF / DKIM / MX records. Proxying breaks email auth.
6. Click **Verify** in Resend. Usually verifies within minutes.

Once verified, update the `from` address in:
- `send-email` edge function default: change `onboarding@resend.dev` → `Cascade Local SEO <hello@cascadelocalseo.com>` (or whatever address you want)
- `audit-request` / `inbound-audit-processor` routines: same change

### 5. Set up `hello@cascadelocalseo.com` (reply address)

Two simple options:

**A) Cloudflare Email Routing (free):**
- Cloudflare dashboard → **Email → Email Routing → Routes**
- Add `hello@cascadelocalseo.com` → forwards to `jonathanluisxc@gmail.com`
- All replies land in your Gmail. You reply from Gmail using "send mail as" with your Resend-verified address.

**B) Use Resend's inbound (more advanced):**
- Resend supports inbound mail via webhook. Configure if you want replies to land in Supabase directly. Skip for v0.

## Form testing

After domain is live:
1. Open https://cascadelocalseo.com
2. Fill the audit form with a real business name + city + your own email
3. Submit — should see "✓ Thanks. Your audit is queued."
4. Check `audit_requests` in Supabase — row should appear with status='pending'
5. Wait up to 2 hours (or run `inbound-audit-processor` manually) → audit lands in the test email

## Files in this folder

- `index.html` — the landing page (self-contained, no build step)
- `DEPLOY.md` — this file

## Iteration

When you want to update content (pricing, copy, benchmarks):
- Edit `index.html` directly
- Re-deploy (drag & drop or git push)
- Benchmarks table is hardcoded — refresh quarterly by running the SQL in the project memory and pasting new numbers

## Known to-dos

- [ ] Replace `onboarding@resend.dev` everywhere with `hello@cascadelocalseo.com` after domain verification
- [ ] Add Open Graph image (currently uses 🏔 emoji favicon)
- [ ] Add Plausible or simple-analytics if you want visit tracking (currently none)
- [ ] Consider a `/blog` for SEO content marketing once first clients land
