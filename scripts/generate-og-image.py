#!/usr/bin/env python3
"""One-off generator for public/og-image.png (1200×630). Run: python3 scripts/generate-og-image.py"""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "og-image.png"
FAVICON = ROOT / "public" / "favicon.png"

W, H = 1200, 630
BG_BASE = (6, 4, 4)


def main() -> None:
    base = Image.new("RGB", (W, H), BG_BASE)

    # Soft red washes (matches coming-soon vibe: red + broken black)
    for cx, cy, rw, rh, rgba in (
        (W * 0.35, H * 0.25, 700, 520, (200, 45, 60, 55)),
        (W * 0.82, H * 0.55, 580, 480, (160, 30, 45, 45)),
        (W * 0.2, H * 0.72, 640, 500, (90, 20, 30, 40)),
    ):
        layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(layer)
        d.ellipse(
            (cx - rw / 2, cy - rh / 2, cx + rw / 2, cy + rh / 2),
            fill=rgba,
        )
        layer = layer.filter(ImageFilter.GaussianBlur(90))
        base = Image.alpha_composite(base.convert("RGBA"), layer).convert("RGB")

    # Subtle vignette (darker edges)
    vignette = Image.new("L", (W, H), 0)
    vd = ImageDraw.Draw(vignette)
    vd.ellipse((-W * 0.1, -H * 0.15, W * 1.1, H * 1.15), fill=220)
    vignette = vignette.filter(ImageFilter.GaussianBlur(80))
    dark = Image.new("RGB", (W, H), (0, 0, 0))
    base = Image.blend(base, dark, 0.22)
    # Re-apply slight warmth on top left - skip, keep simple

    img = base
    draw = ImageDraw.Draw(img)

    # Logo from favicon (already mark on dark rounded tile)
    logo = Image.open(FAVICON).convert("RGBA")
    logo_h = 200
    ratio = logo_h / logo.height
    logo_w = int(logo.width * ratio)
    logo = logo.resize((logo_w, logo_h), Image.Resampling.LANCZOS)
    lx = (W - logo_w) // 2
    ly = int(H * 0.22)
    img.paste(logo, (lx, ly), logo)

    # Typography
    line1 = "Koryun is a design studio."
    line2 = "Our new site launches June 1, 2026."
    font_paths = [
        "/System/Library/Fonts/Supplemental/SFNS.ttf",
        "/System/Library/Fonts/SFNS.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ]
    font_lg = font_sm = None
    for fp in font_paths:
        p = Path(fp)
        if p.exists():
            try:
                font_lg = ImageFont.truetype(str(p), 32)
                font_sm = ImageFont.truetype(str(p), 24)
                break
            except OSError:
                continue
    if font_lg is None:
        font_lg = font_sm = ImageFont.load_default()

    text_y = ly + logo_h + 48
    tw1 = draw.textlength(line1, font=font_lg) if hasattr(draw, "textlength") else None
    if tw1 is None:
        bbox = draw.textbbox((0, 0), line1, font=font_lg)
        tw1 = bbox[2] - bbox[0]
    else:
        tw1 = int(tw1)
    draw.text(((W - tw1) // 2, text_y), line1, fill=(235, 232, 228), font=font_lg)

    tw2 = draw.textlength(line2, font=font_sm) if hasattr(draw, "textlength") else None
    if tw2 is None:
        bbox = draw.textbbox((0, 0), line2, font=font_sm)
        tw2 = bbox[2] - bbox[0]
    else:
        tw2 = int(tw2)
    draw.text(((W - tw2) // 2, text_y + 44), line2, fill=(160, 158, 155), font=font_sm)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    img.save(OUT, "PNG", optimize=True)
    print(f"Wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
