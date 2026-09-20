"""章の定義。castle = その章の王宮依頼、magic = クリア報酬の魔法。
王宮依頼はその章の酒場依頼 (隠し依頼を除く) を全部クリアすると受けられる (data/quests.castle_open)。need_tavern は未使用。"""

CHAPTERS = {
    1: dict(title=("旅立ち", "Departure"), sub=("新顔", "The New Face"), castle="q1_castle", magic=["magic"], need_tavern=1),
    2: dict(title=("森の異変", "The Stirring Forest"), sub=("帰らぬ者たち", "Those Who Never Returned"), castle="q2_castle", magic=["holy"], need_tavern=1),
    3: dict(title=("死者の谷", "Valley of the Dead"), sub=("語られぬ記録", "The Untold Record"), castle="q3_castle", magic=["zap"], need_tavern=1),
    4: dict(title=("魔城の影", "Shadow of the Castle"), sub=("王の告白", "The King's Confession"), castle="q4_castle", magic=["tower", "fire"], need_tavern=1),
    5: dict(title=("決戦", "Showdown"), sub=("精霊", "The Spirit"), castle="q5_final", magic=[], need_tavern=0),
    # ---- 後編 (アリア編): 6〜10 章。主人公はアリア (新しいセーブ状態で始まる)。image は章タイトルの絵 ----
    6: dict(title=("拾えない光", "The Light You Cannot Hold"), sub=("港町リド", "The Port of Lido"), castle="p2_q1_cave", magic=["magic"], need_tavern=1, image="p2_chapter1"),
    7: dict(title=("英雄の噂", "Rumors of a Hero"), sub=("ルーメンの廃墟", "The Ruins of Lumen"), castle="p2_q2_lumen", magic=["frost"], need_tavern=1, image="p2_chapter2"),
    8: dict(title=("精霊の谷", "The Spirit's Valley"), sub=("夜に聞こえる歌", "A Song in the Night"), castle="p2_q3_valley", magic=["zap", "holy"], need_tavern=1, image="p2_chapter3"),
    9: dict(title=("白い図書室", "The White Library"), sub=("読めない本", "Books No One Can Read"), castle="p2_q4_library", magic=["meteor", "tower"], need_tavern=1, image="p2_chapter4"),
    10: dict(title=("終曲", "Finale"), sub=("光を喰う者", "The Devourer of Light"), castle="p2_q5_final", magic=[], need_tavern=0, image="p2_chapter5"),
}
FINAL_CHAPTER = 5          # 前編の最終章 (エンディング)
PART2_FIRST = 6            # 後編の最初の章
PART2_FINAL = 10           # 後編の最終章


def is_part2(chapter):
    return chapter >= PART2_FIRST


def local_number(chapter):
    """章タイトルなどで見せる番号 (後編は 1 から)"""
    return chapter - PART2_FIRST + 1 if is_part2(chapter) else chapter


def is_final(chapter):
    return chapter == FINAL_CHAPTER or chapter == PART2_FINAL
