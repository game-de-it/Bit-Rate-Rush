import pyxel

from core import audio, palette, settings, sprites
from core.input import Input
from ui import font


class Game:
    """シーンスタック。overlay=True のシーンは下のシーンを描画した上に重ねる。"""

    def __init__(self):
        settings.load()
        palette.load()
        font.load()
        sprites.build()
        audio.setup()
        self.input = Input()
        self.stack = []
        self.fade_t = 0            # フェード中のフレーム (0 = なし)
        self.fade_len = 12         # 片道のフレーム数
        self.fade_cb = None
        from scenes.title import TitleScene
        self.push(TitleScene(self))

    def push(self, scene):
        self.stack.append(scene)
        scene.enter()

    def pop(self):
        s = self.stack.pop()
        s.exit()
        if self.stack:
            self.stack[-1].resume()

    def replace(self, scene):
        while self.stack:
            self.stack.pop().exit()
        self.push(scene)

    # --- 暗転付きの遷移: 暗くなりきったところで cb を実行し、明けていく ---
    FADE_SCENE = 60        # 場面転換: 暗転 1 秒 + 明転 1 秒
    FADE_FACILITY = 12     # 街のメニュー ⇄ 施設: 短め

    def fade(self, cb, length=None):
        """length = 片道のフレーム数 (暗転 length + 明転 length)。省略時は場面転換用の 1 秒。"""
        if length is None:
            length = self.FADE_SCENE
        if self.fade_t:
            return
        self.fade_len = length
        self.fade_t = 1
        self.fade_cb = cb

    def push_fade(self, scene, length=None):
        self.fade(lambda: self.push(scene), length)

    def pop_fade(self, length=None):
        self.fade(self.pop, length)

    def replace_fade(self, scene, length=None):
        self.fade(lambda: self.replace(scene), length)

    # 街のメニュー ⇄ 施設 (短い暗転)
    def push_facility(self, scene):
        self.fade(lambda: self.push(scene), self.FADE_FACILITY)

    def pop_facility(self):
        self.fade(self.pop, self.FADE_FACILITY)

    def update(self):
        self.input.poll()
        audio.update()
        if self.fade_t:
            self.fade_t += 1
            if self.fade_t == self.fade_len + 1 and self.fade_cb:
                cb, self.fade_cb = self.fade_cb, None
                cb()
            if self.fade_t > self.fade_len * 2:
                self.fade_t = 0
            return
        if self.stack:
            self.stack[-1].update()

    def draw(self):
        # 一番上の非オーバーレイから描く
        start = 0
        for i in range(len(self.stack) - 1, -1, -1):
            if not self.stack[i].overlay:
                start = i
                break
        for s in self.stack[start:]:
            s.draw()
        if self.fade_t:
            t = self.fade_t
            a = t / self.fade_len if t <= self.fade_len else (self.fade_len * 2 - t) / self.fade_len
            pyxel.camera()
            pyxel.dither(max(0.0, min(1.0, a)))
            pyxel.rect(0, 0, 320, 240, 0)
            pyxel.dither(1.0)


class Scene:
    overlay = False

    def __init__(self, game):
        self.game = game
        self.inp = game.input

    def enter(self):
        pass

    def exit(self):
        pass

    def resume(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass
