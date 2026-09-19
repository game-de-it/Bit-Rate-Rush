import pyxel

from config import W, H
from core import palette as P
from data.weapons import WEAPONS, PASSIVES
from data.items import ITEMS, MAX_ITEMS
from ui import font, icons
from core.i18n import t, tt
from data.enemies import ENEMIES


def draw(world):
    p = world.player
    pyxel.camera()
    # XP バー (最上段)
    pyxel.rect(0, 0, W, 6, P.PANEL)
    ratio = min(1.0, p.xp / p.xp_next)
    pyxel.rect(0, 0, int(W * ratio), 6, P.ACCENT)
    pyxel.rectb(0, 0, W, 6, 5)
    font.text(3, 8, f"LV {p.level}", 7)

    # HP バー (左上)
    pyxel.rect(3, 21, 82, 8, P.PANEL)
    hp_ratio = max(0.0, p.hp / p.maxhp)
    pyxel.rect(4, 22, int(80 * hp_ratio), 6, P.HP if hp_ratio > 0.3 else P.GOLD)
    pyxel.rectb(3, 21, 82, 8, 5)
    font.text(88, 20, f"{max(0, int(p.hp))}/{p.maxhp}", 7)

    # タイマー (中央上) — 依頼中は残り時間
    if world.time_limit:
        left = max(0, world.time_limit - world.frame) // 60
        rush = getattr(world, "final_rush", False)
        font.center(8, f"{t('run.left')} {left // 60:02d}:{left % 60:02d}", P.HP if (left <= 30 or rush) else 7)
        if rush and (world.frame // 20) % 2 == 0:
            msg = t("run.bonus").format(world.bonus_rush) if getattr(world, "bonus_rush", 0) else t("run.rush")
            ry = 62 if world.cleared else 46
            tw = font.width(msg) + 16
            pyxel.rect(W // 2 - tw // 2, ry - 2, tw, 14, P.PANEL)
            pyxel.rectb(W // 2 - tw // 2, ry - 2, tw, 14, P.HP)
            font.center(ry, msg, P.HP)
    else:
        sec = world.frame // 60
        font.center(8, f"{sec // 60:02d}:{sec % 60:02d}", 7)

    # キル数・所持金 (右上)
    font.right(8, f"{t('hud.kill')} {p.kills}", 7)
    if world.quest:
        font.right(20, f"{world.gold} {t('hud.gold')}", P.GOLD)
        # 依頼進捗
        q = world.quest
        if q["kind"] == "kill":
            n = world.kill_count.get(q["target"], 0)
            s = f"{tt(ENEMIES[q['target']]['name'])} {min(n, q['count'])}/{q['count']}"
            font.center(32, s, P.ACCENT if n < q["count"] else P.GOLD)
        if world.cleared:
            if world.clear_flash > 0 and (world.clear_flash // 8) % 2 == 0:
                pyxel.rect(W // 2 - 90, 46, 180, 14, P.PANEL)
                pyxel.rectb(W // 2 - 90, 46, 180, 14, P.GOLD)
                font.center(48, t("run.cleared"), P.GOLD)
            elif world.clear_flash <= 0:
                font.center(46, t("run.cleared"), 13)

    # 武器 / パッシブ (左下)
    box = 18
    y = H - box * 2 - 6
    x = 3
    for w in p.weapons:
        pyxel.rect(x, y, box, box, P.PANEL)
        pyxel.rectb(x, y, box, box, 7)
        icons.draw(w.kind, x + 1, y + 1, WEAPONS[w.kind]["col"])
        s = str(w.level)
        pyxel.rect(x + box - font.width(s) - 2, y + box - 9, font.width(s) + 2, 9, P.OUTLINE)
        font.text(x + box - font.width(s) - 1, y + box - 10, s, P.GOLD)
        x += box + 2
    y += box + 2
    x = 3
    for k, lv in p.passives.items():
        pyxel.rect(x, y, box, box, P.PANEL)
        pyxel.rectb(x, y, box, box, 5)
        icons.draw(k, x + 1, y + 1, PASSIVES[k]["col"])
        s = str(lv)
        pyxel.rect(x + box - font.width(s) - 2, y + box - 9, font.width(s) + 2, 9, P.OUTLINE)
        font.text(x + box - font.width(s) - 1, y + box - 10, s, P.GOLD)
        x += box + 2

    # アイテム枠 (右下): L/R で選択、Y で使用
    if world.quest:
        box = 18
        x0 = W - 3 - MAX_ITEMS * (box + 2)
        y = H - box - 4
        for i in range(MAX_ITEMS):
            x = x0 + i * (box + 2)
            pyxel.rect(x, y, box, box, P.PANEL)
            if i < len(p.items):
                it = ITEMS[p.items[i]]
                icons.draw(f"item_{p.items[i]}", x + 1, y + 1, it["col"])
            sel = p.items and i == p.item_cursor
            pyxel.rectb(x, y, box, box, P.GOLD if sel else 5)
        if p.items:
            font.right(y - 12, tt(ITEMS[p.items[p.item_cursor]]["name"]), 7, W - 3)

    # ボス HP バー (下部中央)
    boss = world.boss
    if boss is not None and boss.alive:
        bw = 160
        bx = (W - bw) // 2
        pyxel.rect(bx, H - 12, bw, 7, P.PANEL)
        pyxel.rect(bx + 1, H - 11, int((bw - 2) * max(0, boss.hp) / boss.maxhp), 5, P.BOSS)
        pyxel.rectb(bx, H - 12, bw, 7, 7)
        font.center(H - 24, t("hud.boss"), P.BOSS)
