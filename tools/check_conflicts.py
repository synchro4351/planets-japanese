"""このMODの日本語キーが、ほかの日本語化MODのキーと重なっていないか調べる。

使い方:
    python3 tools/check_conflicts.py <日本語化MODのzip> [<zip> ...]

例:
    python3 tools/check_conflicts.py Any_Japanise_Pack_2.0.45.zip Translate_planet_into_Japanese_1.3.3.zip
"""
import sys
import zipfile
from pathlib import Path

from check_keys import parse_cfg

ROOT = Path(__file__).resolve().parent.parent


def keys_by_file(cfgs):
    result = {}
    for name, text in cfgs:
        for key in parse_cfg(text):
            result.setdefault(key, []).append(name)
    return result


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    ours = keys_by_file(
        (p.name, p.read_text(encoding="utf-8-sig")) for p in sorted((ROOT / "locale" / "ja").glob("*.cfg"))
    )
    found = False
    for zp in sys.argv[1:]:
        with zipfile.ZipFile(zp) as z:
            cfgs = [
                (n, z.read(n).decode("utf-8-sig"))
                for n in z.namelist()
                if "/locale/ja/" in n and n.endswith(".cfg")
            ]
        theirs = keys_by_file(cfgs)
        for key in sorted(ours.keys() & theirs.keys()):
            found = True
            print(f"{key}  ここ: {', '.join(ours[key])}  {Path(zp).name}: {', '.join(theirs[key])}")
    if not found:
        print("重なりはありません")


if __name__ == "__main__":
    main()
