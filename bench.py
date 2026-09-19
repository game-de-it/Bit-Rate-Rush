"""実機負荷計測用の自動プレイ。

    python3 bench.py [stress|run] [seconds]

stress: 敵 150 体 (HP 50 倍) を即湧かせて上限負荷を測る
run   : 通常のウェーブ表で自動プレイ (無敵・円運動・アップグレード自動選択)
5 秒ごとに stdout へ統計を出し、指定秒数で終了する。
"""
import math
import os
import random
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pyxel

from config import W, H, FPS

MODE = sys.argv[1] if len(sys.argv) > 1 else "stress"
DURATION = float(sys.argv[2]) if len(sys.argv) > 2 else 40.0

pyxel.init(W, H, title="Bit-Rate-Rush bench", fps=FPS, quit_key=pyxel.KEY_NONE)
pyxel.perf_monitor(True)

from game import Game
from scenes.play import PlayScene
from scenes.levelup import LevelUpScene
from scenes.result import ResultScene
from systems import upgrades
import data.enemies as DE


class Bench:
    def __init__(self):
        random.seed(7)
        self.g = Game()
        self.play = PlayScene(self.g)
        self.g.replace(self.play)
        p = self.play.player
        p.base_maxhp = p.maxhp = p.hp = 10 ** 9
        if MODE == "stress":
            for d in DE.ENEMIES.values():
                d["hp"] *= 50
            for k in ["magic", "axe", "holy", "orbit", "zap"]:
                p.add_weapon(k)
            for w in p.weapons:
                for _ in range(3):
                    w.level_up()
            for _ in range(150):
                ang = random.uniform(0, 360)
                d = random.uniform(30, 150)
                self.play.spawner.spawn(random.choice(["bat", "zombie", "ghost", "brute"]),
                                        pyxel.cos(ang) * d, pyxel.sin(ang) * d)
            self.play.frame = 60 * 250
        orig = self.g.input.poll

        def poll():
            orig()
            a = self.n_upd * 0.01   # ゆっくり大きな円を描いて歩く
            self.g.input.mx, self.g.input.my = math.cos(a), math.sin(a)
        self.g.input.poll = poll

        self.t_start = time.perf_counter()
        self.t_win = self.t_start
        self.n_upd = self.n_draw = 0
        self.w_upd = self.w_draw = 0
        self.s_upd = self.s_draw = 0.0
        self.mx_upd = self.mx_draw = 0.0
        self.mx_frame = 0.0
        self.t_last = self.t_start
        print(f"[bench] mode={MODE} {W}x{H}@{FPS} duration={DURATION}s", flush=True)

    def update(self):
        now = time.perf_counter()
        self.mx_frame = max(self.mx_frame, now - self.t_last)
        self.t_last = now
        t0 = time.perf_counter()
        top = self.g.stack[-1]
        if isinstance(top, LevelUpScene):
            upgrades.apply(self.play.player, random.choice(top.options))
            self.g.pop()
        elif isinstance(top, ResultScene):
            print(f"[bench] result win={top.win}", flush=True)
            self.report(final=True)
            pyxel.quit()
            return
        else:
            self.g.update()
        dt = time.perf_counter() - t0
        self.n_upd += 1
        self.w_upd += 1
        self.s_upd += dt
        self.mx_upd = max(self.mx_upd, dt)
        if now - self.t_win >= 5.0:
            self.report()
        if now - self.t_start >= DURATION:
            self.report(final=True)
            pyxel.quit()

    def draw(self):
        t0 = time.perf_counter()
        self.g.draw()
        dt = time.perf_counter() - t0
        self.n_draw += 1
        self.w_draw += 1
        self.s_draw += dt
        self.mx_draw = max(self.mx_draw, dt)

    def report(self, final=False):
        now = time.perf_counter()
        el = now - self.t_win
        if el <= 0 or self.w_upd == 0:
            return
        pl = self.play
        print(f"[bench] t={now - self.t_start:5.1f}s fps(draw)={self.w_draw / el:5.1f} ups={self.w_upd / el:5.1f} "
              f"upd={self.s_upd / self.w_upd * 1000:5.2f}ms(max {self.mx_upd * 1000:5.2f}) "
              f"draw={self.s_draw / max(1, self.w_draw) * 1000:5.2f}ms(max {self.mx_draw * 1000:5.2f}) "
              f"frame_max={self.mx_frame * 1000:5.1f}ms "
              f"enemies={len(pl.enemies)} bullets={len(pl.bullets)} gems={len(pl.pickups)} lv={pl.player.level}"
              + (" FINAL" if final else ""), flush=True)
        self.t_win = now
        self.w_upd = self.w_draw = 0
        self.s_upd = self.s_draw = 0.0
        self.mx_upd = self.mx_draw = self.mx_frame = 0.0


b = Bench()
pyxel.run(b.update, b.draw)
