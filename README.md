# kry-planets-japanese

[Kry's All Planet Mods](https://mods.factorio.com/mod/kry-all-planet-mods)（と lite 版）に含まれる惑星MODと、その前提MODを日本語化するFactorio MODです。

## ほかの日本語化MODとの併用

次のMODが既に翻訳しているMOD、それとMOD本体に日本語が入っているMODは対象外にしています。

- [Any_Japanise_Pack](https://mods.factorio.com/mod/Any_Japanise_Pack)
- [Translate_planet_into_Japanese（惑星Mod 日本語化パック）](https://mods.factorio.com/mod/Translate_planet_into_Japanese)

同じロケールキーを両方で定義しないことで、どちらの訳が使われるかで揉めないようにしています。
念のため両方を任意依存にして、読み込み順をこちらが後になるようにしています。

## Factorio 2.0 / 2.1

中身は訳文だけなので、同じソースから2.0用と2.1用のzipを作れます。

```
python3 tools/build.py                                 # 2.1 用
python3 tools/build.py --factorio 2.0 --version X.Y.Z  # 2.0 用
```

対象と進み具合は [docs/targets.md](docs/targets.md) を見てください。

## 構成

- `locale/ja/<対象MOD名>.cfg` … 対象MODごとの日本語ロケール
- `tools/check_keys.py` … 対象MODの英語ロケールと比べて未訳キーを出す
- `tools/check_conflicts.py` … ほかの日本語化MODとキーが重なっていないか調べる
- `tools/build.py` … `dist/` に配布用zipを作る（2.0 / 2.1）

## 翻訳方針

Any_Japanise_Pack に合わせます。

- 基本は直訳
- Factorio公式の日本語訳に寄せる（例: Assembler MK4 → 組立機4）
- バニラの項目名を書き換えるキーは入れない
