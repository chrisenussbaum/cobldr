# Branding

- `logo.svg` — master CoBldr logo (Comfortaa Light lettering converted to outlines, on `#4f46e5`).
- `logo-small.svg` — same logo with heavier strokes so it stays legible at 16–48 px. Also served as `/favicon.svg`.

Icons generated from these (all at the site root):

| File | Source | Used by |
| --- | --- | --- |
| `favicon.ico` (16, 32, 48) | `logo-small.svg` | Older browsers, Google search results |
| `favicon.svg` | `logo-small.svg` | Modern browser tabs |
| `favicon-16x16.png`, `favicon-32x32.png` | `logo-small.svg` | Browser tabs |
| `apple-touch-icon.png` (180) | `logo.svg` | iPhone/iPad home screen |
| `android-chrome-192x192.png`, `-512x512.png` | `logo.svg` | Android home screen, `site.webmanifest`, link previews |

When the logo changes, replace both SVGs and regenerate every file in the table at the same sizes.
