#!/usr/bin/env python3
"""雛形から新しい設定ファイルを作る。

    python3 tools/new.py <type> <slug> [表示名]

例:
    python3 tools/new.py character aria アリア
    python3 tools/new.py location north-tower 北の塔
    python3 tools/new.py concept ash-magic 灰の魔術

表示名を省略すると slug がそのまま name になる。
"""

from __future__ import annotations

import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORLD = ROOT / "world"
TEMPLATES = WORLD / "_templates"

# type -> (配置ディレクトリ, id 接頭辞)
TYPES = {
    "character": ("characters", "char"),
    "faction": ("factions", "faction"),
    "location": ("locations", "loc"),
    "event": ("events", "event"),
    "concept": ("concepts", "concept"),
    "item": ("items", "item"),
}

SLUG_RE = re.compile(r"^[a-z0-9-]+$")


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print(__doc__.strip())
        print(f"\ntype: {' / '.join(TYPES)}")
        return 1

    entry_type, slug = argv[0], argv[1]
    name = argv[2] if len(argv) > 2 else slug

    if entry_type not in TYPES:
        print(f"不明な type: '{entry_type}'（{' / '.join(TYPES)} のいずれか）", file=sys.stderr)
        return 1

    if not SLUG_RE.match(slug):
        print(
            f"slug '{slug}' は不正。半角英小文字・数字・ハイフンのみ使えます。\n"
            "日本語名は第3引数の表示名に渡してください。",
            file=sys.stderr,
        )
        return 1

    dirname, prefix = TYPES[entry_type]
    template = TEMPLATES / f"{entry_type}.md"
    if not template.exists():
        print(f"雛形が見つかりません: {template}", file=sys.stderr)
        return 1

    target = WORLD / dirname / f"{slug}.md"
    if target.exists():
        print(f"すでに存在します: {target.relative_to(ROOT)}", file=sys.stderr)
        return 1

    content = (
        template.read_text(encoding="utf-8")
        .replace("SLUG", slug)
        .replace("NAME", name)
        .replace("TODAY", date.today().isoformat())
    )

    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")

    print(f"作成: {target.relative_to(ROOT)}  (id: {prefix}:{slug})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
