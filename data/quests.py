"""依頼定義。

kind: "survive" (制限時間まで生存) | "kill" (target を count 体倒す) | "boss" (target のボスを倒す)
time_limit: 秒。waves: data/waves.WAVES のキー。
hp_mult: 敵 HP の基礎倍率。hp_ramp: 敵 HP が 2 倍になるまでの秒数 (時間経過の補正)。
reward: クリア報酬 (ゴールド)。再クリア時は 70%。
client: "tavern" (酒場) | "castle" (王宮)。flag: 酒場に並ぶ条件フラグ。
boss_dialog: ボス撃破時に挟む会話キー。after: 依頼達成の瞬間に現地で挟む会話キー (占い師との出会いなど)。after2: after の直後に続けて挟む会話。
intro: 戦闘開始直後に挟む会話キー。no_bits: ビットを拾えない (拾おうとすると消える)。first_bit: 最初のビットが消えたときの会話キー。
event: dict(at=秒, dialog=会話キー, rush=True/False)。戦闘の途中 (at 秒) で会話を挟み、rush ならその後ラッシュ (出現 2 倍) を始める。
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
    # ================= 後編 (アリア編): 12 章。依頼は各章 酒場 2 + 領主 1 (+2 章に占い師)。制限時間は 10 分が既定 =================
    # ---- 1 章 拾えない光 ----
    "p2_t1_patrol": dict(
        chapter=6, client="tavern", kind="survive", target=None, count=0,
        name=('港の見回り', 'Patrol the Harbor'),
        text=('港の倉庫にコウモリが増えてる。2 分だけ見回って、様子を教えておくれ。', 'Bats are gathering around the harbor warehouses. Look around for two minutes and tell me what you see.'),
        time_limit=120, waves="p2_harbor", hp_mult=0.6, hp_ramp=300, reward=200, no_bits=True, after='p2_blessing', first_bit='p2_no_bits', text_key='p2_quest_first',
    ),
    "p2_t1_wisps": dict(
        chapter=6, client="tavern", kind="kill", target='wisp', count=600,
        name=('倉庫の鬼火', 'Wisps in the Warehouse'),
        text=('倉庫の裏に鬼火が湧いてる。ふらふら飛ぶから当てにくいよ。10 分で 600 ほど消しておくれ。', "Wisps are rising behind the warehouses. They weave about, so they're hard to hit. Put out about six hundred in ten minutes."),
        time_limit=600, waves="p2_wharf", hp_mult=0.6, hp_ramp=300, reward=350,
    ),
    "p2_c1_cave": dict(
        chapter=6, client="castle", kind="kill", target='bat', count=900,
        name=('洞窟のコウモリを潰せ', 'Crush the Cave Bats'),
        text=('港の外れの洞窟からコウモリが湧いている。900 匹を潰し、ルーメンの前触れを断て。', 'Bats are pouring out of the cave beyond the harbor. Crush nine hundred and cut off the omen.'),
        time_limit=600, waves="p2_cave", hp_mult=0.65, hp_ramp=300, reward=700,
    ),
    # ---- 2 章 逃れてきた声 ----
    "p2_t2_boars": dict(
        chapter=7, client="tavern", kind="kill", target='boar', count=150,
        name=('街道の魔猪', 'Boars on the Road'),
        text=('東の街道に魔猪が出て、避難民の荷車が通れない。150 頭ほど追い払っておくれ。突っ込んでくるから気をつけて。', "Boars are blocking the east road and the refugees' carts can't pass. Drive off about a hundred and fifty. Watch out ― they charge."),
        time_limit=600, waves="p2_road", hp_mult=0.65, hp_ramp=300, reward=400,
    ),
    "p2_t2_camp": dict(
        chapter=7, client="tavern", kind="kill", target='zombie', count=500,
        name=('野営地の死者', 'The Dead at the Camp'),
        text=('避難民の野営地に、街道で死んだ人たちが起き上がってくる。500 体、眠らせてやっておくれ。', 'The dead from the road are rising around the refugee camp. Put five hundred of them back to rest.'),
        time_limit=600, waves="p2_camp", hp_mult=0.65, hp_ramp=300, reward=450,
    ),
    "p2_t2_seer": dict(
        chapter=7, client="tavern", kind="survive", target=None, count=0,
        name=('港の外れの占い師', 'The Seer Beyond the Harbor'),
        text=('港の外れの小屋に、占い師が住み着いたらしい。会いに行くなら、魔物を 10 分かわす覚悟がいるよ。', 'A seer has settled in the hut beyond the harbor. If you want to meet her, be ready to dodge the monsters for ten minutes.'),
        time_limit=600, waves="p2_wharf", hp_mult=0.7, hp_ramp=300, reward=150, flag='p2_rumor_seer', after='p2_seer_1', magic=['orbit'],
    ),
    "p2_c2_refugees": dict(
        chapter=7, client="castle", kind="kill", target='bat', count=800,
        name=('避難民を守れ', 'Protect the Refugees'),
        text=('街道の避難民が魔物に追われている。野営地を 10 分守り、コウモリを 800 落とせ。証言はそのあとで聞く。', 'The refugees on the road are being hunted. Hold the camp for ten minutes and bring down eight hundred bats. The testimonies can wait.'),
        time_limit=600, waves="p2_refugees", hp_mult=0.7, hp_ramp=280, reward=900, after='p2_testimony',
    ),
    # ---- 3 章 滅びた街 ----
    "p2_t3_ruins": dict(
        chapter=8, client="tavern", kind="kill", target='ghost', count=700,
        name=('廃墟の亡霊', 'Ghosts of the Ruins'),
        text=('ルーメンの廃墟に亡霊が出る。壁をすり抜けるやつだ。700 ほど払っておくれ。', 'Ghosts haunt the ruins of Lumen ― the kind that pass through walls. Banish about seven hundred.'),
        time_limit=600, waves="p2_ruins", hp_mult=0.75, hp_ramp=260, reward=500,
    ),
    "p2_t3_archers": dict(
        chapter=8, client="tavern", kind="kill", target='archer', count=300,
        name=('骸骨の射手', 'Skeleton Archers'),
        text=('廃墟の壁の上から、骸骨が矢を射てくる。距離を取って撃ってくるから、こっちから詰めるんだよ。300 体。', 'Skeletons are shooting from the ruined walls. They keep their distance, so close in on them. Three hundred.'),
        time_limit=600, waves="p2_archers", hp_mult=0.75, hp_ramp=260, reward=550,
    ),
    "p2_c3_lumen": dict(
        chapter=8, client="castle", kind="survive", target=None, count=0,
        name=('ルーメンの調査', 'Survey Lumen'),
        text=('滅びたルーメンを 10 分間調べてこい。生き残りがいるなら、連れ帰れ。', 'Survey the fallen Lumen for ten minutes. If there are survivors, bring them back.'),
        time_limit=600, waves="p2_lumen", hp_mult=0.8, hp_ramp=260, reward=1200, intro='p2_lumen_ruins', after='p2_garld_meet', text_key='p2_quest_lumen',
    ),
    # ---- 4 章 英雄の影 ----
    "p2_t4_outskirts": dict(
        chapter=9, client="tavern", kind="kill", target='wisp', count=750,
        name=('外縁の鬼火', 'Wisps at the Edge'),
        text=('廃墟の外縁に鬼火が増えた。誰かが火を撒いてるみたいにね。750 消しておくれ。', 'Wisps are multiplying at the edge of the ruins, as if someone were scattering fire. Put out seven hundred and fifty.'),
        time_limit=600, waves="p2_outskirts", hp_mult=0.8, hp_ramp=240, reward=600,
    ),
    "p2_t4_hunters": dict(
        chapter=9, client="tavern", kind="kill", target='boar', count=220,
        name=('狩人の頼み', "The Hunters' Request"),
        text=('狩人たちが魔猪に山を追われた。220 頭。ハンマーか槍があると楽だよ。', 'The hunters were driven off the mountain by boars. Two hundred and twenty. A hammer or spear makes it easier.'),
        time_limit=600, waves="p2_hunters", hp_mult=0.8, hp_ramp=240, reward=650,
    ),
    "p2_c4_coda": dict(
        chapter=9, client="castle", kind="survive", target=None, count=0,
        name=('英雄を探せ', 'Find the Hero'),
        text=('廃墟の外縁に『英雄』が現れたという。10 分間、その地を見張れ。会えたら、話を聞け。', "They say the 'hero' has appeared at the edge of the ruins. Watch the area for ten minutes. If you meet him, hear him out."),
        time_limit=600, waves="p2_coda", hp_mult=0.85, hp_ramp=240, reward=1500, event={'at': 300, 'dialog': 'p2_coda_meet', 'rush': True}, after='p2_coda_leaves', text_key='p2_quest_coda',
    ),
    # ---- 5 章 魂の灯 ----
    "p2_t5_skulls": dict(
        chapter=10, client="tavern", kind="kill", target='skull', count=450,
        name=('谷の骸骨', 'Bones of the Valley'),
        text=('谷から骸骨が上がってくる。硬くて速い。450 体砕いておくれ。', 'Skeletons are climbing out of the valley ― hard and fast. Break four hundred and fifty.'),
        time_limit=600, waves="p2_valley_skulls", hp_mult=0.9, hp_ramp=220, reward=700,
    ),
    "p2_t5_knight": dict(
        chapter=10, client="tavern", kind="boss", target='knight', count=1,
        name=('谷の騎士', 'The Knight of the Valley'),
        text=('谷の入口に、鎧の亡霊が立ちふさがってる。弾をばら撒いて、突っ込んでくる。倒しておくれ。', 'A phantom in armor blocks the mouth of the valley. It sprays bullets and charges. Bring it down.'),
        time_limit=600, waves="p2_knight", hp_mult=0.9, hp_ramp=220, reward=900,
    ),
    "p2_c5_valley": dict(
        chapter=10, client="castle", kind="survive", target=None, count=0,
        name=('谷の調査', 'Survey the Valley'),
        text=('夜、谷から歌が聞こえるという。10 分間、谷を調べてこい。', 'They say a song rises from the valley at night. Survey it for ten minutes.'),
        time_limit=600, waves="p2_valley", hp_mult=0.9, hp_ramp=220, reward=2000, after='p2_spirit_valley', text_key='p2_quest_valley',
    ),
    # ---- 6 章 忘れた人々 ----
    "p2_t6_graves": dict(
        chapter=11, client="tavern", kind="kill", target='zombie', count=700,
        name=('名のない墓', 'Nameless Graves'),
        text=('街の墓地で、名前のない墓から死者が起き上がってる。700 体、戻してやっておくれ。', 'The dead are rising from nameless graves in the town cemetery. Put seven hundred back.'),
        time_limit=600, waves="p2_graves", hp_mult=0.95, hp_ramp=200, reward=750,
    ),
    "p2_t6_shades": dict(
        chapter=11, client="tavern", kind="kill", target='ghost', count=850,
        name=('忘れられた影', 'Forgotten Shades'),
        text=('誰にも思い出してもらえない影が、街の周りをさまよってる。850 払っておくれ。', 'Shades no one remembers wander around the town. Banish eight hundred and fifty.'),
        time_limit=600, waves="p2_shades", hp_mult=0.95, hp_ramp=200, reward=800,
    ),
    "p2_c6_forgotten": dict(
        chapter=11, client="castle", kind="survive", target=None, count=0,
        name=('忘れた人々を守れ', 'Guard Those Who Forgot'),
        text=('精霊に記憶を取られた人々が、夜に街の外へ出て行く。10 分間、彼らを守れ。', 'Those whose memories the spirit took wander out of town at night. Guard them for ten minutes.'),
        time_limit=600, waves="p2_forgotten", hp_mult=1.0, hp_ramp=200, reward=2200, after='p2_haru_family',
    ),
    # ---- 7 章 白い図書室 ----
    "p2_t7_guard": dict(
        chapter=12, client="tavern", kind="kill", target='boar', count=250,
        name=('遺跡の番兵', 'Guardians of the Ruins'),
        text=('白い遺跡の周りを魔猪と射手がうろついてる。魔猪を 250 頭、追い払っておくれ。', 'Boars and archers prowl around the white ruins. Drive off two hundred and fifty boars.'),
        time_limit=600, waves="p2_library_guard", hp_mult=1.0, hp_ramp=190, reward=850,
    ),
    "p2_t7_knights": dict(
        chapter=12, client="tavern", kind="kill", target='knight', count=2,
        name=('遺跡の騎士', 'Knights of the Ruins'),
        text=('遺跡の門に、鎧の亡霊が二体いる。二体とも倒しておくれ。', 'Two armored phantoms stand at the gate of the ruins. Bring them both down.'),
        time_limit=600, waves="p2_library_mid", hp_mult=1.0, hp_ramp=190, reward=1100,
    ),
    "p2_c7_library": dict(
        chapter=12, client="castle", kind="survive", target=None, count=0,
        name=('白い遺跡の調査', 'Survey the White Ruins'),
        text=('白い遺跡を 10 分間調べてこい。本があるなら、一冊でいい、持ち帰れ。', 'Survey the white ruins for ten minutes. If there are books, bring back even one.'),
        time_limit=600, waves="p2_library", hp_mult=1.05, hp_ramp=190, reward=3000, after='p2_white_library', text_key='p2_quest_library',
    ),
    # ---- 8 章 消された名前 ----
    "p2_t8_wisps": dict(
        chapter=13, client="tavern", kind="kill", target='wisp', count=950,
        name=('記録の火', 'Fires of the Record'),
        text=('遺跡の奥から鬼火が溢れてくる。記録が燃えてるみたいだって。950 消しておくれ。', 'Wisps are spilling from the depths of the ruins, like records burning. Put out nine hundred and fifty.'),
        time_limit=600, waves="p2_records_a", hp_mult=1.05, hp_ramp=180, reward=950,
    ),
    "p2_t8_skulls": dict(
        chapter=13, client="tavern", kind="kill", target='skull', count=600,
        name=('消された兵', 'The Erased Soldiers'),
        text=('誰の記録にも残っていない兵が、遺跡の奥で立ち上がる。600 体砕いておくれ。', 'Soldiers no record remembers are rising in the depths of the ruins. Break six hundred.'),
        time_limit=600, waves="p2_records_b", hp_mult=1.05, hp_ramp=180, reward=1000,
    ),
    "p2_c8_records": dict(
        chapter=13, client="castle", kind="survive", target=None, count=0,
        name=('記録領域へ', 'Into the Record'),
        text=('白い本が示す場所へ行け。10 分、そこで見たものを持ち帰れ。', 'Go where the white book points. Survive ten minutes and bring back what you see.'),
        time_limit=600, waves="p2_records", hp_mult=1.1, hp_ramp=180, reward=3500, after='p2_erased_name', text_key='p2_quest_records',
    ),
    # ---- 9 章 守られない街 ----
    "p2_t9_gate": dict(
        chapter=14, client="tavern", kind="kill", target='bat', count=1100,
        name=('東門の防衛', 'Hold the East Gate'),
        text=('レートが下がらない。東門にコウモリが押し寄せてる。1100 匹、落としておくれ。', "The rate won't come down. Bats are pouring at the east gate. Bring down eleven hundred."),
        time_limit=600, waves="p2_gate", hp_mult=1.1, hp_ramp=170, reward=1200,
    ),
    "p2_t9_streets": dict(
        chapter=14, client="tavern", kind="kill", target='ghost', count=850,
        name=('通りの影', 'Shades in the Streets'),
        text=('街の通りにまで影が入ってきた。850 払っておくれ。避難が終わるまで持たせて。', 'Shades have come into the streets. Banish eight hundred and fifty and hold until the evacuation is done.'),
        time_limit=600, waves="p2_streets", hp_mult=1.1, hp_ramp=170, reward=1250,
    ),
    "p2_c9_evacuate": dict(
        chapter=14, client="castle", kind="survive", target=None, count=0,
        name=('住民を避難させろ', 'Evacuate the Town'),
        text=('街はもう守れぬ。住民を港へ逃がす。10 分間、門を支えよ。', 'The town can no longer be held. We move the people to the harbor. Hold the gate for ten minutes.'),
        time_limit=600, waves="p2_evacuate", hp_mult=1.15, hp_ramp=170, reward=4000, after='p2_town_falls',
    ),
    # ---- 10 章 歌に残すもの ----
    "p2_t10_escort": dict(
        chapter=15, client="tavern", kind="survive", target=None, count=0,
        name=('避難路の護衛', 'Escort on the Evacuation Road'),
        text=('港へ向かう列を魔物が狙ってる。10 分、列の後ろを守っておくれ。', 'Monsters are stalking the column heading for the harbor. Guard its rear for ten minutes.'),
        time_limit=600, waves="p2_escort", hp_mult=1.15, hp_ramp=160, reward=1300, after='p2_memory_sena',
    ),
    "p2_t10_pier": dict(
        chapter=15, client="tavern", kind="kill", target='wisp', count=1000,
        name=('桟橋の鬼火', 'Wisps on the Pier'),
        text=('桟橋に鬼火が群がって、船が出せない。1000 消しておくれ。', "Wisps are swarming the pier and the boats can't leave. Put out a thousand."),
        time_limit=600, waves="p2_pier", hp_mult=1.15, hp_ramp=160, reward=1350, after='p2_memory_haru',
    ),
    "p2_c10_song": dict(
        chapter=15, client="castle", kind="survive", target=None, count=0,
        name=('記憶を集めよ', 'Gather the Memories'),
        text=('次の世界へ残したい記憶を、皆から集めてこい。10 分、港を守りながらだ。', 'Gather from everyone the memories they want carried to the next world. Ten minutes, while you hold the harbor.'),
        time_limit=600, waves="p2_song", hp_mult=1.2, hp_ramp=160, reward=4500, after='p2_memory_garld', after2='p2_song_complete', text_key='p2_quest_song',
    ),
    # ---- 11 章 大精霊の座 ----
    "p2_t11_seat_a": dict(
        chapter=16, client="tavern", kind="kill", target='skull', count=750,
        name=('座への道', 'The Road to the Seat'),
        text=('大精霊の座へ続く道を、骸骨が埋めてる。750 体砕いておくれ。', "Skeletons fill the road to the Great Spirit's seat. Break seven hundred and fifty."),
        time_limit=600, waves="p2_seat_a", hp_mult=1.2, hp_ramp=150, reward=1400,
    ),
    "p2_t11_seat_b": dict(
        chapter=16, client="tavern", kind="boss", target='knight', count=1,
        name=('座の門番', 'Warden of the Seat'),
        text=('座の門に、いちばん大きな鎧の亡霊がいる。倒しておくれ。', 'The largest armored phantom guards the gate of the seat. Bring it down.'),
        time_limit=600, waves="p2_seat_b", hp_mult=1.2, hp_ramp=150, reward=1500,
    ),
    "p2_c11_seat": dict(
        chapter=16, client="castle", kind="survive", target=None, count=0,
        name=('大精霊の座へ', 'To the Seat of the Great Spirit'),
        text=('座へ入れ。10 分、そこで立っていろ。声が聞こえるはずだ。', 'Enter the seat. Stand there for ten minutes. You should hear the voice.'),
        time_limit=600, waves="p2_seat", hp_mult=1.25, hp_ramp=150, reward=5000, after='p2_great_spirit', after2='p2_white_book', text_key='p2_quest_seat',
    ),
    # ---- 12 章 終曲 ----
    "p2_c12_final": dict(
        chapter=17, client="castle", kind="boss", target='coda', count=1,
        name=('光を喰う者を止めろ', 'Stop the Devourer of Light'),
        text=('谷の奥へ行け。10 分生き延びれば、光を喰う者が現れる。', 'Go to the depths of the valley. Survive ten minutes, and the Devourer of Light will come.'),
        time_limit=600, waves="p2_final", hp_mult=1.0, hp_ramp=120, reward=6000, intro='p2_coda_before', boss_dialog='p2_coda_after', text_key='p2_quest_final',
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
