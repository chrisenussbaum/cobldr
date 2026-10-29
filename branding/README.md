# Branding

- `logo.png` — master CoBldr logo (2000×2000, black cubes on a transparent background).
- `logo-mark.png` — transparent mark for the page header (generated). The page tints it with CSS, so it's black in light mode and white in dark mode.
- `make_icons.py` — regenerates `logo-mark.png` and every icon below from `logo.png`.

| File (site root) | Size | Used by |
| --- | --- | --- |
| `favicon.svg` | any | Chrome/Firefox/Edge tabs; black on light tab bars, white on dark ones |
| `favicon.ico` | 16, 32, 48 | Older browsers, Google search results |
| `favicon-16x16.png`, `favicon-32x32.png` | 16, 32 | Browser tabs |
| `apple-touch-icon.png` | 180 | iPhone/iPad home screen |
| `android-chrome-192x192.png`, `android-chrome-512x512.png` | 192, 512 | Android home screen, `site.webmanifest`, link previews |

Tab icons are transparent and cropped tightly so the mark fills the tab. Home-screen icons sit on white with more breathing room, because iOS fills transparent areas with black.

## Updating the logo

1. Replace `branding/logo.png` with the new square logo (at least 512×512).
2. The script expects a dark mark on a transparent or white background.
3. Run `python3 branding/make_icons.py` from the repo root and commit the results.
