"""PNG を 32 色パレット (assets/brr.pyxpal) に減色して assets/img/ に保存する。

    python3 tools/convert_png.py <入力.png> <出力名> [幅 高さ] [--nodither] [--fit|--crop]

例: python3 tools/convert_png.py ~/Downloads/town.png town_bg 320 240
    → assets/img/town_bg.png (パレット色のみで構成された PNG。pyxel の Image.load でそのまま読める)
--crop (既定): アスペクトを保って拡縮し、中央で切り抜く
--fit          : 全体が入るよう拡縮 (余白は透明色 0 = 黒)
"""
import os
import sys

from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAL_PATH = os.path.join(ROOT, "assets", "brr.pyxpal")
OUT_DIR = os.path.join(ROOT, "assets", "img")


def load_palette():
    cols = []
    with open(PAL_PATH) as f:
        for line in f:
            line = line.strip()
            if line:
                cols.append(tuple(int(line[i:i + 2], 16) for i in (0, 2, 4)))
    return cols


def convert(src, name, w=None, h=None, dither=True, mode="crop"):
    cols = load_palette()
    im = Image.open(src).convert("RGB")
    if w and h:
        sw, sh = im.size
        if mode == "crop":
            scale = max(w / sw, h / sh)
            im = im.resize((max(1, round(sw * scale)), max(1, round(sh * scale))), Image.LANCZOS)
            left = (im.size[0] - w) // 2
            top = (im.size[1] - h) // 2
            im = im.crop((left, top, left + w, top + h))
        else:
            scale = min(w / sw, h / sh)
            im2 = im.resize((max(1, round(sw * scale)), max(1, round(sh * scale))), Image.LANCZOS)
            im = Image.new("RGB", (w, h), cols[0])
            im.paste(im2, ((w - im2.size[0]) // 2, (h - im2.size[1]) // 2))
    pal = Image.new("P", (1, 1))
    flat = [c for rgb in cols for c in rgb]
    flat += [0] * (768 - len(flat))
    pal.putpalette(flat)
    q = im.quantize(palette=pal, dither=Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE)
    out = q.convert("RGB")
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"{name}.png")
    out.save(path)
    return path


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]
    src, name = args[0], args[1]
    w = int(args[2]) if len(args) > 2 else None
    h = int(args[3]) if len(args) > 3 else None
    p = convert(src, name, w, h, dither="--nodither" not in flags, mode="fit" if "--fit" in flags else "crop")
    print("wrote", p)
