# Cartridge updates and releases

## First Yellow release

The first planned Pokémon Yellow Roddsoft Edition version is **1.0.0**. It is currently **unreleased**. The prior Pokémon Red cartridge history is not part of this Yellow release history.

## Release procedure (manual only)

1. Confirm that the pinned 17-mod set works together in Pokémon Yellow.
2. Update the root `cart.json`, `cartridge/manifest.lua`, `cartridge/cart.visual.json`, and `CHANGELOG.md` to the **same** intended version.
3. Push changes and wait for the **Validate Yellow cartridge** workflow to pass.
4. Review the proposed release and explicitly authorize publication.
5. Manually dispatch **Release Yellow cartridge (manual approval only)** on `main`, supplying the exact `v<version>` tag and typing `RELEASE`.
6. The workflow checks metadata, version consistency, published mod pins, and the generated `.g1rcart` before publishing the GitHub Release and SHA-256 checksums.

Pushing commits or tags does **not** publish a cartridge automatically. Existing release tags must not be overwritten.

## Pin policy

Each cartridge release freezes exact mod versions and hashes. Changes to mod pins require a new cartridge version and another combined validation cycle.
