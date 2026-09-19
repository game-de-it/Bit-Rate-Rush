"""街・会話で使う白いウィンドウ (参考デザイン: 紺のフレーム + 角丸の白い窓)。"""
import pyxel

from config import W, H
from core import palette as P

FRAME = P.PANEL        # 画面全体のフレーム色 (紺)
WIN_BG = 7             # 窓の地
WIN_BORDER = 1         # 窓の縁 (紺)
TEXT = P.OUTLINE       # 窓の文字 (ほぼ黒)
SUB = 13               # 補助文字 (灰)
SEL = 6                # 選択行の帯 (水色)
ACCENT = 5             # 強調 (青)
GOLD = 4               # 金額 (茶 — 白地で読める)

# 街画面のレイアウト (x, y, w, h)
MENU = (6, 6, 68, 156)
BG = (80, 6, 234, 156)
DIALOG = (6, 168, 308, 66)


def frame():
    pyxel.camera()
    pyxel.cls(FRAME)


def window(x, y, w, h, fill=WIN_BG, border=WIN_BORDER):
    """角丸 (半径 2) の窓。"""
    pyxel.rect(x + 2, y, w - 4, h, fill)
    pyxel.rect(x, y + 2, w, h - 4, fill)
    pyxel.pset(x + 1, y + 1, fill)
    pyxel.pset(x + w - 2, y + 1, fill)
    pyxel.pset(x + 1, y + h - 2, fill)
    pyxel.pset(x + w - 2, y + h - 2, fill)
    # 縁
    pyxel.line(x + 2, y, x + w - 3, y, border)
    pyxel.line(x + 2, y + h - 1, x + w - 3, y + h - 1, border)
    pyxel.line(x, y + 2, x, y + h - 3, border)
    pyxel.line(x + w - 1, y + 2, x + w - 1, y + h - 3, border)
    pyxel.pset(x + 1, y + 1, border)
    pyxel.pset(x + w - 2, y + 1, border)
    pyxel.pset(x + 1, y + h - 2, border)
    pyxel.pset(x + w - 2, y + h - 2, border)


def sel_bar(x, y, w, h=12):
    pyxel.rect(x, y, w, h, SEL)
