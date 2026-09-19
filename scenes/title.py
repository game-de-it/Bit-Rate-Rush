import pyxel

from config import W, H, DEBUG_WEAPON_SELECT, DEBUG_DIALOG_VIEWER, DEBUG_CHAPTER_START
from core import audio, images, save
from core import palette as P
from core.i18n import t
from core.state import GameState
from game import Scene
from ui import font

ROW = 14


class TitleScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.cursor = 0
        self.anim = 0.0      # リール回転の残り (+1: 次へ, -1: 前へ)
        self.items = []
        if save.exists():
            self.items.append("title.continue")
        self.items += ["title.new"]
        if DEBUG_WEAPON_SELECT:
            self.items.append("title.survival")
        self.items.append("title.options")
        if DEBUG_DIALOG_VIEWER:
            self.items.append("title.dialogs")
        if DEBUG_CHAPTER_START:
            self.items.append("title.chapter")
        self.items.append("title.quit")

    def enter(self):
        audio.bgm("title")

    def update(self):
        inp = self.inp
        if inp.up or inp.left:
            self.cursor = (self.cursor - 1) % len(self.items)
            self.anim = -1.0
            audio.se(audio.SE_SELECT)
        if inp.down or inp.right:
            self.cursor = (self.cursor + 1) % len(self.items)
            self.anim = 1.0
            audio.se(audio.SE_SELECT)
        if self.anim:
            self.anim *= 0.7
            if abs(self.anim) < 0.05:
                self.anim = 0.0
        if inp.confirm and not self.anim:
            audio.se(audio.SE_SELECT)
            key = self.items[self.cursor]
            if key == "title.continue":
                st = save.load() or GameState()
                from scenes.town import TownScene
                self.game.replace_fade(TownScene(self.game, st))
            elif key == "title.new":
                def start_new():
                    st = GameState()
                    save.save(st)
                    from scenes.town import TownScene
                    self.game.replace_fade(TownScene(self.game, st, intro=True))
                if save.exists():
                    from scenes.dialog import DialogScene
                    self.game.push(DialogScene(self.game, "new_game_confirm",
                                               choices=[(t("title.overwrite"), start_new), (t("tavern.leave"), None)]))
                else:
                    start_new()
            elif key == "title.survival":
                if DEBUG_WEAPON_SELECT:
                    from scenes.weapon_select import WeaponSelectScene
                    self.game.push(WeaponSelectScene(self.game))
                else:
                    from scenes.play import PlayScene
                    self.game.replace_fade(PlayScene(self.game))
            elif key == "title.options":
                from scenes.options import OptionsScene
                self.game.push(OptionsScene(self.game))
            elif key == "title.dialogs":
                from scenes.dialog_viewer import DialogViewerScene
                self.game.replace_fade(DialogViewerScene(self.game))
            elif key == "title.chapter":
                from scenes.chapter_select import ChapterSelectScene
                self.game.push(ChapterSelectScene(self.game))
            else:
                pyxel.quit()

    def draw(self):
        pyxel.camera()
        if not images.draw("title_bg", 0, 0):
            pyxel.cls(P.PANEL)
            font.center(44, "BIT-RATE-RUSH", P.GOLD)
        # 下部 1 行のスロットリール
        bh = 16
        top = H - bh
        pyxel.rect(0, top, W, bh, P.PANEL)
        pyxel.line(0, top, W, top, 5)
        n = len(self.items)
        pyxel.clip(0, top + 1, W, bh - 1)
        # anim > 0: 次の項目が下から上がってくる / anim < 0: 前の項目が上から降りてくる
        off = self.anim * bh
        cy = top + 3
        for d in (-1, 0, 1):
            key = self.items[(self.cursor + d) % n]
            y = cy + d * bh + off
            font.center(y, t(key), 7 if d == 0 else 13)
        pyxel.clip()
        if (pyxel.frame_count // 15) % 2 == 0:
            font.text(W // 2 - 70, cy, "<", P.ACCENT)
            font.right(cy, ">", P.ACCENT, W // 2 + 70)
