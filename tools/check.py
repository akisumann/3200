#!/usr/bin/env python3
"""world/ の設定ファイルを検査する。

    python3 tools/check.py

検査するもの:
  - ファイル名が半角英小文字・数字・ハイフンか
  - frontmatter の必須項目 (id / name / type / status) が揃っているか
  - type がディレクトリと一致しているか
  - id の形式・接頭辞・slug がファイル名と一致しているか
  - id の重複
  - [[参照]] と related: の参照先が実在するか
  - status: dropped への参照（警告）

エラーがあれば終了コード 1。警告のみなら 0。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import frontmatter  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
WORLD = ROOT / "world"
PROJECTS = ROOT / "projects"

# ディレクトリ名 -> (type, id 接頭辞)
TYPE_DIRS = {
    "characters": ("character", "char"),
    "factions": ("faction", "faction"),
    "locations": ("location", "loc"),
    "events": ("event", "event"),
    "concepts": ("concept", "concept"),
    "items": ("item", "item"),
}

STATUSES = ("draft", "wip", "canon", "dropped")
REQUIRED = ("id", "name", "type", "status")

SLUG_RE = re.compile(r"^[a-z0-9-]+$")
ID_RE = re.compile(r"^([a-z]+):([a-z0-9-]+)$")
REF_RE = re.compile(r"\[\[([^\]|]+?)(?:\|[^\]]*)?\]\]")

# 記法の説明のために [[...]] を引用したいことがあるので、
# コードブロックとコード span の中は参照とみなさない。
FENCED_RE = re.compile(r"^(```|~~~).*?^\1", re.DOTALL | re.MULTILINE)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

errors: list[str] = []
warnings: list[str] = []


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT))


def strip_code(text: str) -> str:
    """コードブロック / コード span を取り除く。改行数は保つ必要がないので単に落とす。"""
    return INLINE_CODE_RE.sub("", FENCED_RE.sub("", text))


def as_list(value) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [str(v) for v in value if str(v).strip()]
    return []


def collect_entries() -> dict[str, dict]:
    """world/<型ディレクトリ>/*.md を読み、id -> エントリ の辞書を返す。"""
    entries: dict[str, dict] = {}

    for dirname, (expected_type, prefix) in TYPE_DIRS.items():
        directory = WORLD / dirname
        if not directory.is_dir():
            continue

        for path in sorted(directory.glob("*.md")):
            slug = path.stem
            if not SLUG_RE.match(slug):
                errors.append(
                    f"{rel(path)}: ファイル名は半角英小文字・数字・ハイフンのみ"
                    "（日本語名は frontmatter の name に書く）"
                )

            meta, body = frontmatter.parse(path.read_text(encoding="utf-8"))

            missing = [f for f in REQUIRED if not str(meta.get(f, "")).strip()]
            if missing:
                errors.append(f"{rel(path)}: 必須項目が空: {', '.join(missing)}")

            entry_id = str(meta.get("id", "")).strip()
            status = str(meta.get("status", "")).strip()
            entry_type = str(meta.get("type", "")).strip()

            if status and status not in STATUSES:
                errors.append(
                    f"{rel(path)}: status '{status}' は不正（{' / '.join(STATUSES)} のいずれか）"
                )

            if entry_type and entry_type != expected_type:
                errors.append(
                    f"{rel(path)}: type '{entry_type}' はディレクトリと不一致"
                    f"（{dirname}/ なら '{expected_type}'）"
                )

            if entry_id:
                match = ID_RE.match(entry_id)
                if not match:
                    errors.append(f"{rel(path)}: id '{entry_id}' の形式が不正（例: {prefix}:{slug}）")
                else:
                    id_prefix, id_slug = match.groups()
                    if id_prefix != prefix:
                        errors.append(
                            f"{rel(path)}: id の接頭辞 '{id_prefix}' が不正（'{prefix}' であるべき）"
                        )
                    if id_slug != slug:
                        errors.append(
                            f"{rel(path)}: id の slug '{id_slug}' がファイル名 '{slug}' と不一致"
                        )

                if entry_id in entries:
                    errors.append(
                        f"{rel(path)}: id '{entry_id}' が重複（既出: {entries[entry_id]['path']}）"
                    )
                    continue

                entries[entry_id] = {
                    "path": rel(path),
                    "name": str(meta.get("name", "")).strip(),
                    "type": entry_type,
                    "status": status,
                    "related": as_list(meta.get("related")),
                    "body": body,
                }

    return entries


def ref_sources() -> list[Path]:
    """参照を検査する対象ファイル。docs/ と _templates/ は例示を含むので除外する。"""
    paths: list[Path] = []
    for dirname in TYPE_DIRS:
        paths.extend(sorted((WORLD / dirname).glob("*.md")))
    for name in ("glossary.md", "timeline.md"):
        if (WORLD / name).exists():
            paths.append(WORLD / name)
    if PROJECTS.is_dir():
        paths.extend(sorted(PROJECTS.rglob("*.md")))
    return paths


def check_refs(entries: dict[str, dict]) -> None:
    def report(source: str, ref: str, kind: str) -> None:
        if ref not in entries:
            errors.append(f"{source}: {kind} '{ref}' の参照先が存在しない")
        elif entries[ref]["status"] == "dropped":
            warnings.append(f"{source}: '{ref}' は status: dropped（没）を参照している")

    for path in ref_sources():
        text = path.read_text(encoding="utf-8")
        _, body = frontmatter.parse(text)
        for ref in REF_RE.findall(strip_code(body)):
            report(rel(path), ref.strip(), "[[参照]]")

    for entry_id, entry in entries.items():
        for ref in entry["related"]:
            report(entry["path"], ref.strip(), f"{entry_id} の related:")


def summarize(entries: dict[str, dict]) -> None:
    if not entries:
        print("world/ にはまだ設定ファイルがありません。")
        print("  python3 tools/new.py character aria アリア")
        return

    def row(label: str, bucket: list[dict]) -> str:
        counts = [sum(1 for e in bucket if e["status"] == s) for s in STATUSES]
        return f"{label:<12}" + "".join(f"{c:>8}" for c in counts) + f"{len(bucket):>8}"

    header = f"{'':<12}" + "".join(f"{s:>8}" for s in STATUSES) + f"{'total':>8}"
    print(header)
    print("-" * len(header))

    for dirname, (entry_type, _) in TYPE_DIRS.items():
        bucket = [e for e in entries.values() if e["type"] == entry_type]
        if bucket:
            print(row(dirname, bucket))

    print("-" * len(header))
    print(row("total", list(entries.values())))


def main() -> int:
    if not WORLD.is_dir():
        print("world/ が見つかりません", file=sys.stderr)
        return 1

    entries = collect_entries()
    check_refs(entries)

    summarize(entries)

    if warnings:
        print(f"\n警告 {len(warnings)} 件")
        for message in warnings:
            print(f"  ! {message}")

    if errors:
        print(f"\nエラー {len(errors)} 件")
        for message in errors:
            print(f"  x {message}")
        return 1

    print("\n問題なし")
    return 0


if __name__ == "__main__":
    sys.exit(main())
