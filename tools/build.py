"""dist/ に Factorio 用の zip（<name>_<version>.zip）を作る。

使い方:
    python3 tools/build.py                 # info.json のまま（2.1 向け）
    python3 tools/build.py --factorio 2.0  # factorio_version を 2.0 にして作る

MODポータルは同じバージョン番号を2回登録できないので、
2.0 向けは --version で 2.1 向けと別のバージョン番号を付けてください。
"""
import argparse
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["changelog.txt", "thumbnail.png", "locale"]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--factorio", help="factorio_version を上書きする（例: 2.0）")
    parser.add_argument("--version", help="version を上書きする")
    args = parser.parse_args()

    info = json.loads((ROOT / "info.json").read_text(encoding="utf-8"))
    if args.factorio:
        info["factorio_version"] = args.factorio
        major, minor = args.factorio.split(".")
        info["dependencies"] = [
            f"base >= {major}.{minor}.0" if d.startswith("base") else d for d in info["dependencies"]
        ]
    if args.version:
        info["version"] = args.version

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
