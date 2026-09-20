# 画面・共通定数
W, H = 320, 240
FPS = 60

# 同時オブジェクト上限 (設計書 2.2)
MAX_ENEMIES = 150
MAX_BULLETS = 200
MAX_PICKUPS = 300
MAX_PARTICLES = 100

# 敵をリサイクルする距離 (プレイヤーからこれ以上離れたら消して再スポーン)
DESPAWN_DIST = 400
DESPAWN_DIST2 = DESPAWN_DIST * DESPAWN_DIST

# 1プレイ時間 (秒)
RUN_LENGTH = 600

# ---- デバッグ ----
# リリース版では全て OFF。環境変数 BRR_DEBUG=1 か、セーブ先 (user_data_dir) に "debug" という名前のファイルがあると ON。
import os as _os


def _debug_enabled(after_init=False):
    """after_init=False (import 時) は環境変数だけを見る。
    pyxel.user_data_dir は pyxel.init 前に呼ぶと panic する環境がある (plumOS では例外、Web/Pyodide では即死で捕まえられない) ので、
    セーブ先の "debug" ファイルの確認は init 後の refresh_debug() でだけ行う"""
    if _os.environ.get("BRR_DEBUG") == "1":
        return True
    if not after_init:
        return False
    try:
        import pyxel
        return _os.path.exists(_os.path.join(pyxel.user_data_dir("kroot", "Bit-Rate-Rush"), "debug"))
    except BaseException:
        return False


def _apply_debug(on):
    global DEBUG, DEBUG_FIXED_XP, DEBUG_LEVELUP_SKIP, DEBUG_WEAPON_SELECT, DEBUG_PAUSE_TOOLS, DEBUG_DIALOG_VIEWER, DEBUG_CHAPTER_START
    DEBUG = on
    DEBUG_FIXED_XP = 5 if on else None      # 簡単レベルアップ (ジェム 5 個) の初期値
    DEBUG_LEVELUP_SKIP = on                 # レベルアップ画面を X でスキップ
    DEBUG_WEAPON_SELECT = on                # サバイバル開始前の初期武器選択
    DEBUG_PAUSE_TOOLS = on                  # ポーズメニューの DBG 項目
    DEBUG_DIALOG_VIEWER = on                # タイトルの会話ビューア
    DEBUG_CHAPTER_START = on                # タイトルの章スタート


def refresh_debug():
    """pyxel.init() の直後、他のモジュールを import する前に呼ぶ。"""
    _apply_debug(_debug_enabled(after_init=True))


_apply_debug(_debug_enabled())
