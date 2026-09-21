import pyxel

from config import W, H
from core import audio, save
from core import palette as P
from core.i18n import t, tt
from data.quests import QUESTS
from data.chapters import CHAPTERS, FINAL_CHAPTER, PART2_FINAL
from game import Scene
from ui import font
from ui.menu import draw_overlay, draw_panel


class ResultScene(Scene):
    overlay = True

    def __init__(self, game, play, win):
        super().__init__(game)
        self.play = play
        self.win = win
        self.t = 0
        self.story = play.quest is not None
        if self.story:
            self.settle()

    def settle(self):
        """帰還処理: お金・依頼・HP をセーブデータへ反映 (設計書 §2.2)。"""
        play = self.play
        st = play.state
        q = play.quest
        dead = play.outcome == "dead"
        self.gold_found = play.gold
        self.halved = dead
        if dead:
            self.gold_found = play.gold // 2
        self.quest_ok = play.cleared
        self.reward = 0
        if self.quest_ok:
            first = play.quest_id not in st.cleared
            self.first_clear = first
            self.reward = int(q["reward"] * (1.0 if first else 0.7))
            if first:
                st.cleared.append(play.quest_id)
                for m in q.get("magic", []):
                    if m not in st.magic:
                        st.magic.append(m)
                ch = CHAPTERS.get(st.chapter)
                if ch and ch["castle"] == play.quest_id:
                    if st.chapter == PART2_FINAL:
                        st.flags["pending_story"] = "ending2"
                    elif st.chapter == FINAL_CHAPTER:
                        st.flags["pending_story"] = "ending"
                    else:
                        for m in ch["magic"]:
                            if m not in st.magic:
                                st.magic.append(m)
                        st.flags["pending_story"] = f"castle_after_{st.chapter}"
                        st.chapter += 1
            st.quest = None
        elif play.outcome in ("retreat", "timeup"):
            st.quest = None          # 失敗: 受注し直せる
        st.gold += self.gold_found + self.reward
        st.items = list(play.player.items)      # 使った消耗品は戻らない
        # 熟練 EXP
        from core import growth
        boss_killed = any(k in play.kill_count for k in ("forest_lord", "boss1", "boss2", "knight"))
        self.exp_gain = growth.run_exp(play, self.quest_ok, getattr(self, "first_clear", False), boss_killed)
        self.hero_ups = growth.add_exp(st, self.exp_gain)
        # HP: 帰還時の値を持ち越し。50% 未満なら 50% に補正。戦闘不能は 50%
        # ラン中の最大 HP 増加 (生命の心臓) は持ち帰らない: 街の上限 (100) に丸める
        hp = 0 if dead else min(play.player.hp, st.maxhp)
        st.hp = max(hp, st.maxhp * 0.5)
        self.hp_after = st.hp
        save.save(st)

    def update(self):
        self.t += 1
        if self.t > 60 and self.inp.confirm:
            audio.se(audio.SE_SELECT)
            if self.story:
                from scenes.town import TownScene
                self.game.replace_fade(TownScene(self.game, self.play.state), length=60)
            else:
                from scenes.title import TitleScene
                self.game.replace_fade(TitleScene(self.game))

    def draw(self):
        draw_overlay(0.6)
        p = self.play.player
        if not self.story:
            pw, ph = 170, 100
            px, py = (W - pw) // 2, (H - ph) // 2
            draw_panel(px, py, pw, ph)
            font.center(py + 8, t("res.win") if self.win else t("res.lose"), P.GOLD if self.win else P.HP)
            sec = self.play.frame // 60
            font.center(py + 30, f"{t('res.time')}  {sec // 60:02d}:{sec % 60:02d}", 7)
            font.center(py + 44, f"{t('res.level')} {p.level}", 7)
            font.center(py + 58, f"{t('res.kills')} {p.kills}", 7)
            if self.t > 60 and (self.t // 30) % 2 == 0:
                font.center(py + 80, t("res.press"), 6)
            return
        pw, ph = 220, 164
        px, py = (W - pw) // 2, (H - ph) // 2
        draw_panel(px, py, pw, ph)
        dead = self.play.outcome == "dead"
        font.center(py + 8, t("res.dead") if dead else t("res.return"), P.HP if dead else P.GOLD)
        font.center(py + 24, t("res.quest_ok") if self.quest_ok else t("res.quest_ng"), P.GOLD if self.quest_ok else 14)
        y = py + 44
        sec = self.play.frame // 60
        font.text(px + 12, y, f"{t('res.time')}  {sec // 60:02d}:{sec % 60:02d}    {t('res.kills')} {p.kills}", 7); y += 14
        font.text(px + 12, y, f"{t('res.gold')}", 7)
        font.right(y, f"{self.gold_found} G" + (f" {t('res.halved')}" if self.halved else ""), P.GOLD if not self.halved else 14, px + pw - 12); y += 14
        font.text(px + 12, y, f"{t('res.reward')}", 7)
        font.right(y, f"{self.reward} G", P.GOLD, px + pw - 12); y += 14
        font.text(px + 12, y, t("res.hp"), 7)
        font.right(y, f"{int(self.hp_after)}/{self.play.state.maxhp}", 7, px + pw - 12); y += 14
        from core import growth
        if growth.enabled(self.play.state):
            font.text(px + 12, y, t("res.exp"), 7)
            ups = f"  {t('res.hero_up')} Lv{self.play.state.hero_lv}" if self.hero_ups else ""
            font.right(y, f"+{self.exp_gain}{ups}", P.ACCENT if self.hero_ups else 7, px + pw - 12); y += 14
        y += 4
        if self.t > 60 and (self.t // 30) % 2 == 0:
            font.center(y + 6, t("res.to_town"), 6)
