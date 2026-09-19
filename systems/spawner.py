import random

from config import MAX_ENEMIES, W, H
from data.waves import WAVES as WAVE_TABLES
from entities.enemy import Enemy


class Spawner:
    def __init__(self, world, waves="survival", base_mult=1.0, ramp=120.0):
        self.world = world
        self.waves = WAVE_TABLES[waves]
        self.acc = [0.0] * len(self.waves)
        self.done = [False] * len(self.waves)
        self.base_mult = base_mult    # 依頼ごとの基礎倍率
        self.ramp = ramp              # 敵 HP が (1 + t/ramp) 倍になる
        self.hp_mult = base_mult
        self.boss_hp_mult = 1.0
        self.rate_mult = 1.0          # 出現数の倍率 (ラッシュで 2 倍)
        self.wave_time_cap = None     # ボーナスラッシュ中: ウェーブ表の時刻をここで止める (制限時間後も湧かせる)

    def update(self, t_sec):
        world = self.world
        enemies = world.enemies
        self.hp_mult = self.base_mult * (1.0 + t_sec / self.ramp)
        self.boss_hp_mult = 1.0 + t_sec / 400.0
        wt = t_sec if self.wave_time_cap is None else min(t_sec, self.wave_time_cap)
        counts = {}
        for e in enemies:
            counts[e.kind] = counts.get(e.kind, 0) + 1
        total = len(enemies)
        for i, w in enumerate(self.waves):
            if w[1] == "boss":
                if not self.done[i] and wt >= w[0]:
                    self.done[i] = True
                    self.spawn_boss(w[2])
                continue
            start, end, kind, rate, cap = w
            if wt < start or wt >= end:
                continue
            self.acc[i] += rate * self.rate_mult / 60.0
            cap = int(cap * self.rate_mult)
            while self.acc[i] >= 1.0:
                self.acc[i] -= 1.0
                if counts.get(kind, 0) < cap and total < MAX_ENEMIES:
                    self.spawn(kind)
                    counts[kind] = counts.get(kind, 0) + 1
                    total += 1

    def spawn_pos(self):
        """カメラ矩形の外周 +16〜48px のランダム点。"""
        cx, cy = self.world.cam_x, self.world.cam_y
        m = random.randint(16, 48)
        side = random.randint(0, 3)
        if side == 0:
            return cx - m, cy + random.uniform(-m, H + m)
        if side == 1:
            return cx + W + m, cy + random.uniform(-m, H + m)
        if side == 2:
            return cx + random.uniform(-m, W + m), cy - m
        return cx + random.uniform(-m, W + m), cy + H + m

    def spawn(self, kind, x=None, y=None):
        if x is None:
            x, y = self.spawn_pos()
        e = Enemy(kind, x, y)
        e.hp = e.maxhp = int(e.hp * (self.boss_hp_mult if e.boss else self.hp_mult))
        self.world.enemies.append(e)
        return e

    def spawn_boss(self, kind):
        e = self.spawn(kind)
        self.world.on_boss_spawn(e)
        return e
