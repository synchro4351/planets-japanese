"""訳文のタグや変数（[item=...]、__1__、\\n など）が英語と同じかを調べる。

使い方:
    python3 tools/check_tags.py <modフォルダ>
"""
import collections
import re
import sys
import zipfile
from pathlib import Path

from coverage import latest_zips

ROOT = Path(__file__).resolve().parent.parent
RICH = re.compile(r"\[(/?)([a-z\-]+)(?:=([^\]]*))?\]")
VARS = re.compile(r"__[A-Za-z0-9_\-]+__|\\n")
RICH_NAMES = {
    "item", "entity", "fluid", "recipe", "technology", "tile", "planet", "space-location", "virtual-signal",
    "img", "color", "font", "gps", "tooltip", "quality", "item-group", "special-item", "armor", "train",
    "train-stop", "achievement", "space-platform", "space-age", "asteroid-chunk", "shortcut", "space-connection",
}


def tags(text):
    found = VARS.findall(text)
    for slash, name, arg in RICH.findall(text):
        if name not in RICH_NAMES:
            continue
        if name == "tooltip" and arg:
            arg = arg.rsplit(",", 1)[-1]  # 表示テキストは訳してよいので比べない
        found.append(f"[{slash}{name}={arg}]")
    return collections.Counter(found)


def parse(text):
    values, section = {}, ""
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            section = s[1:-1]
            continue
        if "=" in s and not s.startswith((";", "#")):
            key, value = s.split("=", 1)
            values[f"{section}.{key.strip()}"] = value
    return values


def main():
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(1)
    zips = latest_zips(sys.argv[1])
    problems = 0
    for cfg in sorted((ROOT / "locale" / "ja").glob("*.cfg")):
        if cfg.stem not in zips:
            print(f"{cfg.stem}: modフォルダにMODが無いので飛ばしました")
            continue
        en = {}
        with zipfile.ZipFile(zips[cfg.stem]) as z:
            for n in z.namelist():
                parts = n.split("/")
                if len(parts) >= 4 and parts[1] == "locale" and parts[2] == "en" and n.endswith(".cfg"):
                    en.update(parse(z.read(n).decode("utf-8-sig")))
        for key, value in parse(cfg.read_text(encoding="utf-8-sig")).items():
            if key not in en:
                continue
            if tags(en[key]) != tags(value):
                problems += 1
                print(f"{cfg.stem} {key}\n  en: {en[key]}\n  ja: {value}")
            elif (en[key].strip() == "") != (value.strip() == ""):
                problems += 1
                print(f"{cfg.stem} {key}: 空かどうかが英語と違います")
    print(f"問題: {problems} 件")


if __name__ == "__main__":
    main()
