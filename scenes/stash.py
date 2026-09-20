"""装備の整理 (預ける): 所持している武器・魔法ごとに「持ち込む / 預ける」を切り替える。
預けた装備は戦闘中のレベルアップ候補に出なくなる。初期武器は預けられない。出発準備から開く。"""
import pyxel

from config import W, H
from core import audio, save
from core import palette as P
from core.i18n import t, tt
from data.weapons import WEAPONS
from game import Scene
from scenes.shop import ROMAN
from ui import font, icons
from ui.menu import draw_overlay, draw_panel

ROW = 14


class StashScene(Scene):
    overlay = True

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.keys = state.all_owned
        self.cursor = 0

    def update(self):
        inp = self.inp
        st = self.state
        if inp.cancel or inp.pause:
            save.save(st)
            self.game.pop()
            return
        n = len(self.keys)
        if inp.up:
            self.cursor = (self.cursor - 1) % n
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % n
            audio.se(audio.SE_SELECT)
        if inp.confirm or inp.left or inp.right:
            k = self.keys[self.cursor]
            if st.store(k, k not in st.stored):
                audio.se(audio.SE_SELECT)

    def draw(self):
        draw_overlay(0.6)
        st = self.state
        pw, ph = 290, 24 + ROW * len(self.keys) + 26
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 6, t("stash.title"), P.GOLD)
        for i, k in enumerate(self.keys):
            y = py + 24 + i * ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 2, pw - 8, ROW - 1, 5)
            w = WEAPONS[k]
            stored = k in st.stored
            is_equip = k == st.equip
            rank = st.weapons.get(k)
            name = tt(w["name"]) + (f" {ROMAN[rank]}" if rank else "")
            icons.draw(k, px + 10, y - 3, w["col"] if not stored else 13)
            font.text(px + 30, y, name, (7 if sel else 6) if not stored else 13)
            if is_equip:
                tag, col = t("stash.equip"), P.GOLD
            elif stored:
                tag, col = t("stash.stored"), 13
            else:
                tag, col = t("stash.carry"), P.ACCENT
            font.right(y, tag, col, px + pw - 10)
        font.center(py + ph - 14, t("stash.hint"), 13)
