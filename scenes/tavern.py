"""酒場: 依頼板から 1 件受注。背景エリアに依頼板の窓を出す。"""
import pyxel

from core import audio, images
from core.i18n import t, tt
from data.quests import QUESTS, offered
from data.story import DIALOGS
from data.enemies import ENEMIES
from game import Scene
from ui import font
from ui import window as UI

ROW = 26


def goal_text(q):
    if q["kind"] == "survive":
        return t("goal.survive").format(f"{q['time_limit'] // 60}:{q['time_limit'] % 60:02d}")
    if q["kind"] == "boss":
        return t("goal.boss").format(tt(ENEMIES[q["target"]]["name"]))
    return t("goal.kill").format(tt(ENEMIES[q["target"]]["name"]), q["count"])


class TavernScene(Scene):
    overlay = True

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.quests = offered(state)
        self.cursor = 0

    def enter(self):
        audio.bgm("tavern")
        from scenes.dialog import DialogScene
        from data.story import DIALOGS
        st = self.state
        if st.quest:
            key = "tavern_has_quest"
        else:
            key = f"tavern_hello_{st.chapter}" if f"tavern_hello_{st.chapter}" in DIALOGS else "tavern_hello"
        if st.chapter == 2 and not st.flags.get("rumor_seer"):
            st.flags["rumor_seer"] = True          # 噂を聞くと占い師の依頼が並ぶ
            self.quests = offered(st)
        if "tavern_first" in DIALOGS and not st.flags.get("tavern_first"):
            # 初回だけ: 用語の説明 → 通常の挨拶
            st.flags["tavern_first"] = True
            self.game.push(DialogScene(self.game, key))
            self.game.push(DialogScene(self.game, "tavern_first"))
            return
        self.game.push(DialogScene(self.game, key))

    def update(self):
        inp = self.inp
        if inp.cancel or inp.pause:
            self.game.pop_facility()
            return
        if not self.quests:
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % len(self.quests)
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(self.quests)
            audio.se(audio.SE_SELECT)
        self.cursor = min(self.cursor, len(self.quests) - 1)
        if inp.confirm and not self.state.quest:
            qid = self.quests[self.cursor]
            q = QUESTS[qid]
            from scenes.dialog import DialogScene

            def accept():
                self.state.quest = qid
                audio.se(audio.SE_LEVELUP)
                self.game.push(DialogScene(self.game, "tavern_accept", on_done=self.game.pop))

            pages = DIALOGS.get(f"quest_{qid}") or [("master", q["text"])]
            self.game.push(DialogScene(self.game, pages,
                                       choices=[(t("tavern.accept"), accept), (t("tavern.leave"), None)]))

    def draw(self):
        from scenes.dialog import DialogScene
        town = self.game.stack[0]
        town.draw_base(show_bg=False)
        bx, by, bw, bh = UI.BG
        if isinstance(self.game.stack[-1], DialogScene):
            # 会話中は酒場の風景、それ以外は依頼板
            if not images.draw("tavern_bg", bx, by):
                UI.window(bx, by, bw, bh)
            return
        UI.window(bx, by, bw, bh)
        font.center(by + 5, t("tavern.board"), UI.ACCENT, bx + bw // 2)
        for i, qid in enumerate(self.quests):
            q = QUESTS[qid]
            y = by + 22 + i * ROW
            sel = i == self.cursor
            done = qid in self.state.cleared
            active = qid == self.state.quest
            if sel:
                UI.sel_bar(bx + 4, y - 2, bw - 8, ROW - 2)
            name = tt(q["name"]) + (f"  [{t('tavern.cleared')}]" if done else "")
            font.text(bx + 10, y, name, UI.ACCENT if active else UI.TEXT)
            reward = int(q["reward"] * (0.7 if done else 1.0))
            font.text(bx + 10, y + 12, goal_text(q), UI.SUB if not sel else UI.TEXT)
            font.right(y + 12, f"{reward}G", UI.GOLD, bx + bw - 10)
        # 下窓: マスターの立ち絵 + 選択中の依頼の説明
        dx, dy, dw, dh = UI.DIALOG
        UI.window(dx, dy, dw, dh)
        tx = dx + 10
        if images.draw("npc_master", dx + 3, dy + 1):
            tx = dx + 3 + 64 + 8
        if not self.quests:
            # この章は酒場の依頼がない (最終章など)
            font.center(by + 60, t("tavern.empty"), UI.SUB, bx + bw // 2)
            font.text(tx, dy + 8, t("tavern.empty_hint"), UI.TEXT)
            return
        qid = self.quests[self.cursor]
        q = QUESTS[qid]
        from scenes.dialog import wrap
        override = DIALOGS.get(f"quest_{qid}")
        desc = tt(override[0][1]) if override else tt(q["text"])
        for i, line in enumerate(wrap(desc, dx + dw - tx - 8)[:4]):
            font.text(tx, dy + 6 + i * 12, line, UI.TEXT)
        font.right(dy + dh - 13, f"{t('tavern.limit')} {q['time_limit'] // 60}:{q['time_limit'] % 60:02d}", UI.SUB, dx + dw - 8)
