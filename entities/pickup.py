import pyxel

from core import sprites as S


class Pickup:
    __slots__ = ("x", "y", "kind", "value", "attracted", "spd", "alive", "sprite")

    def __init__(self, kind, x, y, value=0):
        self.kind = kind
        self.x, self.y = x, y
        self.value = value
        self.attracted = False
        self.spd = 1.0
        self.alive = True
        if kind == "xp":
            self.sprite = S.GEM_S if value < 5 else (S.GEM_M if value < 20 else S.GEM_L)
        elif kind == "heal":
            self.sprite = S.HEAL
        elif kind == "coin":
            self.sprite = S.COIN
        else:
            self.sprite = S.MAGNET

    def draw(self):
        u, v, w, h = self.sprite
        pyxel.blt(self.x - w / 2, self.y - h / 2, 0, u, v, w, h, S.COLKEY)
