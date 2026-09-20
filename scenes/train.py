"""鍛錬 (宿屋): 熟練ポイントを基礎能力・スキルに振る。"""
import pyxel

from config import W, H
from core import audio, growth, save
from core import palette as P
from core.i18n import t, tt
from game import Scene
from ui import font
from ui.menu import draw_overlay, draw_panel

ROW = 12


class TrainScene(Scene):
    overlay = True

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.keys = list(growth.STATS) + list(growth.SKILLS)
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
        if inp.confirm or inp.right:
            if growth.spend(st, self.keys[self.cursor]):
                audio.se(audio.SE_LEVELUP)
            else:
                audio.se(audio.SE_SELECT)

    def draw(self):
        draw_overlay(0.6)
        st = self.state
        pw, ph = 300, 40 + ROW * (len(self.keys) + 2) + 26
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 6, f"{t('train.title')}   {t('res.exp').split(' ')[0]} Lv{st.hero_lv}", P.GOLD)
        need = growth.need_exp(st.hero_lv)
        font.text(px + 10, py + 20, f"{t('train.points')}: {st.points}", P.ACCENT if st.points else 7)
        font.right(py + 20, f"{t('train.next')} {st.exp}/{need}", 13, px + pw - 10)
        # EXP バー
        pyxel.rect(px + 10, py + 31, pw - 20, 3, 5)
        pyxel.rect(px + 10, py + 31, int((pw - 20) * min(1.0, st.exp / need)), 3, P.ACCENT)
        y = py + 40
        for i, k in enumerate(self.keys):
            if i == 0:
                font.text(px + 10, y, t("train.stats"), 13); y += ROW
            if i == len(growth.STATS):
                font.text(px + 10, y, t("train.skills"), 13); y += ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 2, pw - 8, ROW - 1, 5)
            if k in growth.STATS:
                d = growth.STATS[k]
                cur = d["max"] and st.growth.get(k, 0)
                col = 7 if sel else 6
                font.text(px + 16, y, tt(d["name"]), col)
                font.text(px + 70, y, tt(d["desc"]), 13 if not sel else 6)
                # ピップ
                x = px + pw - 12 - d["max"] * 6
                for j in range(d["max"]):
                    pyxel.rect(x + j * 6, y + 2, 4, 5, d["col"] if j < cur else 1)
            else:
                d = growth.SKILLS[k]
                got = st.skills.get(k)
                col = (7 if sel else 6) if not got else P.GOLD
                font.text(px + 16, y, tt(d["name"]), col)
                font.text(px + 70, y, tt(d["desc"]), 13 if not sel else 6)
                if got:
                    font.right(y, t("train.done"), P.GOLD, px + pw - 12)
            y += ROW
        font.center(py + ph - 12, t("train.hint"), 13)
