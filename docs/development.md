# 開発メモ

このMODを更新する人向けのメモです。遊ぶだけなら読む必要はありません。

## ビルドとバージョン番号

中身は訳文だけなので、同じ訳文から 2.0 用と 2.1 用の zip を作ります。
Factorio は info.json の `factorio_version` に1つの値しか書けず、2.1 は 2.0 向けのMODを読み込まないためです。
MODポータルでは同じMODページに両方のリリースを載せるので、遊ぶ人はふつうに有効化するだけで、自分の Factorio に合う方が入ります。

```
python3 tools/check_format.py   # Factorio が読めない書き方（重複セクションなど）がないか確認
python3 tools/build.py          # dist/ に 2.0 用と 2.1 用の zip を作る
```

バージョン番号の末尾は Factorio のバージョンを表します（例: 0.2.0 が 2.0 用、0.2.1 が 2.1 用）。
中身を更新したときは真ん中の数字を上げます。ポータルには 2.0 用、2.1 用の順に上げます。

## 構成

- `locale/ja/<対象MOD名>.cfg` … 対象MODごとの日本語ロケール
- `tools/check_keys.py` … 対象MODの英語ロケールと比べて未訳キーを出す
- `tools/coverage.py` … modフォルダを見て、MODごとの訳済み・未訳のキー数を表にする
- `tools/check_conflicts.py` … ほかの日本語化MODとキーが重なっていないか調べる
- `tools/check_tags.py` … 訳文のタグや変数が英語と同じか調べる
- `tools/check_format.py` … 同じセクションやキーが1ファイルに2回出ていないか確認する（`--fix` で重複セクションをまとめる）
- `tools/build.py` … `dist/` に配布用zipを作る（2.0 / 2.1）

## 翻訳方針

Any_Japanise_Pack に合わせます。

- 基本は直訳
- Factorio公式の日本語訳に寄せる（例: Assembler MK4 → 組立機4）。用語は [glossary.md](glossary.md)
- バニラの項目名を書き換えるキーは入れない

## 同じキーを複数のMODが定義している場合

元のMODどうしで同じキーを上書きしているもの（cr-extras → foliax / obsidiax、Arcanyx・IridescentIndustry → Voidcraft、ribbonia → liquid_recycler）は、上書きする側のMODの訳だけを入れています。パックをまとめて入れる前提の選び方です。

## 依存関係に対象MODを入れない理由

入れるとこのMODが必ず対象MODより後に読み込まれ、対象MODが後から自前の日本語訳を入れたときに、
こちらの古い訳で上書きしてしまうためです。対象MODが更新されたら `tools/coverage.py` で本体の日本語訳を確認し、
重なったキーをこちらから削除します。
