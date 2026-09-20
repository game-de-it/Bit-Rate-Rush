"""宿屋: 休む (有料で全回復 + セーブ)。食事バフは Phase C。"""
from core import audio, images, save
from ui import window as UI
from core.i18n import t
from game import Scene


def rest_cost(state):
    from core import growth
    return int(30 * state.chapter * growth.discount(state))


class InnScene(Scene):
    overlay = True

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state

    def enter(self):
        audio.bgm("inn")
        from scenes.dialog import DialogScene
        from data.story import DIALOGS
        from data.story import resolve
        st = self.state
        key = resolve(st, f"mira_{st.chapter}")
        if key in DIALOGS and not st.flags.get(key):
            st.flags[key] = True
            self.game.push(DialogScene(self.game, key, on_done=self.enter))
            return
        cost = rest_cost(st)
        R = lambda k: resolve(st, k)

        pts = f" +{st.points}" if st.points else ""
        train_choice = (t("inn.train").format(st.hero_lv, pts), self.open_train)
        if st.hp >= st.maxhp:
            self.game.push(DialogScene(self.game, R("inn_full"),
                                       choices=[train_choice, (t("inn.leave"), self.game.pop_facility)]))
            return

        def rest():
            if st.gold < cost:
                self.game.push(DialogScene(self.game, R("inn_poor"), on_done=self.game.pop_facility))
                return
            st.gold -= cost
            st.hp = st.maxhp
            st.day += 1
            save.save(st)
            audio.se(audio.SE_LEVELUP)
            self.game.push(DialogScene(self.game, R("inn_rest"), on_done=self.game.pop_facility))

        self.game.push(DialogScene(self.game, R("inn_hello"),
                                   choices=[(t("inn.rest_cost").format(cost), rest), train_choice,
                                            (t("inn.leave"), self.game.pop_facility)]))

    def open_train(self):
        from scenes.train import TrainScene
        self.game.push(TrainScene(self.game, self.state))

    def resume(self):
        # 鍛錬 (TrainScene) から戻ったら宿屋の会話をやり直す
        if isinstance(self.game.stack[-1], InnScene):
            self.enter()

    def update(self):
        pass

    def draw(self):
        town = self.game.stack[0]
        town.draw_base(show_bg=False)
        bx, by, bw, bh = UI.BG
        from data.story import bg_name
        if not images.draw(bg_name(self.state, "inn_bg"), bx, by):
            images.draw("town_bg", bx, by)
