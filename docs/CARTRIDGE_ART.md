# Cartridge appearance — Yellow Roddsoft Edition

The authoritative cartridge appearance configuration is in the root `cart.json`.

- Title: **G1R Deluxe - Yellow Roddsoft Edition**
- Base game: **yellow**
- Shell: `#e6c21b` (yellow)
- Finish: `holo`
- Label: `label.png` (custom Roddsoft artwork)
- Cartridge ID: `g1r-deluxe-yellow-roddsoft`

The build workflow normalizes the existing custom label to a 512 × 512 RGB PNG under 256 KiB for launcher compatibility. It does not replace the source artwork in the repository.

`cartridge/cart.visual.json` is a non-authoritative visual reference. Its identity and appearance fields must agree with root `cart.json`.
