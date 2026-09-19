"""街 (ハブ)。紺のフレーム + 左メニュー窓 + 右に背景 PNG + 下に会話窓 (参考デザイン準拠)。"""
import pyxel

from config import W, H
from core import audio, images, save
from core.i18n import t, tt
from data.quests import QUESTS
from game import Scene
from ui import font
from ui import window as UI

MENU = [
    ("town.castle", "castle"),
    ("town.tavern", "tavern"),
    ("town.smith_s", "smith"),
    ("town.shop_s", "shop"),
    ("town.inn", "inn"),
    ("town.depart", "depart"),
]
ROW = 14


class TownScene(Scene):
    def __init__(self, game, state, intro=False, chapter_title=False):
        super().__init__(game)
        self.state = state
        self.cursor = 0
        self.intro = intro
        self.chapter_title = chapter_title      # 街に入った直後にその章のタイトルを出す (章スタート用)

    def enter(self):
        from scenes.dialog import DialogScene
        if self.chapter_title:
            # 章スタート: ジングル付きの章タイトル → 街 (街の曲はタイトルが終わってから)
            self.chapter_title = False
            from scenes.chapter_title import ChapterTitleScene
            self.game.push(ChapterTitleScene(self.game, self.state.chapter, on_done=lambda: audio.bgm("town")))
            return
        audio.bgm("town")
        if self.intro:
            self.intro = False
            # オープニング (VN) → 第一章のタイトル → 街。街の曲は章タイトルが終わってから
            from scenes.chapter_title import ChapterTitleScene
            self.game.push(DialogScene(self.game, "intro", fade_out=True,
                                       on_done=lambda: self.game.push(ChapterTitleScene(self.game, 1, on_done=lambda: audio.bgm("town")))))
            return
        pending = self.state.flags.pop("pending_story", None)
        if pending == "ending":
            from scenes.ending import EndingScene
            self.game.push(DialogScene(self.game, "ending_town",
                                       on_done=lambda: self.game.replace_fade(EndingScene(self.game, self.state), length=60)))
        elif pending:
            if pending.startswith("castle_after_"):
                # 王の会話のあと、新しい章のタイトルを出す
                from scenes.chapter_title import ChapterTitleScene
                ch = self.state.chapter
                self.game.push(DialogScene(self.game, pending, fade_out=True,
                                           on_done=lambda: self.game.push(ChapterTitleScene(self.game, ch))))
            else:
                self.game.push(DialogScene(self.game, pending))

    def resume(self):
        from scenes.chapter_title import ChapterTitleScene
        if any(isinstance(sc, ChapterTitleScene) for sc in self.game.stack):
            return
        audio.bgm("town")

    def update(self):
        inp = self.inp
        if inp.up:
            self.cursor = (self.cursor - 1) % len(MENU)
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(MENU)
            audio.se(audio.SE_SELECT)
        if inp.pause or inp.cancel:
            from scenes.pause import TownPauseScene
            self.game.push(TownPauseScene(self.game, self))
            return
        if inp.confirm:
            audio.se(audio.SE_SELECT)
            key = MENU[self.cursor][1]
            from scenes.dialog import DialogScene
            if key == "tavern":
                from scenes.tavern import TavernScene
                self.game.push_facility(TavernScene(self.game, self.state))
            elif key == "inn":
                from scenes.inn import InnScene
                self.game.push_facility(InnScene(self.game, self.state))
            elif key == "castle":
                from scenes.castle import CastleScene
                self.game.push_facility(CastleScene(self.game, self.state))
            elif key == "smith":
                from scenes.shop import SmithScene
                self.game.push_facility(SmithScene(self.game, self.state))
            elif key == "shop":
                from scenes.shop import ItemShopScene
                self.game.push_facility(ItemShopScene(self.game, self.state))
            elif key == "depart":
                if self.state.quest:
                    from scenes.depart import DepartScene
                    self.game.push_facility(DepartScene(self.game, self.state))
                else:
                    self.game.push(DialogScene(self.game, "no_quest"))
            else:
                self.game.push(DialogScene(self.game, "closed"))

    # --- 描画 (施設シーンからも部分的に呼ぶ) ---
    def draw_base(self, show_bg=True):
        UI.frame()
        st = self.state
        # 背景
        bx, by, bw, bh = UI.BG
        if show_bg:
            if not images.draw("town_bg", bx, by):
                UI.window(bx, by, bw, bh)
        # メニュー窓
        mx, my, mw, mh = UI.MENU
        UI.window(mx, my, mw, mh)
        for i, (key, _) in enumerate(MENU):
            y = my + 6 + i * ROW
            sel = i == self.cursor
            if sel:
                UI.sel_bar(mx + 3, y - 2, mw - 6)
            font.text(mx + 8, y, t(key), UI.TEXT if sel else UI.SUB)
        # ステータス (メニュー窓の下部)
        sy = my + mh - 40
        pyxel.line(mx + 4, sy - 3, mx + mw - 5, sy - 3, UI.SUB)
        from core import i18n
        day = f"{st.day}{t('town.day')}" if i18n.lang == "ja" else f"{t('town.day')} {st.day}"
        font.text(mx + 5, sy, f"{t('town.chapter')}{st.chapter} {day}", UI.SUB)
        font.text(mx + 5, sy + 12, f"HP{int(st.hp)}/{st.maxhp}", P_HP if st.hp < st.maxhp * 0.5 else UI.TEXT)
        font.text(mx + 5, sy + 24, f"{st.gold}G", UI.GOLD)

    def draw_dialog_idle(self):
        """会話が無いときの下窓: 施設の説明と受注中の依頼。"""
        dx, dy, dw, dh = UI.DIALOG
        UI.window(dx, dy, dw, dh)
        key = MENU[self.cursor][1]
        font.text(dx + 10, dy + 8, t(f"town.d.{key}"), UI.TEXT)
        q = self.state.quest
        qs = tt(QUESTS[q]["name"]) if q else t("town.noquest")
        font.text(dx + 10, dy + 26, f"{t('town.d.quest')}: {qs}", UI.ACCENT if q else UI.SUB)

    def draw(self):
        self.draw_base()
        self.draw_dialog_idle()


from core import palette as _P
P_HP = _P.HP
