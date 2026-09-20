import pyxel

from core import debug
from core import sprites as S
from data.weapons import weapon_stats, MAX_PASSIVE_SLOTS


class WeaponState:
    __slots__ = ("kind", "level", "rank", "stats", "cd", "burst", "burst_t", "orbits", "last")

    def __init__(self, kind, rank=1):
        self.kind = kind
        self.level = 1
        self.rank = rank
        self.stats = weapon_stats(kind, 1, rank)
        self.cd = 30          # 次の発射までのフレーム
        self.burst = 0        # 連射の残り数
        self.burst_t = 0
        self.orbits = []      # orbit 用: 周回している弾
        self.last = None      # fire 用: 最後に置いた位置

    def level_up(self):
        self.level += 1
        self.stats = weapon_stats(self.kind, self.level, self.rank)


class Player:
    R = 6
    INV_FRAMES = 30

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.fx, self.fy = 1.0, 0.0     # 向き
        self.base_speed = 1.5
        self.base_maxhp = 100
        self.maxhp = self.base_maxhp
        self.hp = self.maxhp
        self.level = 1
        self.xp = 0
        self.xp_next = self.need_xp(1)
        self.inv = 0
        self.anim = 0
        self.weapons = []            # list[WeaponState]
        self.passives = {}           # kind -> level
        self.kills = 0
        self.magnet_pending = False  # 磁石アイテム取得フラグ
        self.max_weapon_slots = 4    # ストーリーでは章で決まる
        self.max_passive_slots = MAX_PASSIVE_SLOTS
        self.allowed = None          # レベルアップ候補にできる装備 (None = 全部)
        self.ranks = {}              # 物理武器のランク (ストーリー)
        self.items = []              # 持ち込んだ消耗品 (最大 3)
        self.item_cursor = 0
        self.shield = 0              # 無敵アイテムの残りフレーム
        self.sharpen = 0             # 砥石: 攻撃力 +50% の残りフレーム

    @staticmethod
    def need_xp(level):
        if debug.easy_levelup:
            return debug.EASY_XP
        # 序盤 (Lv2〜8) はテンポよく、後半は二次関数で伸びる。Lv26 以降は 330 で頭打ち (決戦で伸び続けられるように)
        return min(330, 8 + 4 * (level - 1) + (level * level) // 3)

    # --- 派生ステータス ---
    @property
    def speed(self):
        return self.base_speed * (1 + 0.1 * self.passives.get("speed", 0))

    @property
    def might(self):
        return (1 + 0.1 * self.passives.get("might", 0)) * (1.5 if self.sharpen > 0 else 1.0)

    @property
    def cooldown(self):
        return 1 - 0.08 * self.passives.get("cooldown", 0)

    @property
    def magnet(self):
        return 24 * (1 + 0.25 * self.passives.get("magnet", 0))

    @property
    def extra_amount(self):
        return self.passives.get("amount", 0)

    def add_passive(self, kind):
        self.passives[kind] = self.passives.get(kind, 0) + 1
        if kind == "maxhp":
            self.maxhp = self.base_maxhp + 20 * self.passives[kind]
            self.hp = min(self.maxhp, self.hp + 20)

    def add_weapon(self, kind):
        for w in self.weapons:
            if w.kind == kind:
                w.level_up()
                return w
        if len(self.weapons) >= self.max_weapon_slots:
            return None
        w = WeaponState(kind, self.ranks.get(kind, 1))
        self.weapons.append(w)
        return w

    def gain_xp(self, v):
        self.xp += v

    def check_level_up(self):
        if self.xp >= self.xp_next:
            self.xp -= self.xp_next
            self.level += 1
            self.xp_next = self.need_xp(self.level)
            return True
        return False

    def hurt(self, dmg):
        if self.inv > 0 or self.shield > 0:
            return False
        self.hp -= dmg
        self.inv = self.INV_FRAMES
        return True

    def update(self, inp):
        mx, my = inp.mx, inp.my
        if mx or my:
            sp = self.speed
            self.x += mx * sp
            self.y += my * sp
            self.fx, self.fy = mx, my
            self.anim += 1
        if self.inv > 0:
            self.inv -= 1
        if self.shield > 0:
            self.shield -= 1
        if self.sharpen > 0:
            self.sharpen -= 1

    def draw(self):
        if self.shield > 0:
            pyxel.circb(self.x, self.y, 11 + (self.shield // 4) % 2, 10 if (self.shield // 3) % 2 else 7)
        if self.inv > 0 and (self.inv // 3) % 2 == 0:
            return
        u, v, w, h = S.PLAYER
        flip = -w if self.fx < 0 else w
        bob = (self.anim // 6) % 2
        pyxel.blt(self.x - 8, self.y - 8 - bob, 0, u, v, flip, h, S.COLKEY)
