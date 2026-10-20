# planets-japanese（All Planet Mods 日本語化）

[Kry's All Planet Mods](https://mods.factorio.com/mod/kry-all-planet-mods)（と lite 版）に含まれる惑星MODと、その前提MODを日本語化するFactorio MODです。
パックの作者とは関係のない、有志の日本語化MODです。

## ほかの日本語化MODとの併用

次のMODが既に翻訳しているMOD、それとMOD本体に日本語が入っているMODは対象外にしています。

- [Any_Japanise_Pack](https://mods.factorio.com/mod/Any_Japanise_Pack)
- [Translate_planet_into_Japanese（惑星Mod 日本語化パック）](https://mods.factorio.com/mod/Translate_planet_into_Japanese)

同じロケールキーを両方で定義しないことで、どちらの訳が使われるかで揉めないようにしています。
念のため両方を任意依存にして、読み込み順をこちらが後になるようにしています。

対象のMODは依存関係に入れていません。入れるとこのMODが必ず後に読み込まれ、
対象MODが後から自前の日本語訳を入れたときに、こちらの古い訳で上書きしてしまうためです。
主な対象は info.json の説明文に、全一覧は [docs/targets.md](docs/targets.md) にあります。

## Factorio 2.0 / 2.1

中身は訳文だけなので、同じソースから2.0用と2.1用のzipを作れます。

```
python3 tools/check_format.py   # Factorio が読めない書き方（重複セクションなど）がないか確認
python3 tools/build.py          # dist/ に 2.0 用と 2.1 用の zip を作る
```

バージョン番号の末尾は Factorio のバージョンを表します（例: 0.2.0 が 2.0 用、0.2.1 が 2.1 用）。
中身を更新したときは真ん中の数字を上げます。

対象と進み具合は [docs/targets.md](docs/targets.md) を見てください。

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
- Factorio公式の日本語訳に寄せる（例: Assembler MK4 → 組立機4）。用語は [docs/glossary.md](docs/glossary.md)
- バニラの項目名を書き換えるキーは入れない

## 同じキーを複数のMODが定義している場合

元のMODどうしで同じキーを上書きしているもの（cr-extras → foliax / obsidiax、Arcanyx・IridescentIndustry → Voidcraft、ribbonia → liquid_recycler）は、上書きする側のMODの訳だけを入れています。パックをまとめて入れる前提の選び方です。
