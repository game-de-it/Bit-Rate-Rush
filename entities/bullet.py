import pyxel

from core import palette as P
from core import sprites as S

FRAME = 0   # 描画用: 現在フレーム (play.draw が設定)


class Bullet:
    """攻撃判定の共通型。kind ごとに update / draw を分岐する。

    kind: "knife" | "bow" | "spear" | "axe" | "magic" | "holy" | "hammer" | "sweep" | "orbit" | "zap"
    pierce: 残りヒット可能数 (-1 で無限)。tick > 0 なら範囲攻撃で、同じ敵に tick フレームおきにヒットする。
    delay: 0 になるまで判定・描画しない (ハンマーの衝撃波が順に伸びる演出用)。
    sweep: angle = 向き (度)、r = 半径。前方 180 度の半円が判定。
    """
    __slots__ = ("kind", "x", "y", "vx", "vy", "life", "maxlife", "dmg", "r", "pierce", "kb",
                 "hit", "tick", "alive", "col", "angle", "dist", "rot", "owner", "delay", "spin")

    def __init__(self, kind, x, y, dmg, r, col, life=60, vx=0.0, vy=0.0, pierce=1, kb=0.0, tick=0, delay=0):
        self.kind = kind
        self.x, self.y = x, y
        self.vx, self.vy = vx, vy
        self.life = self.maxlife = life
        self.dmg = dmg
        self.r = r
        self.pierce = pierce
        self.kb = kb
        self.hit = {} if tick else set()
        self.tick = tick
        self.alive = True
        self.col = col
        self.angle = pyxel.atan2(vy, vx) if (vx or vy) else 0.0
        self.dist = 0.0
        self.rot = 0.0
        self.owner = None
        self.delay = delay
        self.spin = 0.0

    def update(self, player):
        if self.delay > 0:
            self.delay -= 1
            return
        k = self.kind
        if k == "orbit":
            self.angle += self.rot
            self.x = player.x + pyxel.cos(self.angle) * self.dist
            self.y = player.y + pyxel.sin(self.angle) * self.dist
            return
        if k == "sweep":
            self.x, self.y = player.x, player.y
        if k == "axe":
            self.vy += 0.02
            self.spin += 8
        elif k == "boomerang":
            self.spin += 15
            if self.life > self.maxlife // 2:
                # 往路: 一定の角速度で大きく旋回
                a = pyxel.atan2(self.vy, self.vx) + self.rot
                sp = (self.vx * self.vx + self.vy * self.vy) ** 0.5
                self.vx, self.vy = pyxel.cos(a) * sp, pyxel.sin(a) * sp
            else:
                # 復路: プレイヤーへ誘導。走って逃げても追いつくよう加速し、手元に戻るまで消えない
                dx, dy = player.x - self.x, player.y - self.y
                d2 = dx * dx + dy * dy
                if d2 < 144:
                    self.alive = False
                    return
                d = d2 ** 0.5
                sp = min(7.0, (self.vx * self.vx + self.vy * self.vy) ** 0.5 + 0.08)
                self.vx += (dx / d * sp - self.vx) * 0.2
                self.vy += (dy / d * sp - self.vy) * 0.2
                self.x += self.vx
                self.y += self.vy
                self.dist += 1                  # 復路の経過フレーム (安全弁)
                if self.dist > 600:
                    self.alive = False
                return
        elif k == "shuriken":
            self.spin += 20
        self.x += self.vx
        self.y += self.vy
        self.life -= 1
        if self.life <= 0:
            self.alive = False

    # --- 描画 ---
    def draw(self):
        if self.delay > 0:
            return
        k = self.kind
        x, y = self.x, self.y
        if k == "knife":
            # 残像 + 刃
            pyxel.line(x - self.vx * 4.5, y - self.vy * 4.5, x - self.vx * 1.2, y - self.vy * 1.2, 13)
            _blt_rot(S.KNIFE, x, y, self.angle)
        elif k == "bow":
            pyxel.pset(x - self.vx * 3.6, y - self.vy * 3.6, 13)
            _blt_rot(S.ARROW, x, y, self.angle)
        elif k == "spear":
            # スピード線 2 本 + 槍
            nx, ny = -self.vy, self.vx
            d = (nx * nx + ny * ny) ** 0.5 or 1.0
            nx, ny = nx / d * 3, ny / d * 3
            for sgn in (1, -1):
                pyxel.line(x - self.vx * 7.5 + nx * sgn, y - self.vy * 7.5 + ny * sgn,
                           x - self.vx * 3.0 + nx * sgn, y - self.vy * 3.0 + ny * sgn, 13)
            _blt_rot(S.SPEAR, x, y, self.angle)
        elif k == "axe":
            _blt_rot(S.AXE, x, y, self.spin)
        elif k == "boomerang":
            pyxel.pset(x - self.vx * 3, y - self.vy * 3, 13)
            pyxel.pset(x - self.vx * 6, y - self.vy * 6, 5)
            _blt_rot(S.BOOMERANG, x, y, self.spin)
        elif k == "shuriken":
            _blt_rot(S.SHURIKEN, x, y, self.spin)
        elif k == "fire":
            # 火柱: 赤い床 + ゆらめく炎
            age = self.maxlife - self.life
            pyxel.dither(0.5)
            pyxel.circ(x, y, self.r, P.BOSS_DARK)
            pyxel.dither(1.0)
            h = self.r + 4 + ((age // 3) % 3) * 2
            if self.life > 15 or (self.life // 3) % 2 == 0:
                pyxel.tri(x - self.r * 0.7, y, x + self.r * 0.7, y, x, y - h, P.BOSS)
                pyxel.tri(x - self.r * 0.4, y, x + self.r * 0.4, y, x + ((age // 4) % 3 - 1) * 2, y - h * 0.7, 9)
                pyxel.tri(x - self.r * 0.2, y, x + self.r * 0.2, y, x, y - h * 0.4, P.GOLD)
            # 火の粉
            for i in range(2):
                a = (age * 11 + i * 180) % 360
                pyxel.pset(x + pyxel.cos(a) * self.r * 0.6, y - (age * 1.5 + i * 7) % (h + 6), P.GOLD)
        elif k == "tower":
            # 避雷針: 範囲円 + 棒 + 先端の球。直近に感電させた敵へ稲妻
            pyxel.dither(0.25)
            pyxel.circb(x, y, self.r, P.ACCENT)
            pyxel.dither(1.0)
            pyxel.line(x, y, x, y - 14, 13)
            pyxel.rect(x - 2, y - 1, 5, 2, 13)
            pyxel.circ(x, y - 15, 2, P.GOLD if (FRAME // 3) % 2 else 7)
            for e, f in self.hit.items():
                if FRAME - f < 4 and e.alive:
                    _bolt(x, y - 15, e.x, e.y)
        elif k == "magic":
            # 尾を引く光球
            for i, rr in ((3, 1), (2, 1), (1, 2)):
                pyxel.circ(x - self.vx * i * 4.0, y - self.vy * i * 4.0, rr, 5 if i == 3 else self.col)
            pyxel.circ(x, y, 3, self.col)
            pyxel.circ(x, y, 1, 7)
            if (self.life // 2) % 2:
                pyxel.pset(x + 4, y, 7)
                pyxel.pset(x - 4, y, 7)
            else:
                pyxel.pset(x, y + 4, 7)
                pyxel.pset(x, y - 4, 7)
        elif k == "holy":
            if self.life > 20 or (self.life // 3) % 2 == 0:
                pyxel.dither(0.5)
                pyxel.circ(x, y, self.r, self.col)
                pyxel.dither(1.0)
                pyxel.circb(x, y, self.r, 7)
                # 泡
                f = self.maxlife - self.life
                for i in range(4):
                    a = (f * 7 + i * 90) % 360
                    rr = (f * 0.7 + i * 5) % self.r
                    pyxel.pset(x + pyxel.cos(a) * rr, y + pyxel.sin(a) * rr, 7)
        elif k == "hammer":
            age = self.maxlife - self.life
            # 広がる衝撃波リング → 残留する地割れ
            if age < 6:
                pyxel.circb(x, y, self.r * age / 6.0, 7)
                pyxel.circb(x, y, max(0, self.r * age / 6.0 - 3), P.GOLD)
            if self.life > 12 or (self.life // 3) % 2 == 0:
                pyxel.dither(0.4)
                pyxel.circ(x, y, self.r, self.col)
                pyxel.dither(1.0)
                # 地割れの線
                for i in range(5):
                    a = i * 72 + (int(x) * 13) % 40
                    pyxel.line(x, y, x + pyxel.cos(a) * self.r * 0.9, y + pyxel.sin(a) * self.r * 0.9, P.GOLD)
                pyxel.circb(x, y, self.r, P.GOLD)
        elif k == "sweep":
            # 鎖でつながった鎌が前方 180 度を薙ぐ
            prog = 1.0 - self.life / self.maxlife
            a = self.angle - 90 + 180 * prog
            r = self.r
            tx, ty = x + pyxel.cos(a) * r, y + pyxel.sin(a) * r
            # 残像の弧
            for i in range(1, 5):
                aa = a - i * 9
                if aa < self.angle - 90:
                    break
                pyxel.line(x + pyxel.cos(aa) * r * 0.6, y + pyxel.sin(aa) * r * 0.6,
                           x + pyxel.cos(aa) * r, y + pyxel.sin(aa) * r, 5 if i > 2 else 13)
            # 鎖 (点線)
            n = max(2, int(r / 5))
            for i in range(1, n):
                t_ = i / n
                pyxel.pset(x + (tx - x) * t_, y + (ty - y) * t_, 13 if i % 2 else 7)
            _blt_rot(S.SICKLE, tx, ty, a + 90)
        elif k == "orbit":
            pyxel.circ(x, y, self.r - 1, self.col)
            pyxel.circb(x, y, self.r - 1, 7)
            pyxel.pset(x - pyxel.cos(self.angle) * 3, y - pyxel.sin(self.angle) * 3, 7)
        elif k == "zap":
            top = y - 120
            zx = x
            for i in range(6):
                nx = x + ((i * 7 + int(y)) % 11 - 5)
                ny = top + (i + 1) * 20
                pyxel.line(zx, top + i * 20, nx, ny, 7 if self.life % 2 else 10)
                zx = nx
            pyxel.circb(x, y, self.r, 10)


def _bolt(x0, y0, x1, y1):
    """ギザギザの稲妻線。"""
    px_, py_ = x0, y0
    for i in range(1, 5):
        t_ = i / 4.0
        jx = ((int(x1) * 7 + i * 13 + FRAME) % 9 - 4) if i < 4 else 0
        jy = ((int(y1) * 5 + i * 17 + FRAME) % 9 - 4) if i < 4 else 0
        qx, qy = x0 + (x1 - x0) * t_ + jx, y0 + (y1 - y0) * t_ + jy
        pyxel.line(px_, py_, qx, qy, 7 if (FRAME + i) % 2 else P.GOLD)
        px_, py_ = qx, qy


def _blt_rot(spr, x, y, angle):
    u, v, w, h = spr
    pyxel.blt(x - w / 2, y - h / 2, 0, u, v, w, h, S.COLKEY, rotate=angle)
