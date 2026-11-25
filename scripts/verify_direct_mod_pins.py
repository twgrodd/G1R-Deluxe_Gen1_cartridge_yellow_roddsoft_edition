#!/usr/bin/env python3
"""Verify FAFF0x's indexed direct ZIPs and standard GitHub release pins.

The six FAFF0x mods are published as immutable versioned ZIPs in the index
repository, not as GitHub release assets. This checks those exact archive
bytes, then asks upstream cartkit to resolve the remaining release pins.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

DIRECT = {
    "move_inspector": ("1.0.0", "move_inspector_v1.0.0.zip",
        "582d5e0eb9a095b17a6a12f1f02fb8e91a392903b6f8e37f775a4d69759e3e39"),
    "move_learn_stats": ("1.0.2", "move_learn_stats_v1.0.2.zip",
        "ca11def1869d2bfce63360743e32ed6e538256a29e7cfcc144afc4c138417e3f"),
    "reusable_machines": ("1.0.1", "reusable_machines_v1.0.1.zip",
        "0d49953dac24adbed6d9774dc12f57941cc61899a3c6e4394d55a54ed3ab86f7"),
    "moves_manager": ("1.0.1", "moves_manager_v1.0.1.zip",
        "98801ee1329bdd08a110a8184de17a0558b3d677316e7c81a26c4b28d86e53cc"),
    "pokedex_plus": ("1.3.4", "pokedex_plus_v1.3.4.zip",
        "c9f17b525dd48db01c2f1c8c798c44e7241ce6844cfa29d0d30eaeb11aa2133d"),
    "hm_anywhere": ("1.2.0", "hm_anywhere_v1.2.0.zip",
        "5a7022f488746ce7135b5df8dbb846780e38b2fc58de4262eee1ce4a9e39aeae"),
}
INDEX_REPO = "FAFF0x/gen1recomp"
UA = "G1R-Deluxe-cartridge-pin-check/1.0"


def fail(message):
    print("direct-pin-check: ERROR: " + message, file=sys.stderr)
    raise SystemExit(1)


def main():
    if len(sys.argv) != 3:
        fail("usage: verify_direct_mod_pins.py CART_DIR CARTKIT_PY")
    cart_dir = Path(sys.argv[1]).resolve()
    cartkit = Path(sys.argv[2]).resolve()
    cart_path = cart_dir / "cart.json"
    cart = json.loads(cart_path.read_text(encoding="utf-8"))
    mods = {entry.get("id"): entry for entry in cart.get("mods", [])
            if isinstance(entry, dict)}
    missing = set(DIRECT) - set(mods)
    if missing:
        fail("cart removed required direct-pinned mods: " + ", ".join(sorted(missing)))

    for mod_id, (version, filename, expected) in DIRECT.items():
        entry = mods[mod_id]
        if entry.get("source") != "github" or entry.get("repo") != INDEX_REPO:
            fail(f"{mod_id} must point to {INDEX_REPO} as its source repository")
        if entry.get("version") != version or entry.get("sha256") != expected:
            fail(f"{mod_id} version/hash no longer matches the pinned indexed archive")
        url = f"https://raw.githubusercontent.com/{INDEX_REPO}/main/{filename}"
        request = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(request, timeout=90) as response:
                archive = response.read()
        except Exception as exc:
            fail(f"could not fetch {filename}: {exc}")
        actual = hashlib.sha256(archive).hexdigest()
        if actual != expected:
            fail(f"{filename} SHA-256 mismatch: expected {expected}, got {actual}")
        try:
            with zipfile.ZipFile(BytesIO(archive)) as zf:
                bad = zf.testzip()
                if bad:
                    fail(f"{filename} has a corrupt ZIP member: {bad}")
        except zipfile.BadZipFile:
            fail(f"{filename} is not a valid ZIP archive")
        print(f"OK {mod_id} {version} SHA-256 verified ({len(archive)} bytes)")

    # Upstream cartkit knows GitHub releases and GameBanana. Validate the other
    # pins online in a temporary manifest while preserving the full cart for
    # the separate offline schema/pack checks in the workflow.
    remaining = [entry for entry in cart["mods"] if entry.get("id") not in DIRECT]
    temp_cart = dict(cart)
    temp_cart["mods"] = remaining
    temp_cart["load_order"] = [mod_id for mod_id in cart.get("load_order", [])
                               if mod_id not in DIRECT]
    with tempfile.TemporaryDirectory(prefix="g1r-pin-check-") as temp:
        temp = Path(temp)
        (temp / "cart.json").write_text(
            json.dumps(temp_cart, indent=2) + "\n", encoding="utf-8")
        label = cart.get("label")
        if label:
            source = cart_dir / label
            if source.is_file():
                shutil.copy2(source, temp / label)
        env = os.environ.copy()
        cmd = [sys.executable, str(cartkit), "validate", str(temp),
               "--online", "--strict", "--quiet"]
        result = subprocess.run(cmd, env=env, check=False)
        if result.returncode:
            fail("upstream cartkit online validation failed for the other mod pins")
    print("OK remaining published mod pins verified by upstream cartkit")


if __name__ == "__main__":
    main()
