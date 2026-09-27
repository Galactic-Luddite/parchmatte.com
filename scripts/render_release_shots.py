#!/usr/bin/env python3
"""Render captioned release images from unmodified macOS screen captures.

Requires Pillow. The larger menu panels are crops of the same source capture,
not recreated UI. Keep the raw captures alongside the store PNGs until review
finishes, and inspect every final image before publishing it.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont


@dataclass(frozen=True)
class Shot:
    stem: str
    caption: str
    menu_crop: tuple[int, int, int, int] | None = None


SHOTS = (
    Shot("01-hero", "Your screen, with the feel of real paper"),
    Shot("02-menu", "Strength and softness, right in the menu bar", (2660, 70, 3250, 1200)),
    Shot("03-texture", "Seven real-paper textures", (2660, 70, 3550, 1220)),
    Shot("04-page-light", "Page Light for evening work", (2660, 70, 3550, 1220)),
    Shot("05-per-window", "Give each window its own paper", (2660, 70, 3340, 1580)),
    Shot("06-schedule", "Turns on at sunset, off at sunrise", (2660, 70, 3730, 1230)),
)

CANVAS = (2880, 1800)
PAPER = "#f0e9dd"
INK = "#2c2825"
FONT = "/System/Library/Fonts/HelveticaNeue.ttc"


def rounded_layer(image: Image.Image, radius: int) -> Image.Image:
    layer = image.convert("RGBA")
    mask = Image.new("L", image.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        (0, 0, image.width - 1, image.height - 1), radius=radius, fill=255
    )
    layer.putalpha(mask)
    return layer


def place_with_shadow(
    canvas: Image.Image, image: Image.Image, position: tuple[int, int], radius: int
) -> None:
    x, y = position
    layer = rounded_layer(image, radius)
    shadow = Image.new("RGBA", canvas.size, (0, 0, 0, 0))
    shadow.paste((45, 37, 30, 95), (x + 8, y + 20, x + 8 + image.width, y + 20 + image.height), layer.getchannel("A"))
    canvas.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(26)))
    canvas.alpha_composite(layer, position)


def render(shot: Shot, raw_dir: Path, store_dir: Path, site_dir: Path) -> None:
    source = raw_dir / f"{shot.stem}.png"
    capture = Image.open(source).convert("RGB")
    if capture.size != (4112, 2658):
        raise ValueError(f"{source}: expected 4112x2658 physical capture, got {capture.size}")

    canvas = Image.new("RGBA", CANVAS, PAPER)
    title_font = ImageFont.truetype(FONT, 79)
    draw = ImageDraw.Draw(canvas)
    bbox = draw.textbbox((0, 0), shot.caption, font=title_font)
    title_width = bbox[2] - bbox[0]
    if title_width > 2630:
        title_font = ImageFont.truetype(FONT, 70)
        bbox = draw.textbbox((0, 0), shot.caption, font=title_font)
        title_width = bbox[2] - bbox[0]
    draw.text(((CANVAS[0] - title_width) // 2, 62), shot.caption, font=title_font, fill=INK)

    # Remove a small right-edge wallpaper strip and empty screen bottom. The
    # captured UI and overlay remain untouched.
    desktop = capture.crop((0, 0, 4070, 2450))
    desktop = desktop.resize((2530, 1523), Image.Resampling.LANCZOS)
    place_with_shadow(canvas, desktop, (175, 225), 32)

    if shot.menu_crop:
        menu = capture.crop(shot.menu_crop)
        ratio = min(1040 / menu.width, 1400 / menu.height)
        menu = menu.resize(
            (round(menu.width * ratio), round(menu.height * ratio)),
            Image.Resampling.LANCZOS,
        )
        place_with_shadow(canvas, menu, (CANVAS[0] - menu.width - 125, 265), 30)

    store_dir.mkdir(parents=True, exist_ok=True)
    site_dir.mkdir(parents=True, exist_ok=True)
    flattened = canvas.convert("RGB")
    flattened.save(store_dir / f"{shot.stem}.png", optimize=True)
    for width in (1600, 800):
        flattened.resize((width, width * 5 // 8), Image.Resampling.LANCZOS).save(
            site_dir / f"{shot.stem}-{width}.jpg", quality=90, subsampling=0, optimize=True
        )


def render_social_preview(raw_dir: Path, site_dir: Path) -> None:
    capture = Image.open(raw_dir / "01-hero.png").convert("RGB")
    canvas = Image.new("RGBA", (1200, 630), PAPER)
    title = "Your screen, with the feel of real paper"
    font = ImageFont.truetype(FONT, 51)
    draw = ImageDraw.Draw(canvas)
    box = draw.textbbox((0, 0), title, font=font)
    draw.text(((1200 - (box[2] - box[0])) // 2, 30), title, font=font, fill=INK)
    desktop = capture.crop((0, 0, 4070, 1885))
    desktop = desktop.resize((1060, 491), Image.Resampling.LANCZOS)
    place_with_shadow(canvas, desktop, (70, 105), 20)
    canvas.convert("RGB").save(
        site_dir.parent / "og.jpg", quality=90, subsampling=0, optimize=True
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("raw_dir", type=Path)
    parser.add_argument("store_dir", type=Path)
    parser.add_argument("site_dir", type=Path)
    args = parser.parse_args()
    for shot in SHOTS:
        render(shot, args.raw_dir, args.store_dir, args.site_dir)
        print(f"rendered {shot.stem}")
    render_social_preview(args.raw_dir, args.site_dir)
    print("rendered social preview")


if __name__ == "__main__":
    main()
