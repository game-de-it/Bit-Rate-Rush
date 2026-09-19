"""アイコンシート (黒背景のグリッド) から 16x16 のアイコンを切り出して assets/img/icon_<key>.png に保存する。
    python3 tools/make_icons.py art/icons_sheet.png          # 武器・パッシブ (7x3)
    python3 tools/make_icons.py art/items_sheet.png items    # 消耗品 (4x2、icon_item_<key>.png)
黒 (透過) は色 0 になる。空のセルは飛ばす。"""
import os
import sys

from PIL import Image

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tools.convert_png import load_palette, OUT_DIR

KEYS = [
    ["knife", "spear", "bow", "shuriken", "hammer", "sickle", "boomerang"],
    ["axe", "magic", "holy", "orbit", "zap", "fire", "tower"],
    ["might", "cooldown", "speed", "maxhp", "magnet", "amount", "heal"],
]
KEYS_ITEMS = [
    ["item_herb", "item_bomb", "item_magnet", "item_charm"],
    ["item_tome", "item_elixir", "item_arrow", None],
]
SIZE = 16


def _segments(mask, min_gap):
    """1 次元の投影 (True/False の列) から連続区間を返す。min_gap 未満の切れ目は無視。"""
    segs = []
    start = None
    gap = 0
    for i, v in enumerate(mask):
        if v:
            if start is None:
                start = i
            gap = 0
        elif start is not None:
            gap += 1
            if gap >= min_gap:
                segs.append((start, i - gap))
                start = None
                gap = 0
    if start is not None:
        segs.append((start, len(mask) - 1))
    return segs


def _quantizer():
    cols_pal = load_palette()
    pal = Image.new("P", (1, 1))
    flat = [c for rgb in cols_pal for c in rgb]
    flat += [0] * (768 - len(flat))
    pal.putpalette(flat)
    return pal


def _save(im, box, key, pal):
    x0, y0, x1, y1 = box
    side = max(x1 - x0, y1 - y0) + 1
    pad = int(side * 0.06)
    side += pad * 2
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    sq = Image.new("RGB", (side, side), (0, 0, 0))
    sq.paste(im.crop((cx - side // 2, cy - side // 2, cx - side // 2 + side, cy - side // 2 + side)), (0, 0))
    small = sq.resize((SIZE, SIZE), Image.LANCZOS)
    small.quantize(palette=pal, dither=Image.Dither.NONE).convert("RGB").save(os.path.join(OUT_DIR, f"icon_{key}.png"))


def _boxes_by_cluster(bright, W, H):
    """行 → 列の順に非黒のかたまりのバウンディングボックスを返す (グリッドが不均等なシート用)。"""
    boxes = []
    row_mask = [any(bright[y]) for y in range(H)]
    for (ry0, ry1) in _segments(row_mask, min_gap=int(H * 0.03)):
        col_mask = [any(bright[y][x] for y in range(ry0, ry1 + 1)) for x in range(W)]
        for (cx0, cx1) in _segments(col_mask, min_gap=int(W * 0.03)):
            ys = [y for y in range(ry0, ry1 + 1) if any(bright[y][x] for x in range(cx0, cx1 + 1))]
            boxes.append((cx0, min(ys), cx1, max(ys)))
    return boxes


def _boxes_by_grid(bright, W, H, cols, rows):
    """均等グリッドの各セル内で非黒のバウンディングボックス。"""
    boxes = []
    cw, ch = W / cols, H / rows
    for r in range(rows):
        for c in range(cols):
            x0g, y0g, x1g, y1g = int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)
            xs, ys = [], []
            for y in range(y0g, y1g):
                for x in range(x0g, x1g):
                    if bright[y][x]:
                        xs.append(x); ys.append(y)
            boxes.append((min(xs), min(ys), max(xs), max(ys)) if xs else None)
    return boxes


def main(path, keys=KEYS):
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    bright = [[(sum(px[x, y]) > 60) for x in range(W)] for y in range(H)]
    flat_keys = [k for row in keys for k in row]
    expected = sum(1 for k in flat_keys if k)
    boxes = _boxes_by_cluster(bright, W, H)
    if len(boxes) == expected:
        pairs = list(zip([k for k in flat_keys if k], boxes))
        print("cluster mode")
    else:
        boxes = _boxes_by_grid(bright, W, H, len(keys[0]), len(keys))
        pairs = [(k, b) for k, b in zip(flat_keys, boxes) if k and b]
        print("grid mode (clusters found:", len(boxes), ")")
    pal = _quantizer()
    os.makedirs(OUT_DIR, exist_ok=True)
    for key, box in pairs:
        _save(im, box, key, pal)
    print("wrote", len(pairs), "icons to", OUT_DIR, "(expected", expected, ")")


def single(path, key):
    """1 枚絵 (黒背景) から 1 個だけ切り出す。"""
    im = Image.open(path).convert("RGB")
    W, H = im.size
    px = im.load()
    xs, ys = [], []
    for y in range(H):
        for x in range(W):
            if sum(px[x, y]) > 60:
                xs.append(x); ys.append(y)
    _save(im, (min(xs), min(ys), max(xs), max(ys)), key, _quantizer())
    print("wrote icon_%s.png" % key)


if __name__ == "__main__":
    if len(sys.argv) > 3 and sys.argv[1] == "--single":
        single(sys.argv[2], sys.argv[3])
    else:
        path = sys.argv[1] if len(sys.argv) > 1 else "art/icons_sheet.png"
        main(path, KEYS_ITEMS if len(sys.argv) > 2 and sys.argv[2] == "items" else KEYS)
