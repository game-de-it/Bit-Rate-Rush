"""エンディング: 宿屋の夜の独白 → 暗転 → スタッフロール → ラッシュのカット → タイトル。"""
import random

import pyxel

from config import W, H
from core import audio, images, save
from core import palette as P
from core import sprites as S
from core.i18n import tt
from game import Scene
from ui import font

# スタッフロールの文言は assets/story.md の `## credits` で編集する。無いときの予備
FALLBACK_CREDITS = [
    ("BIT-RATE-RUSH", "BIT-RATE-RUSH"),
    ("", ""),
    ("Thank you for playing", "Thank you for playing"),
]


def credits():
    from data.story import CREDITS
    return CREDITS or FALLBACK_CREDITS


class EndingScene(Scene):
    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.phase = "night"     # night → credits → rush → done
        self.t = 0
        self.rush = []

    def enter(self):
        audio.bgm("inn")
        from scenes.dialog import DialogScene
        self.game.push(DialogScene(self.game, "ending_night", on_done=self.start_credits))

    def start_credits(self):
        def go():
            self.phase = "credits"
            self.t = 0
            audio.bgm("title")
        self.game.fade(go, length=60)

    def update(self):
        self.t += 1
        if self.phase == "credits":
            if (self.t > 60 * 14 + len(credits()) * 14 or (self.t > 120 and self.inp.confirm)) and not self.game.fade_t:
                def to_rush():
                    self.phase = "rush"
                    self.t = 0
                    audio.bgm_stop()
                self.game.fade(to_rush)
        elif self.phase == "rush":
            # 最後の一枚 (ending.png、比率そのまま) を見せて終わる。A で早送り
            if self.t > 60 * 10 or (self.t > 90 and self.inp.confirm):
                self.phase = "done"
                self.t = 0
        elif self.phase == "done":
            if self.t > 90 and not self.game.fade_t:
                st = self.state
                st.flags["cleared_once"] = True
                st.quest = None
                save.save(st)
                # 後編の導入 (p2_intro) を見せて「後編へ続く」→ タイトル
                from scenes.dialog import DialogScene
                from scenes.tbc import ToBeContinuedScene
                from data.story import DIALOGS
                self.phase = "teaser"
                if "p2_intro" in DIALOGS:
                    self.game.push_fade(DialogScene(self.game, "p2_intro", fade_out=True,
                                                    on_done=lambda: self.game.replace(ToBeContinuedScene(self.game, st))))
                else:
                    self.game.replace_fade(ToBeContinuedScene(self.game, st))
        elif self.phase == "teaser":
            pass

    def draw(self):
        pyxel.camera()
        pyxel.cls(0)
        if self.phase == "night":
            # 宿屋の夜: 暗い街
            pyxel.dither(0.25)
            images.draw("town_bg", 43, 10)
            pyxel.dither(1.0)
        elif self.phase == "credits":
            y0 = H - self.t * 0.5
            for i, (ja, en) in enumerate(credits()):
                y = y0 + i * 14
                if -12 < y < H:
                    font.center(y, tt((ja, en)), P.GOLD if i == 0 else 7)
        elif self.phase == "rush":
            a = min(1.0, self.t / 60.0)
            pyxel.dither(a)
            if not images.draw("ending", 0, 0):
                images.draw("town_bg", 43, 42)
            pyxel.dither(1.0)
            if self.t > 60 * 9:
                pyxel.dither(min(1.0, (self.t - 60 * 9) / 60.0))
                pyxel.rect(0, 0, W, H, 0)
                pyxel.dither(1.0)
        else:
            pass
