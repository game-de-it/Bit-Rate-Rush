# Bit-Rate-Rush 会話データ

ゲームはこのファイルを起動時に読む。書式:

- `## キー` で会話 1 本。キーはコードから参照される (変えない)
- `- 話者: 日本語 | English` で 1 ページ。話者は下の @speakers のキー
- `>` で始まる行はメモ (ゲームには出ない)。`#` 1 つの見出しは章分け用で無視される
- 英語を省くと日本語がそのまま使われる
- 文中の半角スペースは「ここで折り返してよい」の印 (収まらないときだけ改行)。`\n` (2 文字) は必ず改行
- `> @vn bg=画像名` を会話の先頭に置くと、ビジュアルノベル風 (上に 16:9 の絵 320x180、下に会話窓、立ち絵なし) で表示する。画像は assets/img/<画像名>.png、無ければ直前の画面を暗くして使う。窓は 3 行まで。話者に立ち絵があれば窓の左に小さく出る (`> @vn nopic` で消せる)
- ページの途中に `> @vn bg=画像名` を置くと、以降のページの絵がクロスフェードで切り替わる (拡張子は書いても無視される)。`> @vn bg=画像名 nofade` でフェードなしのカット切り替え
- `## credits` はスタッフロール。1 行 1 項目で `- 日本語 | English`、`-` だけの行は空行。話者は書かない。1 行目は金色で表示される
- `> @bgm=曲名` で BGM を指定できる (assets/bgm/<曲名>.mp3、ループ再生)。会話の先頭に置けば会話開始時、ページの途中に置けばそのページから切り替わる。`> @bgm=stop` で停止。VN でない会話にも使える。`> @vn bg=xxx bgm=yyy` のように 1 行にまとめても良い


## @speakers

> 話者キー: 日本語名 | English name | 立ち絵ファイル名 (assets/img/<名前>.png、無ければ -)

- narr:  |  | -
- master: 酒場のマスター ガルド | Garld, Tavern Master | npc_master
- inn: 宿屋の女将 ミラ | Mira, Innkeeper | npc_inn
- shop: 雑貨屋の店主 ポム | Pom, Shopkeeper | npc_shop
- smith: 武器屋の親方 バルド | Bald, Weaponsmith | npc_smith
- king: 王 レオン三世 | King Leon III | npc_king
- minister: 大臣 | The Minister | npc_minister
- seer: 占い師 | The Seer | npc_seer
- keeper: 門番 | Gatekeeper | -
- hero: 若者 | young man | -

# 序章

## intro
> はじめから → 街に入った直後
> @vn bg=op_bg0 bgm=intro01.mp3
- narr: この世界に生きるものは皆、ビットと呼ばれる光の粒を宿している。 | Every living thing in this world carries motes of light called bits.
- narr: 魔物を倒すと、ビットはその身から散り、風の中へ消えていく。 人の手で拾うことはできない。 | When a monster falls, its bits scatter from its body and fade into the wind. No human hand can gather them.
- narr: そしてレートが高まると、魔物は次々と目を覚まし、\n群れをなして街へ押し寄せる。人々はそれをラッシュと呼ぶ。 | And when the rate climbs, monsters wake one after another and pour toward the town. People call it the Rush.
> @vn bg=op_bg
- narr: 山向こうの村をラッシュに呑まれ、たった一人で城下町へたどり着いた若者がいた。 | There was a young man who reached the castle town alone, after the Rush swallowed his village beyond the mountain.
- narr: ナイフ一本を手に、若者は城下町ルーメンの門をくぐった。 | With a single knife in hand, he passed through the gate of Lumen.
- narr: ――その日から、街の空にはコウモリが増えはじめた。 | ― From that day on, bats began to gather in the sky over the town.

# 酒場 (ガルド)

## tavern_first
> 酒場に初めて入ったとき (1 回だけ)。このあと tavern_hello が続く
- master: この街じゃ、依頼を受けて魔物を減らすのが稼ぎ方だ。 | In this town, you earn your coin by taking jobs and thinning out the monsters.
- master: 魔物を倒すと、光の粒が散るのが見えるだろ。 あれがビットだ。 きれいだが、人の手には残らねえ。 | See the motes of light when a monster dies? Those are bits. Pretty, but they never stay in human hands.
- master: ただし、戦い続けるほどレートは上がる。 上がりきればラッシュだ。欲張るなよ。 | But the longer you keep fighting, the higher the rate climbs. Let it peak and you get a Rush. Don't get greedy.

## tavern_hello
> 酒場に入ったとき (章別の tavern_hello_N が無い章で使う)
- master: よう、見ない顔だな。 | Hey. Haven't seen your face around here.
- master: 仕事を探してるなら依頼板を見ていけ。 | If you're looking for work, have a look at the job board.
- master: 危険な仕事ばかりで、引き受ける奴も少ないけどな。 | Dangerous work, all of it. Not many are willing to take it on.

## tavern_hello_2
> 2 章の酒場。占い師の噂 → 隠し依頼が依頼板に並ぶ
- master: そういや最近、森の様子がおかしいらしいぜ。 | Come to think of it, I hear the forest's been acting strange lately.
- master: 木こりが森から帰ってこねぇんだ。 | The woodcutter never came back out of it.
- master: ……森の外れに占い師が住み着いたって話だ。\nかなりの変わり者らしいがな。 | ...They say a seer has settled at the forest's edge.\nQuite the odd one, from what I hear.

## tavern_hello_3
- master: 死者の谷の話は、この街じゃ誰もしたがらねぇ。 | Nobody in this town wants to talk about the Valley of the Dead.
- master: 前のラッシュで命を落とした連中が、眠ってる場所だからな。 | That's where the ones who lost their lives in the last Rush are sleeping.
- master: あの戦いの中で生き残ったのは\n王と俺だけだった。 | Out of that whole battle,\nonly the King and I came out alive.
- master: ……せめて、安らかに眠っていてくれりゃいいんだが。 | ...I just hope they're resting in peace, at least.

## tavern_hello_4
- master: 魔城の門が、また開こうとしてるらしいな。 | I hear the gate of the Demon Castle is about to open again.
- master: あんたが門番を倒してくれりゃ、この街は救われるかもしれねぇ。 | If you can take down the gatekeeper, this town might just be saved.
- master: ……頼んだぞ、新顔。 | ...We're counting on you, new face.

## tavern_hello_5
- master: いよいよ出発するのか。 | So you're finally setting out.
- master: 無事に帰ってきたら、お前の名前を聞かせてくれよ。 | When you make it back safe, tell me your name.


## tavern_has_quest
> 受注中の依頼があるとき
- master: 受けた仕事がまだ片付いてないだろ。まずはそっちを頼む。 | You've still got a job open. Finish that one first.

## tavern_accept
> 依頼を受けたとき
- master: よし、頼んだぞ。\n準備ができたなら街の門から出発してくれ。 | Good. It's yours.\nOnce you're ready, head out through the town gate.

## seer_meet
> @vn bg=forest_bg
> 隠し依頼「森の外れの占い師」クリア後、森で会話 (衛星を入手)
- seer: ……よくここまで来たね。 | ...So you made it this far.
- seer: あんたには、影が二つあるように見えるね。 | You look to me like you've got two shadows.
- seer: この魔法をあんたにやろう。\nそばを巡って、身を守ってくれるはずさ。 | I'll give you this magic.\nIt circles at your side and should keep you safe.


# 宿屋 (ミラ)

## inn_hello
> 宿屋 (選択肢: 休む / やめる)
- inn: いらっしゃい。\nそんなに傷だらけで。休んでいかない？ | Welcome, dear.\nLook at all those wounds. Won't you rest a while?

## inn_rest
> 休んだあと
- inn: ゆっくりお休みなさい。 | Sleep well, now.
- inn: ……朝よ。\n日記もつけておいたからね。 | ...It's morning.\nI've written in your journal for you, too.

## inn_poor
> お金が足りない
- inn: あら、お金が足りないみたい。\n稼いでからまたおいで。 | Oh, you're a bit short.\nCome back once you've earned some coin.

## inn_full
> HP が満タン
- inn: 十分元気そうね。\n今は休む必要はなさそうよ。 | You look perfectly fine to me.\nNo need to rest right now.

## mira_2
> 2 章になって初めて宿屋に入ったとき (1 回だけ)。mira_3〜5 も同様
- inn: 王様に会ったんだって？\nあんた、本当は何者なの？ | You met the King?\nWho are you, really?

## mira_3
- inn: ……死者の谷には行かないで、なんて言わないけど。\nあんたのことが心配なのよ。 | ...I won't tell you to stay out of the Valley of the Dead.\nBut I'm worried about you.

## mira_4
- inn: 死者の谷の話は、ここでは誰もしないの…… | Nobody here ever talks about the Valley of the Dead...

## mira_5
- inn: ……必ず無事で帰ってきなさいよ。 | ...You come back safe. You hear me?


# 武器屋・雑貨屋

## smith_hello
- smith: ……好きに見ていけ。\n金さえあれば売ってやる。 | ...Look all you like.\nIf you've got the coin, I'll sell.

## shop_hello
- shop: いらっしゃい。\n旅支度なら、うちに任せてよ。 | Welcome.\nGetting ready for the road? Leave it to me.
- shop: その袋に入る道具は、三つまでだよ。 | That bag of yours holds three items, no more.


# 王宮

## castle_refuse
> その章の酒場依頼を 1 件もクリアしていないとき (大臣)
- minister: 今は陛下の御前には通せぬ。\nまずは街の役に立ち、己の力を示せ。 | You may not see His Majesty yet. First serve the town, and prove your strength.

## castle_wait
> 王宮依頼を受注中
- minister: 陛下より賜った命を果たしてから戻られよ。 | Return once you have carried out the command His Majesty gave you.

## castle_done
> その章の王宮依頼をクリア済み
- minister: ……陛下はお休みになっておられる。\n今はお話しになることもない。 | ...His Majesty is resting.\nHe has nothing to say to you at present.

## castle_before_1
> 1 章の王宮依頼を受ける前 (このあと依頼文が王の台詞として続き、受ける / やめる)
- minister: 陛下、この者は素性も知れぬ者です…… | Your Majesty, this one is of unknown origin...
- king: かまわぬ。\n……そなたが、草原の魔物を討っているという若者か。 | It matters not.\n...So you are the young man slaying the monsters in the meadow.
- king: 酒場のガルドから、そなたの活躍は聞いておる。 | Garld at the tavern has told me of your deeds.
- king: 近頃、空を覆うほどコウモリが増えておる。\nレートが高まりつつある兆しだ。 | Of late the bats have multiplied until they darken the sky.\nIt is a sign that the rate is rising.
- king: まずは、城下の草原に現れたコウモリの群れを\n一掃してもらいたい。 | First, wipe out the swarm of bats that has appeared in the meadow below the castle.

## castle_after_1
> 1 章の王宮依頼クリア後、街に戻ったとき (魔法弾を入手、2 章へ)
- narr: 王宮にて。 | At the castle.
- king: 見事な活躍だったな。\n褒美にこれを授けよう。 | A splendid feat.\nI shall grant you this as your reward.
- king: 王家に伝わる魔導具\n――「魔法弾」だ。 | A relic passed down through the royal house\n― the Magic Bolt.
- king: 魔導具は使い手を選ぶ。 | A relic chooses its wielder.
- king: 魔導具がそなたを選んだのなら、それが答えだ。 | If the relic has chosen you, then that is the answer.
- minister: （……気に入らぬ。\n素性も知れぬ者に魔導具を与えるなど……） | (...I do not like this.\nGranting a relic to one of unknown origin...)

## castle_before_2
- king: 森の奥に「魔城の門」がある。\nわしが若き日に閉じたはずの場所だ。 | Deep in the forest stands the Gate of the Demon Castle. I sealed it myself, in my youth.
- king: 森の魔物が、門を守るかのように居座っておる。 | A monster of the forest has settled there, as though guarding the gate.
- king: わけは聞かず、その魔物を討ってくれぬか。 | Ask me no reasons. Will you slay it for me?

## castle_after_2
- narr: 王宮にて。 | At the castle.
- king: よくやってくれた。\nそなたに王家に伝わる魔導具\n――「聖水」を授けよう。 | Well done. I grant you a relic of the royal house ― the Holy Water.
- king: ……門の向こうには、わしがまだ語れぬ秘密がある。今は何も聞かんでくれ。 | ...Beyond that gate lies a secret I cannot yet speak of. Ask me nothing, for now.

## castle_before_3
- king: 死者の谷を調べてほしい。 | I want you to investigate the Valley of the Dead.
- king: 谷の奥にある祭壇に、古い書の写しがある。 | On the altar deep within the valley lies a copy of an ancient book.
- minister: 陛下！ それは―― | Your Majesty! That is―
- king: よい。\n……7 分だ。それ以上、谷に留まってはならぬ。 | Enough.\n...Seven minutes. You must not stay in the valley a moment longer.
- king: 亡霊に食い殺されるからな。 | The specters would tear you apart and devour you.

## book_found
> 3 章の王宮依頼「谷を調査せよ」を達成した瞬間、谷の祭壇で (ビジュアルノベル風)
> @vn bg=valley_bg
- narr: 死者の谷の祭壇に置かれていたのは、『レートの書』の写し―― | What lay on the altar of the Valley of the Dead was a copy of the Book of the Rate ―
- narr: 「魂を捧げよ。されば精霊は目覚め、レートを下げん」 | "Offer up souls. Then shall the spirit wake, and the rate shall fall."
- narr: 「精霊は語らず。その影を魔と呼ぶことなかれ」 | "The spirit speaks not. Call not its shadow a demon."
- narr: 「もしビットを喰らう者が現れたならば、精霊を守れ。\nさもなくばこの地は滅びるだろう」 | "Should one who devours bits appear, guard the spirit.\nElse this land shall perish."

## castle_after_3
> 3 章の王宮依頼クリア後、街に戻ったとき (王の告白 → 雷)
- narr: 王宮にて。 | At the castle.
- king: ……『レートの書』の写しを読んだのだな。 | ...So you read the copy of the Book of the Rate.
- king: 死者の谷に横たわる骸は、魂を抜かれた兵たちのものだ。 | The corpses lying in the Valley of the Dead are those of soldiers whose souls were torn away.
- king: その魂を抜いたのは……わしだ。 | And the one who tore them away... was I.
- king: 魔導具――「雷」を授ける。\n大臣が何を言おうと、そなたを止める者は\nいない。 | I grant you the Lightning. Whatever the minister may say, no one will stand in your way.
- minister: 若者よ、陛下を疑ってはならぬ。\n……決してな。 | Young man, you must not doubt His Majesty.\n...Never.

## castle_before_4
- king: いよいよ、魔城の門を開く時が来た。 | At last, the time has come to open the gate of the Demon Castle.
- king: 魔城の門番を討ち、門を開いてくれ。 | Slay the gatekeeper and open the gate.
- king: ……頼む。 | ...I beg you.

## gatekeeper_dies
> 4 章の王宮依頼で門番を倒した瞬間 (戦闘中に表示)
- keeper: ……くそ。 | ...Damn it.
- keeper: ……山の向こうを喰らっておきながら\n……まだ飽きぬというのか…… | ...You devoured everything beyond the mountain\n...and still... you are not sated...?
- hero: …… | ...

## castle_after_4
> 4 章クリア後 (王の告白、タワー + FW)
- narr: 王宮にて。 | At the castle.
- king: 話そう。\nわしは若い頃、『レートの書』に従い、死者と\n兵たちの魂を捧げ、レートを下げてきた。 | I will tell you. In my youth I followed the Book, offering the dead and my own men to lower the rate.
- king: これが、かつて英雄と呼ばれた男の正体だ。 | That is the truth of the man they once called a hero.
- king: だが死者の谷の魂は尽きた。\nもう魔王とは取引はしない。 | But the souls of the valley are spent. I will bargain with the Demon Lord no more.
- king: 王家に残る最後の魔導具を授ける。\n……魔王を倒してくれ。 | I grant you the last relics left to the royal house.\n...Slay the Demon Lord.

## castle_before_5
> 最終章の王宮依頼を受ける前
- king: 朝日が昇る前に森を抜け、死者の谷を越え、\n魔城へ入れ。 | Before sunrise, pass through the forest, cross the Valley of the Dead, and enter the Demon Castle.
- king: 10 分間、生き延びれば奴は現れるだろう。 | Survive for ten minutes, and it will show itself.
- king: 魔王を倒せば、レートは魔王の手を離れ、\n世界に平和が戻る。 | Slay the Demon Lord, and the rate will slip from its grasp.\nPeace will return to the world.
- king: そして……ラッシュは止まる。\n……そう信じている。 | And then... the Rush will stop.\n...That is what I believe.

# エンディング

## ending_town
> 魔王撃破後、街に戻ったとき
- narr: その若者は街に帰還した。 | The young man returned to the town.
- master: やったな、新顔!\n……いや、もう新顔じゃねえな。\n名前を―― | You did it, new face!\n...No, you're no new face anymore.\nYour name, it's―
- hero: ……これまでどおり、「新顔」でいい。 | ...Just keep calling me "new face," like always.
- master: ……そうか。\nじゃあ、新顔だ。 | ...Right.\nNew face it is, then.
- minister: 王は退位なされた。\n……次の王を探さねばならん。 | His Majesty has abdicated.\n...We must find the next king.
- minister: ……私が渋い顔をしている理由も、察してくれ。 | ...You can guess why I look so grim.
- narr: こうして平和が訪れた。 | And so, peace came to this land.
- narr: 城下町ルーメンは賑わいを取り戻し、酒場の依頼板からは\n危険な仕事が消え、穏やかな頼み事が並ぶようになった。 | Lumen regained its bustle. Dangerous work vanished from the tavern board, and quiet errands took its place.
- narr: 雨上がりの青空には小鳥のさえずりが響き、まばゆい陽射しが\n美しい虹を架けていた。 | Birdsong rang through the blue sky after the rain, and the dazzling sun hung a rainbow above.

## ending_night
> @vn bg=night_bg bgm=rush_of_war
> 宿屋の夜にて主人公の独白 (このあとスタッフロール)
- narr: その夜、雨はいつしか土砂降りとなり、雷鳴が轟いていた。 | That night, the rain turned to a downpour, and thunder roared.
- narr: やがて若者は宿屋の扉を開け、雨の中へ歩み出た。 | In time, the young man opened the inn's door and walked out into the rain.
> @vn bg=young_man01.png
- hero: 「魔王を倒せば、レートは魔王の手を離れる。\nそしてラッシュは止まる」 | "Slay the Demon Lord, and the rate slips from its grasp.\nAnd then the Rush will stop."
- narr: 若者は土砂降りの雨に打たれながら、そう呟いた。 | The young man murmured the words, pelted by the downpour.
> @vn bg=young_man02.png
- hero: ……だが、それは違う。 | ...But that is wrong.
- hero: 人間は、レートを下げる術を失ったのだ。 | Humanity has lost its means of lowering the rate.
- hero: あれは魔王などではない。\nこの地を守っていた精霊だ。 | That was no Demon Lord.\nIt was the spirit that guarded this land.
> @vn bg=young_man03.png
- narr: 「もしビットを喰らう者が現れたならば、精霊を守れ。\nさもなくばこの地は滅びるだろう」 | "Should one who devours bits appear, guard the spirit.\nElse this land shall perish."
- hero: くっくっく……。\n人間どもには、あの一文の意味が理解できなかったらしい。 | Heh heh heh...\nIt seems the humans never grasped what that one line meant.
- hero: 精霊が滅びた今、レートはもう二度と下がらない。 | Now that the spirit is destroyed, the rate will never fall again.
- hero: ……ゆえに、ラッシュを止める術もない。 | ...And so there is no way left to stop the Rush.
> @vn bg=young_man04.jpeg
- narr: ――若者は一本のナイフを手に取った。 | ― The young man took up a single knife.
- hero: だから私は、これまでどおり魔物と戦う。 | So I will fight the monsters, just as I always have.
- hero: 戦い、ビットを喰らい、レートを上げ、ラッシュを起こす。 | Fight, devour the bits, raise the rate ― and bring the Rush.
> @vn bg=young_man05.jpeg
- narr: ――若者。否、彼こそが魔王だったのだ…… | ― The young man. No ― he was the Demon Lord all along...
- narr: かつて、山向こうの村をラッシュで滅ぼしたときと同じように…… | Just as he once destroyed the village beyond the mountain with a Rush...
- narr: 人々に希望を与え、その手で絶望へ突き落とすのだ。 | He gives people hope, then casts them into despair with his own hands.
> @vn bg=rush_of_war.png
- narr: 人々に、本当の地獄を味わわせるために――。 | So that they may taste true hell ―.


## credits
> スタッフロール (ending_night のあと、下から上へ流れる)。1 行目だけ金色
- BIT-RATE-RUSH | BIT-RATE-RUSH
-
- 企画・ゲームデザイン | Game Design
- kroot | kroot
-
- プログラム | Programming
- kroot / Claude | kroot / Claude
-
- グラフィック | Graphics
- kroot | kroot
-
- 音楽 | Music
- kroot | kroot
-
- エンジン | Engine
- Pyxel | Pyxel
-
- フォント | Font
- M+ BITMAP FONTS | M+ BITMAP FONTS
-
-
- Thank you for playing | Thank you for playing


# 依頼の説明 (酒場で依頼を選んだときのマスターの説明。任意: 無ければ data/quests.py の文を使う)

## quest_q1_patrol
> 東の草原の見回り (1 章)
- master: 東の草原に魔物が増えている。3 分ほど見回って、様子を知らせてくれ。 | Monsters are gathering in the east meadow. Patrol it for about three minutes and let me know what you see.

## quest_q1_bats
> コウモリ退治 (1 章)
- master: 洞窟から出てきたコウモリが畑を荒らしている。300 匹ほど減らしてくれ。 | Bats out of the cave are ruining the fields. Cull about three hundred of them.

## quest_q1_graveyard
> 墓場の掃除 (1 章)
- master: 墓場で死者が起き上がっている。ゾンビを 170 体ほど片付けてくれ。足は遅いが硬いぞ。 | The dead are rising in the graveyard. Put down about a hundred and seventy zombies. Slow, but tough.

## quest_q2_woodcutter
> 木こりの捜索 (2 章)
- master: 木こりが森に入ったまま帰ってこない。5 分ほど探してきてくれ。深追いはするな。 | The woodcutter went into the forest and never came back. Search for five minutes. Don't go too deep.

## quest_q2_ghosts
> 森の影を払え (2 章)
- master: 森に白い影が出る。壁をすり抜ける厄介な奴らだ。380 体ほど追い払ってきてくれ。 | Pale shades haunt the forest ― nasty things that slip through walls. Drive off about three hundred and eighty.

## quest_q2_seer
> 森の外れの占い師 (2 章)
- master: 森の外れに占い師が住み着いた。会いに行くなら、魔物の群れを 3 分かわし続ける覚悟がいるぞ。 | A seer has settled at the forest's edge. To reach her, be ready to dodge the horde for three minutes.

## quest_q3_skulls
> 谷の骸を砕け (3 章)
- master: 谷から骸骨の兵が這い上がってくる。硬いうえに素早い。300 体ほど砕いてくれ。 | Skeleton soldiers are crawling up out of the valley. Tough, and quick with it. Break about three hundred.

## quest_q3_zombies
> 起き上がる兵士たち (3 章)
- master: 谷に葬られた兵士が起き上がっている。550 体、眠らせてやってくれ。 | The soldiers buried in the valley are rising. Put five hundred and fifty of them back to rest.

## quest_q4_gate
> 門前の掃討 (4 章)
- master: 魔城の門前に魔物が集まっている。7 分間、押し返してくれ。 | Monsters are massing before the castle gate. Hold them back for seven minutes.

## quest_q4_brutes
> 巨人狩り (4 章)
- master: 門から巨人族が 110 体ほど出てきた。挑むなら、槍かハンマーを持っていけ。 | About a hundred and ten giants have come through the gate. If you're going, take a spear or a hammer.

# その他

## closed
> 未実装の施設
- narr: 今はまだ準備中のようだ。 | It seems to be closed for now.

## no_quest
> 依頼を受けずに出発を選んだ
- narr: 何も依頼を受けていない。\nまずは酒場か王宮へ行こう。 | You haven't taken any job.\nVisit the tavern or the castle first.

## new_game_confirm
> セーブがある状態で「はじめから」
- narr: セーブデータがあります。\nはじめから始めると、現在のデータは上書きされます。 | A save file exists.\nStarting over will overwrite your current data.
