"""ストーリーモードの永続状態 (セーブ対象)。"""

SLOTS_BY_CHAPTER = {1: 1, 2: 2, 3: 3}   # 章 → 武器スロット数 (4 章以降は 4)


class GameState:
    def __init__(self):
        self.chapter = 1
        self.gold = 0
        self.maxhp = 100
        self.hp = 100
        self.weapons = {"knife": 1}     # 物理武器 kind → ランク
        self.magic = []                 # 所持魔法 kind
        self.items = []                 # 消耗品 (Phase B)
        self.materials = {}             # 素材 kind → 個数 (Phase C)
        self.quest = None               # 受注中の依頼 id
        self.cleared = []               # クリア済み依頼 id
        self.flags = {}                 # ストーリーフラグ
        self.buff = None                # 宿屋バフ (Phase C)
        self.runs = 0                   # 出撃回数
        self.equip = "knife"            # 出発時の初期武器
        self.day = 1

    # --- 派生 ---
    @property
    def slots(self):
        return SLOTS_BY_CHAPTER.get(self.chapter, 4)

    @property
    def owned(self):
        """ラン中のレベルアップ候補になる装備 (所持物理 + 所持魔法)。"""
        return list(self.weapons.keys()) + list(self.magic)

    def to_dict(self):
        return dict(chapter=self.chapter, gold=self.gold, maxhp=self.maxhp, hp=self.hp,
                    weapons=self.weapons, magic=self.magic, items=self.items, materials=self.materials,
                    quest=self.quest, cleared=self.cleared, flags=self.flags, buff=self.buff,
                    runs=self.runs, day=self.day, equip=self.equip)

    @classmethod
    def from_dict(cls, d):
        s = cls()
        for k, v in d.items():
            if hasattr(s, k):
                setattr(s, k, v)
        return s
