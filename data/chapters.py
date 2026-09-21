"""章の定義。castle = その章の王宮依頼、magic = クリア報酬の魔法。
王宮依頼はその章の酒場依頼 (隠し依頼を除く) を全部クリアすると受けられる (data/quests.castle_open)。need_tavern は未使用。"""

CHAPTERS = {
    1: dict(title=("旅立ち", "Departure"), sub=("新顔", "The New Face"), castle="q1_castle", magic=["magic"], need_tavern=1),
    2: dict(title=("森の異変", "The Stirring Forest"), sub=("帰らぬ者たち", "Those Who Never Returned"), castle="q2_castle", magic=["holy"], need_tavern=1),
    3: dict(title=("死者の谷", "Valley of the Dead"), sub=("語られぬ記録", "The Untold Record"), castle="q3_castle", magic=["zap"], need_tavern=1),
    4: dict(title=("魔城の影", "Shadow of the Castle"), sub=("王の告白", "The King's Confession"), castle="q4_castle", magic=["tower", "fire"], need_tavern=1),
    5: dict(title=("決戦", "Showdown"), sub=("精霊", "The Spirit"), castle="q5_final", magic=[], need_tavern=0),
    # ---- 後編 (アリア編): 通し 6〜17 章 = 後編 1〜12 章。三部作 (private/STORY_PART2_構想.md §15) ----
    # image: 章タイトルの絵。magic: 領主依頼クリアの報酬。after_lord: 領主の会話のあとに挟む会話 (無ければ飛ばす)。
    # on_enter: 章タイトルのあと一度だけ挟む会話。part: 三部作の何部か
    # 第一部「英雄を追う歌」
    6:  dict(title=("拾えない光", "The Light You Cannot Hold"), sub=("港町リド", "The Port of Lido"), castle="p2_c1_cave", magic=["magic"], image="p2_chapter1", part=1),
    7:  dict(title=("逃れてきた声", "Voices of the Fled"), sub=("英雄の証言", "Tales of a Hero"), castle="p2_c2_refugees", magic=[], image="p2_chapter2", part=1),
    8:  dict(title=("滅びた街", "The Fallen Town"), sub=("ルーメンの廃墟", "The Ruins of Lumen"), castle="p2_c3_lumen", magic=["frost"], image="p2_chapter3", part=1, after_lord=["p2_seer_2"]),
    9:  dict(title=("英雄の影", "Shadow of the Hero"), sub=("先に救う者", "He Who Saves First"), castle="p2_c4_coda", magic=[], image="p2_chapter4", part=1),
    # 第二部「白紙の記憶」
    10: dict(title=("魂の灯", "Lamp of Souls"), sub=("精霊の谷", "The Spirit's Valley"), castle="p2_c5_valley", magic=["zap"], image="p2_chapter5", part=2, after_lord=["p2_seer_3"]),
    11: dict(title=("忘れた人々", "Those Who Forgot"), sub=("静かな街", "The Quiet Town"), castle="p2_c6_forgotten", magic=["holy"], image="p2_chapter6", part=2),
    12: dict(title=("白い図書室", "The White Library"), sub=("読めない本", "Books No One Can Read"), castle="p2_c7_library", magic=["tower"], image="p2_chapter7", part=2, after_lord=["p2_seer_4"]),
    13: dict(title=("消された名前", "The Erased Name"), sub=("繰り返す記録", "Records That Repeat"), castle="p2_c8_records", magic=[], image="p2_chapter8", part=2),
    # 第三部「観測者の終曲」
    14: dict(title=("守られない街", "The Unguarded Town"), sub=("常態化するラッシュ", "The Endless Rush"), castle="p2_c9_evacuate", magic=["meteor"], image="p2_chapter9", part=3),
    15: dict(title=("歌に残すもの", "What the Song Keeps"), sub=("集めた記憶", "Gathered Memories"), castle="p2_c10_song", magic=[], image="p2_chapter10", part=3),
    16: dict(title=("大精霊の座", "Seat of the Great Spirit"), sub=("白い本", "The White Book"), castle="p2_c11_seat", magic=["fire"], image="p2_chapter11", part=3, after_lord=["p2_seer_5"]),
    17: dict(title=("終曲", "Finale"), sub=("光を喰う者", "The Devourer of Light"), castle="p2_c12_final", magic=[], image="p2_chapter12", part=3, on_enter=["p2_seer_final"]),
}
FINAL_CHAPTER = 5          # 前編の最終章 (エンディング)
PART2_FIRST = 6            # 後編の最初の章
PART2_FINAL = 17           # 後編の最終章 (後編 12 章)


def is_part2(chapter):
    return chapter >= PART2_FIRST


def local_number(chapter):
    """章タイトルなどで見せる番号 (後編は 1 から)"""
    return chapter - PART2_FIRST + 1 if is_part2(chapter) else chapter


def is_final(chapter):
    return chapter == FINAL_CHAPTER or chapter == PART2_FINAL


def part_of(chapter):
    """三部作の何部か (前編は 0)"""
    return CHAPTERS.get(chapter, {}).get("part", 0)
