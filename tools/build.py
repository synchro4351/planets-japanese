"""dist/ に Factorio 用の zip（<name>_<version>.zip）を作る。"""
import json
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INCLUDE = ["info.json", "changelog.txt", "thumbnail.png", "locale"]


def main():
    info = json.loads((ROOT / "info.json").read_text(encoding="utf-8"))
    folder = f"{info['name']}_{info['version']}"
    out = ROOT / "dist" / f"{folder}.zip"
    out.parent.mkdir(exist_ok=True)
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for item in INCLUDE:
            path = ROOT / item
            if not path.exists():
                continue
            files = [path] if path.is_file() else sorted(p for p in path.rglob("*") if p.is_file())
            for f in files:
                if f.name == "README.txt":
                    continue
                z.write(f, f"{folder}/{f.relative_to(ROOT).as_posix()}")
    print(out)


if __name__ == "__main__":
    main()
