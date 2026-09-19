"""依頼ごとの敵出現仕様を表にする。
    python3 tools/waves_report.py  > docs/WAVES.md
各ウェーブ行の「見込み数」= 秒間出現数 × 継続秒 (同時上限で頭打ちになるので実数はこれ以下)。
XP/秒 = Σ(秒間出現数 × その敵の XP)。倒しきった場合の経験値の入り方の目安。"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.quests import QUESTS
from data.waves import WAVES
from data.enemies import ENEMIES
from data.chapters import CHAPTERS


def fmt_time(s):
    return f"{s // 60}:{s % 60:02d}"


print("# 依頼ごとの敵出現仕様\n")
print("`python3 tools/waves_report.py` の出力。値は `data/quests.py` / `data/waves.py` / `data/enemies.py`。\n")
print("| 敵 | HP | 速度 | 攻撃 | XP |")
print("|---|---:|---:|---:|---:|")
for k, e in ENEMIES.items():
    print(f"| {e['name'][0]} ({k}) | {e['hp']} | {e['spd']} | {e['dmg']} | {e['xp']} |")
print()

for ch in sorted(CHAPTERS):
    print(f"## {ch} 章 {CHAPTERS[ch]['title'][0]}\n")
    for qid, q in QUESTS.items():
        if q["chapter"] != ch:
            continue
        client = "王宮" if q["client"] == "castle" else "酒場"
        if q["kind"] == "survive":
            goal = "生存"
        elif q["kind"] == "kill":
            goal = f"{ENEMIES[q['target']]['name'][0]} {q['count']} 体"
        else:
            goal = f"ボス {ENEMIES[q['target']]['name'][0]}"
        limit = q["time_limit"]
        print(f"### {q['name'][0]} (`{qid}`) — {client} / {goal} / 制限 {fmt_time(limit)} / 敵HP x{q['hp_mult']} (+{limit // q['hp_ramp'] * 100 if q['hp_ramp'] else 0}% で終了時 x{q['hp_mult'] * (1 + limit / q['hp_ramp']):.2f}) / 報酬 {q['reward']}G\n")
        print("| 時間 | 敵 | 秒間 | 同時上限 | 見込み数 | XP/秒 |")
        print("|---|---|---:|---:|---:|---:|")
        xp_total = 0.0
        xps_by_window = {}
        for w in WAVES[q["waves"]]:
            if w[1] == "boss":
                print(f"| {fmt_time(w[0])} | **{ENEMIES[w[2]]['name'][0]}** (ボス) | 1 体 | - | 1 | - |")
                continue
            s, e, kind, rate, cap = w
            e = min(e, limit)
            if e <= s:
                continue
            n = rate * (e - s)
            xps = rate * ENEMIES[kind]["xp"]
            xp_total += n * ENEMIES[kind]["xp"]
            print(f"| {fmt_time(s)}〜{fmt_time(e)} | {ENEMIES[kind]['name'][0]} | {rate} | {cap} | {n:.0f} | {xps:.1f} |")
        print(f"\n倒しきった場合の合計 XP: 約 {xp_total:.0f} (平均 {xp_total / limit:.1f} XP/秒)\n")
