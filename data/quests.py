"""依頼定義。

kind: "survive" (制限時間まで生存) | "kill" (target を count 体倒す) | "boss" (target のボスを倒す)
time_limit: 秒。waves: data/waves.WAVES のキー。
hp_mult: 敵 HP の基礎倍率。hp_ramp: 敵 HP が 2 倍になるまでの秒数 (時間経過の補正)。
reward: クリア報酬 (ゴールド)。再クリア時は 70%。
client: "tavern" (酒場) | "castle" (王宮)。flag: 酒場に並ぶ条件フラグ。
boss_dialog: ボス撃破時に挟む会話キー。after: 依頼達成の瞬間に現地で挟む会話キー (占い師との出会いなど)。
"""

QUESTS = {
    # ---- 1 章: 旅立ち ----
    "q1_patrol": dict(
        chapter=1, client="tavern", kind="survive", count=0, target=None,
        name=("東の草原の見回り", "Patrol the East Meadow"),
        text=("東の草原に魔物が増えている。3 分ほど見回って、様子を報せてくれ。",
              "Monsters are gathering in the east meadow. Patrol it for three minutes and report back."),
        time_limit=180, waves="ch1_field", hp_mult=0.6, hp_ramp=300, reward=200,
    ),
    "q1_bats": dict(
        chapter=1, client="tavern", kind="kill", target="bat", count=300,
        name=("コウモリ退治", "Bat Hunt"),
        text=("洞窟から出てきたコウモリが畑を荒らしている。300 匹ほど減らしてくれ。",
              "Bats from the cave are ruining the fields. Cull about three hundred of them."),
        time_limit=180, waves="ch1_bats", hp_mult=0.6, hp_ramp=300, reward=300,
    ),
    "q1_graveyard": dict(
        chapter=1, client="tavern", kind="kill", target="zombie", count=170,
        name=("墓場の掃除", "Graveyard Cleanup"),
        text=("墓場で死者が起き上がっている。ゾンビを 170 体片付けてくれ。足は遅いが硬いぞ。",
              "The dead are rising in the graveyard. Put down a hundred and seventy zombies. Slow, but tough."),
        time_limit=240, waves="ch1_graveyard", hp_mult=0.7, hp_ramp=300, reward=350,
    ),
    "q1_castle": dict(
        chapter=1, client="castle", kind="kill", target="bat", count=330,
        name=("城下の草原を一掃せよ", "Clear the Castle Meadow"),
        text=("城下の草原にコウモリが群れている。330 匹を討ち、レートの兆しを断て。",
              "Bats swarm the meadow below the castle. Slay three hundred and thirty and cut off the omen."),
        time_limit=180, waves="ch1_castle", hp_mult=0.7, hp_ramp=240, reward=500,
    ),
    # ---- 2 章: 森の異変 ----
    "q2_woodcutter": dict(
        chapter=2, client="tavern", kind="survive", count=0, target=None,
        name=("木こりの捜索", "Search for the Woodcutter"),
        text=("森へ入った木こりが帰ってこない。5 分ほど森を探ってきてくれ。深追いはするな。",
              "A woodcutter went into the forest and never came back. Search it for five minutes. Don't go too deep."),
        time_limit=300, waves="ch2_forest", hp_mult=0.75, hp_ramp=240, reward=400,
    ),
    "q2_ghosts": dict(
        chapter=2, client="tavern", kind="kill", target="ghost", count=380,
        name=("森の影を払え", "Banish the Forest Shades"),
        text=("森に白い影が出る。壁をすり抜けるやつだ。380 体ほど払ってきてくれ。",
              "Pale shades haunt the forest ― the kind that slip through walls. Banish three hundred and eighty."),
        time_limit=240, waves="ch2_ghosts", hp_mult=0.75, hp_ramp=240, reward=450,
    ),
    "q2_seer": dict(
        chapter=2, client="tavern", kind="survive", count=0, target=None, flag="rumor_seer",
        name=("森の外れの占い師", "The Seer at the Forest's Edge"),
        text=("森の外れに占い師が住み着いた。会いに行くなら、魔物の群れを 3 分かわす覚悟がいる。",
              "A seer has settled at the forest's edge. To reach her you'll dodge the swarm for three minutes."),
        time_limit=180, waves="ch2_forest", hp_mult=0.8, hp_ramp=240, reward=100, after="seer_meet", magic=["orbit"],
    ),
    "q2_castle": dict(
        chapter=2, client="castle", kind="boss", target="forest_lord", count=1,
        name=("森の主を討て", "Slay the Lord of the Forest"),
        text=("森の奥に主がいる。門を守るように居座っている。討て。",
              "A lord dwells deep in the forest, squatting before a gate. Slay it."),
        time_limit=360, waves="ch2_castle", hp_mult=0.8, hp_ramp=240, reward=1000,
    ),
    # ---- 3 章: 死者の谷 ----
    "q3_skulls": dict(
        chapter=3, client="tavern", kind="kill", target="skull", count=300,
        name=("谷の骸を砕け", "Break the Valley Bones"),
        text=("谷から骸骨の兵が上がってくる。硬くて速い。300 体砕いてくれ。",
              "Skeleton soldiers climb out of the valley ― hard and fast. Break three hundred."),
        time_limit=300, waves="ch3_skulls", hp_mult=0.9, hp_ramp=200, reward=600,
    ),
    "q3_zombies": dict(
        chapter=3, client="tavern", kind="kill", target="zombie", count=550,
        name=("起き上がる兵士たち", "The Rising Soldiers"),
        text=("谷に葬られた兵士が起き上がっている。550 体、眠らせてやってくれ。",
              "Soldiers buried in the valley are rising. Put five hundred and fifty of them back to rest."),
        time_limit=300, waves="ch3_zombies", hp_mult=0.9, hp_ramp=200, reward=650,
    ),
    "q3_castle": dict(
        chapter=3, client="castle", kind="survive", count=0, target=None,
        name=("谷を調査せよ", "Survey the Valley"),
        text=("死者の谷を 7 分間調べよ。谷の祭壇に、古い書の写しがあるはずだ。",
              "Survey the Valley of the Dead for seven minutes. A copy of an old book should lie at the altar."),
        time_limit=420, waves="ch3_castle", hp_mult=0.9, hp_ramp=200, reward=2000, after="book_found",
    ),
    # ---- 4 章: 魔城の影 ----
    "q4_gate": dict(
        chapter=4, client="tavern", kind="survive", count=0, target=None,
        name=("門前の掃討", "Sweep the Gate"),
        text=("魔城の門前に魔物が集まっている。7 分間、押し返してくれ。",
              "Monsters mass before the castle gate. Hold them back for seven minutes."),
        time_limit=420, waves="ch4_gate", hp_mult=1.0, hp_ramp=180, reward=900,
    ),
    "q4_brutes": dict(
        chapter=4, client="tavern", kind="kill", target="brute", count=110,
        name=("巨人狩り", "Giant Hunt"),
        text=("門の巨人族が 110 体ほど出てきた。相手にするなら、槍かハンマーだ。",
              "A hundred and ten giants or so have come out from the gate. Bring a spear or a hammer."),
        time_limit=360, waves="ch4_brutes", hp_mult=1.0, hp_ramp=180, reward=1000,
    ),
    "q4_castle": dict(
        chapter=4, client="castle", kind="boss", target="boss1", count=1,
        name=("魔城の門番を倒せ", "Defeat the Gatekeeper"),
        text=("魔城の門番を倒し、門を開け。……頼む。", "Defeat the gatekeeper and open the castle gate. ...Please."),
        time_limit=480, waves="ch4_castle", hp_mult=1.0, hp_ramp=180, reward=3000, boss_dialog="gatekeeper_dies",
    ),
    # ---- 最終章: 決戦 ----
    "q5_final": dict(
        chapter=5, client="castle", kind="boss", target="boss2", count=1,
        name=("魔王を討て", "Slay the Demon Lord"),
        text=("魔城へ入り、魔王を討て。10 分、生き延びれば奴は現れる。",
              "Enter the castle and slay the Demon Lord. Survive ten minutes and it will come."),
        time_limit=1200, waves="survival", hp_mult=1.0, hp_ramp=120, reward=5000,
    ),
}


def offered(state):
    """酒場に並ぶ依頼: 現在章の酒場依頼 (フラグ条件付きは満たしたときだけ)。"""
    out = []
    for q, d in QUESTS.items():
        if d["client"] != "tavern" or d["chapter"] != state.chapter:
            continue
        if d.get("flag") and not state.flags.get(d["flag"]):
            continue
        out.append(q)
    return out


def tavern_cleared(state, chapter):
    return sum(1 for q, d in QUESTS.items()
               if d["client"] == "tavern" and d["chapter"] == chapter and q in state.cleared)


def tavern_required(chapter):
    """王宮依頼を受けるのに必要な酒場依頼: その章の酒場依頼すべて (隠し依頼を除く)。"""
    return [q for q, d in QUESTS.items()
            if d["client"] == "tavern" and d["chapter"] == chapter and not d.get("flag")]


def castle_open(state, chapter):
    return all(q in state.cleared for q in tavern_required(chapter))
