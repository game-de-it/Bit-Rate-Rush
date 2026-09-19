"""王宮: 章のストーリー依頼。大臣が受付、王が依頼を出す。"""
from core import audio, images
from core.i18n import t, tt
from data.chapters import CHAPTERS, FINAL_CHAPTER
from data.quests import QUESTS, castle_open
from game import Scene
from ui import font
from ui import window as UI


class CastleScene(Scene):
    overlay = True

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state

    def enter(self):
        audio.bgm("castle")
        from scenes.dialog import DialogScene
        st = self.state
        ch = CHAPTERS.get(st.chapter)
        if ch is None or ch["castle"] in st.cleared:
            self.game.push(DialogScene(self.game, "castle_done", on_done=self.game.pop_facility))
            return
        qid = ch["castle"]
        if st.quest == qid:
            self.game.push(DialogScene(self.game, "castle_wait", on_done=self.game.pop_facility))
            return
        if st.quest:
            self.game.push(DialogScene(self.game, "tavern_has_quest", on_done=self.game.pop_facility))
            return
        if not castle_open(st, st.chapter):
            self.game.push(DialogScene(self.game, "castle_refuse", on_done=self.game.pop_facility))
            return
        q = QUESTS[qid]

        def accept():
            st.quest = qid
            audio.se(audio.SE_LEVELUP)
            self.game.pop_facility()

        # story.md の castle_before_N をそのまま使う (依頼の内容は会話文に含める)
        self.game.push(DialogScene(self.game, f"castle_before_{st.chapter}",
                                   choices=[(t("tavern.accept"), accept), (t("tavern.leave"), self.game.pop_facility)]))

    def update(self):
        pass

    def draw(self):
        town = self.game.stack[0]
        town.draw_base(show_bg=False)
        bx, by, bw, bh = UI.BG
        if not images.draw("castle_bg", bx, by):
            UI.window(bx, by, bw, bh)
            st = self.state
            ch = CHAPTERS.get(st.chapter)
            font.center(by + 5, t("town.castle"), UI.ACCENT, bx + bw // 2)
            if ch:
                font.center(by + 24, f"{t('town.chapter')}{st.chapter}  {tt(ch['title'])}", UI.TEXT, bx + bw // 2)
                q = QUESTS[ch["castle"]]
                font.center(by + 40, tt(q["name"]), UI.SUB, bx + bw // 2)
