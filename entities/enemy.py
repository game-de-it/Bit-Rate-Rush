import pyxel

from core import sprites as S
from data.enemies import ENEMIES


class Enemy:
    __slots__ = ("x", "y", "kind", "hp", "maxhp", "spd", "dmg", "xp", "r", "sprite",
                 "alive", "flash", "kx", "ky", "phase", "boss", "final", "summon",
                 "dash", "dash_cd", "summon_cd", "shoot_cd", "dx", "dy", "data")

    def __init__(self, kind, x, y):
        d = ENEMIES[kind]
        self.kind = kind
        self.x, self.y = x, y
        self.hp = self.maxhp = d["hp"]
        self.spd = d["spd"]
        self.dmg = d["dmg"]
        self.xp = d["xp"]
        self.r = d["r"]
        self.sprite = d["sprite"]
        self.phase = d.get("phase", False)
        self.boss = d.get("boss", False)
        self.final = d.get("final", False)
        self.summon = d.get("summon")
        self.data = d
        self.alive = True
        self.flash = 0
        self.kx = self.ky = 0.0
        self.dash = 0
        self.dash_cd = 180
        self.summon_cd = d.get("summon_cd", 300)
        self.shoot_cd = d.get("shoot_cd", 180)
        self.dx = self.dy = 0.0

    def draw(self):
        u, v, w, h = self.sprite
        if self.flash > 0:
            for c in range(1, len(pyxel.colors)):
                pyxel.pal(c, 7)
            pyxel.blt(self.x - w / 2, self.y - h / 2, 0, u, v, w, h, S.COLKEY)
            pyxel.pal()
        else:
            flip = -w if self.dx < 0 else w
            pyxel.blt(self.x - w / 2, self.y - h / 2, 0, u, v, flip, h, S.COLKEY)
