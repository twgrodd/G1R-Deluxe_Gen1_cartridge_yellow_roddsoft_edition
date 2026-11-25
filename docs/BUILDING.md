# Building / Testing

The cartridge is a Yellow adaptation of the Red Roddsoft cartridge. The v1.0.2 candidate retains all 18 mods. Six FAFF0x mods are supplied as direct versioned ZIPs, so `scripts/verify_direct_mod_pins.py` checks their pinned archive hashes and ZIP integrity while upstream cartkit validates the other release pins online. Full in-game integration testing is still required before claiming runtime compatibility.

## Requirements

1. Obtain and set up Gen1Recomp from its upstream project.
2. Follow Gen1Recomp's instructions to import your own legally obtained Pokémon Yellow game data.
3. Do not place ROM files or extracted proprietary assets in this repository.
4. Review the pinned mods in `cart.json`; use their manifests and project documentation to confirm declared Yellow / Gen 1 support.
5. Check the cartridge load order against `cart.json` and the installed mod versions.

## Validation target

As the mod collection is populated, validation should use Gen1Recomp's modkit against imported base data where applicable:

```sh
python3 tools/modkit.py validate mods/<mod-id> --base imported
python3 tools/modkit.py lint mods/<mod-id>
```

Each included/local mod should eventually have an effect-level test, not merely a load test.
