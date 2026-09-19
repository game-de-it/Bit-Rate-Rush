"""UI 用フォント (M+ 10px BDF)。pyxel.init 後に load() すること。"""
import os

import pyxel

from config import W

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "umplus_j10r.bdf")
FONT = None
LINE = 12   # 行送り


def load():
    global FONT
    FONT = pyxel.Font(PATH)


def text(x, y, s, col):
    pyxel.text(x, y, s, col, FONT)


def width(s):
    return FONT.text_width(s)


def center(y, s, col, x=W // 2):
    pyxel.text(x - width(s) // 2, y, s, col, FONT)


def right(y, s, col, x=W - 2):
    pyxel.text(x - width(s), y, s, col, FONT)
