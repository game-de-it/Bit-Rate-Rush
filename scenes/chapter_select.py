"""デバッグ: 所持金 MAX で任意の章の最初から始める。前章までの王宮依頼はクリア済み扱い (報酬の魔法も所持)。"""
import pyxel

from config import W, H
from core import audio, save
from core import palette as P
from core.i18n import tt
from core.state import GameState
from data.chapters import CHAPTERS, FINAL_CHAPTER
from data.quests import QUESTS
from game import Scene
from ui import font
from ui.menu import draw_overlay, draw_panel

ROW = 16


def make_state(chapter):
    st = GameState()
    st.chapter = chapter
    st.gold = 99999
    for ch in range(1, chapter):
        info = CHAPTERS[ch]
        st.cleared.append(info["castle"])
        for m in info["magic"]:
            if m not in st.magic:
                st.magic.append(m)
        # その章の酒場依頼を全部クリア済みに (王宮の受付条件)
        for qid, q in QUESTS.items():
            if q["chapter"] == ch and q["client"] == "tavern" and not q.get("flag"):
                st.cleared.append(qid)
        if ch >= 2:
            st.flags["rumor_seer"] = True
            st.flags[f"mira_{ch}"] = True
            # 2 章の隠し依頼 (占い師) もクリア済み → 衛星を所持
            for qid, q in QUESTS.items():
                if q["chapter"] == ch and q.get("flag") and qid not in st.cleared:
                    st.cleared.append(qid)
                    for m in q.get("magic", []):
                        if m not in st.magic:
                            st.magic.append(m)
    st.day = 1 + (chapter - 1) * 3
    return st


def make_ending_state():
    """ラスボス (5 章の王宮依頼) を倒して街へ戻る直前の状態。街に入るとエンディングが始まる"""
    st = make_state(FINAL_CHAPTER)
    st.cleared.append(CHAPTERS[FINAL_CHAPTER]["castle"])
    st.quest = None
    st.flags["pending_story"] = "ending"
    return st


class ChapterSelectScene(Scene):
    overlay = True

    def __init__(self, game):
        super().__init__(game)
        self.cursor = 0
        self.chapters = sorted(CHAPTERS) + ["ending"]   # 最後の項目: ラスボス撃破後 (エンディングから)

    def update(self):
        inp = self.inp
        if inp.cancel or inp.pause:
            self.game.pop()
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % len(self.chapters)
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(self.chapters)
            audio.se(audio.SE_SELECT)
        if inp.confirm:
            ch = self.chapters[self.cursor]
            audio.se(audio.SE_LEVELUP)
            from scenes.town import TownScene
            if ch == "ending":
                st = make_ending_state()
                save.save(st)
                self.game.replace_fade(TownScene(self.game, st))
                return
            st = make_state(ch)
            save.save(st)
            self.game.replace_fade(TownScene(self.game, st, intro=(ch == 1), chapter_title=(ch != 1)))

    def draw(self):
        draw_overlay(0.6)
        pw, ph = 240, 24 + ROW * len(self.chapters) + 22
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 6, "DBG 章スタート (所持金 MAX)", P.GOLD)
        for i, ch in enumerate(self.chapters):
            y = py + 24 + i * ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 2, pw - 8, ROW - 2, 5)
                font.text(px + 8, y, ">", P.ACCENT)
            label = "ED  ラスボス撃破後 (エンディングから)" if ch == "ending" else f"{ch} 章  {tt(CHAPTERS[ch]['title'])}"
            font.text(px + 20, y, label, 7 if sel else 6)
        font.center(py + ph - 14, "セーブは上書きされます", 13)
