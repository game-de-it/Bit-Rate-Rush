import random

import pyxel

from core import audio
from entities.particle import Particle
from entities.pickup import Pickup
from config import MAX_PARTICLES, MAX_PICKUPS

COIN_VALUE = {"bat": 2, "zombie": 3, "ghost": 4, "skull": 8, "brute": 20}


def bullets_vs_enemies(world):
    grid = world.grid
    frame = world.frame
    for b in world.bullets:
        if not b.alive or b.delay > 0:
            continue
        r = b.r
        bx, by = b.x, b.y
        tick = b.tick
        sweep = b.kind == "sweep"
        if sweep:
            fx, fy = pyxel.cos(b.angle), pyxel.sin(b.angle)
        for e in grid.nearby(bx, by, r + 16):
            if not e.alive:
                continue
            dx = e.x - bx
            dy = e.y - by
            rr = r + e.r
            if dx * dx + dy * dy >= rr * rr:
                continue
            if sweep and dx * fx + dy * fy < 0:      # 後方の敵には当たらない
                continue
            if tick:
                last = b.hit.get(e)
                if last is not None and frame - last < tick:
                    continue
                b.hit[e] = frame
            else:
                if e in b.hit:
                    continue
                b.hit.add(e)
            _damage(world, e, b.dmg, dx, dy, b.kb)
            if b.pierce > 0:
                b.pierce -= 1
                if b.pierce == 0:
                    b.alive = False
                    break


def damage(world, e, dmg, dx, dy, kb):
    _damage(world, e, dmg, dx, dy, kb)


def _damage(world, e, dmg, dx, dy, kb):
    e.hp -= dmg
    e.flash = 4
    if kb and not e.boss:
        d = (dx * dx + dy * dy) ** 0.5 or 1.0
        e.kx += dx / d * kb
        e.ky += dy / d * kb
    if len(world.particles) < MAX_PARTICLES:
        world.particles.append(Particle(e.x, e.y, random.uniform(-1, 1), random.uniform(-1, 1), 8, 7))
    if e.hp <= 0:
        e.alive = False
        world.on_enemy_killed(e)
        audio.se(audio.SE_KILL if e.boss or random.random() < 0.3 else audio.SE_HIT)
        for _ in range(4):
            if len(world.particles) < MAX_PARTICLES:
                world.particles.append(Particle(e.x, e.y, random.uniform(-2, 2), random.uniform(-2, 2), 14, 8))
        _drop(world, e)
    elif random.random() < 0.2:
        audio.se(audio.SE_HIT)


def _drop(world, e):
    pickups = world.pickups
    roll = random.random()
    if roll < 0.004:
        pickups.append(Pickup("heal", e.x, e.y))
    elif roll < 0.006:
        pickups.append(Pickup("magnet", e.x, e.y))
    if len(pickups) >= MAX_PICKUPS:
        _merge_gems(world)
    pickups.append(Pickup("xp", e.x, e.y, e.xp))
    # お金: 雑魚 15%、ボス確定
    if e.boss:
        pickups.append(Pickup("coin", e.x + 6, e.y, 300))
    elif random.random() < 0.15:
        pickups.append(Pickup("coin", e.x + random.uniform(-6, 6), e.y + random.uniform(-6, 6), COIN_VALUE.get(e.kind, 2)))


def _merge_gems(world):
    """ジェムが溢れたら、プレイヤーから最も遠い XP ジェムを最も近いジェムに合算して消す。"""
    p = world.player
    gems = [g for g in world.pickups if g.kind == "xp"]
    if len(gems) < 2:
        return
    far = max(gems, key=lambda g: (g.x - p.x) ** 2 + (g.y - p.y) ** 2)
    near = min(gems, key=lambda g: (g.x - p.x) ** 2 + (g.y - p.y) ** 2)
    near.value += far.value
    far.alive = False
    world.pickups = [g for g in world.pickups if g.alive]


def enemies_vs_player(world):
    p = world.player
    if p.inv > 0:
        return
    for e in world.grid.nearby(p.x, p.y, p.R + 16):
        if not e.alive:
            continue
        dx = e.x - p.x
        dy = e.y - p.y
        rr = e.r + p.R
        if dx * dx + dy * dy < rr * rr:
            if p.hurt(e.dmg):
                audio.se(audio.SE_HURT)
                world.shake = 4
            return


def enemy_bullets_vs_player(world):
    p = world.player
    if p.inv > 0:
        return
    px, py = p.x, p.y
    for b in world.enemy_bullets:
        if not b.alive:
            continue
        dx = b.x - px
        dy = b.y - py
        rr = b.r + p.R
        if dx * dx + dy * dy < rr * rr:
            b.alive = False
            if p.hurt(b.dmg):
                audio.se(audio.SE_HURT)
                world.shake = 4
            return
