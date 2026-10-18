"""対象MODの英語ロケールと、このMODの日本語ロケールを比べて、未訳・余分なキーを表示する。

使い方:
    python3 tools/check_keys.py <対象MODのzipまたはフォルダ> locale/ja/<対象MOD名>.cfg
"""
import sys
import zipfile
from pathlib import Path


def parse_cfg(text):
    keys = set()
    section = ""
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith((";", "#")):
            continue
        if line.startswith("[") and line.endswith("]"):
            section = line[1:-1]
            continue
        if "=" in line:
            keys.add(f"{section}.{line.split('=', 1)[0].strip()}")
    return keys


def load_en_keys(source):
    source = Path(source)
    keys = set()
    if source.is_dir():
        for cfg in source.glob("locale/en/*.cfg"):
            keys |= parse_cfg(cfg.read_text(encoding="utf-8-sig"))
        return keys
    with zipfile.ZipFile(source) as z:
        for name in z.namelist():
            parts = name.split("/")
            if len(parts) >= 3 and parts[-3] == "locale" and parts[-2] == "en" and name.endswith(".cfg"):
                keys |= parse_cfg(z.read(name).decode("utf-8-sig"))
    return keys


def main():
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(1)
    en = load_en_keys(sys.argv[1])
    ja_path = Path(sys.argv[2])
    ja = parse_cfg(ja_path.read_text(encoding="utf-8-sig")) if ja_path.exists() else set()
    missing = sorted(en - ja)
    extra = sorted(ja - en)
    print(f"英語キー {len(en)} / 訳済み {len(en & ja)} / 未訳 {len(missing)} / 余分 {len(extra)}")
    for k in missing:
        print("未訳:", k)
    for k in extra:
        print("余分:", k)


if __name__ == "__main__":
    main()
