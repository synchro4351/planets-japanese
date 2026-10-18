# kry-planets-japanese

[Kry's All Planet Mods](https://mods.factorio.com/mod/kry-all-planet-mods) に含まれる惑星MODと、その前提MODを日本語化するFactorio MODです。

## Any_Japanise_Pack との併用

[Any_Japanise_Pack](https://mods.factorio.com/mod/Any_Japanise_Pack) が既に翻訳しているMODは対象外にしています。
同じロケールキーを両方で定義しないことで、どちらの訳が使われるかで揉めないようにしています。
念のため Any_Japanise_Pack を任意依存にして、読み込み順をこちらが後になるようにしています。

対象と進み具合は [docs/targets.md](docs/targets.md) を見てください。

## 構成

- `locale/ja/<対象MOD名>.cfg` … 対象MODごとの日本語ロケール
- `tools/check_keys.py` … 対象MODの英語ロケールと比べて未訳キーを出す
- `tools/build.py` … `dist/` に配布用zipを作る

## 翻訳方針

Any_Japanise_Pack に合わせます。

- 基本は直訳
- Factorio公式の日本語訳に寄せる（例: Assembler MK4 → 組立機4）
- バニラの項目名を書き換えるキーは入れない
