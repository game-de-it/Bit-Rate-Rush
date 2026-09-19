"""章の定義。castle = その章の王宮依頼、magic = クリア報酬の魔法。
王宮依頼はその章の酒場依頼 (隠し依頼を除く) を全部クリアすると受けられる (data/quests.castle_open)。need_tavern は未使用。"""

CHAPTERS = {
    1: dict(title=("旅立ち", "Departure"), sub=("新顔", "The New Face"), castle="q1_castle", magic=["magic"], need_tavern=1),
    2: dict(title=("森の異変", "The Stirring Forest"), sub=("帰らぬ者たち", "Those Who Never Returned"), castle="q2_castle", magic=["holy"], need_tavern=1),
    3: dict(title=("死者の谷", "Valley of the Dead"), sub=("語られぬ記録", "The Untold Record"), castle="q3_castle", magic=["zap"], need_tavern=1),
    4: dict(title=("魔城の影", "Shadow of the Castle"), sub=("王の告白", "The King's Confession"), castle="q4_castle", magic=["tower", "fire"], need_tavern=1),
    5: dict(title=("決戦", "Showdown"), sub=("精霊", "The Spirit"), castle="q5_final", magic=[], need_tavern=0),
}
FINAL_CHAPTER = 5
