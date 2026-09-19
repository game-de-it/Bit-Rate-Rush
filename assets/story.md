# Bit-Rate-Rush 会話データ

ゲームはこのファイルを起動時に読む。書式:

- `## キー` で会話 1 本。キーはコードから参照される (変えない)
- `- 話者: 日本語 | English` で 1 ページ。話者は下の @speakers のキー
- `>` で始まる行はメモ (ゲームには出ない)。`#` 1 つの見出しは章分け用で無視される
- 英語を省くと日本語がそのまま使われる
- 文中の半角スペースは「ここで折り返してよい」の印 (収まらないときだけ改行)。`\n` (2 文字) は必ず改行
- `> @vn bg=画像名` を会話の先頭に置くと、ビジュアルノベル風 (上に 16:9 の絵 320x180、下に会話窓、立ち絵なし) で表示する。画像は assets/img/<画像名>.png、無ければ直前の画面を暗くして使う。窓は 3 行まで。話者に立ち絵があれば窓の左に小さく出る (`> @vn nopic` で消せる)
- ページの途中に `> @vn bg=画像名` を置くと、以降のページの絵がクロスフェードで切り替わる (拡張子は書いても無視される)。`> @vn bg=画像名 nofade` でフェードなしのカット切り替え
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
- narr: この世界の生き物は、ビットと呼ばれる光の粒を宿している。 | Every living thing in this world carries motes of light called bits.
- narr: 魔物を倒せばビットは散り、風に消える。 人は、それを拾うことができない。 | Slay a monster and its bits scatter on the wind. No human can gather them.
- narr: そしてレートが上がるとき、魔物は際限なく目を覚まし、\n群れとなって街へ押し寄せる。人はそれをラッシュと呼ぶ。 | And when the rate rises, monsters wake without end and pour toward the town. People call it the Rush.
> @vn bg=op_bg
- narr: 山向こうの村をラッシュに呑まれ、たった一人で城下町にたどり着いた若者。 | A young man who reached the castle town alone, after the Rush swallowed his village beyond the mountain.
- narr: ナイフ一本を手に、若者は城下町ルーメンの門をくぐった。 | Knife in hand, the youth passed through the gate of Lumen.
- narr: ――その日から、街の空にはコウモリが増えはじめたのだった。 | ― From that day on, bats began to gather over the town.

# 酒場 (ガルド)

## tavern_first
> 酒場に初めて入ったとき (1 回だけ)。このあと tavern_hello が続く
- master: 依頼を受けて魔物を減らすのが、この街の稼ぎ方だ。 | Taking jobs and thinning the monsters ― that's how you earn coin here.
- master: 魔物を倒すと光の粒が散るのを見るだろう。 ビットってやつだ。 きれいだが、人の手には残らねえ。 | When a monster dies, motes of light scatter ― bits. Pretty, but they slip through human hands.
- master: ただし長く戦うほどレートは上がる。 レートが上がりきったらラッシュだ。欲張るなよ。 | But the longer you fight, the higher the rate climbs. Let it peak, and the Rush comes. Don't get greedy.

## tavern_hello
> 酒場に入ったとき (章別の tavern_hello_N が無い章で使う)
- master: よう、新顔だな。 | Hey, new face.
- master: 仕事を探してるなら依頼板を見ていけ。 | If you're looking for a job, check out the job posting board.
- master: 危険な内容の依頼が多いから誰もやりたがらねぇけどな。 | Most of them are dangerous, though, so nobody wants to take them.

## tavern_hello_2
> 2 章の酒場。占い師の噂 → 隠し依頼が依頼板に並ぶ
- master: そういえば最近、森の様子がおかしいらしいぜ。 | Come to think of it, the forest has been acting strangely lately.
- master: 木こりが森から帰ってこねぇんだ。 | The woodcutter hasn't come back from the forest.
- master: ……そういや、森の外れに占い師が住み着いたって噂だ。\n変わり者らしいがな。 | ...Word is a seer's settled at the forest's edge. Odd one, they say.

## tavern_hello_3
- master: 死者の谷の話は、この街じゃ誰もしたがらねぇ。 | Nobody in this town wants to talk about the Valley of the Dead.
- master: 前のラッシュで死んだ連中が眠ってる場所だからだな。 | It's because that's where the guys who died in the last rush are resting.
- master: あの戦いの中で生き残ったのは\n王と俺だけだった。 | Only the King and I came out of that battle alive.
- master: ……死んだ連中が安らかに眠っていることを願うよ。 | ...I hope those who died are resting in peace.

## tavern_hello_4
- master: 魔城の門が開きかけてるらしいな。 | Word is the gate of the Demon Castle is starting to open.
- master: あんたが門番を倒せるなら、この街は救われるかもしれねぇ。 | If you can beat the gatekeeper, this town might just be saved.
- master: ……頼んだぞ、新顔。 | ...We're counting on you, new face.

## tavern_hello_5
- master: いよいよ出発か。 | So, the time has finally come to set off.
- master: 無事に帰ってきたら、お前の名前を聞かせてくれよ。 | When you get back safely, tell me your name.


## tavern_has_quest
> 受注中の依頼があるとき
- master: 受けた仕事はまだ片付いてないだろうから、まずはそっちを頼むよ。 | You've still got a job open. Finish that one first.

## tavern_accept
> 依頼を受けたとき
- master: よし、頼んだぞ。\n準備ができたなら街の門から出発してくれ。 | Good. It's yours. Head out through the town gate.

## seer_meet
> @vn bg=forest_bg
> 隠し依頼「森の外れの占い師」クリア後、森で会話 (衛星を入手)
- seer: ……よくここまで来たね。 | ...So you made it this far.
- seer: あんた、影が二つあるように見えるね。 | You look like you've got two shadows.
- seer: この魔法をあんたにやろう。\nあんたの周りを回って、守ってくれるはずさ。 | I'll give you this magic. It circles around you and should keep you safe.


# 宿屋 (ミラ)

## inn_hello
> 宿屋 (選択肢: 休む / やめる)
- inn: いらっしゃい。\n体が傷だらけじゃないの。休んでいかない? | Welcome, dear. You look battered. Care to rest?

## inn_rest
> 休んだあと
- inn: ゆっくりお休み。 | Sleep well...
- inn: ……朝よ。\n日記もつけておいたわ。 | It's morning. I've kept your journal, too.

## inn_poor
> お金が足りない
- inn: あら、お金が足りないみたい。\n稼いでからまたおいで。 | Oh, you're a bit short. Come back when you've earned some coin.

## inn_full
> HP が満タン
- inn: 十分元気そうね。\n今は休む必要はなさそうよ。 | You look fine to me. No need to rest right now.

## mira_2
> 2 章になって初めて宿屋に入ったとき (1 回だけ)。mira_3〜5 も同様
- inn: 王様に会ったんだって?\nあんた、本当に何者なの。 | You met the King? Who are you, really?

## mira_3
- inn: ……死者の谷には行かないで、\nとは言わないけど、あんたのことが心配なのよ。 | ...I won't tell you to stay out of the Valley of the Dead, but I'm worried about you.

## mira_4
- inn: 死者の谷の話は、ここでは誰もしないの…… | Nobody talks about the Valley of the Dead here...

## mira_5
- inn: ……無事に帰ってきなさいよ。 | ...Come back. That's all.


# 武器屋・雑貨屋

## smith_hello
- smith: ……見ていけ。\n金があるなら売ってやるぞ。 | ...Have a look. If you've got the money, I'll sell it to you.

## shop_hello
- shop: いらっしゃい。\n旅の道具なら何でも揃うよ。 | Welcome. We stock everything you need for your journey.
- shop: あなたの持っている袋には、3つまで収納できるよ。 | You can fit up to three items in the bag you're carrying.


# 王宮

## castle_refuse
> その章の酒場依頼を 1 件もクリアしていないとき (大臣)
- minister: 今は王の前には通せぬ。\nまずは街の役に立ってみせよ。 | I cannot grant you an audience with the King just yet. First, prove your worth to the town.

## castle_wait
> 王宮依頼を受注中
- minister: すでに下っている王の命令を果たしてから戻られよ。 | Return only after you have carried out the King's order that has already been issued.

## castle_done
> その章の王宮依頼をクリア済み
- minister: ……王は休んでおられる。\n今は何も話すことはない。 | ...The King is resting. There is nothing to discuss right now.

## castle_before_1
> 1 章の王宮依頼を受ける前 (このあと依頼文が王の台詞として続き、受ける / やめる)
- minister: 陛下、この者の素性は知れません…… | Your Majesty, the identity of this person is unknown...
- king: かまわぬ。\n……そなたが、草原の魔物を退治している者か。 | It matters not. ...So you are the one thinning the monsters in the meadow?
- king: 酒場のガルドから、そなたの活躍は聞いておる。 | I've heard about your achievements from Garld.
- king: 最近になってコウモリが空を覆い始めており、\nレートが上がる兆しを感じるのだ。 | Of late, bats have begun to darken the sky. I sense the rate is about to rise.
- king: まずは城下の草原に現れたコウモリの群れを\n一掃してもらいたい。 | First, I want you to wipe out the swarm of bats in the meadow below the castle.

## castle_after_1
> 1 章の王宮依頼クリア後、街に戻ったとき (魔法弾を入手、2 章へ)
- narr: 王宮にて。 | At the castle.
- king: 見事な活躍だったな。\n褒美にこれを授けよう。 | You performed magnificently. I shall bestow this upon you as a reward.
- king: 王家に伝わる魔導具\n――魔法弾だ。 | A relic passed down through the royal house ― the Magic Bolt.
- king: 魔導具は使い手を選ぶ。 | A relic chooses its wielder.
- king: 魔導具がそなたを選んだのなら、それが答えだ。 | If the relic chose you, then that is the answer.
- minister: (……気に入らぬ。\n素性もわからぬものに魔導具を与えるなど……) | (...I do not like this. Handing a relic to someone of unknown origin...)

## castle_before_2
- king: 森の奥に「魔城の門」がある。\nわしが若い頃に閉じたはずの場所だ。 | Deep in the forest lies the Gate of the Demon Castle. I thought I had sealed it in my youth.
- king: 森の魔物がそれを守るように居座っている。 | A monster of the forest has settled there, as if guarding it.
- king: 理由は聞かずにその魔物を討ってくれぬか。 | Slay it for me ― and ask no reason.

## castle_after_2
- narr: 王宮にて。 | At the castle.
- king: よくやってくれた。\nそなたに王家に伝わる魔導具\n――聖水を授けよう。 | Well done. I grant you the Holy Water, a relic of the royal house.
- king: ……門の向こうには、わしが語らぬ理由がある。今はまだ、聞かんでくれ。 | ...Beyond that gate lies a reason I do not speak of. Not yet. Do not ask.

## castle_before_3
- king: 死者の谷を調べてほしい。 | I want you to investigate the Valley of the Dead.
- king: 谷の奥にある祭壇に、古い書の写しがある。 | There is a copy of an ancient text on the altar deep within the valley.
- minister: 陛下! それは―― | Your Majesty! That is―
- king: よい。\n……7 分だ。それ以上は谷に留まるなよ。 | Enough. ...Seven minutes. Do not stay in the valley any longer than that.
- king: 亡霊に食い殺されるからな。 | The specters would tear you apart and devour you.

## book_found
> 3 章の王宮依頼「谷を調査せよ」を達成した瞬間、谷の祭壇で (ビジュアルノベル風)
> @vn bg=valley_bg
- narr: 死者の谷の祭壇にあったのは『レートの書』の写し―― | On the altar of the Valley of the Dead lay a copy of the Book of the Rate ―
- narr: 「魂を捧げれば精霊は目覚め、レートを下げる」 | "Offer souls, and the spirit wakes to lower the rate."
- narr: 「精霊は語らず。その影を魔と呼ぶなかれ」 | "The spirit speaks not. Call not its shadow a demon."
- narr: 「もしビットを喰らう者が現れたならば、精霊を守れ。\nさもなくばこの地は滅びるだろう」 | "Should the Devourer of Bits appear, guard the spirit ― or this land shall perish."

## castle_after_3
> 3 章の王宮依頼クリア後、街に戻ったとき (王の告白 → 雷)
- narr: 王宮にて。 | At the castle.
- king: ……『レートの書』の写しを読んだか。 | ...You read the copy of the Book of the Rate, then.
- king: 死者の谷の骸たちは、魂を抜かれた兵士だ。 | The corpses in the valley are soldiers whose souls were torn away.
- king: 魂を抜いたのは、この、わしだ。 | It was I who tore out their souls.
- king: 魔導具――雷を授ける。\n大臣が何を言おうと、そなたを止める者は\nいない。 | I grant you the Lightning. Whatever the minister says, no one will stop you.
- minister: 若者よ、陛下を疑うな。\n……疑うなよ。 | Young man, do not doubt His Majesty. ...Do not doubt him.

## castle_before_4
- king: 魔城の門を開ける時がついに来た。 | The time has come at last to open the gate of the Demon Castle.
- king: 魔城の門番を倒し、門を開けてくれ。 | Defeat the gatekeeper and open the gate.
- king: ……頼む。 | ...Please.

## gatekeeper_dies
> 4 章の王宮依頼で門番を倒した瞬間 (戦闘中に表示)
- keeper: ……くそ。 | ...Damn it.
- keeper: ……山の向こうを、喰った\n……まだ飽きたらぬのか…… | ...Beyond the mountain... all of it, devoured... and still... not sated...?
- hero: …… | ...

## castle_after_4
> 4 章クリア後 (王の告白、タワー + FW)
- narr: 王宮にて。 | At the castle.
- king: 話そう。\nわしは若い頃、『レートの書』に従って死者と\n兵の魂を捧げ、レートを下げてきた。 | In my youth I followed the Book: I offered the souls of the dead and of my men, and the rate fell.
- king: これが昔、英雄と呼ばれた男の正体だ。 | This is the true identity of the man once hailed as a hero.
- king: だが死者の谷の魂は尽きた。\nもう魔王とは取引はしない。 | But the souls of the valley are spent. I will bargain with the Demon Lord no more.
- king: 王家最後の魔導具を授ける。\n……魔王を、倒してくれ。 | I grant you the last relics of the royal house. ...Slay the Demon Lord.

## castle_before_5
> 最終章の王宮依頼を受ける前
- king: 朝日が昇る前に森を抜け、死者の谷を越え、\n魔城へ入れ。 | Before the sun rises, leave the forest, cross the Valley of the Dead, and enter the Demon Castle.
- king: 10 分間、生き延びれば奴は現れるだろう。 | Survive ten minutes, and it will come.
- king: 魔王を倒せば、レートは魔王の手を離れ、\n世界に平和が戻る。 | Slay the Demon Lord, and the rate will slip from its grasp. Peace will return to the world.
- king: そして……ラッシュは止まる。\n……そう信じている。 | And then... the rush will stop. ...That is what I believe.

# エンディング

## ending_town
> 魔王撃破後、街に戻ったとき
- narr: その若者は街に帰還した。 | The young man returned to the town.
- master: やったな、新顔!\n……いや、もう新顔じゃねえな。\n名前を―― | You did it, new face! ...No, not a new face anymore. Your name, it's―
- hero: ……いつも通りそのまま「新顔」でいい。 | ...You can just keep calling me "New Face," as always.
- master: ……そうか。\nじゃあ、新顔だ。 | ...Right. New face it is, then.
- minister: 王は退位なされた。\n……次の王を探さねばならん。 | The King has abdicated. ...We must find the next.
- minister: 渋い顔になるのも、分かってくれ。 | You must understand why I look so grim.
- narr: こうして平和が訪れた。 | And so, peace came to this land.
- narr: 城下町ルーメンは賑わいを取り戻し、酒場の依頼板には\nかつてのような危険な依頼は消え、平和な依頼が並んでいた。 | Lumen regained its bustle. The dangerous jobs vanished from the tavern board, replaced by peaceful ones.
- narr: 青空には小鳥達がさえずり、まばゆいばかりに輝く太陽が\n綺麗な虹を作り上げるのだった。 | Small birds chirped in the blue sky, and the dazzling sun created a beautiful rainbow.

## ending_night
> @vn bg=night_bg bgm=rush_of_war
> 宿屋の夜にて主人公の独白 (このあとスタッフロール)
- narr: その夜、雨は土砂降りに変わり、雷が鳴り響いていた。 | That night, the rain turned into a downpour, and thunder rumbled loudly.
- narr: 宿屋の扉を開けて外に出る、若者の後ろ姿が見えた。 | The young man was seen opening the inn's door and stepping out into the night.
> @vn bg=young_man01.png
- hero: 「魔王を倒せば、レートは魔王の手を離れ、世界に戻る。\nラッシュは止まる」 | "Slay the Demon Lord, and the rate returns to the world. The rush will end."
- narr: その若者は土砂降りに打たれながら、そう呟く。 | He murmurs it, pelted by the downpour.
> @vn bg=young_man02.png
- hero: ……でも、それは違う。 | ...But that's not right.
- hero: 人は、レートを下げる手段を失ったのだ。 | Humans have lost the means to lower the rate.
- hero: あれは魔王ではない。\nこの地を守る精霊だったのだ。 | That was no Demon Lord. It was the spirit that guarded this land.
> @vn bg=young_man03.png
- narr: 「もしビットを喰らう者が現れたならば、精霊を守れ。\nさもなくばこの地は滅びるだろう」 | "Should the Devourer of Bits appear, guard the spirit ― or this land shall perish."
- hero: くっくっく……\n人間にはあの文の意味を理解できなかったようだ。 | Heh heh heh... It seems humans never grasped the meaning of those words.
- hero: 精霊が滅びた今、もう"レート"は下がらない。 | Now that the spirit is gone, the rate will never fall again.
- hero: ……そしてラッシュは防げない。 | ...And the rush cannot be stopped.
> @vn bg=young_man04.jpeg
- narr: ――若者は、ナイフを一本、手に取った。 | ― The youth picked up a single knife.
- hero: だから私は、いつものように魔物と戦う。 | So I will fight the monsters, as I always have.
- hero: 戦い、ビットを喰らい、レートを上げ、ラッシュを起こす。 | Fight, devour the bits, raise the rate ― and bring the rush.
> @vn bg=young_man05.jpeg
- narr: ――若者、違う。\n彼こそ魔王だったのだ…… | ―Young man, no. He was the Demon King...
- narr: 山向こうの村をラッシュによって滅ぼした時のように…… | Like when the village on the other side of the mountain was destroyed by rush...
- narr: 人々に希望を与えてから……絶望させるのだ。 | Give people hope and then... make them despair.
> @vn bg=rush_of_war.png
- narr: 本当の地獄を……人々に味わわせるために。 | To make them taste true hell...



# 依頼の説明 (酒場で依頼を選んだときのマスターの説明。任意: 無ければ data/quests.py の文を使う)

## quest_q1_patrol
> 東の草原の見回り (1 章)
- master: 東の草原に魔物が増えている。3 分ほど見回って、様子を報せてくれ。 | Monsters are gathering in the east meadow. Patrol it for three minutes and report back.

## quest_q1_bats
> コウモリ退治 (1 章)
- master: 洞窟から出てきたコウモリが畑を荒らしている。300 匹ほど減らしてくれ。 | Bats from the cave are ruining the fields. Cull about three hundred of them.

## quest_q1_graveyard
> 墓場の掃除 (1 章)
- master: 墓場で死者が起き上がっている。ゾンビを 170 体片付けてくれ。足は遅いが硬いぞ。 | The dead are rising in the graveyard. Put down a hundred and seventy zombies. Slow, but tough.

## quest_q2_woodcutter
> 木こりの捜索 (2 章)
- master: 森へ入った木こりが帰ってこない。5 分ほど森を探ってきてくれ。深追いはするな。 | A woodcutter went into the forest and never came back. Search it for five minutes. Don't go too deep.

## quest_q2_ghosts
> 森の影を払え (2 章)
- master: 森に白い影が出る。壁をすり抜けるやつだ。380 体ほど払ってきてくれ。 | Pale shades haunt the forest ― the kind that slip through walls. Banish three hundred and eighty.

## quest_q2_seer
> 森の外れの占い師 (2 章)
- master: 森の外れに占い師が住み着いた。会いに行くなら、魔物の群れを 3 分かわす覚悟がいる。 | A seer has settled at the forest's edge. To reach her you'll dodge the swarm for three minutes.

## quest_q3_skulls
> 谷の骸を砕け (3 章)
- master: 谷から骸骨の兵が上がってくる。硬くて速い。300 体砕いてくれ。 | Skeleton soldiers climb out of the valley ― hard and fast. Break three hundred.

## quest_q3_zombies
> 起き上がる兵士たち (3 章)
- master: 谷に葬られた兵士が起き上がっている。550 体、眠らせてやってくれ。 | Soldiers buried in the valley are rising. Put five hundred and fifty of them back to rest.

## quest_q4_gate
> 門前の掃討 (4 章)
- master: 魔城の門前に魔物が集まっている。7 分間、押し返してくれ。 | Monsters mass before the castle gate. Hold them back for seven minutes.

## quest_q4_brutes
> 巨人狩り (4 章)
- master: 門の巨人族が 110 体ほど出てきた。相手にするなら、槍かハンマーだ。 | A hundred and ten giants or so have come out from the gate. Bring a spear or a hammer.

# その他

## closed
> 未実装の施設
- narr: まだ準備中のようだ。 | It seems to be closed for now.

## no_quest
> 依頼を受けずに出発を選んだ
- narr: 依頼を受けていない。\nまず酒場か王宮へ行こう。 | No job accepted. Visit the tavern or the castle first.

## new_game_confirm
> セーブがある状態で「はじめから」
- narr: セーブデータがあります。\nはじめから始めると上書きされます。 | A save exists. Starting over will overwrite it.
