# Tuesday 17 November 2026 — the world's news in one picture

A newspaper front page for Tuesday 17 November 2026: 43 stories across
6 continents — the Kerch Bridge strike, the Iran–US exchange over
Bahrain, Nvidia's $115.8bn quarter, Ebola in DR Congo, COP31, and 31
more — plus a world map with numbered pins for the top 12 stories.

## Files

- `entry.png` — the image itself, 1024×1024, drawn by `build_image.py`
- `build_image.py` — the generator (Pillow, system fonts, deterministic)
- `main.py` — the entry point: copies `entry.png` to the output directory

## Run

```sh
python3 build_image.py        # re-draw entry.png (optional)
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

`main.py` uses the standard library only and needs no network. Running it
twice writes identical bytes.
