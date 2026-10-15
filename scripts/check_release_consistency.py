#!/usr/bin/env python3
"""Fail closed when cartridge release versions/identities disagree."""
import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
def fail(message):
    raise SystemExit("release consistency: " + message)
def check(version, tag=None, bundle=None):
    cart = json.loads((ROOT / "cart.json").read_text(encoding="utf-8"))
    expected_id = "g1r-deluxe-yellow-roddsoft"
    if cart.get("version") != version or cart.get("id") != expected_id or cart.get("base") != "yellow":
        fail("cart.json version, id or Yellow base mismatch")
    if cart.get("repo") != "twgrodd/G1R-Deluxe_Gen1_cartridge_yellow_roddsoft_edition":
        fail("cart.json repository mismatch")
    if tag and tag != "v" + version:
        fail("release tag must equal v" + version)
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
    if not re.search(r"(?m)^##\s+v" + re.escape(version) + r"(?=\s|$)", changelog):
        fail("CHANGELOG.md lacks a matching version heading")
    manifest = (ROOT / "cartridge/manifest.lua").read_text(encoding="utf-8")
    if not re.search(r"\bversion\s*=\s*[\"']" + re.escape(version) + r"[\"']", manifest):
        fail("cartridge/manifest.lua version mismatch")
    if not re.search(r"\bid\s*=\s*[\"']g1r_deluxe_yellow_roddsoft[\"']", manifest):
        fail("cartridge/manifest.lua ID mismatch")
    if bundle:
        data = pathlib.Path(bundle).read_text(encoding="utf-8")
        # cartkit emits a Lua table, NOT a ZIP. Match keys inside its cart table.
        if not re.search(r'\bcart\s*=\s*\{', data):
            fail("packed .g1rcart is missing cart table")
        for key, value in (("version", version), ("id", expected_id), ("base", "yellow")):
            if not re.search(r"\b" + key + r"\s*=\s*[\"']" + re.escape(value) + r"[\"']", data):
                fail("packed .g1rcart missing expected " + key)
        if not re.search(r'\bformatVersion\s*=', data):
            fail("packed .g1rcart missing formatVersion")
    print("Version and identity consistency OK:", version)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="")
    parser.add_argument("--bundle")
    args = parser.parse_args()
    cart = json.loads((ROOT / "cart.json").read_text(encoding="utf-8"))
    check(cart["version"], args.tag or None, args.bundle)
