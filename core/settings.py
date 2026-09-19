"""設定 (言語など) の永続化。user_data_dir/settings.json。"""
import json
import os

import pyxel

from core import i18n

_data = {"lang": "en", "bgm": 7, "se": 5, "battle_vol": 7, "battle_mode": "shuffle", "battle_track": "", "battle_seq": 0}


def _path():
    try:
        d = pyxel.user_data_dir("kroot", "Bit-Rate-Rush")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, "settings.json")
    except Exception:
        return None


def load():
    p = _path()
    if p and os.path.exists(p):
        try:
            with open(p, "r", encoding="utf-8") as f:
                _data.update(json.load(f))
        except Exception:
            pass
    i18n.set_lang(_data.get("lang", "en"))
    apply_volume()


def save():
    p = _path()
    if not p:
        return
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(_data, f, ensure_ascii=False, indent=1)
    except Exception:
        pass


def get(key, default=None):
    return _data.get(key, default)


def set(key, value):
    _data[key] = value
    if key == "lang":
        i18n.set_lang(value)
    elif key in ("bgm", "se", "battle_vol"):
        apply_volume()


def apply_volume():
    from core import audio
    audio.set_volume(_data.get("bgm", 7), _data.get("se", 5), _data.get("battle_vol", 7))


def pick_battle_track(advance=True):
    """設定に従って戦闘曲を選ぶ。shuffle: 直前と違う曲をランダム / sequence: 順番 (advance で次へ) / それ以外: 指定曲。"""
    import random
    from core import audio
    tracks = audio.battle_tracks()
    if not tracks:
        return "battle01"
    mode = _data.get("battle_mode", "shuffle")
    if mode == "sequence":
        i = _data.get("battle_seq", 0) % len(tracks)
        if advance:
            _data["battle_seq"] = (i + 1) % len(tracks)
            save()
        return tracks[i]
    if mode == "select":
        t = _data.get("battle_track") or tracks[0]
        return t if t in tracks else tracks[0]
    # シャッフル: 全曲を 1 巡してから次の巡へ (バッグ方式)。巡の境目でも同じ曲が続かないようにする
    last = _data.get("battle_last")
    if not advance:
        # 試聴など: 巡の状態を進めずに、直前と違う曲を 1 つ返す
        cands = [t for t in tracks if t != last] or tracks
        return random.choice(cands)
    bag = [t for t in _data.get("battle_bag", []) if t in tracks]
    if not bag:
        bag = list(tracks)
        random.shuffle(bag)
        if len(bag) > 1 and bag[-1] == last:      # pop() は末尾から取るので末尾が次の曲
            bag.insert(0, bag.pop())
    t = bag.pop()
    _data["battle_bag"] = bag
    _data["battle_last"] = t
    save()
    return t
