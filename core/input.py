import pyxel

DEADZONE = 0.25
AXIS_MAX = 32767.0


class Input:
    """キー / パッドを move_x, move_y, confirm, cancel, pause に正規化する。"""

    def __init__(self):
        self.mx = 0.0
        self.my = 0.0
        self.confirm = False
        self.cancel = False
        self.pause = False
        self.up = self.down = self.left = self.right = False
        self.l = self.r = self.use = False

    def poll(self):
        btn, btnp = pyxel.btn, pyxel.btnp
        mx = my = 0.0
        if btn(pyxel.KEY_LEFT) or btn(pyxel.KEY_A) or btn(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT):
            mx -= 1
        if btn(pyxel.KEY_RIGHT) or btn(pyxel.KEY_D) or btn(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT):
            mx += 1
        if btn(pyxel.KEY_UP) or btn(pyxel.KEY_W) or btn(pyxel.GAMEPAD1_BUTTON_DPAD_UP):
            my -= 1
        if btn(pyxel.KEY_DOWN) or btn(pyxel.KEY_S) or btn(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN):
            my += 1
        if mx == 0 and my == 0:
            ax = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTX) / AXIS_MAX
            ay = pyxel.btnv(pyxel.GAMEPAD1_AXIS_LEFTY) / AXIS_MAX
            if ax * ax + ay * ay > DEADZONE * DEADZONE:
                mx, my = ax, ay
        d2 = mx * mx + my * my
        if d2 > 1.0:
            inv = d2 ** -0.5
            mx *= inv
            my *= inv
        self.mx, self.my = mx, my

        self.confirm = (
            btnp(pyxel.KEY_Z) or btnp(pyxel.KEY_RETURN) or btnp(pyxel.KEY_SPACE)
            or btnp(pyxel.GAMEPAD1_BUTTON_A)
        )
        self.cancel = btnp(pyxel.KEY_X) or btnp(pyxel.GAMEPAD1_BUTTON_B)
        self.pause = btnp(pyxel.KEY_ESCAPE) or btnp(pyxel.GAMEPAD1_BUTTON_START)

        # アイテム: L/R で選択、Y (キーボード C) で使用
        self.l = btnp(pyxel.GAMEPAD1_BUTTON_LEFTSHOULDER) or btnp(pyxel.KEY_Q)
        self.r = btnp(pyxel.GAMEPAD1_BUTTON_RIGHTSHOULDER) or btnp(pyxel.KEY_E)
        self.use = btnp(pyxel.GAMEPAD1_BUTTON_Y) or btnp(pyxel.KEY_C)

        # メニュー用 (押した瞬間 + 長押しリピート)
        hold, rep = 15, 5
        self.up = btnp(pyxel.KEY_UP, hold, rep) or btnp(pyxel.KEY_W, hold, rep) or btnp(pyxel.GAMEPAD1_BUTTON_DPAD_UP, hold, rep)
        self.down = btnp(pyxel.KEY_DOWN, hold, rep) or btnp(pyxel.KEY_S, hold, rep) or btnp(pyxel.GAMEPAD1_BUTTON_DPAD_DOWN, hold, rep)
        self.left = btnp(pyxel.KEY_LEFT, hold, rep) or btnp(pyxel.KEY_A, hold, rep) or btnp(pyxel.GAMEPAD1_BUTTON_DPAD_LEFT, hold, rep)
        self.right = btnp(pyxel.KEY_RIGHT, hold, rep) or btnp(pyxel.KEY_D, hold, rep) or btnp(pyxel.GAMEPAD1_BUTTON_DPAD_RIGHT, hold, rep)
