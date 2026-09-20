import os

import pyxel

BGM_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "bgm")
BGM_BASE = 16          # BGM 用サウンドスロット 16〜
_bgm_slot = {}         # 曲名 → サウンド番号 (読み込み済み)
_bgm_now = None

BGM_VOL_DEFAULT = 7    # 0〜10。ch0 の gain = v/10 (Pyxel 既定は 0.125)
SE_VOL_DEFAULT = 5     # 0〜10。ch1〜3 の gain = v/10 * 0.3
_vol = {"bgm": BGM_VOL_DEFAULT, "battle": BGM_VOL_DEFAULT, "se": SE_VOL_DEFAULT}
_bgm_is_battle = False


def set_volume(bgm_v, se_v, battle_v=None):
    _vol["bgm"] = max(0, min(10, bgm_v))
    _vol["se"] = max(0, min(10, se_v))
    if battle_v is not None:
        _vol["battle"] = max(0, min(10, battle_v))
    _apply_bgm_gain()
    for ch in (1, 2, 3):
        pyxel.channels[ch].gain = _vol["se"] / 10.0 * 0.3


def _apply_bgm_gain():
    pyxel.channels[0].gain = (_vol["battle"] if _bgm_is_battle else _vol["bgm"]) / 10.0


def battle_tracks():
    """assets/bgm/battle*.mp3 の曲名 (拡張子なし) を番号順に。"""
    try:
        names = sorted(f[:-4] for f in os.listdir(BGM_DIR) if f.startswith("battle") and f.endswith(".mp3"))
    except Exception:
        names = []
    return names


def track_title(name):
    """表示名: ID3 の曲名があればそれ、無ければファイル名。"""
    from core.mp3tag import title
    t = title(os.path.join(BGM_DIR, f"{name}.mp3"))
    return t or name


SE_HIT, SE_KILL, SE_PICKUP, SE_HURT, SE_LEVELUP, SE_SELECT, SE_ZAP, SE_BOSS = range(8)

_se_ch = 1
_pickup_frame = -10


def setup():
    s = pyxel.sounds
    s[SE_HIT].set("a2", "n", "3", "f", 3)
    s[SE_KILL].set("c2", "n", "5", "f", 5)
    s[SE_PICKUP].set("c4e4", "p", "3", "n", 3)
    s[SE_HURT].set("c1", "n", "7", "f", 8)
    s[SE_LEVELUP].set("c3e3g3c4", "s", "6", "n", 6)
    s[SE_SELECT].set("e3", "t", "5", "n", 4)
    s[SE_ZAP].set("c4c1", "n", "6", "f", 4)
    s[SE_BOSS].set("c1c1g1", "s", "7", "f", 10)


def se(n):
    """効果音。ch1〜3 をローテーションして鳴らす (ch0 は BGM 用)。"""
    global _se_ch
    pyxel.play(_se_ch, n)
    _se_ch = 1 + (_se_ch % 3)


def pickup():
    global _pickup_frame
    if pyxel.frame_count - _pickup_frame >= 4:
        _pickup_frame = pyxel.frame_count
        pyxel.play(3, SE_PICKUP)


def bgm(name, battle=False, loop=True):
    """assets/bgm/<name>.mp3 を ch0 で再生 (既定はループ)。同じ曲なら何もしない。初回のみデコード (実機で ~1 秒)。
    battle=True なら戦闘 BGM の音量を使う。loop=False は戦闘のプレイリスト再生用 (曲が終わったら呼び出し側が次を選ぶ)。"""
    global _bgm_now, _bgm_is_battle
    if name == _bgm_now:
        if battle != _bgm_is_battle:
            _bgm_is_battle = battle
            _apply_bgm_gain()
        return
    if name is None:
        bgm_stop()
        return
    # 先に今の曲を止めてからデコードする。デコード中 (実機で ~1 秒) は音声が更新されないので、
    # 鳴らしたままだと Web 版で「ブブブ」というバッファ切れのノイズになる
    bgm_stop()
    slot = _load(name)
    if slot is None:
        return
    _bgm_is_battle = battle
    _apply_bgm_gain()
    pyxel.play(0, slot, loop=loop)
    _bgm_now = name


def _load(name):
    """曲をデコードしてサウンド番号を返す (キャッシュ済みならそのまま)。無い / 失敗なら None。実機で 1 曲 ~1 秒かかる"""
    slot = _bgm_slot.get(name)
    if slot is not None:
        return slot
    path = os.path.join(BGM_DIR, f"{name}.mp3")
    if not os.path.exists(path):
        return None
    slot = BGM_BASE + len(_bgm_slot)
    try:
        pyxel.sounds[slot].pcm(path)
    except Exception:
        return None
    _bgm_slot[name] = slot
    return slot


def jingle(name):
    """ch0 で 1 回だけ再生 (ループなし)。BGM は止まる。"""
    global _bgm_now
    bgm_stop()
    slot = _load(name)
    if slot is None:
        return False
    pyxel.channels[0].gain = _vol["bgm"] / 10.0
    pyxel.play(0, slot, loop=False)
    _bgm_now = None
    return True


def playing():
    """ch0 が再生中か。"""
    return pyxel.play_pos(0) is not None


def bgm_stop():
    global _bgm_now
    pyxel.stop(0)
    _bgm_now = None
