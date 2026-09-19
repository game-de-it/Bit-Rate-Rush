import pyxel


class Particle:
    __slots__ = ("x", "y", "vx", "vy", "life", "col", "alive")

    def __init__(self, x, y, vx, vy, life, col):
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = life
        self.col = col
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vx *= 0.9
        self.vy *= 0.9
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    def draw(self):
        pyxel.pset(self.x, self.y, self.col)
