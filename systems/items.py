"""ラン中の消耗アイテム使用。"""
import random

from core import audio
from data.items import ITEMS
from entities.particle import Particle
from config import MAX_PARTICLES


def update(world):
    """入力を見て選択 / 使用。"""
    p = world.player
    inp = world.inp
    if not p.items:
        return
    if inp.l:
        p.item_cursor = (p.item_cursor - 1) % len(p.items)
        audio.se(audio.SE_SELECT)
    if inp.r:
        p.item_cursor = (p.item_cursor + 1) % len(p.items)
        audio.se(audio.SE_SELECT)
    if inp.use:
        use(world, p.item_cursor)


def use(world, idx):
    p = world.player
    if idx >= len(p.items):
        return False
    kind = p.items[idx]
    if kind == "charm" and p.shield > 0:
        return False
    ok = _apply(world, kind)
    if not ok:
        return False
    p.items.pop(idx)
    p.item_cursor = min(p.item_cursor, max(0, len(p.items) - 1))
    audio.se(audio.SE_LEVELUP)
    return True


def _apply(world, kind):
    p = world.player
    if kind == "herb":
        if p.hp >= p.maxhp:
            return False
        p.hp = min(p.maxhp, p.hp + 40)
    elif kind == "elixir":
        if p.hp >= p.maxhp:
            return False
        p.hp = p.maxhp
    elif kind == "bomb":
        _damage_all(world, 50, screen_only=True)
        world.shake = 8
    elif kind == "arrow":
        best = None
        for e in world.enemies:
            if e.alive and (best is None or e.hp > best.hp):
                best = e
        if best is None:
            return False
        from systems.collision import damage
        damage(world, best, 500, 0, -1, 0)
        world.shake = 4
    elif kind == "magnet":
        p.magnet_pending = True
    elif kind == "charm":
        p.shield = 300
    elif kind == "tome":
        p.xp = p.xp_next
    return True


def _damage_all(world, dmg, screen_only=True):
    from systems.collision import damage
    cx, cy = world.cam_x, world.cam_y
    for e in list(world.enemies):
        if not e.alive:
            continue
        if screen_only and not (cx - 8 < e.x < cx + 328 and cy - 8 < e.y < cy + 248):
            continue
        damage(world, e, dmg, 0, -1, 0)
        if len(world.particles) < MAX_PARTICLES:
            world.particles.append(Particle(e.x, e.y, random.uniform(-2, 2), random.uniform(-2, 2), 12, 9))
