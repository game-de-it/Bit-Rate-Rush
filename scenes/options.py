import pyxel

from config import W, H
from core import audio, settings
from core import palette as P
from core.i18n import t, LANGS
from game import Scene
from ui import font
from ui.menu import draw_overlay, draw_panel

LANG_NAMES = {"ja": "日本語", "en": "English"}
ITEMS = ["opt.lang", "opt.bgm", "opt.se", "opt.battle_vol", "opt.battle", "opt.back"]
ROW = 18


class OptionsScene(Scene):
    """オプション。in_battle=True (戦闘中のポーズから) なら戦闘曲の変更をその場で反映し、閉じても戦闘曲のまま。
    タイトルからのときは曲を選ぶと試聴し、閉じるとタイトル曲に戻る。"""
    overlay = True

    def __init__(self, game, in_battle=False):
        super().__init__(game)
        self.cursor = 0
        self.in_battle = in_battle
        self.previewed = False

    # 戦闘 BGM の選択肢: シャッフル / 順番 / 各曲
    def battle_choices(self):
        return [("shuffle", t("opt.shuffle")), ("sequence", t("opt.sequence"))] + \
               [(name, audio.track_title(name)) for name in audio.battle_tracks()]

    def battle_index(self):
        mode = settings.get("battle_mode", "shuffle")
        keys = [k for k, _ in self.battle_choices()]
        key = settings.get("battle_track", "") if mode == "select" else mode
        return keys.index(key) if key in keys else 0

    def set_battle(self, idx):
        key, _ = self.battle_choices()[idx]
        if key in ("shuffle", "sequence"):
            settings.set("battle_mode", key)
        else:
            settings.set("battle_mode", "select")
            settings.set("battle_track", key)
        # その場で反映 / 試聴
        if self.in_battle or key not in ("shuffle", "sequence"):
            audio.bgm(settings.pick_battle_track(advance=False), battle=True,
                      loop=settings.battle_loop_one() or not self.in_battle)
            self.previewed = True

    def close(self):
        settings.save()
        if self.previewed and not self.in_battle:
            audio.bgm("title")
        self.game.pop()

    def update(self):
        inp = self.inp
        if inp.cancel or inp.pause:
            self.close()
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % len(ITEMS)
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(ITEMS)
            audio.se(audio.SE_SELECT)
        key = ITEMS[self.cursor]
        step = (-1 if inp.left else 0) + (1 if inp.right else 0)
        if key == "opt.lang" and (step or inp.confirm):
            cur = LANGS.index(settings.get("lang", "ja"))
            settings.set("lang", LANGS[(cur + (step or 1)) % len(LANGS)])
            audio.se(audio.SE_SELECT)
        elif key in ("opt.bgm", "opt.se", "opt.battle_vol") and step:
            k = {"opt.bgm": "bgm", "opt.se": "se", "opt.battle_vol": "battle_vol"}[key]
            v = max(0, min(10, settings.get(k, 5) + step))
            settings.set(k, v)
            audio.se(audio.SE_LEVELUP if k == "se" else audio.SE_SELECT)
        elif key == "opt.battle" and (step or inp.confirm):
            n = len(self.battle_choices())
            self.set_battle((self.battle_index() + (step or 1)) % n)
            audio.se(audio.SE_SELECT)
        elif key == "opt.back" and inp.confirm:
            self.close()

    def draw(self):
        draw_overlay(0.6)
        pw, ph = 250, 24 + ROW * len(ITEMS) + 24
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 6, t("opt.title"), P.GOLD)
        for i, key in enumerate(ITEMS):
            y = py + 26 + i * ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 3, pw - 8, ROW - 2, 5)
            font.text(px + 12, y, t(key), 7 if sel else 6)
            col = P.ACCENT if sel else 6
            if key == "opt.lang":
                font.right(y, f"< {LANG_NAMES[settings.get('lang', 'ja')]} >", col, px + pw - 12)
            elif key in ("opt.bgm", "opt.se", "opt.battle_vol"):
                v = settings.get({"opt.bgm": "bgm", "opt.se": "se", "opt.battle_vol": "battle_vol"}[key], 5)
                font.right(y, f"< {'■' * v + '□' * (10 - v)} >", col, px + pw - 12)
            elif key == "opt.battle":
                label = self.battle_choices()[self.battle_index()][1]
                font.right(y, f"< {label} >", col, px + pw - 12)
        font.center(py + ph - 16, t("opt.hint"), 13)
