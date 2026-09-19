"""一枚絵を全画面で見せるだけの場面 (エンディングの ending.png と同じ見せ方)。
暗転明けで表示 → 数秒保持 (A で早送り) → 暗転して next() へ。"""
import pyxel

from config import W, H
from core import images
from game import Scene

HOLD = 60 * 10
SKIP_AFTER = 90


class StillScene(Scene):
    def __init__(self, game, image, next_scene, hold=HOLD):
        super().__init__(game)
        self.image = image            # assets/img/<image>.png (320x240)
        self.next_scene = next_scene  # 次の場面を作る関数
        self.hold = hold
        self.t = 0

    def update(self):
        self.t += 1
        if self.game.fade_t:
            return
        if self.t > self.hold or (self.t > SKIP_AFTER and self.inp.confirm):
            self.game.replace_fade(self.next_scene())

    def draw(self):
        pyxel.camera()
        pyxel.cls(0)
        images.draw(self.image, 0, 0)
