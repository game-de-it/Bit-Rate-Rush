"""武器・パッシブのアイコン (assets/img/icon_<key>.png、16x16、黒 = 透過)。無ければ色付きの四角で代用。"""
import pyxel

from core import images


def draw(key, x, y, col=13, size=16):
    """(x, y) に 16x16 のアイコンを描く。画像が無ければ size 四方の色の四角。True = 画像を描いた。"""
    img = images.get(f"icon_{key}")
    if img is None:
        pyxel.rect(x, y, size, size, col)
        pyxel.rectb(x, y, size, size, 7)
        return False
    pyxel.blt(x, y, img, 0, 0, 16, 16, 0)
    return True
