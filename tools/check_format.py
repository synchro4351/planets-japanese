"""locale/ja の .cfg を Factorio が読み込めるか確認する。

Factorio は1つのファイルの中で同じ [セクション] が2回出てきたり、
同じセクションに同じキーが2回あったりすると「Duplicate key」で読み込みに失敗する。
念のため、別のファイル同士で同じキーを定義していないかも確認する。

使い方:
    python3 tools/check_format.py          # 問題があれば一覧を出して終了コード1
    python3 tools/check_format.py --fix    # 重複セクションを1つにまとめる
"""
import argparse
import sys
from pathlib import Path

LOCALE = Path(__file__).resolve().parent.parent / "locale" / "ja"


def read_sections(text):
    """[(セクション名, [行...])] を出現順で返す。最初のセクションより前の行は名前 None。"""
    sections = [(None, [])]
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            sections.append((s[1:-1], []))
        else:
            sections[-1][1].append(line)
    return sections


def problems(path):
    found = []
    seen_sections = set()
    for name, lines in read_sections(path.read_text(encoding="utf-8-sig")):
        if name in seen_sections:
            found.append(f"セクション [{name}] が2回以上ある")
        seen_sections.add(name)
    keys = set()
    section = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            section = s[1:-1]
        elif "=" in s and not s.startswith((";", "#")):
            key = (section, s.split("=", 1)[0])
            if key in keys:
                found.append(f"キー [{section}] {key[1]} が2回以上ある")
            keys.add(key)
    return found


def parse_keys(path):
    section = None
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        s = line.strip()
        if s.startswith("[") and s.endswith("]"):
            section = s[1:-1]
        elif "=" in s and not s.startswith((";", "#")):
            yield (section, s.split("=", 1)[0])


def merge(path):
    merged = {}
    for name, lines in read_sections(path.read_text(encoding="utf-8-sig")):
        merged.setdefault(name, []).extend(l for l in lines if l.strip() and not l.startswith("; ===="))
    out = []
    for name, lines in merged.items():
        if name is None and not lines:
            continue
        if name is not None:
            out.append(f"[{name}]")
        out.extend(lines)
        out.append("")
    path.write_text("\n".join(out).rstrip("\n") + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    args = parser.parse_args()
    bad = 0
    owner = {}
    for path in sorted(LOCALE.glob("*.cfg")):
        for key in parse_keys(path):
            if key in owner:
                print(f"{path.name}: キー [{key[0]}] {key[1]} は {owner[key]} にもある")
                bad += 1
            else:
                owner[key] = path.name
    for path in sorted(LOCALE.glob("*.cfg")):
        if args.fix and any("セクション" in p for p in problems(path)):
            merge(path)
        for p in problems(path):
            print(f"{path.name}: {p}")
            bad += 1
    print("問題はありません" if bad == 0 else f"{bad} 件の問題があります")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
