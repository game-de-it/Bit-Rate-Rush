"""会話ウィンドウ (画面下の白い窓)。pages = [(話者キー, (ja, en) or str), ...]。
choices = [(ラベル, callback), ...] は最終ページ後に表示。
話者に img があり assets/img/<img>.png があれば左に立ち絵 (64x64)。無ければ枠だけ。"""
import pyxel

from config import W, H
from core import audio, images
from core.i18n import tt
from data.story import SPEAKERS, DIALOGS, OPTIONS, PAGE_BG, PAGE_BGM
from core import palette as P
from game import Scene
from ui import font
from ui import window as UI


def wrap(text, width):
    """フォント幅で折り返す。
    - 半角スペースで区切られた塊は単語扱い: 行に収まらなければスペースの位置で改行 (日本語の折り返し指定にも使える)
    - スペースが無い部分は 1 文字単位。1 つの塊が 1 行より長い場合も文字単位に落とす
    - 文中の "\\n" (2 文字) は強制改行
    """
    lines = []
    for para in text.replace("\\n", "\n").split("\n"):
        cur = ""
        for chunk in para.split(" "):
            cand = chunk if not cur else cur + " " + chunk
            if font.width(cand) <= width:
                cur = cand
                continue
            if cur:
                lines.append(cur)
                cur = ""
            # 塊だけで幅を超えるなら文字単位で割る
            if font.width(chunk) > width:
                for ch in chunk:
                    if font.width(cur + ch) > width:
                        lines.append(cur)
                        cur = ch
                    else:
                        cur += ch
            else:
                cur = chunk
        lines.append(cur)
    return lines


class DialogScene(Scene):
    overlay = True

    def __init__(self, game, pages, choices=None, on_done=None, vn=None, bg=None, fade_out=False):
        super().__init__(game)
        self.fade_out = fade_out        # 最後のページの後、暗転してから閉じる
        opt = {}
        self.page_bg = {}
        self.page_bgm = {}
        self.start_bgm = None
        if isinstance(pages, str):
            opt = OPTIONS.get(pages, {})
            self.page_bg = PAGE_BG.get(pages, {})
            self.page_bgm = PAGE_BGM.get(pages, {})
            self.start_bgm = opt.get("bgm")
            pages = DIALOGS[pages]
        self.vn = opt.get("vn", False) if vn is None else vn      # ビジュアルノベル風 (全画面背景 + 下窓)
        self.bg = opt.get("bg") if bg is None else bg
        self.vn_pic = not opt.get("nopic", False)      # VN 窓の左に小さい立ち絵を出す
        self.pages = pages
        self.choices = choices or []
        self.on_done = on_done
        self.i = 0
        self.shown = 0
        self.cursor = 0
        self.choosing = False
        self.shown_bg = None       # 表示中の絵 (クロスフェードの元)
        self.fade_from = None      # フェード中: 前の絵
        self.fade_t = 0
        self.FADE_LEN = 24

    def enter(self):
        if self.start_bgm:
            self._play_bgm(self.start_bgm)

    @staticmethod
    def _play_bgm(name):
        if name in ("stop", "none", "off"):
            audio.bgm_stop()
        else:
            audio.bgm(name)

    def _text(self):
        return tt(self.pages[self.i][1])

    def _bg(self):
        """現在ページの絵と、そのページで切り替わる場合にフェードするか。"""
        bg, fade = self.bg, True
        for idx in sorted(self.page_bg):
            if idx <= self.i:
                bg, fade = self.page_bg[idx]
        return bg, fade

    def _sync_bg(self):
        """ページが進んで絵が変わったらクロスフェードを始める。"""
        bg, fade = self._bg()
        if self.shown_bg is None:
            self.shown_bg = bg
            return
        if bg != self.shown_bg:
            if fade and images.get(bg) is not None and images.get(self.shown_bg) is not None:
                self.fade_from = self.shown_bg
                self.fade_t = 0
            self.shown_bg = bg

    def update(self):
        inp = self.inp
        if self.choosing:
            if inp.up:
                self.cursor = (self.cursor - 1) % len(self.choices)
                audio.se(audio.SE_SELECT)
            if inp.down:
                self.cursor = (self.cursor + 1) % len(self.choices)
                audio.se(audio.SE_SELECT)
            if inp.confirm:
                audio.se(audio.SE_SELECT)
                cb = self.choices[self.cursor][1]
                self.game.pop()
                if cb:
                    cb()
            elif inp.cancel:
                audio.se(audio.SE_SELECT)
                self.game.pop()
                cb = self.choices[-1][1]
                if cb:
                    cb()
            return
        self.shown += 2
        if self.fade_from is not None:
            self.fade_t += 1
            if self.fade_t >= self.FADE_LEN:
                self.fade_from = None
            return                      # フェード中は送らない
        if inp.confirm:
            if self.shown < len(self._text()):
                self.shown = 999
            elif self.i + 1 < len(self.pages):
                self.i += 1
                self.shown = 0
                if self.vn:
                    self._sync_bg()
                if self.i in self.page_bgm:
                    self._play_bgm(self.page_bgm[self.i])
            elif self.choices:
                self.choosing = True
            elif self.fade_out:
                cb = self.on_done
                def done():
                    self.game.pop()
                    if cb:
                        cb()
                self.game.fade(done)
            else:
                self.game.pop()
                if self.on_done:
                    self.on_done()

    def draw(self):
        if self.vn:
            self.draw_vn()
            return
        pyxel.camera()
        sp = SPEAKERS.get(self.pages[self.i][0], SPEAKERS["narr"])
        dx, dy, dw, dh = UI.DIALOG
        UI.window(dx, dy, dw, dh)
        tx = dx + 10
        if sp["img"]:
            px, py = dx + 3, dy + 1
            if not images.draw(sp["img"], px, py):        # 不透明で描く (黒 = 0 を透過にすると暗部に穴が空く)
                pyxel.rect(px, py, 64, 64, UI.SEL)
                pyxel.rectb(px, py, 64, 64, UI.SUB)
                font.center(py + 27, "?", UI.TEXT, px + 32)
            tx = px + 64 + 8
        name = tt(sp["name"])
        ty = dy + 6
        if name:
            font.text(tx, ty, name, UI.ACCENT)
            ty += 13
        text = self._text()[: self.shown]
        for i, line in enumerate(wrap(text, dx + dw - tx - 8)):
            if i >= 3:
                break
            font.text(tx, ty + i * 12, line, UI.TEXT)
        if self.choosing:
            cw = 120
            ch = 14 * len(self.choices) + 8
            cx, cy = dx + dw - cw - 4, dy - ch - 2
            UI.window(cx, cy, cw, ch)
            for i, (label, _) in enumerate(self.choices):
                sel = i == self.cursor
                if sel:
                    UI.sel_bar(cx + 3, cy + 3 + i * 14, cw - 6, 13)
                font.text(cx + 8, cy + 5 + i * 14, ("> " if sel else "  ") + label, UI.TEXT if sel else UI.SUB)
        elif self.shown >= len(self._text()) and (pyxel.frame_count // 20) % 2 == 0:
            font.right(dy + dh - 13, "▼", UI.ACCENT, dx + dw - 8)

    # --- ビジュアルノベル風: 上に 16:9 の絵 (320x180) をそのまま、下に暗い会話窓 + 名前札 ---
    VN_IMG_H = 180

    def draw_vn(self):
        from config import W, H
        pyxel.camera()
        if self.shown_bg is None:
            self._sync_bg()
        bg = self.shown_bg
        if bg and images.get(bg) is not None:
            pyxel.cls(0)
            if self.fade_from is not None:
                # クロスフェード: 前の絵の上に新しい絵をディザで重ねる
                images.draw(self.fade_from, 0, 0)
                pyxel.dither(min(1.0, self.fade_t / self.FADE_LEN))
                images.draw(bg, 0, 0)
                pyxel.dither(1.0)
            else:
                images.draw(bg, 0, 0)
        else:
            # 背景指定なし (または画像が無い): 下のシーンを暗くして使う
            pyxel.dither(0.35)
            pyxel.rect(0, 0, W, H, 0)
            pyxel.dither(1.0)
        sp = SPEAKERS.get(self.pages[self.i][0], SPEAKERS["narr"])
        wx, wy, ww, wh = 0, self.VN_IMG_H, W, H - self.VN_IMG_H
        pyxel.rect(wx, wy, ww, wh, P.OUTLINE)
        pyxel.rectb(wx, wy, ww, wh, 13)
        pyxel.rectb(wx + 1, wy + 1, ww - 2, wh - 2, 5)
        name = tt(sp["name"])
        if name:
            nw = font.width(name) + 14
            pyxel.rect(wx + 8, wy - 13, nw, 14, P.ACCENT)
            pyxel.rectb(wx + 8, wy - 13, nw, 14, 7)
            font.text(wx + 15, wy - 12, name, P.OUTLINE)
        tx, ty = wx + 12, wy + 10
        img = images.get(sp["img"]) if (sp["img"] and self.vn_pic) else None
        if img is not None:
            # 64x64 を 48x48 に縮小して窓の左に (blt の scale は中心基準なので位置を補正)
            px, py = wx + 8, wy + 6
            pyxel.blt(px - 8, py - 8, img, 0, 0, 64, 64, None, scale=0.75)
            pyxel.rectb(px, py, 48, 48, 13)
            tx = px + 48 + 8
        text = self._text()[: self.shown]
        for i, line in enumerate(wrap(text, wx + ww - tx - 12)):
            if i >= 3:
                break
            font.text(tx, ty + i * 13, line, P.ACCENT if not name else 7)
        if self.choosing:
            cw = 120
            ch = 14 * len(self.choices) + 8
            cx, cy = wx + ww - cw - 4, wy - ch - 2
            UI.window(cx, cy, cw, ch)
            for i, (label, _) in enumerate(self.choices):
                sel = i == self.cursor
                if sel:
                    UI.sel_bar(cx + 3, cy + 3 + i * 14, cw - 6, 13)
                font.text(cx + 8, cy + 5 + i * 14, ("> " if sel else "  ") + label, UI.TEXT if sel else UI.SUB)
        elif self.shown >= len(self._text()) and (pyxel.frame_count // 20) % 2 == 0:
            font.right(wy + wh - 14, "▼", P.ACCENT, wx + ww - 10)
