#!/usr/bin/env python3
"""
Deploy cascadelocalseo Worker via Cloudflare REST API (no wrangler dependency).

Required env vars:
  CF_TOKEN          Cloudflare API token (Workers Scripts: Edit + Account: Read)
  CF_ACCOUNT_ID     Cloudflare account ID

Reads wrangler.jsonc for script_name, main, compatibility_date, compatibility_flags.
Uploads everything under ./public/ as static assets, then PUTs the main worker.

Used by .github/workflows/deploy.yml. Can also be run locally:
  CF_TOKEN=xxx CF_ACCOUNT_ID=yyy python3 scripts/deploy.py
"""
import base64
import hashlib
import json
import mimetypes
import os
import re
import ssl
import sys
import urllib.error
import urllib.request
import uuid
from pathlib import Path

CF_TOKEN = os.environ["CF_TOKEN"]
ACCT = os.environ["CF_ACCOUNT_ID"]
PROJECT = Path(__file__).resolve().parent.parent

# Use system CA bundle; fall back to unverified only as last resort
SSL_CTX = ssl.create_default_context()
for ca_path in ("/etc/ssl/certs/ca-certificates.crt", "/etc/ssl/cert.pem", "/private/etc/ssl/cert.pem"):
    if os.path.exists(ca_path):
        SSL_CTX = ssl.create_default_context(cafile=ca_path)
        break
OPENER = urllib.request.build_opener(urllib.request.HTTPSHandler(context=SSL_CTX))


def load_wrangler_config():
    """Read wrangler.jsonc, stripping // and /* */ comments."""
    raw = (PROJECT / "wrangler.jsonc").read_text()
    no_block = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)
    no_line = re.sub(r"^\s*//.*$", "", no_block, flags=re.MULTILINE)
    return json.loads(no_line)


def req(method, url, headers=None, data=None):
    h = {"Authorization": f"Bearer {CF_TOKEN}"}
    if headers:
        h.update(headers)
    r = urllib.request.Request(url, method=method, headers=h, data=data)
    try:
        resp = OPENER.open(r)
        return resp.status, resp.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


def cf_hash(path: Path, content: bytes) -> str:
    """CF asset hash = first 32 chars of hex(SHA256(content + extension))."""
    ext = path.suffix.lstrip(".")
    return hashlib.sha256(content + ext.encode("utf-8")).hexdigest()[:32]


def build_manifest(assets_dir: Path):
    manifest = {}
    files_by_hash = {}
    for p in sorted(assets_dir.rglob("*")):
        if not p.is_file():
            continue
        rel = "/" + str(p.relative_to(assets_dir))
        content = p.read_bytes()
        h = cf_hash(p, content)
        manifest[rel] = {"hash": h, "size": len(content)}
        files_by_hash[h] = (p, content)
    return manifest, files_by_hash


def initiate_upload_session(script_name, manifest):
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts/{script_name}/assets-upload-session"
    body = json.dumps({"manifest": manifest}).encode()
    status, resp = req("POST", url, {"Content-Type": "application/json"}, body)
    j = json.loads(resp)
    if not j.get("success"):
        sys.exit(f"upload-session failed [{status}]: {resp}")
    return j["result"]


def upload_buckets(buckets, jwt, files_by_hash):
    current_jwt = jwt
    for i, bucket in enumerate(buckets):
        if not bucket:
            continue
        boundary = f"----CF{uuid.uuid4().hex}"
        parts = []
        for h in bucket:
            p, content = files_by_hash[h]
            ctype, _ = mimetypes.guess_type(str(p))
            if not ctype:
                ctype = "application/octet-stream"
            b64 = base64.b64encode(content).decode("ascii")
            parts.append(f"--{boundary}\r\n")
            parts.append(f'Content-Disposition: form-data; name="{h}"; filename="{h}"\r\n')
            parts.append(f"Content-Type: {ctype}\r\n")
            parts.append("Content-Transfer-Encoding: base64\r\n\r\n")
            parts.append(b64)
            parts.append("\r\n")
        parts.append(f"--{boundary}--\r\n")
        body = "".join(parts).encode("utf-8")
        url = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/assets/upload?base64=true"
        status, resp = req("POST", url, {
            "Content-Type": f"multipart/form-data; boundary={boundary}",
            "Authorization": f"Bearer {current_jwt}",
        }, body)
        j = json.loads(resp)
        if not j.get("success"):
            sys.exit(f"bucket {i} upload failed [{status}]: {resp}")
        new_jwt = (j.get("result") or {}).get("jwt")
        if new_jwt:
            current_jwt = new_jwt
        print(f"  bucket {i+1}/{len(buckets)}: {len(bucket)} files uploaded")
    return current_jwt


def deploy_worker(script_name, main_module_name, main_module_content, completion_jwt, compatibility_date, compatibility_flags):
    metadata = {
        "main_module": main_module_name,
        "compatibility_date": compatibility_date,
        "compatibility_flags": compatibility_flags,
        "bindings": [{"type": "assets", "name": "ASSETS"}],
        # run_worker_first: the Worker fetch handler runs before static-asset serving, so routes
        # like the /exec-dashboard token-wall execute even when a matching asset exists. The handler
        # falls through to env.ASSETS.fetch for everything else, so normal asset serving is unchanged.
        "assets": {"jwt": completion_jwt, "config": {"run_worker_first": True}},
    }
    boundary = f"----CF{uuid.uuid4().hex}"
    parts = [
        f"--{boundary}\r\n",
        'Content-Disposition: form-data; name="metadata"\r\n',
        "Content-Type: application/json\r\n\r\n",
        json.dumps(metadata),
        "\r\n",
        f"--{boundary}\r\n",
        f'Content-Disposition: form-data; name="{main_module_name}"; filename="{main_module_name}"\r\n',
        "Content-Type: application/javascript+module\r\n\r\n",
        main_module_content,
        "\r\n",
        f"--{boundary}--\r\n",
    ]
    body = "".join(parts).encode("utf-8")
    url = f"https://api.cloudflare.com/client/v4/accounts/{ACCT}/workers/scripts/{script_name}"
    status, resp = req("PUT", url, {"Content-Type": f"multipart/form-data; boundary={boundary}"}, body)
    j = json.loads(resp)
    if not j.get("success"):
        sys.exit(f"worker PUT failed [{status}]: {resp}")
    return j["result"]


def main():
    cfg = load_wrangler_config()
    script_name = cfg["name"]
    main_rel = cfg["main"]
    main_path = PROJECT / main_rel
    main_basename = main_path.name
    assets_dir = PROJECT / cfg.get("assets", {}).get("directory", "./public").lstrip("./")
    compat_date = cfg.get("compatibility_date")
    compat_flags = cfg.get("compatibility_flags", [])

    print(f"Deploying {script_name}: main={main_rel}, assets={assets_dir.relative_to(PROJECT)}")
    print(f"  compatibility_date={compat_date} flags={compat_flags}")

    manifest, files_by_hash = build_manifest(assets_dir)
    print(f"\nManifest ({len(manifest)} files):")
    for p, info in manifest.items():
        print(f"  {p}: {info['size']} bytes  hash={info['hash']}")

    print("\nInitiating upload session...")
    session = initiate_upload_session(script_name, manifest)
    jwt = session["jwt"]
    buckets = session.get("buckets", [])
    print(f"  session jwt obtained, {len(buckets)} bucket(s) to upload")

    if buckets and any(buckets):
        jwt = upload_buckets(buckets, jwt, files_by_hash)
    else:
        print("  (no new files to upload — all hashes already cached)")

    print("\nDeploying Worker script...")
    result = deploy_worker(script_name, main_basename, main_path.read_text(), jwt, compat_date, compat_flags)
    print(f"  deployed: id={result.get('id')} etag={result.get('etag', '')[:16]}")
    print(f"  modified_on: {result.get('modified_on')}")


if __name__ == "__main__":
    main()
