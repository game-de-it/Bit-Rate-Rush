"""実行中に切り替えられるデバッグフラグ (ポーズメニューの DBG 項目)。初期値は config の DEBUG_*。"""
from config import DEBUG_FIXED_XP

easy_levelup = bool(DEBUG_FIXED_XP)      # True: ジェム 5 個でレベルアップ
EASY_XP = DEBUG_FIXED_XP or 5
