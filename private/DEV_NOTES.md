> 開発メモ (非公開)。公開用の README は リポジトリ直下の README.md / README.en.md。

# Bit-Rate-Rush (BRR)

Pyxel 製ヴァンサバ系ゲーム。設計は [DESIGN.md](DESIGN.md)。

## 起動

```bash
python3 main.py
```

要 `pyxel >= 2.9` (`pip install pyxel`)。画像・音はすべてコード生成なので pyxres 不要。

- パレット: `assets/brr.pyxpal` (標準 16 色 + ゲーム用 16 色 + 画像用 32 色 = **64 色**、`core/palette.py` に名前定義)。スプライト・UI は 0〜31 だけで描き、32〜63 は立ち絵・背景の減色用 (紫・肌・木・石・緑・空・金属など)。背景は暗い低彩度 (16〜18)、敵は高彩度 + 縁取り (19)
- フォント: `assets/umplus_j10r.bdf` (M+ 10px、日本語グリフ入り) を `ui/font.py` 経由で使う
- 多言語: 表示文字列は `core/i18n.py` の `t(key)`、データ側は `(ja, en)` タプルを `tt()` で引く。設定は `core/settings.py` が `user_data_dir/settings.json` に保存

## 操作

| 操作 | キーボード | ゲームパッド |
|---|---|---|
| 移動 | WASD / 矢印 | D-pad / 左スティック |
| 決定 | Z / Enter / Space | A |
| ポーズ | Esc | START |
| ポーズメニュー | 上下 + Z で選択 (再開 / タイトル / 終了) | D-pad + A |
| アイテム (依頼中) | Q / E で選択、C で使用 | L / R で選択、Y で使用 |
| タイトルメニュー | 上下 + Z (はじめる / オプション / 終了) | D-pad + A |
| オプション | 左右で言語切替 (日本語 / English)、X でもどる | 左右 + B |

## 構成

```
main.py            起動 (320x240 / 60fps)
config.py          画面サイズ・オブジェクト上限
game.py            シーンスタック + Scene 基底
core/   input.py   入力正規化   spatial.py 空間ハッシュ   sprites.py プロトタイプ絵   audio.py SE/BGM   palette.py 32色パレット
data/   enemies.py 敵表   weapons.py 武器・パッシブ表   waves.py ウェーブ表
entities/ player / enemy / bullet / pickup / particle
systems/ spawner.py 出現   weapons.py 発射 (一斉/連射/ハンマー/衛星)   collision.py 当たり判定   upgrades.py 3択抽選
scenes/ title / options / play (メインループ) / levelup / pause / result
ui/     hud.py     menu.py   font.py (BDF フォント)
```

## ストーリーモード

タイトル「はじめから / つづきから」→ 街 (`scenes/town.py`) → 酒場で依頼受注 → 出発 → 戦闘 (依頼の条件付き) → 帰還リザルト → 街。
「サバイバル (検証用)」は従来の 10 分モード。

- セーブ: `core/save.py` が `user_data_dir/save.json` に保存 (`core/state.py` の GameState)
- 依頼: `data/quests.py` (生存 / 討伐)、ウェーブ表は `data/waves.py` の `WAVES[キー]`
- 会話の表示は 2 種類: 街用 (白い窓 + 立ち絵) と、`> @vn bg=画像名` を付けたビジュアルノベル風 (全画面背景 + 暗い窓 + 名前札)。VN 用の絵は `op_bg` (オープニング) / `forest_bg` (占い師) / `valley_bg` (書の発見) / `night_bg` (エンディング) を **320x180 (16:9)** で置く (画面上部にそのまま表示、下 60px が会話窓)
- 施設の出入り・出発・帰還は `game.push_fade / pop_fade / replace_fade` で暗転する
- 会話: **`assets/story.md`** (Markdown、書式はファイル冒頭) を `data/story.py` が起動時に読み、`scenes/dialog.py` が表示。後編の導入は `assets/story_teaser.md`。ストーリー資料と後編の草稿は `private/` (リポジトリ非公開)。`python3 tools/check_story.py` でキーの漏れを検証。話者の `img` に対応する `assets/img/<名前>.png` があれば立ち絵 (64x64) を出す
- 画像: `tools/convert_png.py <png> <名前> [幅 高さ]` で 64 色に減色して `assets/img/` へ。`core/images.py` が読み込む
  - 街の背景 `town_bg.png` (234x156)、タイトル `title_bg.png` (320x240)、酒場 `tavern_bg.png` (234x156)
  - NPC 立ち絵 (64x64) は `npc_master` / `npc_inn` / `npc_shop` / `npc_smith` / `npc_king`。**小さい絵は `--nodither` の方がきれい** (ディザは 64px だと潰れる)。元絵 (1:1) を切り抜かずそのまま変換するのが正 (雰囲気と小道具が伝わる)。顔を大きく見せたい場合だけ元絵側でクロップする。立ち絵は不透明で描く (透過なし)
- 帰還ルール: HP 持ち越し (50% 未満なら 50% に補正)、戦闘不能は拾った金が半分、撤退は依頼失敗
- 武器スロットは章で決まる (`core/state.py` の SLOTS_BY_CHAPTER)、レベルアップ候補は所持装備のみ
- 武器屋: `data/shop.py` (品揃え・価格・ランク費)。雑貨屋: `data/items.py`。ラン中のアイテム効果: `systems/items.py`

## バランス調整のポイント

- 敵の出現量: `data/waves.py`
- 敵の強さ: `data/enemies.py` (+ `systems/spawner.py` の `hp_mult` で時間経過補正)
- 武器の伸び: `data/weapons.py` の `levels`
- レベル必要 XP: `entities/player.py` の `need_xp`
- 同時数上限: `config.py`

## 開発メモ

- `pyxel.perf_monitor(True)` を `main.py` で有効にするとフレーム時間が見える。
- 実機 (ハンドヘルド) で 60fps が出ない場合は `config.py` の上限を下げるか、`FPS = 30` にして速度定数を 2 倍にする。

## 実機 (plumOS-Bubble / RK3566) での実行

```bash
SSHPASS=<password> ./deploy_bubble.sh run
```

- 転送先: `/storage/user/Roms/pyxel/Bit-Rate-Rush/`
- 起動は plumOS の `plumos-pyxel-bubble-launch` 経由 (CPU を performance に切替、KMSDRM + Mali、640x480 に整数倍フィット)
- **フロントエンド (plumos-controller-ui-fbdev) は止めてから実行する。** 同時に動かすと描画が競合してフレームが落ちる。`plumos-portmaster-frontend-control acquire / release` で停止・復帰できる (スクリプトが自動で行う)
- ログ: `/storage/plumos/logs/pyxel/runtime.log`

### 負荷計測

```bash
SSHPASS=<password> ./deploy_bubble.sh bench stress 40   # 敵150体の上限負荷
SSHPASS=<password> ./deploy_bubble.sh bench run 690     # 10分通し自動プレイ
```

`bench.py` は無敵の自動プレイで 5 秒ごとに fps / update / draw の時間をログに出す。

計測結果 (2026-09-13, performance governor, FE 停止):

| ケース | fps | update | draw |
|---|---|---|---|
| 敵 150 体 + 全武器 Lv4 | 60.0 固定 | 4.4〜5.6ms (max 6.7) | 1.4〜1.8ms (max 2.6) |

→ 設計時の上限 (敵 150 / 弾 200 / ジェム 300) のままで 60fps に収まる。

### pyxapp 化

```bash
# 実行に不要なファイルを除いた複製から作る (bench.py 等を含めない)
rsync -a --exclude bench.py --exclude '*.sh' --exclude 'README.md' --exclude 'DESIGN*.md' --exclude dist --exclude tools --exclude docs --exclude art ./ /tmp/pkg/Bit-Rate-Rush/
cd /tmp/pkg && pyxel package Bit-Rate-Rush Bit-Rate-Rush/main.py
```

できた `Bit-Rate-Rush.pyxapp` を実機の `/storage/user/Roms/pyxel/` に置くとフロントエンドから起動できる。最新ビルドは `dist/Bit-Rate-Rush.pyxapp`。
