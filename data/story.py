"""会話データ。assets/story.md を起動時に読む (書式はファイル冒頭を参照)。

SPEAKERS[key] = dict(name=(ja, en), img=画像名 or None)
DIALOGS[key]  = [(話者キー, (ja, en)), ...]
"""
import os

PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "story.md")
PATH_TEASER = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "story_teaser.md")      # 後編の導入 (p2_intro)
PATH_PART2 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "private", "story_part2.md")     # 後編本体 (非公開。あれば teaser を上書き)

SPEAKERS = {"narr": dict(name=("", ""), img=None)}
DIALOGS = {}
OPTIONS = {}     # key -> dict(vn=True, bg="forest_bg") など。story.md の `> @vn bg=...` 行
PAGE_BG = {}     # key -> {ページ番号: (画像名, フェードするか)}。ページの途中に置いた `> @vn bg=...` で以降のページの絵を切り替える (`nofade` でカット)
PAGE_BGM = {}    # key -> {ページ番号: 曲名}。ページの途中に置いた `> @bgm=曲名` でそのページから曲を切り替える (`stop` で停止)


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
                if cur != "@speakers":
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
