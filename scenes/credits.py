"""スタッフロール。文言は assets/story.md の `## credits` (data.story.CREDITS)。
EndingScene の credits フェーズと、デバッグの会話ビューアから使う。"""
import pyxel

from config import H
from core import audio
from core import palette as P
from core.i18n import tt
from game import Scene
from ui import font

SPEED = 0.5      # 1 フレームに流れる px
LINE_H = 14

FALLBACK = [
    ("BIT-RATE-RUSH", "BIT-RATE-RUSH"),
    ("", ""),
    ("Thank you for playing", "Thank you for playing"),
]


def lines():
    from data.story import CREDITS
    return CREDITS or FALLBACK


def duration():
    """流れきるまでのフレーム数"""
    return 60 * 14 + len(lines()) * LINE_H


def draw(t):
    y0 = H - t * SPEED
    for i, (ja, en) in enumerate(lines()):
        y = y0 + i * LINE_H
        if -12 < y < H:
            font.center(y, tt((ja, en)), P.GOLD if i == 0 else 7)


class CreditsScene(Scene):
    """単体再生 (会話ビューア用)。流れきるか A / B で戻る。"""

    def __init__(self, game):
        super().__init__(game)
        self.t = 0

    def enter(self):
        audio.bgm("title")

    def update(self):
        self.t += 1
        if self.game.fade_t:
            return
        if self.t > duration() or (self.t > 30 and (self.inp.confirm or self.inp.cancel)):
            self.game.pop_fade()

    def draw(self):
        pyxel.camera()
        pyxel.cls(0)
        draw(self.t)
