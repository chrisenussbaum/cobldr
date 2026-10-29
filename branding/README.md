# Branding

- `logo.png` — master CoBldr logo (2000×2000, white lettering on `#4f46e5`).
- `make_icons.py` — regenerates every icon below from `logo.png`.

| File (site root) | Size | Used by |
| --- | --- | --- |
| `favicon.ico` | 16, 32, 48 | Browser tabs, Google search results |
| `favicon-16x16.png`, `favicon-32x32.png` | 16, 32 | Browser tabs |
| `apple-touch-icon.png` | 180 | iPhone/iPad home screen |
| `android-chrome-192x192.png`, `android-chrome-512x512.png` | 192, 512 | Android home screen, `site.webmanifest`, link previews |

The 16–48 px icons thicken the logo's strokes so the thin lettering stays legible; the larger ones are straight downscales.

## Updating the logo

1. Replace `branding/logo.png` with the new square logo (at least 512×512).
2. If the background colour changed, update `BG` in `make_icons.py`, and `theme_color`/`background_color` in `site.webmanifest`.
3. Run `python3 branding/make_icons.py` from the repo root and commit the results.
