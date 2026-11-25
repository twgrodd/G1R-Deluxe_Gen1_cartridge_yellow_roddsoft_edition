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
        "25bee1303652c77657a756a1ce03ec32efe4a43f5e6da1a362c85f29ab9028ff"),
    "move_learn_stats": ("1.0.2", "move_learn_stats_v1.0.2.zip",
        "5e464dfbc543632dd3d3a2bac3d1380f66d1c4cf42994b101f64a4af61fcbf28"),
    "reusable_machines": ("1.0.1", "reusable_machines_v1.0.1.zip",
        "84766c594d2cfb4bb4d370873cefce2b1c5886d6f1d4268158bcc49412fe9776"),
    "moves_manager": ("1.0.1", "moves_manager_v1.0.1.zip",
        "918cd1f4974818583e1c8117b38cf1504fe187b5da5ccc4abb58c6ef9c7cf764"),
    "pokedex_plus": ("1.3.4", "pokedex_plus_v1.3.4.zip",
        "00a040bad3da328309f61439c08b0abdc5c81b79d8090f9ca09b4d9a8c32115c"),
    "hm_anywhere": ("1.2.0", "hm_anywhere_v1.2.0.zip",
        "ecc76b2d5ec73cfa7d39b32f536e62ac5b824ee1a85d91beafd74c97058c1d4e"),
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
