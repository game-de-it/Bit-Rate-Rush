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


def _shuffle_bag(tracks):
    """シャッフルの袋 (次に鳴らす候補。末尾から取る)。空なら全曲を混ぜ直す (境目で同じ曲が続かないように)"""
    import random
    last = _data.get("battle_last")
    bag = [t for t in _data.get("battle_bag", []) if t in tracks]
    if not bag:
        bag = list(tracks)
        random.shuffle(bag)
        if len(bag) > 1 and bag[-1] == last:
            bag.insert(0, bag.pop())
    return bag


def pick_battle_track(advance=True, loaded_only=False):
    """設定に従って戦闘曲を選ぶ。
    shuffle: 全曲を 1 巡してから次の巡へ (バッグ方式) / sequence: 順番 / select: 指定曲。
    advance=False は試聴用 (巡の状態を進めない)。
    loaded_only=True は戦闘中の曲送り用: デコード済みの曲だけから選ぶ (未デコードの曲はプレイ中に読み込むと止まるため)。
    候補が無ければ None (呼び出し側は今の曲をもう一度かける)。"""
    import random
    from core import audio
    tracks = audio.battle_tracks()
    if not tracks:
        return None if loaded_only else "battle01"
    mode = _data.get("battle_mode", "shuffle")
    ok = (lambda t: audio.loaded(t)) if loaded_only else (lambda t: True)
    if mode == "sequence":
        i = _data.get("battle_seq", 0) % len(tracks)
        for k in range(len(tracks)):
            j = (i + k) % len(tracks)
            if ok(tracks[j]):
                if advance:
                    _data["battle_seq"] = (j + 1) % len(tracks)
                    save()
                return tracks[j]
        return None
    if mode == "select":
        t = _data.get("battle_track") or tracks[0]
        t = t if t in tracks else tracks[0]
        return t if ok(t) else None
    # シャッフル
    last = _data.get("battle_last")
    if not advance:
        cands = [t for t in tracks if t != last and ok(t)] or [t for t in tracks if ok(t)]
        return random.choice(cands) if cands else None
    bag = _shuffle_bag(tracks)
    for k in range(len(bag) - 1, -1, -1):      # 末尾 = 次の曲。デコード済みのものを末尾側から探す
        if ok(bag[k]):
            t = bag.pop(k)
            _data["battle_bag"] = bag
            _data["battle_last"] = t
            save()
            return t
    return None


def upcoming_battle_tracks(n=2):
    """この先かかる予定の曲 (先読み用)。shuffle は袋の末尾から、sequence は次から順に"""
    from core import audio
    tracks = audio.battle_tracks()
    if not tracks:
        return []
    mode = _data.get("battle_mode", "shuffle")
    if mode == "select":
        t = _data.get("battle_track") or tracks[0]
        return [t if t in tracks else tracks[0]]
    if mode == "sequence":
        i = _data.get("battle_seq", 0) % len(tracks)
        return [tracks[(i + k) % len(tracks)] for k in range(n)]
    bag = _shuffle_bag(tracks)
    up = list(reversed(bag))[:n]
    if len(up) < n:                            # 袋の残りが少なければ次の巡も候補に (順不同)
        up += [t for t in tracks if t not in up][: n - len(up)]
    return up
