"""出発準備: 依頼の確認、初期武器の選択 (所持武器から)、持ち物の確認 → 戦闘へ。"""
import pyxel

from core import audio, save
from core.i18n import t, tt
from data.items import ITEMS
from data.quests import QUESTS
from data.weapons import WEAPONS
from game import Scene
from scenes.shop import ROMAN
from scenes.tavern import goal_text
from ui import font, icons
from ui import window as UI


class DepartScene(Scene):
    overlay = True

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.cursor = 0                       # 0: 初期武器, 1: 出発, 2: 戻る
        self.owned = state.owned
        if state.equip not in self.owned:
            state.equip = self.owned[0]

    def update(self):
        inp = self.inp
        st = self.state
        if inp.cancel:
            self.game.pop_facility()
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % 3
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % 3
            audio.se(audio.SE_SELECT)
        if self.cursor == 0 and (inp.left or inp.right):
            i = self.owned.index(st.equip)
            st.equip = self.owned[(i + (1 if inp.right else -1)) % len(self.owned)]
            audio.se(audio.SE_SELECT)
        if inp.confirm:
            if self.cursor == 2:
                self.game.pop_facility()
                return
            if self.cursor == 0:
                self.cursor = 1
                return
            st.runs += 1
            save.save(st)
            audio.se(audio.SE_LEVELUP)
            from scenes.play import PlayScene
            self.game.replace_fade(PlayScene(self.game, start_weapons=[st.equip], quest=st.quest, state=st))

    def draw(self):
        town = self.game.stack[0]
        town.draw_base(show_bg=False)
        st = self.state
        q = QUESTS[st.quest]
        bx, by, bw, bh = UI.BG
        UI.window(bx, by, bw, bh)
        font.center(by + 5, t("depart.title"), UI.ACCENT, bx + bw // 2)
        y = by + 20
        font.text(bx + 10, y, tt(q["name"]), UI.TEXT); y += 12
        font.text(bx + 10, y, f"{t('depart.goal')}: {goal_text(q)}", UI.TEXT); y += 12
        font.text(bx + 10, y, f"{t('tavern.limit')}: {q['time_limit'] // 60}:{q['time_limit'] % 60:02d}   {t('tavern.reward')}: {q['reward']}G", UI.TEXT); y += 15
        # 初期武器 (ラベル行 + 値の行。名前が長くても重ならないように 2 行にする)
        sel0 = self.cursor == 0
        if sel0:
            UI.sel_bar(bx + 4, y - 2, bw - 8, 26)
        w = WEAPONS[st.equip]
        rank = st.weapons.get(st.equip)
        label = tt(w["name"]) + (f" {ROMAN[rank]}" if rank else "")
        font.text(bx + 10, y, f"{t('depart.equip')}:", UI.TEXT if sel0 else UI.SUB)
        y += 12
        icons.draw(st.equip, bx + 24, y - 2, w["col"])
        font.text(bx + 44, y, f"< {label} >" if sel0 else label, UI.ACCENT if sel0 else UI.TEXT)
        y += 14
        font.text(bx + 10, y, f"{t('depart.slots')} {st.slots} / {t('depart.pslots')} {st.passive_slots}   HP {int(st.hp)}/{st.maxhp}", UI.SUB); y += 13
        # 持ち物
        font.text(bx + 10, y, f"{t('depart.items')}:", UI.SUB)
        x = bx + 60
        for k in st.items:
            d = ITEMS[k]
            icons.draw(f"item_{k}", x, y - 3, d["col"])
            font.text(x + 19, y, tt(d["name"]), UI.TEXT)
            x += 22 + font.width(tt(d["name"])) + 6
        if not st.items:
            font.text(x, y, "-", UI.SUB)
        for i, key in enumerate(("depart.go", "depart.back")):
            yy = by + bh - 28 + i * 13
            sel = self.cursor == i + 1
            if sel:
                UI.sel_bar(bx + 4, yy - 2, bw - 8)
            font.center(yy, ("> " if sel else "") + t(key), UI.TEXT if sel else UI.SUB, bx + bw // 2)
        dx, dy, dw, dh = UI.DIALOG
        UI.window(dx, dy, dw, dh)
        font.text(dx + 10, dy + 8, t("town.d.depart"), UI.TEXT)
