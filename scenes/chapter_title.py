"""章のサブタイトル画面: 上に 16:9 の絵、下の帯に章番号と題。
jingle01.mp3 を 1 回再生し、鳴り終わったら暗転して次へ。キー入力ではスキップできない。"""
import pyxel

from config import W, H
from core import audio, images
from core import palette as P
from core.i18n import t, tt
from data.chapters import CHAPTERS, FINAL_CHAPTER
from game import Scene
from ui import font

MIN_HOLD = 60 * 2        # ジングルが無い / 短すぎる場合の最低表示時間
MAX_HOLD = 60 * 8        # 安全弁 (ジングルは約 5 秒)


class ChapterTitleScene(Scene):
    overlay = True

    def __init__(self, game, chapter, on_done=None):
        super().__init__(game)
        self.chapter = chapter
        self.on_done = on_done
        self.t = 0
        self.has_jingle = False
        self.closing = False

    def enter(self):
        self.has_jingle = audio.jingle("jingle01")

    def update(self):
        self.t += 1
        if self.game.fade_t or self.closing:
            return
        done = (self.t >= MIN_HOLD and (not self.has_jingle or not audio.playing())) or self.t >= MAX_HOLD
        if done:
            self.closing = True
            cb = self.on_done

            def finish():
                self.game.pop()
                if cb:
                    cb()
            self.game.fade(finish)

    def draw(self):
        pyxel.camera()
        pyxel.cls(0)
        images.draw(f"chapter{self.chapter}", 0, 0)
        ch = CHAPTERS[self.chapter]
        y0 = 180
        pyxel.rect(0, y0, W, H - y0, P.PANEL)
        pyxel.line(0, y0, W, y0, P.GOLD)
        num = t("chapter.final") if self.chapter >= FINAL_CHAPTER else t("chapter.n").format(self.chapter)
        rows = [(num, P.GOLD), (tt(ch["title"]), 7), (tt(ch["sub"]), 13)]
        for i, (s, col) in enumerate(rows):
            if self.t < 15 + i * 20:
                continue
            font.center(y0 + 8 + i * 15, s, col)
