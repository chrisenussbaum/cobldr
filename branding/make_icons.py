"""Regenerate every favicon/app icon and the header logo from branding/logo.png.

Run from the repo root:  python3 branding/make_icons.py   (needs Pillow)
"""
from PIL import Image, ImageOps

LOGO = "branding/logo.png"
LZ = Image.LANCZOS

src = Image.open(LOGO).convert("L")  # black mark on white
ink = ImageOps.invert(src)             # mark as white-on-black, i.e. an opacity mask
bbox = ink.point(lambda v: 255 if v > 128 else 0).getbbox()
mark = ink.crop(bbox)


def framed(size, padding):
    """The mark centred on a white square, with `padding` (fraction of size) clear on the widest side."""
    inner = round(size * (1 - 2 * padding))
    scale = inner / max(mark.size)
    m = mark.resize((round(mark.width * scale), round(mark.height * scale)), LZ)
    canvas = Image.new("L", (size, size), 0)
    canvas.paste(m, ((size - m.width) // 2, (size - m.height) // 2))
    return ImageOps.invert(canvas).convert("RGB")


# Browser tabs: tight padding so the cubes are as large as possible at 16-48px.
small = {n: framed(n * 8, 0.04).resize((n, n), LZ) for n in (16, 32, 48)}
small[16].save("favicon-16x16.png")
small[32].save("favicon-32x32.png")
small[48].save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[small[16], small[32]])

# Home-screen icons and link previews: more breathing room, as platforms show them as tiles.
for size, name in [(180, "apple-touch-icon.png"), (192, "android-chrome-192x192.png"), (512, "android-chrome-512x512.png")]:
    framed(size * 4, 0.14).resize((size, size), LZ).save(name, optimize=True)

# Header logo: transparent, tightly cropped mask. The page colours it with CSS so it follows light/dark mode.
# Shown 36px tall, saved at 4x for sharp high-DPI screens.
h = 144
header = Image.new("L", (round(mark.width * h / mark.height), h), 0)
alpha = mark.resize(header.size, LZ)
header = Image.merge("LA", (Image.new("L", header.size, 0), alpha))
header.save("branding/logo-mark.png", optimize=True)

print("Icons regenerated from", LOGO)
