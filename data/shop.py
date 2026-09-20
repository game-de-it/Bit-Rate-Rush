"""武器屋の品揃えと価格。chapter 以上で並ぶ。rank_cost はランク II / III / IV への強化費 (素材は Phase C で追加)。"""

# 入手順 (DESIGN_RPG §5.1): ナイフ (初期) → 槍 → 弓 → 手裏剣 → ハンマー → 鎖鎌 → ブーメラン → 斧
# 1 章はナイフのみ (お金はランク強化・宿・アイテムに使う)
WEAPON_STOCK = {
    "spear":     dict(chapter=2, price=1000),
    "bow":       dict(chapter=2, price=1200),
    "shuriken":  dict(chapter=3, price=1600),
    "hammer":    dict(chapter=3, price=3000),
    "sickle":    dict(chapter=4, price=4000),
    "boomerang": dict(chapter=4, price=5000),
    "axe":       dict(chapter=4, price=6000),
    # 後編 (章番号は後編の章構成が決まったら調整)
    "whip":      dict(chapter=6, price=7000),
    "crossbow":  dict(chapter=6, price=8000),
    "grenade":   dict(chapter=7, price=9000),
}

RANK_COST = {2: 300, 3: 800, 4: 2000}
MAX_RANK = 4
RANK_BONUS = 0.2       # ランクごとに基礎ダメージ +20%


def stock(state):
    return [k for k, v in WEAPON_STOCK.items() if v["chapter"] <= state.chapter]
