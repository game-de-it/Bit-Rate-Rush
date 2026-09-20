import random

import pyxel

from config import W, H, DESPAWN_DIST2, RUN_LENGTH
from data.quests import QUESTS
from core import audio
from core import palette as P
from core.spatial import SpatialHash
from game import Scene
from entities.player import Player
from entities.enemy_bullet import EnemyBullet
from entities import bullet as bullet_mod
from systems import weapons, collision, items
from systems.spawner import Spawner
from ui import hud


class PlayScene(Scene):
    """メインループ。ワールドの状態 (敵・弾・ジェム) もここが持つ。"""

    def __init__(self, game, start_weapons=("knife",), quest=None, state=None, debug=None):
        """debug: 検証ステージの設定 dict (scenes.debug_stage)。waves / time_limit / hp_mult / hp_ramp / slots / passive_slots"""
        super().__init__(game)
        self.quest_id = quest
        self.quest = QUESTS[quest] if quest else None
        self.state = state
        self.debug = debug
        self.player = Player(0.0, 0.0)
        if debug:
            self.player.max_weapon_slots = debug.get("slots", self.player.max_weapon_slots)
            self.player.max_passive_slots = debug.get("passive_slots", self.player.max_passive_slots)
        if self.quest:
            self.player.max_weapon_slots = state.slots
            self.player.allowed = set(state.owned)
            self.player.maxhp = state.maxhp
            self.player.hp = state.hp
            self.player.ranks = dict(state.weapons)
            self.player.items = list(state.items)
        for k in start_weapons:
            self.player.add_weapon(k)
        self.time_limit = self.quest["time_limit"] * 60 if self.quest else None
        if debug and debug.get("time_limit"):
            self.time_limit = debug["time_limit"] * 60
        self.kill_count = {}       # 敵種ごとの撃破数 (討伐依頼用)
        self.gold = 0              # このランで拾った金
        self.cleared = False       # 依頼達成
        self.clear_flash = 0
        self.outcome = None        # "return" | "dead" | "retreat" | "timeup"
        self.final_rush = False    # ラッシュ (出現 2 倍) 中か
        self.bonus_rush = 0        # 討伐依頼: 制限時間後のボーナスラッシュの長さ (分)。撃破数 ÷ 目標数
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.pickups = []
        self.particles = []
        self.grid = SpatialHash(32)
        if self.quest:
            self.spawner = Spawner(self, self.quest["waves"], self.quest["hp_mult"], self.quest["hp_ramp"])
        elif debug:
            self.spawner = Spawner(self, debug["waves"], debug.get("hp_mult", 1.0), debug.get("hp_ramp", 120.0))
        else:
            self.spawner = Spawner(self)
        self.frame = 0
        self.cam_x = -W / 2
        self.cam_y = -H / 2
        self.shake = 0
        self.boss = None
        self.result = None      # "win" | "lose"
        self.pending_levelups = 0
        self.no_levelup = False  # デバッグ: レベルアップ停止

    def enter(self):
        # 戦闘曲は依頼開始時に 1 曲選んでループ。曲の途中切替は初回デコード (実機で ~1 秒) がプレイ中に走って止まるのでしない
        from core import settings
        audio.bgm(settings.pick_battle_track(), battle=True)

    def exit(self):
        audio.bgm_stop()

    # --- イベント (他システムから呼ばれる) ---
    def on_enemy_killed(self, e):
        self.player.kills += 1
        self.kill_count[e.kind] = self.kill_count.get(e.kind, 0) + 1
        if e.boss and self.quest and self.quest.get("boss_dialog") and e.kind == self.quest.get("target"):
            self.push_story(self.quest["boss_dialog"])
        if e.boss:
            self.shake = 12
            if e.final and not self.quest:
                self.result = "win"
            if self.boss is e:
                self.boss = None

    def on_boss_spawn(self, e):
        self.boss = e
        self.shake = 8
        audio.se(audio.SE_BOSS)

    # --- 問い合わせ ---
    def nearest_enemy(self, x, y, rng):
        best = None
        bd = rng * rng
        for e in self.enemies:
            dx = e.x - x
            dy = e.y - y
            d = dx * dx + dy * dy
            if d < bd:
                bd = d
                best = e
        return best

    def enemies_within(self, x, y, rng):
        r2 = rng * rng
        return [e for e in self.enemies if (e.x - x) ** 2 + (e.y - y) ** 2 < r2]

    # --- 更新 ---
    def update(self):
        inp = self.inp
        if inp.pause:
            from scenes.pause import PauseScene
            self.game.push(PauseScene(self.game, self))
            return

        self.frame += 1
        p = self.player
        t_sec = self.frame / 60.0

        if self.quest and self.time_limit:
            q = self.quest
            if q["kind"] == "survive":
                # 生存依頼: ラスト 1 分は出現数 2 倍
                last = self.time_limit - self.frame <= 3600
                if last and not self.final_rush:
                    self.start_rush()
                self.spawner.rate_mult = 2.0 if last else 1.0
            elif q["kind"] == "kill" and self.frame >= self.time_limit and not self.bonus_rush:
                # 討伐依頼: 制限時間の時点で目標の N 倍倒していれば N 分のボーナスラッシュ
                n = self.kill_count.get(q["target"], 0) // q["count"]
                if n >= 1:
                    self.bonus_rush = n
                    self.time_limit += n * 3600
                    self.spawner.wave_time_cap = q["time_limit"] - 0.5   # 制限時間直前のウェーブを続ける
                    self.start_rush()
                    self.spawner.rate_mult = 2.0
        self.spawner.update(t_sec)
        p.update(inp)
        items.update(self)
        weapons.update(self)
        self.update_enemies()
        self.update_bullets()
        self.update_enemy_bullets()
        collision.bullets_vs_enemies(self)
        collision.enemies_vs_player(self)
        collision.enemy_bullets_vs_player(self)
        self.update_pickups()
        self.update_particles()
        self.update_camera()

        if self.quest:
            self.check_quest()
        if p.hp <= 0:
            self.result = "lose"
            self.outcome = "dead"
        if self.quest and self.time_limit and self.frame >= self.time_limit and not self.result:
            self.result = "win" if self.cleared else "lose"
            self.outcome = "timeup"
        if self.debug and self.time_limit and self.frame >= self.time_limit and not self.result:
            self.result = "win"                  # 検証ステージ: 時間まで生き延びたら終了
            self.outcome = "timeup"
        if self.result:
            from scenes.result import ResultScene
            self.game.push(ResultScene(self.game, self, self.result == "win"))
            return
        if not self.no_levelup and p.check_level_up():
            audio.se(audio.SE_LEVELUP)
            from scenes.levelup import LevelUpScene
            self.game.push(LevelUpScene(self.game, self))

    def check_quest(self):
        if self.cleared:
            if self.clear_flash > 0:
                self.clear_flash -= 1
            return
        q = self.quest
        ok = False
        if q["kind"] == "survive":
            ok = self.frame >= self.time_limit - 1
        elif q["kind"] in ("kill", "boss"):
            ok = self.kill_count.get(q["target"], 0) >= q["count"]
        if ok:
            self.cleared = True
            self.clear_flash = 180
            audio.se(audio.SE_LEVELUP)
            if q.get("after"):
                # 現地で起きる会話 (占い師との出会いなど)。戦闘は一時停止
                self.push_story(q["after"])

    def push_story(self, key):
        """戦闘中の物語会話。VN 会話なら暗転で出入りする (街用の窓なら暗転なし)。"""
        from scenes.dialog import DialogScene
        from data.story import OPTIONS
        if OPTIONS.get(key, {}).get("vn"):
            self.game.push_fade(DialogScene(self.game, key, fade_out=True))
        else:
            self.game.push(DialogScene(self.game, key))

    def start_rush(self):
        self.final_rush = True
        audio.se(audio.SE_BOSS)
        self.shake = 24

    def finish(self, outcome):
        """ポーズメニューからの帰還 / 撤退。"""
        self.outcome = outcome
        self.result = "win" if self.cleared else "lose"
        from scenes.result import ResultScene
        self.game.push(ResultScene(self.game, self, self.result == "win"))

    def update_enemies(self):
        p = self.player
        px, py = p.x, p.y
        enemies = self.enemies
        frame = self.frame
        # 追尾移動
        for e in enemies:
            dx = px - e.x
            dy = py - e.y
            d2 = dx * dx + dy * dy
            if d2 > DESPAWN_DIST2 and not e.boss:
                e.alive = False          # 追いつけない敵は消す (ドロップなし)
                continue
            spd = e.spd
            if e.boss:
                spd = self.update_boss(e, spd)
            if d2 > 1.0:
                inv = spd / (d2 ** 0.5)
                e.dx = dx * inv
                e.dy = dy * inv
            e.x += e.dx + e.kx
            e.y += e.dy + e.ky
            e.kx *= 0.8
            e.ky *= 0.8
            if e.flash > 0:
                e.flash -= 1
        if len(enemies) and not all(e.alive for e in enemies):
            self.enemies = enemies = [e for e in enemies if e.alive]

        # 空間ハッシュ再構築 → 押し出し (偶奇で半分ずつ)
        grid = self.grid
        grid.rebuild(enemies)
        parity = frame & 1
        for i in range(parity, len(enemies), 2):
            e = enemies[i]
            if e.phase or e.boss:      # ボスは雑魚に押されない
                continue
            ex, ey, er = e.x, e.y, e.r
            for o in grid.nearby(ex, ey, er + 8):
                if o is e or o.phase:
                    continue
                dx = ex - o.x
                dy = ey - o.y
                rr = er + o.r
                d2 = dx * dx + dy * dy
                if d2 < rr * rr:
                    if d2 < 0.01:
                        dx, dy, d2 = random.uniform(-1, 1), random.uniform(-1, 1), 1.0
                    d = d2 ** 0.5
                    push = (rr - d) / d * 0.5
                    e.x += dx * push
                    e.y += dy * push

    def update_boss(self, e, spd):
        """ボス: 周期的に突進 + 取り巻き召喚 + 放射弾。速度を返す。"""
        d = e.data
        e.dash_cd -= 1
        if e.dash > 0:
            e.dash -= 1
            spd *= 3.5
        elif e.dash_cd <= 0:
            e.dash = 30
            e.dash_cd = 180
        e.summon_cd -= 1
        if e.summon_cd <= 0:
            e.summon_cd = d.get("summon_cd", 300)
            for _ in range(d.get("summon_n", 6)):
                ang = random.uniform(0, 360)
                kind = random.choice(e.summon)
                self.spawner.spawn(kind, e.x + pyxel.cos(ang) * 40, e.y + pyxel.sin(ang) * 40)
        e.shoot_cd -= 1
        if e.shoot_cd <= 0:
            e.shoot_cd = d.get("shoot_cd", 180)
            self.boss_shoot(e)
        return spd

    def boss_shoot(self, e):
        d = e.data
        n = d.get("shots", 8)
        spd = d.get("shot_spd", 1.2)
        dmg = e.dmg * 0.6
        base = random.uniform(0, 360)
        for i in range(n):
            ang = base + 360.0 * i / n
            self.enemy_bullets.append(EnemyBullet(e.x, e.y, pyxel.cos(ang) * spd, pyxel.sin(ang) * spd, dmg))
        if d.get("aimed"):
            # プレイヤー狙いの 3 way
            p = self.player
            dx, dy = p.x - e.x, p.y - e.y
            ang0 = pyxel.atan2(dy, dx)
            for off in (-12, 0, 12):
                a = ang0 + off
                self.enemy_bullets.append(EnemyBullet(e.x, e.y, pyxel.cos(a) * spd * 1.6, pyxel.sin(a) * spd * 1.6, dmg))
        audio.se(audio.SE_ZAP)
        self.shake = 3

    def update_enemy_bullets(self):
        dead = False
        for b in self.enemy_bullets:
            b.update()
            if not b.alive:
                dead = True
        if dead:
            self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]

    def update_bullets(self):
        p = self.player
        dead = False
        for b in self.bullets:
            b.update(p)
            if not b.alive:
                dead = True
        if dead:
            self.bullets = [b for b in self.bullets if b.alive]

    def update_pickups(self):
        p = self.player
        px, py = p.x, p.y
        mag = p.magnet
        mag2 = mag * mag
        dead = False
        if p.magnet_pending:
            p.magnet_pending = False
            for g in self.pickups:
                if g.kind in ("xp", "coin"):
                    g.attracted = True
        for g in self.pickups:
            dx = px - g.x
            dy = py - g.y
            d2 = dx * dx + dy * dy
            if not g.attracted:
                if d2 < mag2:
                    g.attracted = True
                else:
                    continue
            if d2 < 36:
                g.alive = False
                dead = True
                if g.kind == "xp":
                    p.gain_xp(g.value)
                    audio.pickup()
                elif g.kind == "heal":
                    p.hp = min(p.maxhp, p.hp + 30)
                    audio.se(audio.SE_LEVELUP)
                elif g.kind == "coin":
                    self.gold += g.value
                    audio.pickup()
                else:
                    p.magnet_pending = True
                    audio.se(audio.SE_LEVELUP)
                continue
            g.spd = min(6.0, g.spd + 0.25)
            inv = g.spd / (d2 ** 0.5)
            g.x += dx * inv
            g.y += dy * inv
        if dead:
            self.pickups = [g for g in self.pickups if g.alive]

    def update_particles(self):
        dead = False
        for pt in self.particles:
            pt.update()
            if not pt.alive:
                dead = True
        if dead:
            self.particles = [pt for pt in self.particles if pt.alive]

    def update_camera(self):
        p = self.player
        self.cam_x = p.x - W / 2
        self.cam_y = p.y - H / 2
        if self.shake > 0:
            self.shake -= 1
            self.cam_x += random.randint(-2, 2)
            self.cam_y += random.randint(-2, 2)

    # --- 描画 ---
    def draw(self):
        bullet_mod.FRAME = self.frame
        cx, cy = self.cam_x, self.cam_y
        pyxel.camera(cx, cy)
        self.draw_floor(cx, cy)

        # 描画順: 床 → 床系の弾 (聖水) → ジェム → 敵 → プレイヤー → 弾 → パーティクル
        x0, y0, x1, y1 = cx - 24, cy - 24, cx + W + 24, cy + H + 24
        for b in self.bullets:
            if b.kind in ("holy", "fire", "tower") and b.alive:
                b.draw()
        for g in self.pickups:
            if g.kind == "xp" and x0 < g.x < x1 and y0 < g.y < y1:
                g.draw()
        for e in self.enemies:
            if e.alive and x0 < e.x < x1 and y0 < e.y < y1:
                e.draw()
        self.player.draw()
        for b in self.bullets:
            if b.alive and b.kind not in ("holy", "fire", "tower") and x0 < b.x < x1 and y0 < b.y < y1:
                b.draw()
        for b in self.enemy_bullets:
            if x0 < b.x < x1 and y0 < b.y < y1:
                b.draw()
        # アイテム (回復・磁石) は敵に隠れないよう最前面 + 点滅リング
        blink = (self.frame // 8) % 2 == 0
        for g in self.pickups:
            if g.kind != "xp" and x0 < g.x < x1 and y0 < g.y < y1:
                g.draw()
                if blink:
                    pyxel.circb(g.x, g.y, 9, 7)
        for pt in self.particles:
            pt.draw()
        hud.draw(self)

    def draw_floor(self, cx, cy):
        pyxel.cls(P.FLOOR)
        tile = 32
        sx = int(cx // tile) * tile
        sy = int(cy // tile) * tile
        for ty in range(sy, sy + H + tile, tile):
            for tx in range(sx, sx + W + tile, tile):
                h = (tx * 73856093 ^ ty * 19349663) & 0xFF
                if h < 40:
                    pyxel.pset(tx + 5, ty + 9, P.FLOOR_LIGHT)
                    pyxel.pset(tx + 6, ty + 9, P.FLOOR_LIGHT)
                elif h < 80:
                    pyxel.rect(tx + 18, ty + 20, 3, 2, P.FLOOR_DARK)
                elif h < 100:
                    pyxel.rect(tx + 24, ty + 5, 2, 2, P.FLOOR_DARK)
