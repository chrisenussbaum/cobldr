"""Regenerate every favicon/app icon from branding/logo.png.

Run from the repo root:  python3 branding/make_icons.py   (needs Pillow)
"""
from PIL import Image, ImageChops, ImageFilter

LOGO = "branding/logo.png"
BG = (79, 70, 229)  # #4f46e5, the logo's background colour
LZ = Image.LANCZOS

src = Image.open(LOGO).convert("RGB")


def thickened(k, work=512):
    """The logo with its white strokes widened by a k-pixel filter at 512px, so thin lettering survives tiny sizes."""
    im = src.resize((work, work), LZ)
    mask = ImageChops.subtract(im, Image.new("RGB", im.size, BG)).convert("L").point(lambda v: min(255, v * 2))
    if k > 1:
        mask = mask.filter(ImageFilter.MaxFilter(k))
    return Image.composite(Image.new("RGB", im.size, "white"), Image.new("RGB", im.size, BG), mask)


small = {
    16: thickened(11).resize((16, 16), LZ),
    32: thickened(7).resize((32, 32), LZ),
    48: thickened(7).resize((48, 48), LZ),
}
small[16].save("favicon-16x16.png")
# Header logo on the page: shown at 36px, saved at 4x for sharp high-DPI screens.
thickened(7).resize((144, 144), LZ).save("branding/logo-mark.png", optimize=True)
small[32].save("favicon-32x32.png")
small[48].save("favicon.ico", sizes=[(16, 16), (32, 32), (48, 48)], append_images=[small[16], small[32]])

for size, name in [(180, "apple-touch-icon.png"), (192, "android-chrome-192x192.png"), (512, "android-chrome-512x512.png")]:
    src.resize((size, size), LZ).save(name, optimize=True)

print("Icons regenerated from", LOGO)
