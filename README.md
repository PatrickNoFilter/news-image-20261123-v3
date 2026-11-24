# The World in One Image — 23 November 2026

A deterministic Python/Pillow program that renders a 1024x1024 news summary image for Monday, 23 November 2026. Every pixel is generated from the constants in `main.py`, so rerunning the program always produces the identical `entry.png`.

## Contents

- 19 stories across seven regions, arranged as three illustrated hero cards, eight grid cards, and an "Also on Monday" list.
- A regions legend with colour swatches matching each card's accent colour.
- Simple line icons drawn programmatically for each story (gavel, drones, house, plane, ship, exam, rings, blast, boat, space, book, protest, UFO, virus, globe).

## Building

```
python3 main.py
```

Requires Python 3 and Pillow (`PIL`), plus the DejaVu Sans fonts at `/usr/share/fonts/truetype/dejavu/`. The script writes `entry.png` into the script's own directory (roughly 130 KB).

## License

MIT — see `LICENSE`.
