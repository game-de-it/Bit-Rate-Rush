"""ストーリーモードの永続状態 (セーブ対象)。"""

# 章 → 武器スロット数 / パッシブ枠。前編 (1〜5 章) は武器 1→4、パッシブ 4。後編 (6 章〜) で武器 5→6、パッシブ 5→6 に広げる
# (後編の章番号と増えるタイミングは戦闘バランスを見て調整する)
SLOTS_BY_CHAPTER = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4, 6: 5, 7: 5, 8: 6}
PASSIVE_SLOTS_BY_CHAPTER = {1: 4, 2: 4, 3: 4, 4: 4, 5: 4, 6: 5, 7: 5, 8: 6}


def weapon_slots(chapter):
    return SLOTS_BY_CHAPTER.get(chapter, 6 if chapter > 8 else 4)


def passive_slots(chapter):
    return PASSIVE_SLOTS_BY_CHAPTER.get(chapter, 6 if chapter > 8 else 4)


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
        self.stored = []                # 預けた装備 kind (戦闘中のレベルアップ候補に出ない)

    # --- 派生 ---
    @property
    def slots(self):
        return weapon_slots(self.chapter)

    @property
    def passive_slots(self):
        return passive_slots(self.chapter)

    @property
    def all_owned(self):
        """所持している装備すべて (物理 + 魔法)。預けたものも含む"""
        return list(self.weapons.keys()) + list(self.magic)

    @property
    def owned(self):
        """ラン中のレベルアップ候補になる装備 (所持物理 + 所持魔法、預けたものを除く)。"""
        out = [k for k in self.all_owned if k not in self.stored]
        return out or self.all_owned[:1]

    def store(self, kind, on):
        """預ける / 引き出す。初期武器は預けられない (預ける前に初期武器を変える)"""
        if on:
            if kind == self.equip or kind in self.stored:
                return False
            self.stored.append(kind)
        else:
            if kind in self.stored:
                self.stored.remove(kind)
        return True

    def to_dict(self):
        return dict(chapter=self.chapter, gold=self.gold, maxhp=self.maxhp, hp=self.hp,
                    weapons=self.weapons, magic=self.magic, items=self.items, materials=self.materials,
                    quest=self.quest, cleared=self.cleared, flags=self.flags, buff=self.buff,
                    runs=self.runs, day=self.day, equip=self.equip, stored=self.stored)

    @classmethod
    def from_dict(cls, d):
        s = cls()
        for k, v in d.items():
            if hasattr(s, k):
                setattr(s, k, v)
        return s
