"""武器屋 / 雑貨屋。右エリアに商品一覧、下窓に店主の立ち絵 + 説明。"""
import pyxel

from core import audio, images, save
from core.i18n import t, tt
from data.items import ITEMS, MAX_ITEMS, stock as item_stock
from core import growth
from data.story import bg_name
from data.shop import WEAPON_STOCK, RANK_COST, MAX_RANK, stock as weapon_stock
from data.weapons import WEAPONS
from game import Scene
from ui import font, icons
from ui import window as UI

ROW = 16
ROMAN = {1: "I", 2: "II", 3: "III", 4: "IV"}


class ShopScene(Scene):
    overlay = True
    kind = "smith"          # "smith" | "shop"

    def __init__(self, game, state):
        super().__init__(game)
        self.state = state
        self.cursor = 0
        self.msg = None
        self.msg_t = 0

    # --- 商品 ---
    def entries(self):
        st = self.state
        if self.kind == "smith":
            out = []
            for k in weapon_stock(st):
                if k in st.weapons:
                    r = st.weapons[k]
                    if r < MAX_RANK:
                        out.append(("rank", k, int(RANK_COST[r + 1] * growth.discount(self.state))))
                    else:
                        out.append(("max", k, 0))
                else:
                    out.append(("buy", k, WEAPON_STOCK[k]["price"]))
            # 所持中でまだ品揃えに無い武器 (ナイフ) の強化も出す
            for k, r in st.weapons.items():
                if k not in WEAPON_STOCK:
                    out.insert(0, ("rank", k, int(RANK_COST[r + 1] * growth.discount(self.state))) if r < MAX_RANK else ("max", k, 0))
            return out
        return [("item", k, ITEMS[k]["price"]) for k in item_stock(st)]

    def enter(self):
        audio.bgm(self.kind)
        from scenes.dialog import DialogScene
        from data.story import resolve
        self.game.push(DialogScene(self.game, resolve(self.state, f"{self.kind}_hello")))

    def say(self, key):
        self.msg = t(key)
        self.msg_t = 90

    def update(self):
        inp = self.inp
        if self.msg_t > 0:
            self.msg_t -= 1
        ents = self.entries()
        if inp.cancel or inp.pause:
            save.save(self.state)
            self.game.pop_facility()
            return
        if not ents:
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % len(ents)
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(ents)
            audio.se(audio.SE_SELECT)
        self.cursor = min(self.cursor, len(ents) - 1)
        if inp.confirm:
            self.buy(ents[self.cursor])

    def buy(self, ent):
        st = self.state
        act, k, price = ent
        if act == "max":
            self.say("shop.max")
            return
        if act == "item" and len(st.items) >= MAX_ITEMS:
            self.say("shop.full")
            audio.se(audio.SE_HURT)
            return
        if st.gold < price:
            self.say("shop.poor")
            audio.se(audio.SE_HURT)
            return
        st.gold -= price
        if act == "buy":
            st.weapons[k] = 1
            self.say("shop.bought")
        elif act == "rank":
            st.weapons[k] += 1
            self.say("shop.ranked")
        else:
            st.items.append(k)
            self.say("shop.bought")
        audio.se(audio.SE_LEVELUP)
        save.save(st)

    def draw(self):
        from scenes.dialog import DialogScene
        town = self.game.stack[0]
        town.draw_base(show_bg=False)
        st = self.state
        bx, by, bw, bh = UI.BG
        if isinstance(self.game.stack[-1], DialogScene):
            # 会話中は店の風景
            if not images.draw(bg_name(self.state, f"{self.kind}_bg"), bx, by):
                UI.window(bx, by, bw, bh)
            return
        UI.window(bx, by, bw, bh)
        title = t("town.smith") if self.kind == "smith" else t("town.shop")
        font.center(by + 5, title, UI.ACCENT, bx + bw // 2)
        font.right(by + 5, f"{st.gold}G", UI.GOLD, bx + bw - 8)
        ents = self.entries()
        for i, (act, k, price) in enumerate(ents):
            y = by + 21 + i * ROW
            sel = i == self.cursor
            if sel:
                UI.sel_bar(bx + 4, y - 3, bw - 8, ROW - 1)
            if act == "item":
                d = ITEMS[k]
                icons.draw(f"item_{k}", bx + 6, y - 3, d["col"])
                n = st.items.count(k)
                font.text(bx + 26, y, tt(d["name"]) + (f" x{n}" if n else ""), UI.TEXT if sel else UI.SUB)
                font.right(y, f"{price}G", UI.GOLD, bx + bw - 8)
            else:
                w = WEAPONS[k]
                icons.draw(k, bx + 6, y - 3, w["col"])
                name = tt(w["name"])
                if act == "buy":
                    label = f"{name}  [{t('shop.buy')}]"
                    right = f"{price}G"
                elif act == "rank":
                    r = st.weapons[k]
                    label = f"{name}  {ROMAN[r]} > {ROMAN[r + 1]}"
                    right = f"{price}G"
                else:
                    label = f"{name}  {ROMAN[MAX_RANK]} ({t('shop.maxed')})"
                    right = "-"
                font.text(bx + 26, y, label, UI.TEXT if sel else UI.SUB)
                font.right(y, right, UI.GOLD, bx + bw - 8)
        if self.kind == "shop":
            font.right(by + bh - 14, f"{t('shop.bag')} {len(st.items)}/{MAX_ITEMS}", UI.SUB, bx + bw - 8)
        # 下窓: 店主 + 説明
        dx, dy, dw, dh = UI.DIALOG
        UI.window(dx, dy, dw, dh)
        tx = dx + 10
        npc = bg_name(self.state, "npc_smith" if self.kind == "smith" else "npc_shop")
        if images.draw(npc, dx + 3, dy + 1):
            tx = dx + 3 + 64 + 8
        if self.msg and self.msg_t > 0:
            font.text(tx, dy + 8, self.msg, UI.ACCENT)
        elif ents:
            act, k, price = ents[self.cursor]
            if act == "item":
                font.text(tx, dy + 8, tt(ITEMS[k]["desc"]), UI.TEXT)
            else:
                font.text(tx, dy + 8, tt(WEAPONS[k]["desc"]), UI.TEXT)
                if act == "rank":
                    font.text(tx, dy + 22, t("shop.rank_desc"), UI.SUB)
        font.right(dy + dh - 13, t("shop.hint"), UI.SUB, dx + dw - 8)


class SmithScene(ShopScene):
    kind = "smith"


class ItemShopScene(ShopScene):
    kind = "shop"
