"""Regenerate every favicon/app icon and the header logo from branding/logo.png.

Run from the repo root:  python3 branding/make_icons.py   (needs Pillow)
"""
import base64
import io

from PIL import Image, ImageChops, ImageOps

LOGO = "branding/logo.png"  # dark mark on a transparent (or white) background
LZ = Image.LANCZOS

src = Image.open(LOGO).convert("RGBA")
# Opacity mask of the mark: opaque AND dark. Ignores light fringe pixels and works for white backgrounds too.
ink = ImageChops.multiply(src.getchannel("A"), ImageOps.invert(src.convert("L")))
bbox = ink.point(lambda v: 255 if v > 128 else 0).getbbox()
mark = ink.crop(bbox)


def mask(size, padding):
    """The mark centred in a size×size mask, with `padding` (fraction of size) clear on the widest side."""
    inner = round(size * (1 - 2 * padding))
    scale = inner / max(mark.size)
    m = mark.resize((round(mark.width * scale), round(mark.height * scale)), LZ)
    canvas = Image.new("L", (size, size), 0)
    canvas.paste(m, ((size - m.width) // 2, (size - m.height) // 2))
    return canvas


def transparent(m):
    """Black mark on a transparent background."""
    return Image.merge("RGBA", (*[Image.new("L", m.size, 0)] * 3, m))


def on_white(m):
    """Black mark on solid white."""
    return ImageOps.invert(m).convert("RGB")


def png_bytes(im):
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return buf.getvalue()


# Browser tabs: transparent, tight padding so the cubes are as large as possible at 16-48px.
small = {n: transparent(mask(n * 8, 0.04).resize((n, n), LZ)) for n in (16, 32, 48)}
small[16].save("favicon-16x16.png")
small[32].save("favicon-32x32.png")
small[48].save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[small[16], small[32]])

# SVG favicon for Chrome/Firefox/Edge: the mark is black on light tab bars and white on dark ones.
svg_mask = base64.b64encode(png_bytes(mask(1024, 0.04).resize((256, 256), LZ))).decode()
with open("favicon.svg", "w") as f:
    f.write(f"""<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" viewBox="0 0 256 256">
  <style>rect {{ fill: #000; }} @media (prefers-color-scheme: dark) {{ rect {{ fill: #fff; }} }}</style>
  <mask id="m" style="mask-type: luminance"><image width="256" height="256" xlink:href="data:image/png;base64,{svg_mask}"/></mask>
  <rect width="256" height="256" mask="url(#m)"/>
</svg>
""")

# Home-screen icons and link previews: white background (iOS fills transparency with black) and more breathing room.
for size, name in [(180, "apple-touch-icon.png"), (192, "android-chrome-192x192.png"), (512, "android-chrome-512x512.png")]:
    on_white(mask(size * 4, 0.14)).resize((size, size), LZ).save(name, optimize=True)

# Header logo: transparent, tightly cropped mask. The page colours it with CSS so it follows light/dark mode.
# Shown 36px tall, saved at 4x for sharp high-DPI screens.
h = 144
alpha = mark.resize((round(mark.width * h / mark.height), h), LZ)
Image.merge("LA", (Image.new("L", alpha.size, 0), alpha)).save("branding/logo-mark.png", optimize=True)

print("Icons regenerated from", LOGO)
