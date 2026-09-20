"""後編のエンディング: 谷での会話 (VN) を順に → スタッフロール → 一枚絵 → タイトル。
会話キーは STORY_PART2.md の p2_ending_* / p2_epilogue_* (無いものは飛ばす)。"""
import pyxel

from config import W, H
from core import audio, images, save
from core.i18n import t
from game import Scene
from scenes import credits

SEQUENCE = ["p2_ending_voice", "p2_ending_restore", "p2_ending_song", "p2_epilogue_observer", "p2_epilogue_beach"]


class Ending2Scene(Scene):
    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.phase = "story"      # story → credits → still → done
        self.t = 0
        self.i = 0

    def enter(self):
        self.next_story()

    def next_story(self):
        from scenes.dialog import DialogScene
        from data.story import DIALOGS
        while self.i < len(SEQUENCE) and SEQUENCE[self.i] not in DIALOGS:
            self.i += 1
        if self.i >= len(SEQUENCE):
            self.start_credits()
            return
        key = SEQUENCE[self.i]
        self.i += 1
        self.game.push_fade(DialogScene(self.game, key, fade_out=True, on_done=self.next_story))

    def start_credits(self):
        def go():
            self.phase = "credits"
            self.t = 0
            audio.bgm("title")
        if self.game.fade_t:
            go()                      # 最後の会話の暗転中に呼ばれる: そのまま切り替える
        else:
            self.game.fade(go, length=60)

    def update(self):
        self.t += 1
        if self.game.fade_t:
            return
        if self.phase == "credits":
            if self.t > credits.duration() or (self.t > 120 and self.inp.confirm):
                def to_still():
                    self.phase = "still"
                    self.t = 0
                    audio.bgm_stop()
                self.game.fade(to_still)
        elif self.phase == "still":
            if self.t > 60 * 8 or (self.t > 90 and self.inp.confirm):
                st = self.state
                st.flags["cleared_part2"] = True
                st.quest = None
                save.save(st)
                from scenes.title import TitleScene
                self.phase = "done"
                self.game.replace_fade(TitleScene(self.game))

    def draw(self):
        pyxel.camera()
        pyxel.cls(0)
        if self.phase == "credits":
            credits.draw(self.t)
        elif self.phase == "still":
            if not images.draw("p2_end", 0, 0):
                from ui import font
                font.center(H // 2 - 4, t("ending.fin"), 7)
