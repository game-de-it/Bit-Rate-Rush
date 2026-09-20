"""デバッグ: 検証ステージ。出す敵と量、ボス、HP 倍率、時間、枠数を決めてサバイバルを始める。
設定は user_data_dir/debug_stage.json に保存され、次回も同じ条件で始められる。

操作: 上下で項目、左右で値、A で開始 (初期武器選択へ)、B で戻る。
"""
import json
import os

import pyxel

from config import W, H
from core import audio
from core import palette as P
from core.i18n import tt
from data.enemies import ENEMIES
from data.weapons import MAX_WEAPON_SLOTS, MAX_PASSIVE_SLOTS
from game import Scene
from ui import font
from ui.menu import draw_overlay, draw_panel

ROW = 12
RATES = [0, 0.25, 0.5, 1, 2, 4, 8, 12]          # 秒間出現数
CAPS = [10, 20, 40, 60, 90, 150]                # 同時上限
HP_MULTS = [0.5, 1.0, 1.5, 2.0, 3.0, 5.0]
RAMPS = [("なし", 1e9), ("400", 400.0), ("240", 240.0), ("200", 200.0), ("120", 120.0), ("60", 60.0)]
TIMES = [3, 5, 7, 10, 0]                        # 分 (0 = 無制限)
BOSS_AT = 15                                    # ボスを出す秒


def _path():
    try:
        d = pyxel.user_data_dir("kroot", "Bit-Rate-Rush")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, "debug_stage.json")
    except Exception:
        return None


def default_config():
    return dict(
        rates={k: (1.0 if k == "bat" else 0) for k in ENEMIES if not ENEMIES[k].get("boss")},
        caps={k: 40 for k in ENEMIES if not ENEMIES[k].get("boss")},
        boss="",
        hp_mult=1.0,
        ramp=120.0,
        time_limit=5,
        slots=MAX_WEAPON_SLOTS,
        passive_slots=MAX_PASSIVE_SLOTS,
    )


def load_config():
    cfg = default_config()
    p = _path()
    if p and os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                saved = json.load(f)
            for k in ("rates", "caps"):
                cfg[k].update({kk: v for kk, v in saved.get(k, {}).items() if kk in cfg[k]})
            for k in ("boss", "hp_mult", "ramp", "time_limit", "slots", "passive_slots"):
                if k in saved:
                    cfg[k] = saved[k]
        except Exception:
            pass
    return cfg


def save_config(cfg):
    p = _path()
    if not p:
        return
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def build_waves(cfg):
    """設定 → ウェーブ表 (systems.spawner の書式)。時間無制限のときは 1 時間分"""
    end = (cfg["time_limit"] or 60) * 60 + 60
    waves = []
    for kind, rate in cfg["rates"].items():
        if rate > 0:
            waves.append((0, end, kind, float(rate), int(cfg["caps"].get(kind, 40))))
    if cfg["boss"]:
        waves.append((BOSS_AT, "boss", cfg["boss"]))
    return waves


def _cycle(values, cur, d):
    """values の中で cur の次 / 前へ。cur が無ければ先頭"""
    try:
        i = values.index(cur)
    except ValueError:
        return values[0]
    return values[(i + d) % len(values)]


class DebugStageScene(Scene):
    overlay = True

    def __init__(self, game):
        super().__init__(game)
        self.cfg = load_config()
        self.kinds = [k for k in ENEMIES if not ENEMIES[k].get("boss")]
        self.bosses = [""] + [k for k in ENEMIES if ENEMIES[k].get("boss")]
        # 行: ("enemy", kind) ×N, ("boss",), ("hp",), ("ramp",), ("time",), ("slots",), ("passive",), ("start",)
        self.rows = [("enemy", k) for k in self.kinds] + [("boss",), ("hp",), ("ramp",), ("time",), ("slots",), ("passive",), ("start",)]
        self.cursor = 0
        self.col = 0          # 敵の行: 0 = 出現率, 1 = 上限

    # --- 値の変更 ---
    def change(self, d):
        row = self.rows[self.cursor]
        cfg = self.cfg
        if row[0] == "enemy":
            k = row[1]
            if self.col == 0:
                cfg["rates"][k] = _cycle(RATES, cfg["rates"][k], d)
            else:
                cfg["caps"][k] = _cycle(CAPS, cfg["caps"][k], d)
        elif row[0] == "boss":
            cfg["boss"] = _cycle(self.bosses, cfg["boss"], d)
        elif row[0] == "hp":
            cfg["hp_mult"] = _cycle(HP_MULTS, cfg["hp_mult"], d)
        elif row[0] == "ramp":
            vals = [v for _, v in RAMPS]
            cfg["ramp"] = _cycle(vals, cfg["ramp"], d)
        elif row[0] == "time":
            cfg["time_limit"] = _cycle(TIMES, cfg["time_limit"], d)
        elif row[0] == "slots":
            cfg["slots"] = max(1, min(8, cfg["slots"] + d))
        elif row[0] == "passive":
            cfg["passive_slots"] = max(1, min(8, cfg["passive_slots"] + d))
        audio.se(audio.SE_SELECT)

    def start(self):
        save_config(self.cfg)
        cfg = dict(self.cfg)
        cfg["waves"] = build_waves(cfg)
        from scenes.weapon_select import WeaponSelectScene
        from scenes.play import PlayScene

        def go(keys):
            self.game.replace_fade(PlayScene(self.game, start_weapons=keys, debug=cfg))
        audio.se(audio.SE_LEVELUP)
        self.game.push(WeaponSelectScene(self.game, on_start=go, max_slots=cfg["slots"]))

    def update(self):
        inp = self.inp
        if inp.cancel:
            save_config(self.cfg)
            self.game.pop()
            return
        n = len(self.rows)
        if inp.up:
            self.cursor = (self.cursor - 1) % n
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % n
            audio.se(audio.SE_SELECT)
        row = self.rows[self.cursor]
        if row[0] == "enemy" and (inp.confirm and not inp.pause):
            self.col = 1 - self.col            # A で出現率 / 上限の切替
            audio.se(audio.SE_SELECT)
        elif row[0] == "start" and inp.confirm:
            self.start()
            return
        elif inp.confirm and row[0] != "enemy":
            self.change(1)
        if inp.left:
            self.change(-1)
        if inp.right:
            self.change(1)
        if inp.pause:
            self.start()

    # --- 描画 ---
    def draw(self):
        draw_overlay(0.7)
        pw, ph = 250, 22 + ROW * len(self.rows) + 10
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 5, "DBG 検証ステージ", P.GOLD)
        cfg = self.cfg
        for i, row in enumerate(self.rows):
            y = py + 20 + i * ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 2, pw - 8, ROW - 1, 5)
            c = 7 if sel else 6
            if row[0] == "enemy":
                k = row[1]
                rate = cfg["rates"][k]
                cap = cfg["caps"][k]
                font.text(px + 8, y, tt(ENEMIES[k]["name"]), c if rate > 0 else 13)
                rc = P.ACCENT if (sel and self.col == 0) else c
                cc = P.ACCENT if (sel and self.col == 1) else c
                font.right(y, f"{rate:g}/秒", rc, px + 150)
                font.right(y, f"上限 {cap}", cc, px + pw - 10)
            elif row[0] == "boss":
                name = tt(ENEMIES[cfg["boss"]]["name"]) if cfg["boss"] else "なし"
                font.text(px + 8, y, f"ボス ({BOSS_AT} 秒で出現)", c)
                font.right(y, name, P.ACCENT if sel else c, px + pw - 10)
            elif row[0] == "hp":
                font.text(px + 8, y, "敵 HP 倍率", c)
                font.right(y, f"x{cfg['hp_mult']:g}", P.ACCENT if sel else c, px + pw - 10)
            elif row[0] == "ramp":
                label = next((n for n, v in RAMPS if v == cfg["ramp"]), "?")
                font.text(px + 8, y, "HP 上昇 (秒で 2 倍)", c)
                font.right(y, label, P.ACCENT if sel else c, px + pw - 10)
            elif row[0] == "time":
                font.text(px + 8, y, "制限時間", c)
                font.right(y, f"{cfg['time_limit']} 分" if cfg["time_limit"] else "無制限", P.ACCENT if sel else c, px + pw - 10)
            elif row[0] == "slots":
                font.text(px + 8, y, "武器スロット", c)
                font.right(y, str(cfg["slots"]), P.ACCENT if sel else c, px + pw - 10)
            elif row[0] == "passive":
                font.text(px + 8, y, "パッシブ枠", c)
                font.right(y, str(cfg["passive_slots"]), P.ACCENT if sel else c, px + pw - 10)
            else:
                font.center(y, "武器を選んで開始 (START)", P.GOLD if sel else 7)
        font.center(py + ph - 12, "左右: 変更  A: 率/上限 切替  B: 戻る", 13)
