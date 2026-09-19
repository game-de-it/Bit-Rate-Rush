"""拡張パレット (assets/brr.pyxpal, 64 色)。0〜15 は Pyxel 標準、16〜31 がゲーム用の追加色、32〜63 は画像 (立ち絵・背景) 用の補完色。

背景は暗い低彩度 (16〜18)、敵は高彩度 + 縁取り (19) で床から浮かせる。
"""
import os

import pyxel

# --- 背景 ---
FLOOR = 16          # 床ベース (暗い青灰)
FLOOR_DARK = 17     # 床の模様 (暗)
FLOOR_LIGHT = 18    # 床の模様 (明)
OUTLINE = 19        # 縁取り (0 は透過キーなので使わない)
# --- 敵 ---
ZOMBIE = 20
ZOMBIE_DARK = 21
BAT = 22
BONE = 23
BRUTE = 24
BRUTE_LIGHT = 25
BOSS = 26
BOSS_DARK = 27
# --- UI ---
ACCENT = 28         # XP バー / 選択カーソル
PANEL = 29          # パネル背景
GOLD = 30           # 見出し
HP = 31             # HP バー

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "brr.pyxpal")


def load():
    pyxel.load_pal(PATH)
