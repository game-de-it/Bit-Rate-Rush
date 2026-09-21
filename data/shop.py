"""武器屋の品揃えと価格。chapter 以上で並ぶ。rank_cost はランク II / III / IV への強化費 (素材は Phase C で追加)。"""

# 入手順 (DESIGN_RPG §5.1): ナイフ (初期) → 槍 → 弓 → 手裏剣 → ハンマー → 鎖鎌 → ブーメラン → 斧
# 1 章はナイフのみ (お金はランク強化・宿・アイテムに使う)
WEAPON_STOCK = {
    # chapter = 前編で並ぶ章、chapter2 = 後編で並ぶ章 (アリアは新しい状態で始まるので前編の武器も買い直す)
    "spear":     dict(chapter=2, chapter2=6, price=1000),
    "bow":       dict(chapter=2, chapter2=7, price=1200),
    "shuriken":  dict(chapter=3, chapter2=8, price=1600),
    "whip":      dict(chapter=99, chapter2=9, price=2000),
    "hammer":    dict(chapter=3, chapter2=10, price=3000),
    "crossbow":  dict(chapter=99, chapter2=11, price=3500),
    "sickle":    dict(chapter=4, chapter2=12, price=4000),
    "boomerang": dict(chapter=4, chapter2=13, price=5000),
    "grenade":   dict(chapter=99, chapter2=14, price=5500),
    "axe":       dict(chapter=4, chapter2=15, price=6000),
}

RANK_COST = {2: 300, 3: 800, 4: 2000}
MAX_RANK = 4
RANK_BONUS = 0.2       # ランクごとに基礎ダメージ +20%


def stock(state):
    if state.chapter >= 6:
        return [k for k, v in WEAPON_STOCK.items() if v.get("chapter2", 99) <= state.chapter]
    return [k for k, v in WEAPON_STOCK.items() if v["chapter"] <= state.chapter]
