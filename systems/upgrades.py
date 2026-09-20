"""レベルアップ 3 択の抽選 (設計書 4.4)。"""
import random

from core.i18n import t, tt
from data.weapons import WEAPONS, PASSIVES, MAX_WEAPON_LV, MAX_WEAPON_SLOTS, MAX_PASSIVE_SLOTS, weapon_level_desc


class Option:
    __slots__ = ("kind", "key", "name", "desc", "col", "level")

    def __init__(self, kind, key, name, desc, col, level):
        self.kind = kind      # "weapon" | "passive" | "heal" | "gold"
        self.key = key
        self.name = name
        self.desc = desc
        self.col = col
        self.level = level


def roll(player, n=3):
    pool = []   # (weight, Option)
    owned_w = {w.kind: w for w in player.weapons}
    for key, w in WEAPONS.items():
        if player.allowed is not None and key not in player.allowed:
            continue
        if key in owned_w:
            lv = owned_w[key].level
            if lv < MAX_WEAPON_LV:
                pool.append((3, Option("weapon", key, tt(w["name"]), weapon_level_desc(key, lv + 1), w["col"], lv + 1)))
        elif len(player.weapons) < player.max_weapon_slots:
            pool.append((2, Option("weapon", key, tt(w["name"]), tt(w["desc"]), w["col"], 1)))
    for key, p in PASSIVES.items():
        lv = player.passives.get(key, 0)
        if lv > 0:
            if lv < p["max"]:
                pool.append((3, Option("passive", key, tt(p["name"]), tt(p["desc"]), p["col"], lv + 1)))
        elif len(player.passives) < getattr(player, "max_passive_slots", MAX_PASSIVE_SLOTS):
            pool.append((2, Option("passive", key, tt(p["name"]), tt(p["desc"]), p["col"], 1)))

    out = []
    while pool and len(out) < n:
        total = sum(w for w, _ in pool)
        r = random.uniform(0, total)
        for i, (w, opt) in enumerate(pool):
            r -= w
            if r <= 0:
                out.append(opt)
                pool.pop(i)
                break
    while len(out) < n:
        out.append(Option("heal", "heal", t("lv.potion"), t("lv.potion.desc"), 8, 0))
    return out


def apply(player, opt):
    if opt.kind == "weapon":
        player.add_weapon(opt.key)
    elif opt.kind == "passive":
        player.add_passive(opt.key)
    elif opt.kind == "heal":
        player.hp = min(player.maxhp, player.hp + 30)
