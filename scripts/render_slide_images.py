"""Typeset the reviewed slide copy into 1920 × 1080 PNGs for both players."""

import argparse
import json
import os
import re
from functools import lru_cache
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
WIDTH, HEIGHT = 1920, 1080
BACKGROUND, INK = "#F8FAFC", "#17324D"
TEAL, AMBER, RULE = "#087F8C", "#B45309", "#D3E0E9"
FONT_DIR = Path(os.environ.get("WINDIR", "C:/Windows")) / "Fonts"
OPERATORS = str.maketrans({"＋": "+", "－": "−", "＝": "="})

HIGHLIGHTS = {
    "S01A": ("25",), "S01B": ("25",),
    "S02A": ("a",), "S02B": ("a",),
    "S03B": ("3x",), "S04A": ("3x",), "S04B": ("3x",),
    "S05B": ("1",), "S06B": ("4a", "−3"),
}


@lru_cache
def font(family, size):
    return ImageFont.truetype(str(FONT_DIR / family), size)


def formula_runs(text, size, marks):
    text = text.translate(OPERATORS)
    patterns = [re.escape(mark) + (r"(?!\d)" if mark.isdecimal() else "") for mark in marks]
    parts = re.split(f"({'|'.join(patterns)})", text) if patterns else [text]
    for part in parts:
        color = AMBER if part == "1" else TEAL
        spaced = re.sub(r"([=+−×·])", r" \1 ", part)
        for piece in re.findall(r"[a-z]+|[^a-z]+", spaced):
            face = "cambriai.ttf" if piece.isalpha() else "cambria.ttc"
            yield piece, font(face, size), color if part in marks else INK


def text_run(text, size, color=INK, bold=False):
    return text, font("msyhbd.ttc" if bold else "msyh.ttc", size), color


def compose(draw, runs, baseline, left=None):
    runs = list(runs)
    width = sum(draw.textlength(text, font=face) for text, face, _ in runs)
    x = (WIDTH - width) / 2 if left is None else left
    if x < 136 or x + width > WIDTH - 136:
        raise ValueError(f"Content exceeds horizontal safe area: {runs[0][0]} ({width:.0f}px)")
    for text, face, color in runs:
        draw.text((x, baseline), text, font=face, fill=color, anchor="ls")
        x += draw.textlength(text, font=face)


def render(page, logo_path):
    pid = page["page_id"].removeprefix("L01-")
    image = Image.new("RGB", (WIDTH, HEIGHT), BACKGROUND)
    draw = ImageDraw.Draw(image)
    draw.line((152, 218, 1768, 218), fill=RULE, width=2)
    draw.line((152, 218, 248, 218), fill=TEAL, width=6)
    if pid == "S01A":
        with Image.open(logo_path) as source:
            logo = source.convert("RGBA")
        logo.thumbnail((510, 138), Image.Resampling.LANCZOS)
        image.paste(logo, (1768 - logo.width, 59), logo)

    lines = list(page["layout"])
    if lines[0][0] in ("head", "warning"):
        kind, text = lines.pop(0)
        compose(draw, [text_run(text, 62, AMBER if kind == "warning" else INK, bold=True)], 163, 152)

    if pid == "S03B":
        baselines = [475, 658]
    elif pid == "S04A":
        baselines = [439, 589, 822]
    elif pid == "S05B":
        baselines = [430, 615, 822]
    elif len(lines) == 3:
        baselines = [502, 705, 822]
    else:
        baselines = [502, 754]

    marks = HIGHLIGHTS.get(pid, ())
    for (kind, text), baseline in zip(lines, baselines, strict=True):
        left = None
        if kind == "formula":
            size = 106 if pid in ("S01A", "S01B", "S04A", "S05B") else 124
            runs = list(formula_runs(text, size, marks))
            if pid in ("S01A", "S01B"):
                full = list(formula_runs("25×7＋25×3＝25×(7＋3)＝250", size, marks))
                left = (WIDTH - sum(draw.textlength(t, font=f) for t, f, _ in full)) / 2
            if pid == "S04A":
                left = 484
        elif kind in ("result", "check"):
            label, math = text.split("：", 1)
            size = 103 if kind == "result" else 78
            runs = [text_run(label + "：", 57 if kind == "result" else 48, TEAL, bold=True)]
            runs.extend(formula_runs(math, size, marks))
        elif kind == "process":
            runs = [text_run(piece, 70, TEAL if piece == " → " else INK, True)
                    for piece in re.split("( → )", text)]
        else:
            size = {"body": 54, "key": 62, "question": 85}[kind]
            if pid == "S08A":
                size = 50
            runs = [text_run(text, size, TEAL if kind == "key" else INK, kind != "body")]
        compose(draw, runs, baseline, left)
    return image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    pages = json.loads((ROOT / "slides/pages.json").read_text(encoding="utf-8"))
    args.output.mkdir(parents=True, exist_ok=True)
    for page in pages:
        picture = render(page, ROOT / "assets/branding/huainan-normal-university.png")
        picture.save(args.output / f"{page['page_id']}.png", optimize=True)
    print(f"Typeset {len(pages)} slide images at {WIDTH} × {HEIGHT}.")


if __name__ == "__main__":
    main()
