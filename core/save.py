"""セーブ / ロード。user_data_dir/save.json に 1 スロット。"""
import json
import os

import pyxel

from core.state import GameState


def _path():
    try:
        d = pyxel.user_data_dir("kroot", "Bit-Rate-Rush")
        os.makedirs(d, exist_ok=True)
        return os.path.join(d, "save.json")
    except Exception:
        return None


def exists():
    p = _path()
    return bool(p) and os.path.exists(p)


def load():
    p = _path()
    if not p or not os.path.exists(p):
        return None
    try:
        with open(p, "r", encoding="utf-8") as f:
            return GameState.from_dict(json.load(f))
    except Exception:
        return None


def save(state):
    p = _path()
    if not p:
        return False
    try:
        with open(p, "w", encoding="utf-8") as f:
            json.dump(state.to_dict(), f, ensure_ascii=False, indent=1)
        return True
    except Exception:
        return False


def delete():
    p = _path()
    if p and os.path.exists(p):
        try:
            os.remove(p)
        except Exception:
            pass
