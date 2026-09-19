"""プロトタイプ用スプライトを起動時に画像バンク 0 へ描画する (pyxres なし)。

配置 (u, v, w, h):
  PLAYER (0, 0, 16, 16)
  BAT (16, 0, 8, 8)   ZOMBIE (24, 0, 8, 8)
  GHOST (16, 8, 8, 8) SKULL (24, 8, 8, 8)
  BRUTE (32, 0, 16, 16)
  BOSS (48, 0, 32, 32)
  GEM_S (0, 16, 8, 8) GEM_M (8, 16, 8, 8) GEM_L (16, 16, 8, 8)
  HEAL (24, 16, 8, 8) MAGNET (32, 16, 8, 8)
全ての敵は OUTLINE 色で 1px 縁取りし、床 (暗色) から浮かせる。
"""
import pyxel

from core import palette as P

PLAYER = (0, 0, 16, 16)
BAT = (16, 0, 16, 16)
ZOMBIE = (32, 0, 16, 16)
GHOST = (48, 0, 16, 16)
SKULL = (64, 0, 16, 16)
BRUTE = (80, 0, 16, 16)
BOSS = (96, 0, 32, 32)
GEM_S = (0, 32, 8, 8)
GEM_M = (8, 32, 8, 8)
GEM_L = (16, 32, 8, 8)
HEAL = (24, 32, 12, 12)
MAGNET = (36, 32, 12, 12)
COIN = (48, 32, 8, 8)
# 飛び道具 (全て右向き。blt の rotate で進行方向へ回す)
KNIFE = (0, 48, 8, 8)
ARROW = (8, 48, 8, 8)
SPEAR = (16, 48, 16, 8)
AXE = (32, 48, 12, 12)
SICKLE = (44, 48, 10, 10)
HAMMER = (56, 48, 12, 12)
BOOMERANG = (68, 48, 8, 8)
SHURIKEN = (76, 48, 8, 8)

COLKEY = 0
O = P.OUTLINE


def _outline(img, u, v, w, h):
    """矩形内の非透明ピクセルの周囲 (透明部分) を縁取り色で塗る。"""
    solid = [[img.pget(u + x, v + y) != COLKEY for x in range(w)] for y in range(h)]
    for y in range(h):
        for x in range(w):
            if solid[y][x]:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and solid[ny][nx]:
                    img.pset(u + x, v + y, O)
                    break


def build():
    img = pyxel.images[0]
    img.cls(0)

    # player: 肌色の頭 + シアンの体
    img.rect(5, 2, 6, 5, 15)
    img.pset(6, 4, 1)
    img.pset(9, 4, 1)
    img.rect(4, 7, 8, 6, 12)
    img.rect(5, 13, 2, 2, 1)
    img.rect(9, 13, 2, 2, 1)
    _outline(img, *PLAYER)

    # bat: 左右に広げた羽 (明るい紫) + 暗い紫の体 + ピンクの目
    _pixels(img, BAT[0], BAT[1], [
        "................",
        ".W............W.",
        ".WW..........WW.",
        ".WWW........WWW.",
        ".WWWW..BB..WWWW.",
        ".WWWWWBEEBWWWWW.",
        "..WWWWBEEBWWWW..",
        "...WWWBBBBWWW...",
        "....WWBBBBWW....",
        ".....WBBBBW.....",
        "......BBBB......",
        ".......BB.......",
        ".......BB.......",
        "................",
        "................",
        "................",
    ], {"W": P.BAT, "B": 2, "E": 14})
    _outline(img, *BAT)

    # zombie: 明るい黄緑の体 + 暗緑の影 + 黒目
    _pixels(img, ZOMBIE[0], ZOMBIE[1], [
        "................",
        "....GGGGGGGG....",
        "...GGGGGGGGGG...",
        "...GGOOGGGGOOG..",
        "...GGOOGGGGOOG..",
        "...GGGGGGGGGG...",
        "...GGGDDDDDGG...",
        "...GGGGGGGGGG...",
        "....GGGGGGGG....",
        "..DDGGGGGGGGDD..",
        "..DDGGGGGGGGDD..",
        "....DDDDDDDD....",
        "....DDDDDDDD....",
        "....DD....DD....",
        "....DD....DD....",
        "................",
    ], {"G": P.ZOMBIE, "D": P.ZOMBIE_DARK, "O": O})
    _outline(img, *ZOMBIE)

    # ghost: 水色の丸に目、裾がギザギザ
    _pixels(img, GHOST[0], GHOST[1], [
        "................",
        ".....LLLLLL.....",
        "....LLLLLLLL....",
        "...LLLLLLLLLL...",
        "...LLLLLLLLLL...",
        "...LLOOLLLOOL...",
        "...LLOOLLLOOL...",
        "...LLLLLLLLLL...",
        "...LLLLLLLLLL...",
        "...LLLLLLLLLL...",
        "...LLLLLLLLLL...",
        "...LLLLLLLLLL...",
        "...LL.LLLL.LL...",
        "...L...LL...L...",
        "................",
        "................",
    ], {"L": 6, "O": 1})
    _outline(img, *GHOST)

    # skull: 骨色のドクロ
    _pixels(img, SKULL[0], SKULL[1], [
        "................",
        ".....KKKKKK.....",
        "....KKKKKKKK....",
        "...KKKKKKKKKK...",
        "...KKKKKKKKKK...",
        "...KOOKKKKOOK...",
        "...KOOKKKKOOK...",
        "...KKKKKKKKKK...",
        "....KKKOOKKK....",
        "....KKKKKKKK....",
        ".....KOKOKO.....",
        ".....KKKKKK.....",
        "................",
        "................",
        "................",
        "................",
    ], {"K": P.BONE, "O": O})
    _outline(img, *SKULL)

    # brute: 茶色の大きい塊
    u, v = BRUTE[0], BRUTE[1]
    img.rect(u + 2, v + 2, 12, 12, P.BRUTE)
    img.rect(u + 4, v + 4, 8, 3, P.BRUTE_LIGHT)
    img.rect(u + 5, v + 5, 2, 1, O)
    img.rect(u + 9, v + 5, 2, 1, O)
    img.rect(u + 4, v + 10, 8, 2, P.BOSS_DARK)
    _outline(img, *BRUTE)

    # boss: 赤い巨大な塊 + 角
    u, v = BOSS[0], BOSS[1]
    img.circ(u + 16, v + 17, 13, P.BOSS)
    img.circ(u + 16, v + 21, 9, P.BOSS_DARK)
    img.tri(u + 4, v + 2, u + 10, v + 2, u + 8, v + 10, P.GOLD)
    img.tri(u + 27, v + 2, u + 21, v + 2, u + 23, v + 10, P.GOLD)
    img.rect(u + 9, v + 12, 5, 4, P.GOLD)
    img.rect(u + 18, v + 12, 5, 4, P.GOLD)
    img.rect(u + 10, v + 22, 12, 3, O)
    _outline(img, *BOSS)

    # gems
    _gem(img, 0, 32, P.ACCENT, 7)
    _gem(img, 8, 32, 11, 7)
    _gem(img, 16, 32, P.HP, 14)
    # heal: 白丸に赤十字 (12x12)
    u, v = HEAL[0], HEAL[1]
    img.circ(u + 6, v + 6, 5, 7)
    img.rect(u + 5, v + 2, 3, 9, P.BOSS)
    img.rect(u + 2, v + 5, 9, 3, P.BOSS)
    _outline(img, *HEAL)
    # magnet: 黄色 U (12x12)
    u, v = MAGNET[0], MAGNET[1]
    img.rect(u + 2, v + 1, 3, 8, P.GOLD)
    img.rect(u + 8, v + 1, 3, 8, P.GOLD)
    img.rect(u + 2, v + 8, 9, 3, P.GOLD)
    img.rect(u + 2, v + 1, 3, 2, 7)
    img.rect(u + 8, v + 1, 3, 2, 7)
    _outline(img, *MAGNET)
    # coin: 金貨
    u, v = COIN[0], COIN[1]
    img.circ(u + 3, v + 3, 3, P.GOLD)
    img.pset(u + 2, v + 2, 7)
    img.rect(u + 3, v + 2, 1, 3, P.BRUTE)
    _outline(img, *COIN)

    # ---- 飛び道具 (右向き) ----
    # ナイフ: 木の柄 + 白い刃
    _pixels(img, KNIFE[0], KNIFE[1], [
        "........",
        "........",
        "HH..777.",
        "HH777777",
        "HH..777.",
        "........",
        "........",
        "........",
    ], {"H": P.BRUTE, "7": 7})
    # 矢: 赤い羽 + 茶色の軸 + 白い鏃
    _pixels(img, ARROW[0], ARROW[1], [
        "........",
        "........",
        "R......7",
        "RRSSSS77",
        "R......7",
        "........",
        "........",
        "........",
    ], {"R": P.BOSS, "S": P.BRUTE_LIGHT, "7": 7})
    # 槍: 長い柄 + 鋼の穂先
    _pixels(img, SPEAR[0], SPEAR[1], [
        "................",
        "................",
        "............77..",
        "SSSSSSSSSSSS7777",
        "............77..",
        "................",
        "................",
        "................",
    ], {"S": P.BRUTE, "7": 7})
    # 斧: 柄 + 鋼の刃 (回転させて使う)
    _pixels(img, AXE[0], AXE[1], [
        "......7777..",
        ".....777777.",
        ".....777777.",
        ".....777777.",
        "....H.7777..",
        "....H..77...",
        "...H........",
        "...H........",
        "..H.........",
        "..H.........",
        ".H..........",
        "H...........",
    ], {"H": P.BRUTE, "7": 7})
    # 鎌の刃 (鎖鎌の先端)
    _pixels(img, SICKLE[0], SICKLE[1], [
        "...7777...",
        "..77..77..",
        ".77....77.",
        ".7......7.",
        "77........",
        "77........",
        ".77.......",
        "..7.HH....",
        ".....HH...",
        "......HH..",
    ], {"H": P.BRUTE, "7": 7})
    # ハンマー頭 (振り下ろし演出用)
    _pixels(img, HAMMER[0], HAMMER[1], [
        "............",
        "..GGGGGGGG..",
        ".GGGGGGGGGG.",
        ".GGGGGGGGGG.",
        ".GGGGGGGGGG.",
        "..GGGGGGGG..",
        ".....HH.....",
        ".....HH.....",
        ".....HH.....",
        ".....HH.....",
        ".....HH.....",
        "............",
    ], {"G": 13, "H": P.BRUTE})
    # ブーメラン: くの字
    _pixels(img, BOOMERANG[0], BOOMERANG[1], [
        "LL......",
        "LLL.....",
        ".LLL....",
        "..LLL...",
        "...LLL..",
        "....LLLL",
        ".....LLL",
        "........",
    ], {"L": P.BRUTE_LIGHT})
    # 手裏剣: 四方の刃
    _pixels(img, SHURIKEN[0], SHURIKEN[1], [
        "...7....",
        "...77...",
        "7..77...",
        "77777777",
        "...7O.77",
        "...77..7",
        "...7....",
        "........",
    ], {"7": 13, "O": 7})


def _pixels(img, u, v, rows, colors):
    """文字のドット絵を描く。'.' は透明のまま。"""
    for y, row in enumerate(rows):
        for x, ch in enumerate(row):
            if ch != ".":
                img.pset(u + x, v + y, colors[ch])


def _gem(img, u, v, col, hi):
    img.tri(u + 3, v + 1, u + 1, v + 4, u + 3, v + 7, col)
    img.tri(u + 4, v + 1, u + 6, v + 4, u + 4, v + 7, col)
    img.pset(u + 3, v + 2, hi)
    _outline(img, u, v, 8, 8)
