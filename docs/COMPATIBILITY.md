# Pokémon Yellow compatibility

## Cartridge baseline

- Target game: **Pokémon Yellow**
- Platform: **Gen1Recomp / Mod API 2**
- Cartridge: **G1R Deluxe — Yellow Roddsoft Edition**
- Current release: **v1.0.2**
- Authoritative mod inventory and exact pinned versions: [`../cart.json`](../cart.json)

## Compatibility evidence

The three refreshed upstream manifests declare Gen 1 support (Running Shoes and Exp Share) or Pokémon Yellow support (Pikachu True Potential). The Pikachu True Potential project also documents player-tested use alongside Running Shoes and Exp Share. The remaining cartridge pins are unchanged from v1.0.1.

The release validation workflow runs cartkit self-tests, strict online validation of every pinned release asset, packaging, and cross-file version/load-order checks. These checks validate package integrity and declared compatibility metadata; they do **not** constitute a full in-game runtime smoke test of all 18 mods together.

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
