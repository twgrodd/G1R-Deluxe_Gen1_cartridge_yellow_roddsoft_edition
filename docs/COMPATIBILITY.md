# Pokémon Yellow compatibility

## Cartridge baseline

- Target game: **Pokémon Yellow**
- Platform: **Gen1Recomp / Mod API 2**
- Cartridge: **G1R Deluxe — Yellow Roddsoft Edition**
- Planned first release: **v1.0.0** (unreleased)
- Authoritative mod inventory and exact pinned versions: [`../cart.json`](../cart.json)

The mod repositories have been adapted for Yellow by the maintainer. This document does not claim that the complete 17-mod combination has passed runtime testing.

## Integration smoke tests before release

1. Import legally obtained Pokémon Yellow game data into Gen1Recomp.
2. Run strict online cartridge validation and pack the test `.g1rcart`.
3. Boot Yellow with all 17 pinned mods enabled in the declared load order.
4. Check Bag, TM/HM, move-learning, PC, and Pokédex interactions.
5. Test contextual CUT, SURF, and STRENGTH interactions with both Quality of Life and HM Anywhere enabled; confirm there is no duplicated action.
6. Check battles, EXP sharing, Move Inspector, sprites, and Dramatic Shape visuals.
7. Test trainer rematches, all-Pokémon-catchable progression, and New Game Plus on suitable saves.
8. Check trade/link behavior if used, and verify a clean save/reload cycle.

## Packaging and distribution

This cartridge references pinned published mod builds; it must not distribute Pokémon ROMs, saves, or proprietary extracted game data.
