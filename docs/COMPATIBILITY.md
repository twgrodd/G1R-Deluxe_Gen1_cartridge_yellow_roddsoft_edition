# Pokémon Yellow compatibility

## Cartridge baseline

- Target game: **Pokémon Yellow**
- Platform: **Gen1Recomp / Mod API 2**
- Cartridge: **G1R Deluxe — Yellow Roddsoft Edition**
- Current candidate: **v1.0.2 (not yet released)**
- Authoritative mod inventory and exact pinned versions: [`../cart.json`](../cart.json)

## Compatibility evidence

Running Shoes and Exp Share declare Gen 1 support; Pikachu True Potential declares Pokémon Yellow support and documents use alongside Running Shoes and Exp Share. The candidate retains the same 18-mod load order.

Six FAFF0x mods are distributed as versioned ZIP files in `FAFF0x/gen1recomp` rather than GitHub release assets. The workflow verifies each exact ZIP against its pinned SHA-256 and checks ZIP integrity, then uses upstream cartkit to validate the other published release pins online. It separately performs strict full-manifest validation and packaging. This is metadata/archive validation—not a full in-game runtime smoke test of all 18 mods together.

## Recommended runtime smoke tests

1. Import legally obtained Pokémon Yellow game data into Gen1Recomp.
2. Boot Yellow with all 18 pinned mods enabled in the declared load order.
3. Check Bag, TM/HM, move-learning, PC, and Pokédex interactions.
4. Test contextual CUT, SURF, and STRENGTH interactions with both Quality of Life and HM Anywhere enabled; confirm there is no duplicated action.
5. Check battles, 20% custom EXP sharing, Move Inspector, sprites, and Dramatic Shape visuals.
6. Test trainer rematches, all-Pokémon-catchable progression, and New Game Plus on suitable saves.
7. Check trade/link behavior if used, and verify a clean save/reload cycle.

## Packaging and distribution

This cartridge references pinned published mod builds; it must not distribute Pokémon ROMs, saves, or proprietary extracted game data.
