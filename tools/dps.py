"""武器・魔法の DPS 計測 (ヘッドレス実測)。

    python3 tools/dps.py [--lv 8] [--might 5] [--haste 5] [--dup 2] [--sec 15]

2 シナリオを実測する:
  single: プレイヤー静止 (右向き)、右 40px に不動のボス型ダミー 1 体 → 単体 DPS
  crowd : 半径 100px 内に不動の雑魚型ダミー 80 体 → 範囲 DPS (合計ダメージ / 秒)
ファイヤーウォールは移動しないと火柱が出ないので、single ではプレイヤーが左右 24px を往復する。
結果を Markdown で標準出力へ出す。
"""
import argparse
import math
import os
import random
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pyxel

from config import W, H
pyxel.init(W, H, headless=True)

from game import Game
from scenes.play import PlayScene
from scenes.levelup import LevelUpScene
from data.weapons import WEAPONS, weapon_stats
from data.enemies import ENEMIES
from entities.enemy import Enemy

ap = argparse.ArgumentParser()
ap.add_argument("--lv", type=int, default=8)
ap.add_argument("--might", type=int, default=5)
ap.add_argument("--haste", type=int, default=5)
ap.add_argument("--dup", type=int, default=2)
ap.add_argument("--sec", type=int, default=15)
args = ap.parse_args()
FRAMES = args.sec * 60


def make_play(g, kind):
    play = PlayScene(g, start_weapons=[kind])
    g.replace(play)
    p = play.player
    p.base_maxhp = p.maxhp = p.hp = 10 ** 9
    for _ in range(args.lv - 1):
        p.weapons[0].level_up()
    for _ in range(args.might):
        p.add_passive("might")
    for _ in range(args.haste):
        p.add_passive("cooldown")
    for _ in range(args.dup):
        p.add_passive("amount")
    play.no_levelup = True
    play.spawner.update = lambda t: None       # 通常の敵は湧かせない
    return play


def dummy(play, kind, x, y):
    e = Enemy(kind, x, y)
    e.hp = e.maxhp = 10 ** 9
    e.spd = 0.0
    e.dmg = 0
    e.shoot_cd = 10 ** 9
    e.summon_cd = 10 ** 9
    e.dash_cd = 10 ** 9
    play.enemies.append(e)
    return e


def run(play, frames, move=None):
    g = play.game
    g.input.poll = lambda: None
    g.input.mx, g.input.my = 0.0, 0.0
    p = play.player
    for i in range(frames):
        if move:
            g.input.mx, g.input.my = move(i)
        else:
            p.fx, p.fy = 1.0, 0.0
        g.update()
        if isinstance(g.stack[-1], LevelUpScene):
            g.pop()


def measure(kind):
    random.seed(1)
    g = Game()
    # --- single ---
    play = make_play(g, kind)
    p = play.player
    e = dummy(play, "boss1", p.x + 40, p.y)
    hp0 = e.hp
    if kind == "fire":
        run(play, FRAMES, move=lambda i: (1.0 if (i // 16) % 2 == 0 else -1.0, 0.0))
    else:
        run(play, FRAMES)
    single = (hp0 - e.hp) / args.sec
    # --- crowd ---
    play = make_play(g, kind)
    p = play.player
    ds = []
    for i in range(80):
        a = random.uniform(0, 360)
        r = random.uniform(20, 100)
        ds.append(dummy(play, "bat", p.x + pyxel.cos(a) * r, p.y + pyxel.sin(a) * r))
    hp0 = sum(d.hp for d in ds)
    if kind == "fire":
        run(play, FRAMES, move=lambda i: (1.0 if (i // 16) % 2 == 0 else -1.0, 0.0))
    else:
        run(play, FRAMES)
    crowd = (hp0 - sum(d.hp for d in ds)) / args.sec
    return single, crowd


might = 1 + 0.1 * args.might
rows = []
for kind, w in WEAPONS.items():
    st = weapon_stats(kind, args.lv)
    per_hit = st["dmg"] * might
    single, crowd = measure(kind)
    rows.append((kind, w["cls"], w["name"][0], per_hit, single, crowd))

print(f"## DPS 実測 (Lv{args.lv}, 剛力{args.might} = x{might:.1f}, 疾風{args.haste} = CD x{1 - 0.08 * args.haste:.2f}, 分身{args.dup}, {args.sec}秒計測)\n")
print("| 武器 | 種別 | 1ヒット | 単体DPS | 範囲DPS (80体) |")
print("|---|---|---:|---:|---:|")
for kind, cls, name, per_hit, single, crowd in sorted(rows, key=lambda r: -r[4]):
    print(f"| {name} ({kind}) | {'魔' if cls == 'magic' else '物'} | {per_hit:.0f} | {single:.0f} | {crowd:.0f} |")

# --- 撃破に必要なヒット数・秒数 ---
print("\n## 敵を倒すのに必要なヒット数 / 秒数 (単体DPS 基準)\n")
targets = []
for t_sec, label in ((0, "0:00"), (300, "5:00"), (600, "10:00")):
    mult = 1 + t_sec / 120.0
    bmult = 1 + t_sec / 400.0
    for ek, ed in ENEMIES.items():
        if ed.get("boss"):
            if (ek == "boss1" and t_sec == 300) or (ek == "boss2" and t_sec == 600):
                targets.append((f"{ek} @{label}", int(ed["hp"] * bmult)))
        elif t_sec in (0, 300, 600):
            targets.append((f"{ek} @{label}", int(ed["hp"] * mult)))
header = "| 武器 | " + " | ".join(n for n, _ in targets) + " |"
print(header)
print("|---|" + "---:|" * len(targets))
print("| (HP) | " + " | ".join(str(hp) for _, hp in targets) + " |")
for kind, cls, name, per_hit, single, crowd in sorted(rows, key=lambda r: -r[4]):
    cells = []
    for _, hp in targets:
        hits = math.ceil(hp / per_hit) if per_hit > 0 else 0
        secs = hp / single if single > 0 else float("inf")
        cells.append(f"{hits}発/{secs:.1f}s" if secs < 999 else "-")
    print(f"| {name} | " + " | ".join(cells) + " |")
