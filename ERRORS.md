# ERRORS.md

## 2026-05-30 — Supabase deploy_edge_function with a placeholder + send-email 414 (GBP Pass build)
- **What didn't work (1):** I put a Read and a deploy_edge_function in the SAME tool block, then deployed with content "PLACEHOLDER" (I'd intended to fill it from the Read, but parallel calls don't see each other's output). The live function was broken for ~3 min until I redeployed the real source.
  - **What worked instead:** deploy is its own turn AFTER the file content is in context; verify with get_edge_function (it echoes the deployed `content`) before relying on it.
  - **Note for next time:** never inline a deploy in the same block as the Read that's supposed to feed it. Confirm the `content` field is real source, not a stub.
- **What didn't work (2):** the edge fn called send-email via GET `?payload=<base64 JSON>` (copied from send-foundations-delivery). For a small payload that's fine, but the 8.5KB GBP deliverable HTML blew past the server URI limit -> HTTP 414 Request-URI Too Large on `approve`. (The small internal review email fit and sent, masking it until the customer-deliverable step.)
  - **What worked instead:** call send-email via POST with a JSON body + `Authorization: Bearer <SERVICE_ROLE>`. send-email accepts both; POST has no URI ceiling. Use POST for anything with a large `html`.
  - **Good failure mode:** approve returned 502 and did NOT mark the order delivered, so no half-sent state. Caught only because we ran a real end-to-end test to our own inbox before going live.
