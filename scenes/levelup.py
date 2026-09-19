import pyxel

from config import W, H, DEBUG_LEVELUP_SKIP
from core import audio
from core import palette as P
from game import Scene
from systems import upgrades
from ui import font, icons
from core.i18n import t
from ui.menu import draw_overlay, draw_panel

ROW = 32


class LevelUpScene(Scene):
    overlay = True

    def __init__(self, game, play):
        super().__init__(game)
        self.play = play
        self.options = upgrades.roll(play.player)
        self.cursor = 0

    def update(self):
        inp = self.inp
        if inp.up:
            self.cursor = (self.cursor - 1) % len(self.options)
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(self.options)
            audio.se(audio.SE_SELECT)
        if inp.confirm:
            upgrades.apply(self.play.player, self.options[self.cursor])
            audio.se(audio.SE_LEVELUP)
            self.play.player.shield = max(self.play.player.shield, 120)   # レベルアップ後 2 秒は無敵
            self.game.pop()
            return
        if DEBUG_LEVELUP_SKIP and (inp.cancel or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_X)):
            audio.se(audio.SE_SELECT)
            self.play.player.shield = max(self.play.player.shield, 120)
            self.game.pop()

    def draw(self):
        draw_overlay(0.6)
        pw, ph = 250, ROW * len(self.options) + 30
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 6, f"{t('lv.title')}  LV {self.play.player.level}", P.GOLD)
        if DEBUG_LEVELUP_SKIP:
            font.right(py + 6, "X: skip", 13, px + pw - 6)
        y = py + 24
        for i, o in enumerate(self.options):
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 3, pw - 8, ROW - 2, 5)
            pyxel.rect(px + 8, y + 2, 20, 20, P.PANEL)
            pyxel.rectb(px + 8, y + 2, 20, 20, 7 if sel else 13)
            icons.draw(o.key, px + 10, y + 4, o.col)
            lv = t("lv.new") if o.level == 1 else (f"LV {o.level}" if o.level else "")
            font.text(px + 34, y, f"{o.name}  {lv}", 7 if sel else 6)
            font.text(px + 34, y + 13, o.desc, 7 if sel else 13)
            if sel:
                font.text(px + pw - 14, y + 6, ">", P.ACCENT)
            y += ROW
