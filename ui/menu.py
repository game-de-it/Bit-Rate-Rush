import pyxel

from config import W, H
from core import palette as P
from ui import font

text_center = font.center


def draw_overlay(alpha=0.5):
    """画面を暗くする。"""
    pyxel.camera()
    pyxel.dither(alpha)
    pyxel.rect(0, 0, W, H, 0)
    pyxel.dither(1.0)


def draw_panel(x, y, w, h, border=7, fill=P.PANEL):
    pyxel.rect(x, y, w, h, fill)
    pyxel.rectb(x, y, w, h, border)
