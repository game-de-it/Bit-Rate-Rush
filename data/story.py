"""会話データ。assets/story.md を起動時に読む (書式はファイル冒頭を参照)。

SPEAKERS[key] = dict(name=(ja, en), img=画像名 or None)
DIALOGS[key]  = [(話者キー, (ja, en)), ...]
"""
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "story.md")
PATH_TEASER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "story_teaser.md")      # 後編の導入 (p2_intro)
PATH_PART2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "private", "STORY_PART2.md")     # 後編本体 (非公開。あれば teaser を上書き)

SPEAKERS = {"narr": dict(name=("", ""), img=None)}
DIALOGS = {}
OPTIONS = {}     # key -> dict(vn=True, bg="forest_bg") など。story.md の `> @vn bg=...` 行
PAGE_BG = {}     # key -> {ページ番号: (画像名, フェードするか)}。ページの途中に置いた `> @vn bg=...` で以降のページの絵を切り替える (`nofade` でカット)
PAGE_BGM = {}    # key -> {ページ番号: 曲名}。ページの途中に置いた `> @bgm=曲名` でそのページから曲を切り替える (`stop` で停止)
CREDITS = []     # スタッフロール。story.md の `## credits` (1 行 1 項目 `- 日本語 | English`、`-` だけの行は空行)


# 後編 (6 章〜) では会話キーを p2_ 付きに読み替える。番号付きのキーは後編内の章番号 (6 章 → 1) に直す。
_P2_RENAME = {"mira_": "haru_", "castle_before_": "lord_before_", "castle_after_": "lord_after_"}


def resolve(state, base):
    """状態に応じた会話キー。後編なら p2_ 版があればそれを、無ければ番号なしの p2_ 版、それも無ければ base"""
    if state is None or state.chapter < 6:
        return base
    stem, num = base, None
    head, _, tail = base.rpartition("_")
    if head and tail.isdigit():
        stem, num = head, int(tail)
        if num >= 6:
            num -= 5                      # 通し章番号 → 後編内の番号
    for a, b in _P2_RENAME.items():
        if (stem + "_").startswith(a):
            stem = b + (stem + "_")[len(a):]
            stem = stem.rstrip("_")
            break
    cands = []
    if num is not None:
        cands.append(f"p2_{stem}_{num}")
    cands.append(f"p2_{stem}")
    for c in cands:
        if c in DIALOGS:
            return c
    return base


def bg_name(state, base):
    """施設などの背景画像名。後編で p2_<base> が置かれていればそれを使う"""
    if state is not None and state.chapter >= 6:
        from core import images
        if images.get(f"p2_{base}") is not None:
            return f"p2_{base}"
    return base


def _split(text, n):
    parts = [p.strip() for p in text.split("|")]
    while len(parts) < n:
        parts.append(parts[0] if parts else "")
    return parts[:n]


def load(path=PATH, extra=(PATH_TEASER, PATH_PART2)):
    SPEAKERS.clear()
    SPEAKERS["narr"] = dict(name=("", ""), img=None)
    DIALOGS.clear()
    OPTIONS.clear()
    PAGE_BG.clear()
    PAGE_BGM.clear()
    CREDITS.clear()
    _load_file(path)
    for p in extra:
        if os.path.exists(p):
            _load_file(p)


def _load_file(path):
    cur = None
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            if line.startswith("## "):
                cur = line[3:].strip()
                if cur == "credits":
                    CREDITS.clear()
                elif cur != "@speakers":
                    DIALOGS[cur] = []
                continue
            if line.startswith("> @") and cur:
                # 表示オプション: > @vn bg=forest_bg  (拡張子は無視)
                opt = OPTIONS.setdefault(cur, {})
                toks = line[3:].split()
                fade = "nofade" not in toks
                for tok in toks:
                    if "=" in tok:
                        k, v = tok.split("=", 1)
                        if k == "bg":
                            v = os.path.splitext(v)[0]
                            if DIALOGS.get(cur):
                                # すでにページがある → 以降のページの絵を切り替える
                                PAGE_BG.setdefault(cur, {})[len(DIALOGS[cur])] = (v, fade)
                                continue
                        if k == "bgm":
                            v = os.path.splitext(v)[0]
                            if DIALOGS.get(cur):
                                PAGE_BGM.setdefault(cur, {})[len(DIALOGS[cur])] = v
                                continue
                        opt[k] = v
                    elif tok != "nofade":
                        opt[tok] = True
                continue
            if line.startswith("#") or line.startswith(">") or not line.strip():
                continue
            if cur == "credits":
                # `- 日本語 | English`。`-` だけなら空行。話者は書かない
                if line.strip() == "-":
                    CREDITS.append(("", ""))
                elif line.startswith("- "):
                    ja, en = _split(line[2:], 2)
                    CREDITS.append((ja, en if en else ja))
                continue
            if not line.startswith("- ") or cur is None:
                continue
            body = line[2:]
            if ":" not in body and "：" not in body:
                continue
            sep = ":" if ":" in body else "："
            key, rest = body.split(sep, 1)
            key = key.strip()
            if cur == "@speakers":
                ja, en, img = _split(rest, 3)
                SPEAKERS[key] = dict(name=(ja, en if en else ja), img=None if img in ("", "-") else img)
            else:
                ja, en = _split(rest, 2)
                DIALOGS[cur].append((key, (ja, en if en else ja)))


load()
