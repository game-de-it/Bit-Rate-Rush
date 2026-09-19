"""デバッグ: story.md の全会話を一覧から再生する。街の画面の上に街用 / VN 用のスタイルで表示。"""
import pyxel

from config import W, H
from core import audio, images
from core import palette as P
from core.state import GameState
from data.story import DIALOGS, OPTIONS, SPEAKERS
from game import Scene
from scenes.town import TownScene
from ui import font
from ui import window as UI

ROW = 12
VISIBLE = 11

# 会話キーの接頭辞 → (施設の絵, BGM)。本編でその会話が出る場面に合わせる
CONTEXT = [
    ("tavern_", ("tavern_bg", "tavern")),
    ("quest_",  ("tavern_bg", "tavern")),
    ("seer_",   ("forest_bg", "battle01")),
    ("inn_",    ("inn_bg", "inn")),
    ("mira_",   ("inn_bg", "inn")),
    ("smith_",  ("smith_bg", "smith")),
    ("shop_",   ("shop_bg", "shop")),
    ("castle_", ("castle_bg", "castle")),
    ("book_",   ("valley_bg", "battle01")),
    ("gatekeeper_", ("castle_bg", "battle01")),
    ("ending_night", ("night_bg", "inn")),
    ("ending_", ("town_bg", "town")),
    ("intro",   ("op_bg0", "intro01")),
]


def context(key):
    for pre, ctx in CONTEXT:
        if key.startswith(pre):
            return ctx
    return ("town_bg", "town")


class DialogViewerScene(Scene):
    def __init__(self, game):
        super().__init__(game)
        self.keys = list(DIALOGS.keys()) + [f"@chapter{n}" for n in range(1, 6)] + ["@credits", "@still:p2_op09"]
        self.cursor = 0
        self.top = 0
        self.state = GameState()
        self.state.chapter = 2
        self.town = TownScene(game, self.state)    # 描画の土台に使う (スタックには積まない)

    def enter(self):
        audio.bgm("town")

    def update(self):
        inp = self.inp
        if inp.cancel or inp.pause:
            from scenes.title import TitleScene
            self.game.replace_fade(TitleScene(self.game))
            return
        n = len(self.keys)
        if inp.up:
            self.cursor = (self.cursor - 1) % n
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % n
            audio.se(audio.SE_SELECT)
        if inp.left:
            self.cursor = max(0, self.cursor - VISIBLE)
        if inp.right:
            self.cursor = min(n - 1, self.cursor + VISIBLE)
        if self.cursor < self.top:
            self.top = self.cursor
        elif self.cursor >= self.top + VISIBLE:
            self.top = self.cursor - VISIBLE + 1
        if inp.confirm:
            from scenes.dialog import DialogScene
            key = self.keys[self.cursor]
            audio.se(audio.SE_SELECT)
            if key.startswith("@chapter"):
                from scenes.chapter_title import ChapterTitleScene
                self.game.push_fade(ChapterTitleScene(self.game, int(key[-1])))
                return
            if key == "@credits":
                from scenes.credits import CreditsScene
                self.game.push_fade(CreditsScene(self.game))
                return
            if key.startswith("@still:"):
                # 一枚絵 (p2_intro 後の p2_op09 など)。表示後はこのビューアへ戻る
                from scenes.still import StillScene
                name = key.split(":", 1)[1]
                self.game.push_fade(StillScene(self.game, name, None))
                return
            audio.bgm(context(key)[1])
            self.game.push(DialogScene(self.game, key))

    def resume(self):
        audio.bgm("town")

    def draw(self):
        from scenes.dialog import DialogScene
        bx, by, bw, bh = UI.BG
        key = self.keys[self.cursor]
        img_key, bgm_key = context(key)
        if isinstance(self.game.stack[-1], DialogScene):
            # 再生中: その場面の施設の絵を右エリアに (無ければ街)
            self.town.draw_base(show_bg=False)
            if not images.draw(img_key, bx, by):
                if not images.draw("town_bg", bx, by):
                    UI.window(bx, by, bw, bh)
            return
        self.town.draw_base(show_bg=True)
        UI.window(bx, by, bw, bh)
        font.center(by + 4, f"DBG 会話ビューア ({self.cursor + 1}/{len(self.keys)})", UI.ACCENT, bx + bw // 2)
        for i in range(VISIBLE):
            idx = self.top + i
            if idx >= len(self.keys):
                break
            key = self.keys[idx]
            y = by + 18 + i * ROW
            sel = idx == self.cursor
            if sel:
                UI.sel_bar(bx + 4, y - 1, bw - 8, ROW)
            opt = OPTIONS.get(key, {})
            tag = "VN" if opt.get("vn") else ("絵" if key.startswith("@still") else ("演出" if key.startswith("@") else "  "))
            spk = DIALOGS[key][0][0] if key in DIALOGS and DIALOGS[key] else ""
            font.text(bx + 8, y, f"{tag} {key}", UI.TEXT if sel else UI.SUB)
            font.right(y, spk, UI.SUB, bx + bw - 8)
        # 下窓: 選択中の会話の 1 行目
        dx, dy, dw, dh = UI.DIALOG
        UI.window(dx, dy, dw, dh)
        key = self.keys[self.cursor]
        pages = DIALOGS.get(key, [])
        if pages:
            spk, (ja, en) = pages[0]
            name = SPEAKERS.get(spk, SPEAKERS["narr"])["name"][0]
            font.text(dx + 10, dy + 6, f"{name}  ({len(pages)} ページ)" if name else f"({len(pages)} ページ)", UI.ACCENT)
            from scenes.dialog import wrap
            for i, line in enumerate(wrap(ja, dw - 20)[:2]):
                font.text(dx + 10, dy + 20 + i * 12, line, UI.TEXT)
        vn_bg = OPTIONS.get(key, {}).get("bg")
        pic = f"{vn_bg} (VN)" if vn_bg else img_key
        has = "" if images.get(vn_bg or img_key) is not None else " [未配置]"
        font.text(dx + 10, dy + dh - 13, f"絵: {pic}{has}   BGM: {bgm_key}", UI.SUB)
        font.right(dy + dh - 13, "A: 再生  B: 戻る", UI.SUB, dx + dw - 8)
