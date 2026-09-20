"""多言語対応。全ての表示文字列は t(key) を通す。データ側の (ja, en) タプルは tt() で引く。"""

LANGS = ["ja", "en"]
lang = "en"      # 既定は英語 (日本語が読めない人がオプションにたどり着けるように)

STR = {
    # タイトル / オプション
    "title.continue": ("つづきから", "CONTINUE"),
    "title.new": ("はじめから", "NEW GAME"),
    "title.survival": ("サバイバル (検証用)", "SURVIVAL (test)"),
    "title.dialogs": ("会話ビューア (検証用)", "DIALOG VIEWER (test)"),
    "ending.tbc": ("後編へ続く", "To be continued"),
    "ending.tbc_sub": ("Bit-Rate-Rush アリア編", "Bit-Rate-Rush: Aria"),
    "title.chapter": ("章スタート (検証用)", "CHAPTER START (test)"),
    "title.stage": ("検証ステージ", "TEST STAGE"),
    "title.start": ("はじめる", "START"),
    "title.overwrite": ("上書きして始める", "Overwrite and start"),
    "title.options": ("オプション", "OPTIONS"),
    "title.quit": ("終了", "QUIT"),
    "title.move": ("移動: 十字キー / スティック / WASD", "MOVE: D-PAD / STICK / WASD"),
    "title.goal": ("10分間 生き延びろ", "SURVIVE 10 MINUTES"),
    "title.proto": ("- プロトタイプ -", "- prototype -"),
    "opt.title": ("オプション", "OPTIONS"),
    "opt.lang": ("言語", "LANGUAGE"),
    "opt.bgm": ("BGM 音量", "BGM VOLUME"),
    "opt.se": ("効果音 音量", "SE VOLUME"),
    "opt.battle_vol": ("戦闘BGM 音量", "BATTLE BGM VOL"),
    "opt.battle": ("戦闘BGM", "BATTLE BGM"),
    "opt.shuffle": ("シャッフル", "Shuffle"),
    "opt.sequence": ("順番", "In order"),
    "pause.options": ("オプション", "Options"),
    "opt.back": ("もどる", "BACK"),
    "opt.hint": ("左右で変更  B: もどる", "LEFT/RIGHT: change  B: back"),
    # 街
    "town.title": ("城下町", "Castle Town"),
    "town.castle": ("王宮", "Castle"),
    "town.tavern": ("酒場", "Tavern"),
    "town.smith": ("武器屋", "Weaponsmith"),
    "town.shop": ("雑貨屋", "General Store"),
    "town.smith_s": ("武器屋", "Smithy"),       # 街の左メニュー用 (幅 68px に収める)
    "town.shop_s": ("雑貨屋", "Store"),
    "town.inn": ("宿屋", "Inn"),
    "town.depart": ("出発", "Depart"),
    "town.gold": ("所持金", "Gold"),
    "town.chapter": ("章", "Ch."),
    "chapter.n": ("第{0}章", "Chapter {0}"),
    "chapter.final": ("最終章", "Final Chapter"),
    "town.quest": ("依頼", "Quest"),
    "town.noquest": ("なし", "none"),
    "town.day": ("日目", "Day"),
    "tavern.board": ("依頼板", "Job Board"),
    "tavern.empty": ("今は依頼がない", "No jobs right now"),
    "tavern.empty_hint": ("王宮へ行こう。", "Head to the castle."),
    "town.d.castle": ("王宮。王からの特別な依頼を受けられる。", "The castle. Special requests from the King."),
    "town.d.tavern": ("酒場。依頼板から仕事を選べる。", "The tavern. Pick a job from the board."),
    "town.d.smith": ("武器屋。物理武器の購入と強化。", "Weaponsmith. Buy and upgrade weapons."),
    "town.d.shop": ("雑貨屋。消耗アイテムを買える。", "General store. Consumable items."),
    "town.d.inn": ("宿屋。休んで回復し、日記をつける。", "The inn. Rest, recover, and save."),
    "town.d.depart": ("街の門から依頼へ出発する。", "Leave through the gate for your quest."),
    "town.d.quest": ("受注中", "Current job"),
    "tavern.reward": ("報酬", "Reward"),
    "tavern.limit": ("制限", "Limit"),
    "tavern.cleared": ("済", "done"),
    "tavern.accept": ("受ける", "Accept"),
    "tavern.leave": ("やめる", "Leave"),
    "shop.buy": ("購入", "Buy"),
    "shop.maxed": ("最大", "MAX"),
    "shop.max": ("これ以上は強化できない。", "It can't be upgraded further."),
    "shop.full": ("袋がいっぱいだ (3 個まで)。", "Your bag is full (3 max)."),
    "shop.poor": ("お金が足りない。", "Not enough gold."),
    "shop.bought": ("買った。", "Purchased."),
    "shop.ranked": ("強化した。", "Upgraded."),
    "shop.rank_desc": ("ランクごとに攻撃力 +20%", "+20% damage per rank"),
    "shop.hint": ("A: 買う  B: 出る", "A: buy  B: leave"),
    "shop.bag": ("袋", "Bag"),
    "depart.equip": ("初期武器 (左右で選択)", "Starting weapon (left/right)"),
    "depart.items": ("持ち物", "Items"),
    "inn.rest": ("休む", "Rest"),
    "inn.rest_cost": ("休む ({0}G)", "Rest ({0}G)"),
    "inn.leave": ("やめる", "Leave"),
    "depart.title": ("出発準備", "Ready to Depart"),
    "depart.goal": ("目標", "Goal"),
    "depart.weapons": ("装備", "Gear"),
    "depart.slots": ("武器枠", "Weapons"),
    "depart.pslots": ("パッシブ枠", "Passives"),
    "depart.stash": ("装備を整理する (預ける)", "Manage gear (stash)"),
    "depart.go": ("出発する", "Depart"),
    "stash.title": ("装備の整理", "Manage Gear"),
    "stash.equip": ("初期武器", "Starting"),
    "stash.stored": ("預けている", "Stashed"),
    "stash.carry": ("持ち込む", "Carry"),
    "stash.hint": ("A: 切替  B: 戻る   預けた装備は戦闘中に出ない", "A: toggle  B: back   Stashed gear stays out of battle"),
    "depart.back": ("戻る", "Back"),
    "goal.survive": ("{0} 生き延びる", "Survive {0}"),
    "goal.kill": ("{0} を {1} 体倒す", "Defeat {1} {0}"),
    "goal.boss": ("{0} を倒す", "Defeat the {0}"),
    "run.cleared": ("依頼達成！  START で帰還", "QUEST CLEAR!  START to return"),
    "run.left": ("残り", "Left"),
    "run.rush": ("ラッシュ！ 出現 2 倍", "RUSH! Double spawns"),
    "run.bonus": ("ボーナスラッシュ {0} 分！ 出現 2 倍", "BONUS RUSH {0} min! Double spawns"),
    "pause.return": ("帰還する", "Return to town"),
    "pause.retreat": ("撤退する (依頼失敗)", "Retreat (fail quest)"),
    "res.return": ("帰還", "Returned"),
    "res.dead": ("戦闘不能", "Knocked out"),
    "res.quest_ok": ("依頼達成", "Quest complete"),
    "res.quest_ng": ("依頼失敗", "Quest failed"),
    "res.gold": ("拾った金", "Gold found"),
    "res.reward": ("依頼料", "Quest reward"),
    "res.halved": ("(半分になった)", "(halved)"),
    "res.hp": ("HP", "HP"),
    "res.to_town": ("A: 街へ戻る", "A: Back to town"),
    "dlg.next": ("A: 次へ", "A: next"),
    # HUD
    "hud.kill": ("撃破", "KILL"),
    "hud.boss": ("ボス", "BOSS"),
    "hud.gold": ("G", "G"),
    # レベルアップ
    "lv.title": ("レベルアップ！", "LEVEL UP!"),
    "lv.new": ("新", "NEW"),
    "lv.potion": ("薬", "Potion"),
    "lv.potion.desc": ("HP 30 回復", "Heal 30 HP"),
    "lv.max": ("最大", "MAX"),
    # ポーズ
    "pause.title": ("ポーズ", "PAUSED"),
    "pause.resume": ("再開", "RESUME"),
    "pause.title_back": ("タイトルへ", "QUIT TO TITLE"),
    "pause.exit": ("ゲーム終了", "EXIT GAME"),
    # リザルト
    "res.win": ("生き延びた！", "YOU SURVIVED!"),
    "res.lose": ("ゲームオーバー", "GAME OVER"),
    "res.time": ("時間", "TIME"),
    "res.level": ("レベル", "LEVEL"),
    "res.kills": ("撃破数", "KILLS"),
    "res.press": ("A / Z ボタン", "PRESS A / Z"),
    # 武器パラメータ名
    "st.dmg": ("攻撃力", "DMG"),
    "st.amount": ("本数", "Amount"),
    "st.cd": ("間隔", "Cooldown"),
    "st.pierce": ("貫通", "Pierce"),
    "st.r": ("範囲", "Area"),
    "st.dur": ("持続", "Duration"),
    "st.rot": ("回転", "Spin"),
    "st.speed": ("弾速", "Speed"),
    "st.reach": ("リーチ", "Reach"),
    "st.length": ("長さ", "Length"),
    "st.range": ("射程", "Range"),
    "st.turn": ("旋回", "Turn"),
}


def t(key):
    v = STR.get(key)
    if v is None:
        return key
    return v[LANGS.index(lang)]


def tt(pair):
    """データ側の (ja, en) タプルから現在言語の文字列を返す。"""
    if isinstance(pair, str):
        return pair
    return pair[LANGS.index(lang)]


def set_lang(l):
    global lang
    if l in LANGS:
        lang = l
