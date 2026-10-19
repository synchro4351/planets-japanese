"""dist/ に Factorio 用の zip（<name>_<version>.zip）を作る。

使い方:
    python3 tools/build.py                 # 2.0 用と 2.1 用を両方作る
    python3 tools/build.py --factorio 2.0  # 2.0 用だけ作る

MODポータルは同じバージョン番号を2回登録できないので、
info.json の version（例 0.2.0）の末尾の数字を Factorio のバージョンで決める。
    Factorio 2.0 用 → 0.2.0
    Factorio 2.1 用 → 0.2.1
中身の更新は 0.2 → 0.3 のように真ん中の数字を上げる。
"""
import argparse
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["changelog.txt", "thumbnail.png", "locale"]
# Factorio のバージョン → MOD バージョンの末尾の数字
PATCH = {"2.0": 0, "2.1": 1}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--factorio", choices=sorted(PATCH), help="片方だけ作る（2.0 か 2.1）")
    args = parser.parse_args()
    for factorio in [args.factorio] if args.factorio else sorted(PATCH):
        build(factorio)


def build(factorio):
    info = json.loads((ROOT / "info.json").read_text(encoding="utf-8"))
    info["factorio_version"] = factorio
    info["dependencies"] = [f"base >= {factorio}.0" if d.startswith("base") else d for d in info["dependencies"]]
    major, minor, _ = info["version"].split(".")
    info["version"] = f"{major}.{minor}.{PATCH[factorio]}"

    folder = f"{info['name']}_{info['version']}"
    out = ROOT / "dist" / f"{folder}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{folder}/info.json", json.dumps(info, ensure_ascii=False, indent=2) + "\n")
        for item in INCLUDE:
            path = ROOT / item
            if not path.exists():
                continue
            files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file())
            for f in files:
                if f.name == "README.txt":
                    continue
                z.write(f, f"{folder}/{f.relative_to(ROOT).as_posix()}")
    print(f"{out}  (factorio {info['factorio_version']})")


if __name__ == "__main__":
    main()
