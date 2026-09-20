"""主人公の成長 (熟練度)。戦闘中のレベルとは別に、戦闘の成果で熟練 EXP が貯まり、熟練 Lv が上がるとポイントを得る。
ポイントは宿屋の「鍛錬」で基礎能力とスキルに振る。セーブ対象 (GameState.exp / hero_lv / points / growth / skills)。

基礎能力 (1 ポイントごと):
  hp   最大 HP +10        atk  攻撃力 +5%      spd  移動速度 +4%
  pick 回収範囲 +12%      bits ビット +8%      gold コイン +10%
スキル (1 ポイント、1 回きり):
  headstart 戦闘開始時にレベルアップ 2 回      revive 戦闘不能から 1 回だけ復活 (HP 50%)
  thrift    宿代と武器の強化費が 20% 引き
"""

STATS = {
    "hp":   dict(name=("体力", "Vitality"), desc=("最大 HP +10", "Max HP +10"), max=10, col=8),
    "atk":  dict(name=("腕力", "Strength"), desc=("攻撃力 +5%", "Damage +5%"), max=10, col=9),
    "spd":  dict(name=("脚力", "Agility"), desc=("移動速度 +4%", "Move speed +4%"), max=8, col=11),
    "pick": dict(name=("感知", "Sense"), desc=("回収範囲 +12%", "Pickup range +12%"), max=6, col=6),
    "bits": dict(name=("集中", "Focus"), desc=("ビット +8%", "Bits +8%"), max=6, col=12),
    "gold": dict(name=("目利き", "Appraisal"), desc=("コイン +10%", "Coins +10%"), max=6, col=10),
}

SKILLS = {
    "headstart": dict(name=("先手", "Head Start"), desc=("戦闘開始時に Lv+2", "Start battles at Lv 3"), col=14),
    "revive":    dict(name=("不屈", "Second Wind"), desc=("1 回だけ復活 (HP 50%)", "Revive once (50% HP)"), col=8),
    "thrift":    dict(name=("倹約", "Thrift"), desc=("宿代・強化費 20% 引き", "Inn & upgrades 20% off"), col=10),
}


def need_exp(lv):
    """熟練 Lv lv → lv+1 に必要な EXP。序盤は 2〜3 戦で 1 つ上がり、後半は緩やかに伸びる"""
    return 150 + 80 * (lv - 1) + 10 * (lv - 1) ** 2


def run_exp(play, quest_ok, first_clear, boss_killed):
    """1 回の戦闘で得る熟練 EXP。撃破数 + 生存時間 + 依頼達成 + ボス撃破"""
    kills = play.player.kills
    sec = play.frame // 60
    exp = kills + sec // 3
    if quest_ok:
        exp += 200 if first_clear else 80
    if boss_killed:
        exp += 150
    if play.outcome == "dead":
        exp = exp // 2
    return int(exp)


def add_exp(state, exp):
    """EXP を加算し、上がった熟練 Lv の数を返す (1 Lv につき 1 ポイント)"""
    state.exp += exp
    ups = 0
    while state.exp >= need_exp(state.hero_lv):
        state.exp -= need_exp(state.hero_lv)
        state.hero_lv += 1
        state.points += 1
        ups += 1
    return ups


def spend(state, key):
    """ポイントを 1 つ使う。基礎能力は max まで、スキルは 1 回。成功したら True"""
    if state.points <= 0:
        return False
    if key in STATS:
        cur = state.growth.get(key, 0)
        if cur >= STATS[key]["max"]:
            return False
        state.growth[key] = cur + 1
    elif key in SKILLS:
        if state.skills.get(key):
            return False
        state.skills[key] = True
    else:
        return False
    state.points -= 1
    return True


def apply_to_player(state, player):
    """戦闘開始時に Player へ反映"""
    g = state.growth
    player.base_maxhp = state.maxhp + 10 * g.get("hp", 0)
    player.maxhp = player.base_maxhp
    player.hp = min(player.hp, player.maxhp)
    player.might_bonus = 0.05 * g.get("atk", 0)
    player.base_speed *= 1 + 0.04 * g.get("spd", 0)
    player.pick_bonus = 0.12 * g.get("pick", 0)
    player.bits_bonus = 0.08 * g.get("bits", 0)
    player.gold_bonus = 0.10 * g.get("gold", 0)
    player.revive = bool(state.skills.get("revive"))
    if state.skills.get("headstart"):
        player.xp = player.xp_next + player.need_xp(2)   # 2 回ぶん


def discount(state):
    return 0.8 if state.skills.get("thrift") else 1.0
