# サードパーティ表記 / Third-party notices

Bit-Rate-Rush が同梱・利用している第三者の成果物とその出所です。

---

## umplus_j10r.bdf（日本語ビットマップフォント）

ゲーム内の全ての文字表示に使用しています。

| | |
|---|---|
| ファイル | `assets/umplus_j10r.bdf` |
| 出所 | [Pyxel](https://github.com/kitao/pyxel) の `pyxel/examples/assets/` に同梱されているものと**バイト単位で同一** |
| BDFヘッダの表記 | `FOUNDRY "umplus"` / `COPYRIGHT "Copyright (C) 2002-2004 COZ"` |
| 系統 | U-M+ / M+ 系のビットマップフォント |

```
FOUNDRY   "umplus"
COPYRIGHT "Copyright (C) 2002-2004 COZ"
```

Used for all in-game text. The file is byte-identical to the one bundled with
Pyxel's example assets. The BDF header credits COZ (2002–2004), foundry "umplus" —
the U-M+ / M+ bitmap font lineage.

---

## Pyxel

本作は [Pyxel](https://github.com/kitao/pyxel)（レトロゲームエンジン）の上で
動作します。Pyxel 自体は同梱していませんが、実行に必要です。

- MIT License / Copyright (c) 2018-2026 Takashi Kitao

---

## パレット / Palette

`assets/brr.pyxpal` の先頭 16 色は Pyxel の標準パレットです。残りの 48 色は本作のために選んだものです。

The first 16 colours of `assets/brr.pyxpal` are Pyxel's default palette; the
remaining 48 are original to this project.

---

## 本作のオリジナル素材

次のものは本作のために作られたもので、上記の第三者成果物には含まれません。
利用条件は [LICENSE-assets.md](LICENSE-assets.md) を参照してください。

- `assets/bgm/` — BGM・ジングル
- `assets/img/` — タイトル、場面の絵、立ち絵、アイコン
- `assets/story*.md` — 会話・物語のテキスト
- ソースコード一式

These are original to this project and are not third-party works. See
[LICENSE-assets.md](LICENSE-assets.md) for their terms.
