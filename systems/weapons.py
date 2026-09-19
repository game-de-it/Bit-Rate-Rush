"""武器ごとの発射ロジック。WeaponState.cd を減らし、0 になったら弾を生成する。

- 一斉発射 (弓): amount 本を扇状に同時に出す
- 連射 (槍・鎖鎌・斧・魔法弾・聖水・雷): amount 回を数フレームおきに出す
- ナイフ: マシンガン型。cd を本数で割った間隔で 1 本ずつ途切れなく投げ続ける (本数が増える = 連射が速くなる)
- ハンマー: 衝撃波を length 区画ぶん進行方向へ順に出す。amount (Duplicator は非加算) が 2 以上なら後方にも
- 衛星: 常時展開
"""
import random

import pyxel

from config import MAX_BULLETS
from data.weapons import WEAPONS
from entities.bullet import Bullet
from core import audio

VOLLEY = ("bow", "shuriken")       # 一斉発射する武器
BURST_GAP = {"spear": 6, "boomerang": 8, "tower": 10, "sickle": 8, "axe": 5, "magic": 5, "holy": 5, "zap": 5}


def update(world):
    player = world.player
    bullets = world.bullets
    for ws in player.weapons:
        k = ws.kind
        if k == "orbit":
            _update_orbit(world, ws)
            continue
        if ws.burst > 0:
            ws.burst_t -= 1
            if ws.burst_t <= 0:
                ws.burst_t = BURST_GAP.get(k, 5)
                ws.burst -= 1
                if len(bullets) < MAX_BULLETS:
                    _fire_one(world, ws)
            continue
        ws.cd -= 1
        if ws.cd <= 0:
            st = ws.stats
            n = _amount(ws, player)
            if k == "knife":
                # 1 サイクル (cd) を本数で等分した間隔で 1 本ずつ
                ws.cd = max(3, int(st["cd"] * player.cooldown / n))
                if len(bullets) < MAX_BULLETS:
                    _fire_one(world, ws)
                continue
            if k == "fire":
                ws.cd = max(6, int(st["cd"] * player.cooldown))
                if len(bullets) < MAX_BULLETS:
                    _fire_trail(world, ws)
                continue
            if k == "hammer":
                # 最後の衝撃波が消えてから cd (1 秒) 後に次を振る。疾風は無視
                ws.cd = (st["length"] - 1) * 4 + st["dur"] + st["cd"]
            elif WEAPONS[k].get("fixed_cd"):
                ws.cd = st["cd"]
            else:
                ws.cd = max(8, int(st["cd"] * player.cooldown))
            if k in VOLLEY:
                if len(bullets) < MAX_BULLETS:
                    _fire_volley(world, ws, n)
            elif k == "hammer":
                if len(bullets) < MAX_BULLETS:
                    _fire_hammer(world, ws)
            else:
                ws.burst = n
                ws.burst_t = 0


def _amount(ws, player):
    n = ws.stats["amount"]
    if WEAPONS[ws.kind].get("dup", True):
        n += player.extra_amount
    return n


def _facing(p):
    fx, fy = p.fx, p.fy
    d = (fx * fx + fy * fy) ** 0.5 or 1.0
    return fx / d, fy / d


def _fire_volley(world, ws, n):
    """扇状に n 本を同時発射 (ナイフ・弓)。"""
    k = ws.kind
    st = ws.stats
    p = world.player
    dmg = st["dmg"] * p.might
    col = WEAPONS[k]["col"]
    fx, fy = _facing(p)
    base = pyxel.atan2(fy, fx)
    spread = st.get("spread", 8)
    life = 120 if k == "bow" else max(6, int(st["range"] / st["speed"]))
    for i in range(n):
        off = (i - (n - 1) / 2.0) * spread + random.uniform(-2, 2)
        a = base + off
        vx, vy = pyxel.cos(a) * st["speed"], pyxel.sin(a) * st["speed"]
        world.bullets.append(Bullet(k, p.x, p.y, dmg, st["r"], col, life=life,
                                    vx=vx, vy=vy, pierce=st["pierce"], kb=st["kb"]))


def _fire_hammer(world, ws):
    st = ws.stats
    p = world.player
    dmg = st["dmg"] * p.might
    col = WEAPONS["hammer"]["col"]
    fx, fy = _facing(p)
    dirs = [(fx, fy)]
    if st["amount"] >= 2:
        dirs.append((-fx, -fy))
    for dx, dy in dirs:
        for i in range(st["length"]):
            d = 18 + i * st["step"]
            r = st["r"] * 1.5 if i == 0 else st["r"]      # 振り下ろし地点 (1 発目) だけ大きい
            world.bullets.append(Bullet("hammer", p.x + dx * d, p.y + dy * d, dmg, r, col,
                                        life=st["dur"], pierce=-1, kb=st["kb"], tick=st["tick"], delay=i * 4))
    audio.se(audio.SE_HIT)
    world.shake = max(world.shake, 2)


def _fire_trail(world, ws):
    """ファイヤーウォール: 足元に火柱。前回と同じ場所には置かない。"""
    st = ws.stats
    p = world.player
    if ws.last is not None:
        lx, ly = ws.last
        if (p.x - lx) ** 2 + (p.y - ly) ** 2 < 64:
            return
    ws.last = (p.x, p.y)
    world.bullets.append(Bullet("fire", p.x, p.y + 2, st["dmg"] * p.might, st["r"], WEAPONS["fire"]["col"],
                                life=st["dur"], pierce=-1, tick=st["tick"]))


def _fire_one(world, ws):
    k = ws.kind
    st = ws.stats
    p = world.player
    dmg = st["dmg"] * p.might
    col = WEAPONS[k]["col"]
    if k == "knife":
        fx, fy = _facing(p)
        a = pyxel.atan2(fy, fx) + random.uniform(-st["spread"], st["spread"])
        ox, oy = -fy * random.uniform(-2, 2), fx * random.uniform(-2, 2)
        b = Bullet("knife", p.x + ox, p.y + oy, dmg, st["r"], col, life=140,
                   vx=pyxel.cos(a) * st["speed"], vy=pyxel.sin(a) * st["speed"], pierce=st["pierce"], kb=st["kb"])
        world.bullets.append(b)
    elif k == "spear":
        fx, fy = _facing(p)
        life = max(4, int(st["reach"] / st["speed"]))
        # 槍の「貫通 N」は N 体を突き抜けて N+1 体目で止まる (ヒット数は pierce+1)
        b = Bullet("spear", p.x + fx * 6, p.y + fy * 6, dmg, st["r"], col, life=life,
                   vx=fx * st["speed"], vy=fy * st["speed"], pierce=st["pierce"] + 1, kb=0.0)
        world.bullets.append(b)
    elif k == "boomerang":
        fx, fy = _facing(p)
        # 連射の偶奇で左右どちらに回るかを変える
        sign = 1 if ws.burst % 2 == 0 else -1
        b = Bullet("boomerang", p.x, p.y, dmg, st["r"], col, life=st["life"],
                   vx=fx * st["speed"], vy=fy * st["speed"], pierce=-1, kb=st["kb"], tick=st["tick"])
        b.rot = st["turn"] * sign
        world.bullets.append(b)
    elif k == "tower":
        fx, fy = _facing(p)
        # 常に 1 本だけ。新しく立てたら前のは消える
        for old in world.bullets:
            if old.kind == "tower":
                old.alive = False
        ws.burst = 0
        b = Bullet("tower", p.x + fx * 24, p.y + fy * 24, dmg, st["r"], col,
                   life=st["dur"], pierce=-1, tick=st["tick"])
        world.bullets.append(b)
        audio.se(audio.SE_ZAP)
    elif k == "sickle":
        fx, fy = _facing(p)
        b = Bullet("sweep", p.x, p.y, dmg, st["r"], col, life=st["dur"], pierce=-1, kb=st["kb"], tick=999)
        b.angle = pyxel.atan2(fy, fx)
        world.bullets.append(b)
    elif k == "magic":
        tgt = world.nearest_enemy(p.x, p.y, st["range"])
        if tgt is None:
            ws.burst = 0
            return
        dx, dy = tgt.x - p.x, tgt.y - p.y
        d = (dx * dx + dy * dy) ** 0.5 or 1.0
        b = Bullet("magic", p.x, p.y, dmg, st["r"], col, life=180,
                   vx=dx / d * st["speed"], vy=dy / d * st["speed"], pierce=st["pierce"], kb=st["kb"])
        world.bullets.append(b)
    elif k == "axe":
        sx = 1 if p.fx >= 0 else -1
        b = Bullet("axe", p.x, p.y - 4, dmg, st["r"], col, life=270,
                   vx=sx * random.uniform(0.27, 0.6), vy=-1.85, pierce=-1, kb=st["kb"])
        world.bullets.append(b)
    elif k == "holy":
        ang = random.uniform(0, 360)
        dist = random.uniform(20, 60)
        b = Bullet("holy", p.x + pyxel.cos(ang) * dist, p.y + pyxel.sin(ang) * dist, dmg, st["r"], col,
                   life=st["dur"], pierce=-1, tick=st["tick"])
        world.bullets.append(b)
    elif k == "zap":
        cands = world.enemies_within(p.x, p.y, st["range"])
        if not cands:
            ws.burst = 0
            return
        e = random.choice(cands)
        b = Bullet("zap", e.x, e.y, dmg, st["r"], col, life=8, pierce=-1, tick=999)
        world.bullets.append(b)
        audio.se(audio.SE_ZAP)


def _update_orbit(world, ws):
    st = ws.stats
    p = world.player
    n = st["amount"] + p.extra_amount
    if len(ws.orbits) != n:
        for b in ws.orbits:
            b.alive = False
        ws.orbits = []
        for i in range(n):
            b = Bullet("orbit", p.x, p.y, st["dmg"], st["r"], WEAPONS["orbit"]["col"], life=1, pierce=-1, tick=st["tick"])
            b.angle = 360.0 * i / n
            b.dist = st["dist"]
            ws.orbits.append(b)
            world.bullets.append(b)
    for b in ws.orbits:
        b.dmg = st["dmg"] * p.might
        b.r = st["r"]
        b.rot = st["rot"]
        if pyxel.frame_count % 120 == 0:
            b.hit = {e: f for e, f in b.hit.items() if e.alive}
