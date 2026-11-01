"""modフォルダの中身を見て、MODごとの日本語化の状況を表にする。

使い方:
    python3 tools/coverage.py <modフォルダ> <パックの内部名> [<パックの内部名> ...]

例:
    python3 tools/coverage.py %APPDATA%/Factorio/mods kry-all-planet-mods kry-planet-mods-lite

パックの必須依存を前提MODまでたどり、各MODの英語キーのうち
- MOD本体の日本語ロケール
- ほかの日本語化MOD（Any_Japanise_Pack）
- このMOD（locale/ja）
で訳されているキー数を Markdown の表で出す。
"""
import json
import re
import sys
import zipfile
from pathlib import Path

from check_keys import parse_cfg

ROOT = Path(__file__).resolve().parent.parent
OTHER_PACKS = ["Any_Japanise_Pack"]
BUILTIN = {"base", "space-age", "quality", "elevated-rails", "recycler"}


def latest_zips(folder):
    latest = {}
    for zp in Path(folder).glob("*.zip"):
        m = re.match(r"(.+)_(\d+(?:\.\d+)*)\.zip$", zp.name)
        if not m:
            continue
        version = tuple(int(x) for x in m.group(2).split("."))
        if m.group(1) not in latest or latest[m.group(1)][0] < version:
            latest[m.group(1)] = (version, zp)
    return {name: zp for name, (_, zp) in latest.items()}


def read_mod(zp):
    en, ja, info = set(), set(), {}
    with zipfile.ZipFile(zp) as z:
        for n in z.namelist():
            parts = n.split("/")
            if len(parts) == 2 and parts[1] == "info.json":
                info = json.loads(z.read(n).decode("utf-8-sig"))
            if len(parts) >= 4 and parts[1] == "locale" and n.endswith(".cfg"):
                keys = parse_cfg(z.read(n).decode("utf-8-sig"))
                if parts[2] == "en":
                    en |= keys
                elif parts[2] == "ja":
                    ja |= keys
    return info, en, ja


def required_deps(info):
    deps = []
    for d in info.get("dependencies", []):
        d = d.strip()
        if d.startswith(("?", "(?)", "!")):
            continue
        d = d.lstrip("~+ ").strip()
        deps.append(re.split(r"\s*[<>=]", d)[0].strip())
    return deps


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    zips = latest_zips(sys.argv[1])
    other = set()
    for name in OTHER_PACKS:
        if name in zips:
            other |= read_mod(zips[name])[2]
    ours = set()
    for cfg in (ROOT / "locale" / "ja").glob("*.cfg"):
        ours |= parse_cfg(cfg.read_text(encoding="utf-8-sig"))

    queue, seen, missing = list(sys.argv[2:]), set(), set()
    rows = []
    while queue:
        name = queue.pop(0)
        if name in seen or name in BUILTIN:
            continue
        seen.add(name)
        if name not in zips:
            missing.add(name)
            continue
        info, en, own = read_mod(zips[name])
        queue += required_deps(info)
        if name in sys.argv[2:]:
            continue
        done_own = len(en & own)
        done_other = len((en - own) & other)
        done_ours = len((en - own - other) & ours)
        left = len(en) - done_own - done_other - done_ours
        rows.append((name, info.get("version", "?"), len(en), done_own, done_other, done_ours, left))

    print("| MOD名 (内部名) | 版 | キー数 | MOD本体 | 他の日本語化MOD | このMOD | 未訳 |")
    print("|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda r: (-r[6], r[0].lower())):
        print("| " + " | ".join(str(x) for x in r) + " |")
    total_left = sum(r[6] for r in rows)
    print(f"\n未訳の合計: {total_left} キー")
    if missing:
        print("\nmodフォルダに無かったMOD: " + ", ".join(sorted(missing)))


if __name__ == "__main__":
    main()
