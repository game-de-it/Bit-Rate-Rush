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


def _debug_enabled():
    if _os.environ.get("BRR_DEBUG") == "1":
        return True
    try:
        import pyxel
        return _os.path.exists(_os.path.join(pyxel.user_data_dir("kroot", "Bit-Rate-Rush"), "debug"))
    except Exception:
        return False


DEBUG = _debug_enabled()
DEBUG_FIXED_XP = 5 if DEBUG else None      # 簡単レベルアップ (ジェム 5 個) の初期値
DEBUG_LEVELUP_SKIP = DEBUG                 # レベルアップ画面を X でスキップ
DEBUG_WEAPON_SELECT = DEBUG                # サバイバル開始前の初期武器選択
DEBUG_PAUSE_TOOLS = DEBUG                  # ポーズメニューの DBG 項目
DEBUG_DIALOG_VIEWER = DEBUG                # タイトルの会話ビューア
DEBUG_CHAPTER_START = DEBUG                # タイトルの章スタート
