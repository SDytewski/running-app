from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


SIZE = 3000
ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "output" / "astro-violet-pdf-extract.png"
OUT = ROOT / "output" / "astro-violet-ride-over-your-wave-planet-v7.jpg"
FONT_DIR = Path("C:/Windows/Fonts")


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def draw_tracking_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    tracking: int,
) -> None:
    widths = [text_size(draw, char, font)[0] for char in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total / 2
    for char, width in zip(text, widths):
        draw.text((x, xy[1]), char, font=font, fill=fill, anchor="la")
        x += width + tracking


def draw_star(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, fill: tuple[int, int, int, int]) -> None:
    cx, cy = center
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.42
        points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw.polygon(points, fill=fill)


def draw_gentle_arc_text(
    base: Image.Image,
    text: str,
    center_x: int,
    baseline_y: int,
    span: int,
    arch_height: int,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    tracking: int,
) -> None:
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    scratch = ImageDraw.Draw(overlay)
    widths = [text_size(scratch, char, font)[0] for char in text]
    natural = sum(widths) + tracking * (len(text) - 1)
    x = center_x - natural / 2
    for char, width in zip(text, widths):
        cx = x + width / 2
        normalized = (cx - center_x) / (span / 2)
        y = baseline_y - arch_height * (1 - normalized * normalized)
        slope = 2 * arch_height * normalized / (span / 2)
        rotation = math.degrees(math.atan(slope)) * 0.55
        glyph = Image.new("RGBA", (max(1, int(width + 110)), 290), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        gd.text((glyph.width / 2, glyph.height / 2), char, font=font, fill=fill, anchor="mm")
        rotated = glyph.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)
        overlay.alpha_composite(rotated, (int(cx - rotated.width / 2), int(y - rotated.height / 2)))
        x += width + tracking
    base.alpha_composite(overlay)


def draw_upright_arc_text(
    base: Image.Image,
    text: str,
    center_x: int,
    baseline_y: int,
    span: int,
    arch_height: int,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    tracking: int,
) -> None:
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    scratch = ImageDraw.Draw(overlay)
    widths = [text_size(scratch, char, font)[0] for char in text]
    natural = sum(widths) + tracking * (len(text) - 1)
    scale = min(1.0, span / natural)
    x = center_x - natural * scale / 2
    for char, width in zip(text, widths):
        cx = x + width * scale / 2
        normalized = (cx - center_x) / (span / 2)
        y = baseline_y - arch_height * (1 - normalized * normalized)
        glyph = Image.new("RGBA", (max(1, int(width + 80)), 250), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        gd.text((glyph.width / 2, glyph.height / 2), char, font=font, fill=fill, anchor="mm")
        if scale != 1.0:
            glyph = glyph.resize((int(glyph.width * scale), int(glyph.height * scale)), Image.Resampling.LANCZOS)
        overlay.alpha_composite(glyph, (int(cx - glyph.width / 2), int(y - glyph.height / 2)))
        x += (width + tracking) * scale
    base.alpha_composite(overlay)


def make_square_background() -> Image.Image:
    src = Image.open(SOURCE).convert("RGB")
    scale = SIZE / src.height
    resized = src.resize((int(src.width * scale), SIZE), Image.Resampling.LANCZOS)
    crop_x = resized.width - SIZE
    square = resized.crop((crop_x, 0, crop_x + SIZE, SIZE)).convert("RGBA")

    # Darken and color-grade to leave text room while preserving the owned art.
    grade = Image.new("RGBA", (SIZE, SIZE), (12, 0, 18, 72))
    square.alpha_composite(grade)

    vignette = Image.new("L", (SIZE, SIZE), 0)
    vd = ImageDraw.Draw(vignette)
    for i in range(0, 1450, 12):
        alpha = int(225 * (i / 1450) ** 2)
        vd.rectangle((i, i, SIZE - i, SIZE - i), outline=alpha, width=12)
    dark = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    dark.putalpha(vignette.filter(ImageFilter.GaussianBlur(95)))
    square.alpha_composite(dark)

    # A subtle left-side plate gives the typography a real printed-cover feel.
    plate = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    pd = ImageDraw.Draw(plate)
    pd.rectangle((0, 0, 1710, SIZE), fill=(0, 0, 0, 118))
    plate = plate.filter(ImageFilter.GaussianBlur(42))
    square.alpha_composite(plate)
    return square


def add_artwork_text(img: Image.Image) -> Image.Image:
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    band_font = ImageFont.truetype(str(FONT_DIR / "ariblk.ttf"), 184)
    title_font = ImageFont.truetype(str(FONT_DIR / "arialbd.ttf"), 104)

    white = (255, 248, 253, 255)
    pink = (248, 42, 175, 250)
    violet = (88, 18, 136, 245)
    black = (3, 0, 9, 245)

    # Flat constructivist blocks: upright type on the page, not perspective-skewed.
    d.polygon(
        [
            (0, 388),
            (1740, 244),
            (1632, 1018),
            (0, 1196),
        ],
        fill=violet,
    )
    d.polygon(
        [
            (0, 486),
            (1638, 350),
            (1530, 908),
            (0, 1076),
        ],
        fill=pink,
    )
    d.polygon([(0, 1114), (1542, 948), (1490, 1034), (0, 1212)], fill=black)
    d.rectangle((0, 1290, 1540, 1490), fill=(0, 0, 0, 178))
    d.line((0, 1244, 1476, 1082), fill=(255, 244, 252, 115), width=10)

    draw_tracking_text(d, (800, 718), "ASTRO VIOLET", band_font, white, -4)

    draw_tracking_text(d, (800, 1402), "RIDE OVER YOUR WAVE", title_font, white, 2)
    d.line((300, 1526, 1300, 1526), fill=pink, width=12)

    glow = layer.filter(ImageFilter.GaussianBlur(10))
    glow_alpha = glow.getchannel("A").point(lambda v: int(v * 0.22))
    glow.putalpha(glow_alpha)
    img.alpha_composite(glow)
    img.alpha_composite(layer)
    return img


def add_film_finish(img: Image.Image) -> Image.Image:
    rng = random.Random(9009)
    grain = Image.new("L", (SIZE, SIZE))
    gp = grain.load()
    for y in range(SIZE):
        for x in range(SIZE):
            gp[x, y] = rng.randrange(0, 20)
    grain_rgba = Image.merge("RGBA", (grain, grain, grain, grain.point(lambda v: int(v * 0.18))))
    img.alpha_composite(grain_rgba)

    scan = ImageDraw.Draw(img)
    for y in range(0, SIZE, 7):
        scan.line((0, y, SIZE, y), fill=(0, 0, 0, 10), width=1)
    return img.convert("RGB")


def main() -> None:
    OUT.parent.mkdir(exist_ok=True)
    cover = make_square_background()
    cover = add_artwork_text(cover)
    cover = add_film_finish(cover)
    cover.save(OUT, quality=96, subsampling=0, optimize=True)
    print(OUT)


if __name__ == "__main__":
    main()
