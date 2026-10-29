# Branding

- `logo.png` — master CoBldr logo (2000×2000, black cubes on white).
- `logo-mark.png` — transparent mark for the page header (generated). The page tints it with CSS, so it's black in light mode and white in dark mode.
- `make_icons.py` — regenerates `logo-mark.png` and every icon below from `logo.png`.

| File (site root) | Size | Used by |
| --- | --- | --- |
| `favicon.ico` | 16, 32, 48 | Browser tabs, Google search results |
| `favicon-16x16.png`, `favicon-32x32.png` | 16, 32 | Browser tabs |
| `apple-touch-icon.png` | 180 | iPhone/iPad home screen |
| `android-chrome-192x192.png`, `android-chrome-512x512.png` | 192, 512 | Android home screen, `site.webmanifest`, link previews |

The 16–48 px icons crop the mark tightly so it fills the tab; the larger icons keep more white space around it.

## Updating the logo

1. Replace `branding/logo.png` with the new square logo (at least 512×512).
2. The script expects a dark mark on a white background. If the background colour changes, update `background_color` in `site.webmanifest` too.
3. Run `python3 branding/make_icons.py` from the repo root and commit the results.
