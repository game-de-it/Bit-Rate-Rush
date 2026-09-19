"""武器 / パッシブ定義。

cls: "physical" (武器屋で購入) | "magic" (王宮・イベントで入手)
base: Lv1 の値。levels[i] は Lv(i+2) で加算される値。cd はフレーム数。
amount は本数 (= 攻撃回数)。"本数系" にはパッシブ Duplicator が加算される (dup=True)。
name / desc は (ja, en)。
"""

WEAPONS = {
    # ---- 物理 ----
    "knife": dict(
        cls="physical", col=7, dup=True,
        name=("ナイフ", "Knife"), desc=("向いた方向へ素早く連投する", "Rapid throws forward"),
        base=dict(cd=30, dmg=6, amount=1, speed=1.7, pierce=1, r=3, kb=1.5, spread=3),
        levels=[dict(amount=1), dict(dmg=2), dict(amount=1), dict(cd=-4), dict(amount=1), dict(dmg=3), dict(amount=1)],
    ),
    "axe": dict(
        cls="physical", col=9, dup=True,
        name=("斧", "Axe"), desc=("山なりに投げ、全て貫通", "Arcing, pierces all"),
        base=dict(cd=80, dmg=18, amount=1, r=5, kb=3.0),
        levels=[dict(dmg=6), dict(amount=1), dict(dmg=6), dict(r=1), dict(amount=1), dict(dmg=8), dict(amount=1)],
    ),
    "spear": dict(
        cls="physical", col=6, dup=True,
        name=("槍", "Spear"), desc=("長い突き。敵を貫通する", "Long thrust, pierces"),
        base=dict(cd=60, dmg=12, amount=1, speed=2.7, pierce=2, reach=168, r=4, kb=2.0),
        levels=[dict(pierce=1), dict(dmg=4), dict(pierce=1), dict(reach=36), dict(pierce=1), dict(dmg=5), dict(pierce=1)],
    ),
    "bow": dict(
        cls="physical", col=25, dup=True,
        name=("弓", "Bow"), desc=("扇状に矢を放つ。貫通なし", "Fan of arrows, no pierce"),
        base=dict(cd=50, dmg=7, amount=2, speed=2.0, pierce=1, r=3, kb=1.0, spread=7),
        levels=[dict(amount=1), dict(dmg=3), dict(speed=0.4), dict(amount=1), dict(dmg=3), dict(amount=1), dict(amount=1)],
    ),
    "hammer": dict(
        cls="physical", col=9, dup=False, fixed_cd=True,   # 最後の衝撃波が消えてから 1 秒後に次を振る (疾風の影響なし)
        name=("ハンマー", "Hammer"), desc=("振り下ろして衝撃波を残す", "Slam, lingering shockwave"),
        base=dict(cd=60, dmg=10, amount=1, length=1, r=12, dur=35, tick=12, kb=4.0, step=20),
        levels=[dict(length=1), dict(dmg=4), dict(length=1), dict(dur=10), dict(length=1), dict(dmg=6), dict(length=1)],
    ),
    "sickle": dict(
        cls="physical", col=23, dup=True,
        name=("鎖鎌", "Kusarigama"), desc=("前方180度を薙ぎ払う", "Sweeps 180 deg. ahead"),
        base=dict(cd=55, dmg=9, amount=1, r=28, dur=10, kb=2.5),
        levels=[dict(r=6), dict(dmg=3), dict(r=6), dict(amount=1), dict(r=6), dict(dmg=4), dict(r=8)],
    ),
    "boomerang": dict(
        cls="physical", col=25, dup=True,
        name=("ブーメラン", "Boomerang"), desc=("大きく弧を描いて手元に戻る", "Loops back to you"),
        base=dict(cd=90, dmg=10, amount=1, speed=2.2, turn=2.4, r=5, kb=2.0, tick=30, life=230),
        levels=[dict(amount=1), dict(dmg=4), dict(r=1), dict(amount=1), dict(dmg=4), dict(amount=1), dict(dmg=6)],
    ),
    "shuriken": dict(
        cls="physical", col=13, dup=True,
        name=("手裏剣", "Shuriken"), desc=("広い扇に短い距離で放つ", "Wide, short-range fan"),
        base=dict(cd=45, dmg=5, amount=3, speed=2.5, pierce=1, r=3, kb=1.0, spread=22, range=70),
        levels=[dict(amount=1), dict(range=15), dict(dmg=2), dict(amount=1), dict(range=15), dict(amount=1), dict(range=20)],
    ),
    # ---- 魔法 ----
    "magic": dict(
        cls="magic", col=12, dup=True,
        name=("魔法弾", "Magic Bolt"), desc=("最寄りの敵を自動で狙う", "Homes to nearest"),
        base=dict(cd=70, dmg=10, amount=1, speed=1.2, pierce=1, r=3, kb=1.5, range=170),
        levels=[dict(dmg=4), dict(amount=1), dict(cd=-10), dict(dmg=4), dict(amount=1), dict(pierce=1), dict(amount=1)],
    ),
    "holy": dict(
        cls="magic", col=6, dup=True,
        name=("聖水", "Holy Water"), desc=("地面にダメージ床を作る", "Damage zone"),
        base=dict(cd=130, dmg=3, amount=1, r=18, dur=120, tick=20),
        levels=[dict(r=3), dict(dmg=1), dict(amount=1), dict(dur=30), dict(r=3), dict(dmg=2), dict(amount=1)],
    ),
    "orbit": dict(
        cls="magic", col=10, dup=True,
        name=("衛星", "Orbit"), desc=("周囲を回って守る", "Circles around you"),
        base=dict(cd=0, dmg=6, amount=1, r=5, dist=30, rot=3.5, tick=18, kb=2.0),
        levels=[dict(dmg=2), dict(amount=1), dict(rot=1.0), dict(dmg=3), dict(amount=1), dict(r=2), dict(amount=1)],
    ),
    "zap": dict(
        cls="magic", col=10, dup=True,
        name=("雷", "Lightning"), desc=("ランダムな敵に落雷", "Strikes random foes"),
        base=dict(cd=110, dmg=20, amount=1, r=12, range=150),
        levels=[dict(dmg=8), dict(amount=1), dict(cd=-15), dict(dmg=8), dict(amount=1), dict(r=4), dict(amount=1)],
    ),
    "fire": dict(
        cls="magic", col=26, dup=False,
        name=("ファイヤーウォール", "Fire Wall"), desc=("歩いた跡に火柱を残す", "Leaves fire in your trail"),
        base=dict(cd=24, dmg=2, amount=1, r=10, dur=90, tick=20),
        levels=[dict(r=2), dict(dur=30), dict(dmg=1), dict(r=2), dict(dur=30), dict(dmg=1), dict(r=3)],
    ),
    "tower": dict(
        cls="magic", col=10, dup=False,
        name=("ライトニングタワー", "Lightning Tower"), desc=("前方に避雷針を立て周囲を感電させる", "Rod that zaps all in range"),
        base=dict(cd=150, dmg=4, amount=1, r=56, dur=120, tick=30),
        levels=[dict(r=10), dict(dmg=1), dict(r=10), dict(dur=30), dict(r=10), dict(dmg=2), dict(r=14)],
    ),
}

MAX_WEAPON_LV = 8

# パッシブ: 値はレベルごとの効果 (乗算系は 1 レベルあたりの倍率増分)
PASSIVES = {
    "might":    dict(name=("剛力", "Might"), col=8, desc=("攻撃力 +10%", "Damage +10%"), max=5),
    "cooldown": dict(name=("疾風", "Haste"), col=10, desc=("攻撃間隔 -8%", "Cooldown -8%"), max=5),
    "speed":    dict(name=("韋駄天の靴", "Boots"), col=11, desc=("移動速度 +10%", "Move +10%"), max=5),
    "maxhp":    dict(name=("生命の心臓", "Heart"), col=8, desc=("最大HP +20", "Max HP +20"), max=5),
    "magnet":   dict(name=("磁石", "Magnet"), col=6, desc=("回収範囲 +25%", "Pickup +25%"), max=5),
    "amount":   dict(name=("分身", "Duplicator"), col=14, desc=("攻撃回数 +1", "Projectiles +1"), max=2),
}

MAX_WEAPON_SLOTS = 4
MAX_PASSIVE_SLOTS = 4

_STAT_KEY = dict(dmg="st.dmg", amount="st.amount", cd="st.cd", pierce="st.pierce", r="st.r",
                 dur="st.dur", rot="st.rot", speed="st.speed", reach="st.reach", length="st.length",
                 range="st.range", turn="st.turn", life="st.dur")


def weapon_stats(kind, level, rank=1):
    """レベル (ラン中) とランク (武器屋で強化、+20%/ランク) を反映した武器パラメータ dict を返す。"""
    w = WEAPONS[kind]
    st = dict(w["base"])
    for i in range(min(level - 1, len(w["levels"]))):
        for k, v in w["levels"][i].items():
            st[k] = st.get(k, 0) + v
    if rank > 1:
        st["dmg"] = st["dmg"] * (1 + 0.2 * (rank - 1))
    return st


def weapon_level_desc(kind, level):
    """次レベル (level) で何が上がるかの短い説明。"""
    from core.i18n import t, tt
    w = WEAPONS[kind]
    if level == 1:
        return tt(w["desc"])
    idx = level - 2
    if idx >= len(w["levels"]):
        return t("lv.max")
    parts = []
    for k, v in w["levels"][idx].items():
        parts.append(f"{t(_STAT_KEY.get(k, k))} {'+' if v > 0 else ''}{v}")
    return ", ".join(parts)
