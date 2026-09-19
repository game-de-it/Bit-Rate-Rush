"""assets/story.md の検証: コードが参照する会話キーが揃っているか、話者キーが定義済みか。
    python3 tools/check_story.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.story import SPEAKERS, DIALOGS, OPTIONS, PAGE_BG, PAGE_BGM
from core import audio as _audio
from core import images as _images
from data.quests import QUESTS
from data.chapters import CHAPTERS, FINAL_CHAPTER

required = ["intro", "tavern_hello", "tavern_has_quest", "tavern_accept", "inn_hello", "inn_rest", "inn_poor", "inn_full",
            "smith_hello", "shop_hello", "castle_refuse", "castle_wait", "castle_done", "ending_town", "ending_night",
            "closed", "no_quest", "new_game_confirm"]
for ch in CHAPTERS:
    required.append(f"castle_before_{ch}")
    if ch < FINAL_CHAPTER:
        required.append(f"castle_after_{ch}")
for q in QUESTS.values():
    for k in ("boss_dialog", "after"):
        if q.get(k):
            required.append(q[k])
ok = True
for k in required:
    if k not in DIALOGS:
        print("MISSING dialog:", k); ok = False
    elif not DIALOGS[k]:
        print("EMPTY dialog:", k); ok = False
for k, pages in DIALOGS.items():
    for spk, _ in pages:
        if spk not in SPEAKERS:
            print(f"UNKNOWN speaker '{spk}' in {k}"); ok = False
# 会話窓 (3 行) に収まるか
try:
    import pyxel
    pyxel.init(320, 240, headless=True)
    from core import palette; palette.load()
    from ui import font; font.load()
    from scenes.dialog import wrap
    from ui import window as UI
    dx, dy, dw, dh = UI.DIALOG
    for k, pages in DIALOGS.items():
        if k == "credits":
            continue
        for i, (spk, (ja, en)) in enumerate(pages):
            vn = OPTIONS.get(k, {}).get("vn")
            if vn:
                pic = SPEAKERS.get(spk, {}).get("img") and not OPTIONS.get(k, {}).get("nopic")
                width, limit = (320 - 12 - 56 - 12 - 12) if pic else (320 - 24), 3
            else:
                tx = dx + 3 + 64 + 8 if SPEAKERS.get(spk, {}).get("img") else dx + 10
                width, limit = dx + dw - tx - 8, 3
            for lang, txt in (("ja", ja), ("en", en)):
                n = len(wrap(txt, width))
                if n > limit:
                    print(f"TOO LONG {k}[{i}] {lang}: {n} lines (max {limit}): {txt[:40]}..."); ok = False
except Exception as e:
    print("(line check skipped:", e, ")")
for k, opt in OPTIONS.items():
    bgs = ([opt["bg"]] if opt.get("bg") else []) + [v[0] for v in PAGE_BG.get(k, {}).values()]
    for b in bgs:
        if not os.path.exists(os.path.join(_images.DIR, f"{b}.png")):
            print(f"(note) image not placed: {b} (used by {k})")
for k, opt in OPTIONS.items():
    names = ([opt["bgm"]] if opt.get("bgm") else []) + list(PAGE_BGM.get(k, {}).values())
    for n in names:
        if n not in ("stop", "none", "off") and not os.path.exists(os.path.join(_audio.BGM_DIR, f"{n}.mp3")):
            print(f"(note) bgm not placed: {n} (used by {k})")
optional = [k for k in DIALOGS if k not in required]
print(f"{len(DIALOGS)} dialogs, {len(SPEAKERS)} speakers. optional keys: {', '.join(optional)}")
print("OK" if ok else "NG")
sys.exit(0 if ok else 1)
