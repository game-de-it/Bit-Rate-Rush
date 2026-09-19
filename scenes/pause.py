import pyxel

from config import W, H, DEBUG_PAUSE_TOOLS
from core import audio, debug, save
from core import palette as P
from core.i18n import t, tt
from data.enemies import ENEMIES
from game import Scene
from ui import font
from ui.menu import draw_overlay, draw_panel

DEBUG_ITEMS = ["dbg.easy", "dbg.nolevel", "dbg.time"]
ROW = 16


class PauseScene(Scene):
    overlay = True

    def __init__(self, game, play):
        super().__init__(game)
        self.play = play
        self.cursor = 0
        items = ["pause.resume"]
        if play.quest:
            items.append("pause.return" if play.cleared else "pause.retreat")
        items += ["pause.options", "pause.title_back", "pause.exit"]
        if DEBUG_PAUSE_TOOLS:
            items += DEBUG_ITEMS
        self.items = items

    def update(self):
        inp = self.inp
        if inp.pause or inp.cancel:
            self.game.pop()
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % len(self.items)
            audio.se(audio.SE_SELECT)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(self.items)
            audio.se(audio.SE_SELECT)
        key = self.items[self.cursor]
        if key == "dbg.easy":
            if inp.confirm or inp.left or inp.right:
                debug.easy_levelup = not debug.easy_levelup
                p = self.play.player
                p.xp_next = p.need_xp(p.level)
                audio.se(audio.SE_SELECT)
            return
        if key == "dbg.nolevel":
            if inp.confirm or inp.left or inp.right:
                self.play.no_levelup = not self.play.no_levelup
                audio.se(audio.SE_SELECT)
            return
        if key == "dbg.time":
            minutes = self.play.frame // 3600
            if inp.left or inp.right:
                minutes = max(0, min(15, minutes + (1 if inp.right else -1)))
                self.play.frame = minutes * 3600
                audio.se(audio.SE_SELECT)
            return
        if inp.confirm:
            audio.se(audio.SE_SELECT)
            if key == "pause.resume":
                self.game.pop()
            elif key == "pause.options":
                from scenes.options import OptionsScene
                self.game.push(OptionsScene(self.game, in_battle=True))
            elif key == "pause.return":
                self.game.pop()
                self.play.finish("return")
            elif key == "pause.retreat":
                self.game.pop()
                self.play.finish("retreat")
            elif key == "pause.title_back":
                from scenes.title import TitleScene
                self.game.replace_fade(TitleScene(self.game))
            else:
                pyxel.quit()

    def draw(self):
        draw_overlay(0.5)
        pw, ph = 200, 24 + ROW * len(self.items) + 6
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 6, t("pause.title"), P.GOLD)
        if DEBUG_PAUSE_TOOLS:
            # 右側に敵種ごとの撃破数と経過時間
            kx, ky = px + pw + 4, py
            kw = W - kx - 4
            draw_panel(kx, ky, kw, ph)
            sec = self.play.frame // 60
            font.text(kx + 4, ky + 4, f"DBG {sec // 60}:{sec % 60:02d}", P.GOLD)
            y = ky + 18
            for kind, n in sorted(self.play.kill_count.items(), key=lambda kv: -kv[1]):
                font.text(kx + 4, y, tt(ENEMIES[kind]["name"]), 6)
                font.right(y, str(n), 7, kx + kw - 4)
                y += 12
                if y > ky + ph - 12:
                    break
            font.text(kx + 4, ky + ph - 13, f"Lv{self.play.player.level} 計{self.play.player.kills}", 13)
        for i, key in enumerate(self.items):
            y = py + 24 + i * ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 2, pw - 8, ROW - 2, 5)
                font.text(px + 8, y, ">", P.ACCENT)
            if key == "dbg.easy":
                font.text(px + 18, y, "DBG 簡単レベルアップ", 13 if not sel else 7)
                font.right(y, "ON" if debug.easy_levelup else "OFF", P.GOLD if debug.easy_levelup else 6, px + pw - 10)
            elif key == "dbg.nolevel":
                font.text(px + 18, y, "DBG レベルアップ停止", 13 if not sel else 7)
                font.right(y, "ON" if self.play.no_levelup else "OFF", P.HP if self.play.no_levelup else 6, px + pw - 10)
            elif key == "dbg.time":
                font.text(px + 18, y, "DBG 時間", 13 if not sel else 7)
                font.right(y, f"< {self.play.frame // 3600:2d}分 >", P.ACCENT if sel else 6, px + pw - 10)
            else:
                col = 7 if sel else 6
                if key == "pause.retreat":
                    col = P.HP if sel else 14
                font.center(y, t(key), col)


class TownPauseScene(Scene):
    """街でのメニュー: タイトルへ / 終了。"""
    overlay = True
    ITEMS = ["pause.resume", "pause.title_back", "pause.exit"]

    def __init__(self, game, town):
        super().__init__(game)
        self.town = town
        self.cursor = 0

    def update(self):
        inp = self.inp
        if inp.pause or inp.cancel:
            self.game.pop()
            return
        if inp.up:
            self.cursor = (self.cursor - 1) % len(self.ITEMS)
        if inp.down:
            self.cursor = (self.cursor + 1) % len(self.ITEMS)
        if inp.confirm:
            audio.se(audio.SE_SELECT)
            key = self.ITEMS[self.cursor]
            if key == "pause.resume":
                self.game.pop()
            elif key == "pause.title_back":
                save.save(self.town.state)
                from scenes.title import TitleScene
                self.game.replace_fade(TitleScene(self.game))
            else:
                save.save(self.town.state)
                pyxel.quit()

    def draw(self):
        draw_overlay(0.5)
        pw, ph = 150, 24 + ROW * len(self.ITEMS) + 6
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        font.center(py + 6, t("pause.title"), P.GOLD)
        for i, key in enumerate(self.ITEMS):
            y = py + 24 + i * ROW
            sel = i == self.cursor
            if sel:
                pyxel.rect(px + 4, y - 2, pw - 8, ROW - 2, 5)
            font.center(y, t(key), 7 if sel else 6)
