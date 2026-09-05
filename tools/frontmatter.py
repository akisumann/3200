"""Markdown frontmatter の読み取り。

PyYAML があればそれを使い、無ければ内蔵の簡易パーサに落ちる。
簡易パーサが解釈できるのは docs/01-writing-rules.md に書いた範囲だけ:

    key: value
    key: [a, b, c]
    key:
      - a
      - b

依存を増やさずに `python3 tools/check.py` がどこでも動くことを優先している。
"""

from __future__ import annotations

try:
    import yaml  # type: ignore

    _HAS_YAML = True
except ImportError:  # pragma: no cover - 環境依存
    _HAS_YAML = False


def split(text: str) -> tuple[str, str]:
    """本文を (frontmatter 文字列, 本文) に分割する。frontmatter が無ければ ('', text)。"""
    if not text.startswith("---"):
        return "", text
    lines = text.split("\n")
    for i in range(1, len(lines)):
        if lines[i].rstrip() in ("---", "..."):
            return "\n".join(lines[1:i]), "\n".join(lines[i + 1 :])
    return "", text


def _unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def _parse_simple(raw: str) -> dict:
    data: dict = {}
    current_list_key: str | None = None

    for line in raw.split("\n"):
        if not line.strip() or line.lstrip().startswith("#"):
            continue

        stripped = line.strip()

        # インデントされた "- item" は直前のキーのリスト要素
        if stripped.startswith("- "):
            if current_list_key is not None:
                data[current_list_key].append(_unquote(stripped[2:]))
            continue

        if ":" not in line:
            continue

        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        current_list_key = None

        if value == "":
            # 続く "- item" 行を集めるためのリストとして開始する。
            # 値なしのスカラーだった場合は check 側が空リストを空として扱う。
            data[key] = []
            current_list_key = key
        elif value.startswith("[") and value.endswith("]"):
            inner = value[1:-1].strip()
            data[key] = [_unquote(v) for v in inner.split(",") if v.strip()] if inner else []
        else:
            data[key] = _unquote(value)

    return data


def parse(text: str) -> tuple[dict, str]:
    """(frontmatter の dict, 本文) を返す。"""
    raw, body = split(text)
    if not raw.strip():
        return {}, body

    if _HAS_YAML:
        try:
            data = yaml.safe_load(raw)
        except Exception:
            return _parse_simple(raw), body
        if not isinstance(data, dict):
            return {}, body
        return data, body

    return _parse_simple(raw), body
