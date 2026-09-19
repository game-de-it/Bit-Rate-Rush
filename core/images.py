"""PNG 画像 (背景・キャラ絵) の読み込み。assets/img/<name>.png。

画像は tools/convert_png.py で 32 色パレットに減色済みのものを置く。
サイズは PNG ヘッダから読む (PIL 不要)。無ければ None を返し、呼び出し側でプレースホルダを描く。
"""
import os
import struct

import pyxel

DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "img")
_cache = {}


def _png_size(path):
    with open(path, "rb") as f:
        head = f.read(24)
    if head[:8] != b"\x89PNG\r\n\x1a\n":
        return None
    w, h = struct.unpack(">II", head[16:24])
    return w, h


def get(name):
    """pyxel.Image を返す (キャッシュ)。ファイルが無ければ None。"""
    if name in _cache:
        return _cache[name]
    path = os.path.join(DIR, f"{name}.png")
    img = None
    if os.path.exists(path):
        try:
            w, h = _png_size(path)
            img = pyxel.Image(w, h)
            img.load(0, 0, path)
        except Exception:
            img = None
    _cache[name] = img
    return img


def draw(name, x, y, colkey=None):
    img = get(name)
    if img is None:
        return False
    pyxel.blt(x, y, img, 0, 0, img.width, img.height, colkey)
    return True
