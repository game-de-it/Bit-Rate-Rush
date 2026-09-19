import pyxel

from core import palette as P


class EnemyBullet:
    """ボスが撃つ弾。プレイヤーにだけ当たる。"""
    __slots__ = ("x", "y", "vx", "vy", "life", "dmg", "r", "alive")
    R = 3

    def __init__(self, x, y, vx, vy, dmg, life=240):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.dmg = dmg
        self.life = life
        self.r = self.R
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self):
        pyxel.circ(self.x, self.y, 3, P.BOSS)
        pyxel.circ(self.x, self.y, 1, P.GOLD if (self.life // 4) % 2 else 7)
