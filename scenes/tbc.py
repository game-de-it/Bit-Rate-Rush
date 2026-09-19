"""「後編へ続く」画面。数秒表示してタイトルへ (暗転)。"""
import pyxel

from config import W, H
from core import audio
from core import palette as P
from core.i18n import t
from game import Scene
from ui import font

HOLD = 60 * 5


class ToBeContinuedScene(Scene):
    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.t = 0

    def enter(self):
        audio.bgm_stop()

    def update(self):
        self.t += 1
        if self.game.fade_t:
            return
        if self.t > HOLD or (self.t > 120 and self.inp.confirm):
            from scenes.title import TitleScene
            self.game.replace_fade(TitleScene(self.game))

    def draw(self):
        pyxel.camera()
        pyxel.cls(0)
        if self.t > 20:
            font.center(H // 2 - 14, t("ending.tbc"), 7)
        if self.t > 60:
            font.center(H // 2 + 4, t("ending.tbc_sub"), 13)
