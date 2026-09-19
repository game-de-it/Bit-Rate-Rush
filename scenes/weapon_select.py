"""デバッグ用: 初期武器を選んでスタートする画面。A でチェック切替、START または最下段の項目で開始。"""
import pyxel

from config import W, H
from core import audio
from core import palette as P
from core.i18n import tt
from data.weapons import WEAPONS, MAX_WEAPON_SLOTS
from game import Scene
from ui import font, icons
from ui.menu import draw_overlay, draw_panel

ROW = 14


class WeaponSelectScene(Scene):
    overlay = True

    def __init__(self, game):
        super().__init__(game)
        self.keys = list(WEAPONS.keys())
        self.selected = {"knife"}
        self.cursor = 0
        self.n = len(self.keys) + 1     # 最後は「スタート」

    def start(self):
        if not self.selected:
            return
        audio.se(audio.SE_LEVELUP)
        from scenes.play import PlayScene
        self.game.replace_fade(PlayScene(self.game, start_weapons=[k for k in self.keys if k in self.selected]))

    def update(self):
        inp = self.inp
        if inp.cancel:
            self.game.pop()
            return
        if inp.pause:
            self.start()
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % self.n
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % self.n
            audio.se(audio.SE_SELECT)
        if inp.confirm:
            if self.cursor == len(self.keys):
                self.start()
                return
            k = self.keys[self.cursor]
            if k in self.selected:
                if len(self.selected) > 1:
                    self.selected.discard(k)
            elif len(self.selected) < MAX_WEAPON_SLOTS:
                self.selected.add(k)
            audio.se(audio.SE_SELECT)

    def draw(self):
        draw_overlay(0.7)
        pw, ph = 220, 22 + ROW * self.n + 8
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 5, f"DEBUG: 初期武器 ({len(self.selected)}/{MAX_WEAPON_SLOTS})", P.GOLD)
        for i in range(self.n):
            y = py + 20 + i * ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 2, pw - 8, ROW - 1, 5)
            if i < len(self.keys):
                k = self.keys[i]
                w = WEAPONS[k]
                on = k in self.selected
                pyxel.rectb(px + 10, y + 1, 8, 8, 7 if on else 13)
                if on:
                    pyxel.rect(px + 12, y + 3, 4, 4, P.ACCENT)
                icons.draw(k, px + 22, y - 3, w["col"])
                cls = "魔" if w["cls"] == "magic" else "物"
                font.text(px + 42, y, f"{cls} {tt(w['name'])}", 7 if on else 6)
            else:
                font.center(y, "スタート (START)", P.GOLD if sel else 7)
