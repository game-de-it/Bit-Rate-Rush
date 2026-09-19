"""消耗アイテム (雑貨屋)。所持は合計 3 個まで。ラン中に L/R で選び Y で使う。"""

ITEMS = {
    "herb":   dict(chapter=1, price=100, col=11, name=("薬草", "Herb"), desc=("HP を 40 回復", "Heal 40 HP")),
    "bomb":   dict(chapter=1, price=200, col=8,  name=("爆弾", "Bomb"), desc=("画面内の敵全体に 50 ダメージ", "50 damage to all on screen")),
    "magnet": dict(chapter=1, price=150, col=10, name=("磁石", "Magnet"), desc=("ビットとコインを全部吸い寄せる", "Pull in all bits and coins")),
    "charm":  dict(chapter=2, price=300, col=6,  name=("守りの護符", "Ward Charm"), desc=("5 秒間 無敵", "Invincible for 5 s")),
    "tome":   dict(chapter=2, price=350, col=12, name=("経験の書", "Tome"), desc=("即レベルアップ", "Level up instantly")),
    "elixir": dict(chapter=3, price=400, col=14, name=("上薬草", "Elixir"), desc=("HP 全回復", "Full heal")),
    "arrow":  dict(chapter=3, price=500, col=7,  name=("聖なる矢", "Holy Arrow"), desc=("最も HP の高い敵に 500 ダメージ", "500 damage to the toughest foe")),
}

MAX_ITEMS = 3


def stock(state):
    return [k for k, v in ITEMS.items() if v["chapter"] <= state.chapter]
