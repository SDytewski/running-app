from __future__ import annotations

import math
import random
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


SIZE = 3000
OUT_DIR = Path("output")
OUT_PATH = OUT_DIR / "ride-over-your-wave-cover-v2.jpg"
TEXT_OUT_PATH = OUT_DIR / "ride-over-your-wave-cover-with-text-v4.jpg"
BADGE_OUT_PATH = OUT_DIR / "astro-violet-ride-over-your-wave-badge-v1.jpg"
FONT_DIR = Path("C:/Windows/Fonts")


def lerp(a: int, b: int, t: float) -> int:
    return int(a + (b - a) * t)


def gradient_background() -> Image.Image:
    img = Image.new("RGB", (SIZE, SIZE))
    px = img.load()
    top = (14, 8, 34)
    middle = (50, 16, 83)
    bottom = (233, 54, 147)
    for y in range(SIZE):
        t = y / (SIZE - 1)
        if t < 0.62:
            k = t / 0.62
            color = tuple(lerp(top[i], middle[i], k) for i in range(3))
        else:
            k = (t - 0.62) / 0.38
            color = tuple(lerp(middle[i], bottom[i], k) for i in range(3))
        for x in range(SIZE):
            vignette = 1.0 - 0.34 * math.hypot((x - SIZE / 2) / SIZE, (y - SIZE / 2) / SIZE)
            px[x, y] = tuple(max(0, min(255, int(c * vignette))) for c in color)
    return img


def draw_stars(draw: ImageDraw.ImageDraw, rng: random.Random) -> None:
    for _ in range(1250):
        x = rng.randrange(0, SIZE)
        y = rng.randrange(0, int(SIZE * 0.67))
        radius = rng.choice([1, 1, 1, 2, 2, 3])
        glow = rng.randrange(70, 180)
        color = (glow + 55, glow + 30, min(255, glow + 75))
        draw.ellipse((x - radius, y - radius, x + radius, y + radius), fill=color)
    for _ in range(55):
        x = rng.randrange(120, SIZE - 120)
        y = rng.randrange(90, int(SIZE * 0.5))
        length = rng.randrange(18, 48)
        color = (255, rng.randrange(145, 205), 235)
        draw.line((x, y, x + length, y + length // 4), fill=color, width=rng.choice([2, 3]))


def draw_planet(base: Image.Image, rng: random.Random) -> None:
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy, r = 2180, 760, 355
    for i in range(r, 0, -2):
        t = i / r
        color = (
            int(109 + 70 * (1 - t)),
            int(30 + 20 * (1 - t)),
            int(142 + 70 * (1 - t)),
            int(58 + 95 * (1 - t)),
        )
        d.ellipse((cx - i, cy - i, cx + i, cy + i), fill=color)
    for offset, alpha in [(-62, 115), (-22, 150), (24, 130), (73, 92)]:
        d.arc((cx - r - 65, cy + offset - 96, cx + r + 65, cy + offset + 96), 190, 350, fill=(255, 117, 204, alpha), width=7)
    for _ in range(115):
        x = rng.randrange(cx - r, cx + r)
        y = rng.randrange(cy - r, cy + r)
        if (x - cx) ** 2 + (y - cy) ** 2 <= r * r:
            d.point((x, y), fill=(255, 190, 234, rng.randrange(45, 130)))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.35)))


def draw_wave(base: Image.Image) -> None:
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    horizon = 1720
    for i in range(42):
        y = horizon + i * 35
        amp = 44 + i * 5.8
        points = []
        for x in range(-80, SIZE + 90, 12):
            phase = x / 155 + i * 0.28
            yy = y + math.sin(phase) * amp + math.sin(x / 70 + i) * 9
            points.append((x, yy))
        alpha = max(16, 175 - i * 4)
        color = (255, 69 + i * 2, 205, alpha)
        d.line(points, fill=color, width=max(3, 12 - i // 5), joint="curve")
    for i in range(26):
        y = horizon + i * 54
        d.line((0, y, SIZE, y + i * 17), fill=(121, 52, 185, max(12, 95 - i * 3)), width=3)
    vanishing_x, vanishing_y = SIZE // 2, horizon - 20
    for x in range(-1200, SIZE + 1300, 185):
        d.line((x, SIZE, vanishing_x, vanishing_y), fill=(246, 62, 180, 55), width=3)
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.25)))


def draw_retro_sun(base: Image.Image) -> None:
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    cx, cy, r = 880, 1280, 440
    for i in range(r, 0, -5):
        t = i / r
        color = (255, int(74 + 92 * (1 - t)), int(160 + 48 * (1 - t)), int(28 + 120 * (1 - t)))
        d.ellipse((cx - i, cy - i, cx + i, cy + i), fill=color)
    for n in range(9):
        y = cy - 310 + n * 75
        d.rectangle((cx - r - 16, y, cx + r + 16, y + 24 + n * 4), fill=(24, 8, 45, 185))
    base.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.4)))


def add_grain_and_finish(img: Image.Image, rng: random.Random) -> Image.Image:
    grain = Image.new("L", (SIZE, SIZE))
    gp = grain.load()
    for y in range(SIZE):
        for x in range(SIZE):
            gp[x, y] = rng.randrange(0, 38)
    grain_rgba = Image.merge("RGBA", (grain, grain, grain, grain.point(lambda v: int(v * 0.42))))
    img = img.convert("RGBA")
    img.alpha_composite(grain_rgba)
    d = ImageDraw.Draw(img)
    for y in range(0, SIZE, 6):
        d.line((0, y, SIZE, y), fill=(10, 0, 18, 16), width=1)
    vignette = Image.new("L", (SIZE, SIZE), 0)
    vd = ImageDraw.Draw(vignette)
    for i in range(0, 1150, 10):
        alpha = int(210 * (i / 1150) ** 2)
        vd.rectangle((i, i, SIZE - i, SIZE - i), outline=alpha, width=10)
    dark = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    dark.putalpha(vignette.filter(ImageFilter.GaussianBlur(80)))
    img.alpha_composite(dark)
    return img.convert("RGB")


def text_size(draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont) -> tuple[int, int]:
    left, top, right, bottom = draw.textbbox((0, 0), text, font=font)
    return right - left, bottom - top


def draw_star(draw: ImageDraw.ImageDraw, center: tuple[int, int], radius: int, fill: tuple[int, int, int, int]) -> None:
    cx, cy = center
    points = []
    for i in range(10):
        angle = -math.pi / 2 + i * math.pi / 5
        r = radius if i % 2 == 0 else radius * 0.42
        points.append((cx + math.cos(angle) * r, cy + math.sin(angle) * r))
    draw.polygon(points, fill=fill)


def draw_tracking_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    tracking: int,
    anchor: str = "mm",
) -> None:
    widths = [text_size(draw, char, font)[0] for char in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x, y = xy
    if anchor == "mm":
        x -= total // 2
    for char, width in zip(text, widths):
        draw.text((x, y), char, font=font, fill=fill, anchor="la")
        x += width + tracking


def draw_arched_text(
    base: Image.Image,
    text: str,
    center: tuple[int, int],
    radius: int,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    angle_start: float,
    angle_end: float,
) -> None:
    overlay = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(overlay)
    chars = list(text)
    if len(chars) == 1:
        angles = [(angle_start + angle_end) / 2]
    else:
        angles = [angle_start + (angle_end - angle_start) * i / (len(chars) - 1) for i in range(len(chars))]
    for char, angle_deg in zip(chars, angles):
        angle = math.radians(angle_deg)
        x = center[0] + math.cos(angle) * radius
        y = center[1] + math.sin(angle) * radius
        w, h = text_size(temp_draw, char, font)
        glyph = Image.new("RGBA", (max(1, w + 90), max(1, h + 90)), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        gd.text((glyph.width / 2, glyph.height / 2), char, font=font, fill=fill, anchor="mm")
        rotated = glyph.rotate(angle_deg + 90, resample=Image.Resampling.BICUBIC, expand=True)
        overlay.alpha_composite(rotated, (int(x - rotated.width / 2), int(y - rotated.height / 2)))
    base.alpha_composite(overlay)


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
    scale = min(1.0, span / natural)
    x = center_x - natural * scale / 2
    for char, width in zip(text, widths):
        cx = x + width * scale / 2
        normalized = (cx - center_x) / (span / 2)
        y = baseline_y - arch_height * (1 - normalized * normalized)
        slope = 2 * arch_height * normalized / (span / 2)
        rotation = math.degrees(math.atan(slope)) * 0.72
        glyph = Image.new("RGBA", (max(1, int(width + 90)), 260), (0, 0, 0, 0))
        gd = ImageDraw.Draw(glyph)
        gd.text((glyph.width / 2, glyph.height / 2), char, font=font, fill=fill, anchor="mm")
        if scale != 1.0:
            glyph = glyph.resize((int(glyph.width * scale), int(glyph.height * scale)), Image.Resampling.LANCZOS)
        rotated = glyph.rotate(rotation, resample=Image.Resampling.BICUBIC, expand=True)
        overlay.alpha_composite(rotated, (int(cx - rotated.width / 2), int(y - rotated.height / 2)))
        x += (width + tracking) * scale
    base.alpha_composite(overlay)


def draw_album_text(img: Image.Image) -> Image.Image:
    base = img.convert("RGBA")
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    band_font = ImageFont.truetype(str(FONT_DIR / "bahnschrift.ttf"), 176)
    title_font = ImageFont.truetype(str(FONT_DIR / "bahnschrift.ttf"), 112)
    small_font = ImageFont.truetype(str(FONT_DIR / "bahnschrift.ttf"), 42)

    # Soft shadow plate for legibility without turning the artwork into a logo badge.
    d.rounded_rectangle((360, 145, 2640, 845), radius=18, fill=(5, 2, 17, 188))
    d.rounded_rectangle((450, 245, 2550, 760), radius=12, outline=(255, 81, 196, 145), width=6)

    draw_star(d, (1500, 295), 48, (255, 70, 190, 245))
    draw_tracking_text(d, (1500, 450), "ASTRO VIOLET", band_font, (255, 218, 238, 255), 18)

    d.line((900, 555, 2100, 555), fill=(255, 68, 188, 190), width=6)

    draw_tracking_text(d, (1500, 678), "RIDE OVER YOUR WAVE.", title_font, (255, 92, 201, 255), 7)
    draw_tracking_text(d, (1500, 765), "SINGLE", small_font, (255, 203, 232, 180), 16)

    glow = layer.filter(ImageFilter.GaussianBlur(9))
    glow_alpha = glow.getchannel("A").point(lambda v: int(v * 0.42))
    glow.putalpha(glow_alpha)
    base.alpha_composite(glow)
    base.alpha_composite(layer)
    return base.convert("RGB")


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    xy: tuple[int, int],
    text: str,
    font: ImageFont.FreeTypeFont,
    fill: tuple[int, int, int, int],
    tracking: int,
) -> None:
    draw_tracking_text(draw, xy, text, font, fill, tracking)


def draw_original_badge_cover() -> Image.Image:
    bg = Image.new("RGB", (SIZE, SIZE), (42, 7, 64))
    px = bg.load()
    for y in range(SIZE):
        for x in range(SIZE):
            nx = (x - SIZE / 2) / (SIZE / 2)
            ny = (y - SIZE / 2) / (SIZE / 2)
            r = min(1.0, math.hypot(nx, ny))
            glow = max(0.0, 1.0 - r)
            wave = 0.035 * math.sin((x + y) / 90)
            px[x, y] = (
                int(42 + 95 * glow + 25 * wave),
                int(7 + 24 * glow),
                int(64 + 72 * glow + 18 * wave),
            )

    img = bg.convert("RGBA")
    layer = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)

    cream = (255, 209, 234, 255)
    hot = (255, 45, 174, 255)
    soft = (255, 118, 206, 220)
    dark = (28, 3, 45, 255)

    band_font = ImageFont.truetype(str(FONT_DIR / "bahnschrift.ttf"), 185)
    title_font = ImageFont.truetype(str(FONT_DIR / "bahnschrift.ttf"), 94)

    d.rounded_rectangle((250, 250, 2750, 2750), radius=120, outline=hot, width=18)
    d.rounded_rectangle((355, 355, 2645, 2645), radius=90, outline=(255, 126, 211, 130), width=7)

    draw_star(d, (1500, 575), 118, hot)
    draw_gentle_arc_text(
        layer,
        "ASTRO VIOLET",
        center_x=1500,
        baseline_y=1020,
        span=1670,
        arch_height=135,
        font=band_font,
        fill=cream,
        tracking=24,
    )

    d.line((720, 1160, 2280, 1160), fill=hot, width=16)
    d.line((860, 1225, 2140, 1225), fill=soft, width=7)

    # Original wave-wing emblem: nods to retro badge geometry without copying the coffee logo.
    center = (1500, 1510)
    d.ellipse((1375, 1385, 1625, 1635), fill=hot)
    d.ellipse((1436, 1446, 1564, 1574), fill=dark)
    for i, radius in enumerate((36, 62, 88)):
        d.arc(
            (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius),
            205,
            335,
            fill=cream,
            width=9,
        )
    for side in (-1, 1):
        root_x = 1410 if side == -1 else 1590
        tip_x = 575 if side == -1 else 2425
        d.pieslice(
            (
                min(root_x, tip_x),
                1290,
                max(root_x, tip_x),
                1755,
            ),
            180 if side == -1 else 0,
            360 if side == -1 else 180,
            fill=hot,
        )
        d.polygon(
            [
                (root_x, 1440),
                (tip_x, 1265),
                (tip_x + side * -85, 1455),
                (root_x, 1595),
            ],
            fill=hot,
        )
        for n in range(5):
            y = 1365 + n * 72
            d.line((root_x + side * 45, y + 38, tip_x - side * 145, y), fill=cream, width=10)

    draw_centered_text(d, (1500, 1925), "RIDE OVER YOUR WAVE", title_font, cream, 12)
    d.line((780, 2025, 2220, 2025), fill=hot, width=10)
    draw_centered_text(d, (1500, 2150), "SINGLE", ImageFont.truetype(str(FONT_DIR / "bahnschrift.ttf"), 54), soft, 22)

    glow = layer.filter(ImageFilter.GaussianBlur(14))
    glow_alpha = glow.getchannel("A").point(lambda v: int(v * 0.30))
    glow.putalpha(glow_alpha)
    img.alpha_composite(glow)
    img.alpha_composite(layer)

    final = img.convert("RGB")
    grain = Image.new("L", (SIZE, SIZE))
    rng = random.Random(404)
    gp = grain.load()
    for y in range(SIZE):
        for x in range(SIZE):
            gp[x, y] = rng.randrange(0, 24)
    grain_rgba = Image.merge("RGBA", (grain, grain, grain, grain.point(lambda v: int(v * 0.20))))
    finished = final.convert("RGBA")
    finished.alpha_composite(grain_rgba)
    return finished.convert("RGB")


def main() -> None:
    rng = random.Random(1984)
    OUT_DIR.mkdir(exist_ok=True)
    bg = gradient_background().convert("RGBA")
    draw = ImageDraw.Draw(bg)
    draw_stars(draw, rng)
    draw_planet(bg, rng)
    draw_retro_sun(bg)
    draw_wave(bg)
    final = add_grain_and_finish(bg, rng)
    final.save(OUT_PATH, quality=95, subsampling=0, optimize=True)
    with_text = draw_album_text(final)
    with_text.save(TEXT_OUT_PATH, quality=95, subsampling=0, optimize=True)
    badge = draw_original_badge_cover()
    badge.save(BADGE_OUT_PATH, quality=95, subsampling=0, optimize=True)
    print(OUT_PATH.resolve())
    print(TEXT_OUT_PATH.resolve())
    print(BADGE_OUT_PATH.resolve())


if __name__ == "__main__":
    main()
