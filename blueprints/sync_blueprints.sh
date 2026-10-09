#!/bin/sh
# Syncs blueprint files from this repo into a Home Assistant instance's
# /config/blueprints directory, per blueprints/sync_manifest.json.
#
# Intended to be invoked by a Home Assistant shell_command:
#   curl -fsSL <raw-url>/blueprints/sync_blueprints.sh | SHA=<commit> sh
# SHA defaults to the current head of the configured branch.

set -eu

MANIFEST_REMOTE="blueprints/sync_manifest.json"

python3 - "$SHA" <<'PYEOF'
import json, os, sys, urllib.request

sha = sys.argv[1]
manifest_url_base = "https://raw.githubusercontent.com/jeeftor/HomeAssistant"

def fetch(url):
    with urllib.request.urlopen(url) as r:
        return r.read()

manifest = json.loads(fetch(f"{manifest_url_base}/{sha}/{MANIFEST_REMOTE}"))
root = "/config/blueprints"

updated, errors = [], []
for entry in manifest["entries"]:
    domain = entry["repo"].split("/", 1)[0]
    src = f"{manifest_url_base}/{sha}/blueprints/{entry['repo']}"
    dst = os.path.join(root, domain, entry["ha"])
    try:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        content = fetch(src)
        if os.path.exists(dst) and open(dst, "rb").read() == content:
            continue
        with open(dst, "wb") as f:
            f.write(content)
        updated.append(f"{domain}/{entry['ha']}")
    except Exception as e:
        errors.append(f"{entry['repo']}: {e}")

print(f"synced {len(updated)} blueprint(s)")
for u in updated:
    print(f"  updated: {u}")
for e in errors:
    print(f"  ERROR: {e}", file=sys.stderr)
sys.exit(1 if errors else 0)
PYEOF
