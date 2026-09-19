"""宿屋: 休む (有料で全回復 + セーブ)。食事バフは Phase C。"""
from core import audio, images, save
from ui import window as UI
from core.i18n import t
from game import Scene


def rest_cost(state):
    return 30 * state.chapter


class InnScene(Scene):
    overlay = True

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state

    def enter(self):
        audio.bgm("inn")
        from scenes.dialog import DialogScene
        from data.story import DIALOGS
        st = self.state
        key = f"mira_{st.chapter}"
        if key in DIALOGS and not st.flags.get(key):
            st.flags[key] = True
            self.game.push(DialogScene(self.game, key, on_done=self.enter))
            return
        if st.hp >= st.maxhp:
            self.game.push(DialogScene(self.game, "inn_full", on_done=self.game.pop_facility))
            return
        cost = rest_cost(st)

        def rest():
            if st.gold < cost:
                self.game.push(DialogScene(self.game, "inn_poor", on_done=self.game.pop_facility))
                return
            st.gold -= cost
            st.hp = st.maxhp
            st.day += 1
            save.save(st)
            audio.se(audio.SE_LEVELUP)
            self.game.push(DialogScene(self.game, "inn_rest", on_done=self.game.pop_facility))

        self.game.push(DialogScene(self.game, "inn_hello",
                                   choices=[(t("inn.rest_cost").format(cost), rest), (t("inn.leave"), self.game.pop_facility)]))

    def update(self):
        pass

    def draw(self):
        town = self.game.stack[0]
        town.draw_base(show_bg=False)
        bx, by, bw, bh = UI.BG
        if not images.draw("inn_bg", bx, by):
            images.draw("town_bg", bx, by)
