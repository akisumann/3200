# 3200

世界設定を正典（カノン）として管理し、そこからゲーム・その他の作品へ展開していくためのリポジトリ。

## 基本方針

**設定と数値を分ける。**

| | 置き場所 | 例 |
|---|---|---|
| 設定（正典） | `world/` | 「この剣は失われた王家の遺物で、持ち主を選ぶ」 |
| 実装（数値・仕様） | `projects/` | 「攻撃力 120、装備条件：王家の血統フラグ」 |

世界設定はどの媒体にも共通する事実、`projects/` 以下はその一実装にすぎません。ゲームの仕様が変わっても、ボツになっても、`world/` は無傷で残ります。逆に `world/` に数値を書き込むと、仕様変更のたびに設定を書き換えることになり、設定が仕様に引きずられて壊れます。

## ディレクトリ

```
world/          正典。世界設定そのもの
  characters/     人物
  factions/       勢力・組織
  locations/      土地・場所
  events/         出来事（年表の材料）
  concepts/       概念・体系（魔法、技術、宗教、言語など）
  items/          物品
  _templates/     新規ファイルの雛形
  glossary.md     用語集
  timeline.md     年表

projects/       world/ を素材にした派生物
  game/           ゲーム化。数値・システム・未決事項はここ

docs/           このリポジトリ自体のルール
tools/          検査・生成スクリプト
```

## 使い方

新しい設定ファイルを作る:

```sh
python3 tools/new.py character aria アリア
# → world/characters/aria.md を雛形から生成
```

書いたものを検査する（ID 重複、参照切れ、必須項目もれ）:

```sh
python3 tools/check.py
```

## まず読むもの

- [docs/00-repository-guide.md](docs/00-repository-guide.md) — どこに何を書くか
- [docs/01-writing-rules.md](docs/01-writing-rules.md) — ID・記法・命名のルール
- [docs/02-canon-policy.md](docs/02-canon-policy.md) — 確定／暫定／没の扱い

## 権利

このリポジトリの世界設定・文章は著作物です。既定では **All rights reserved**（第三者への利用許諾なし）として扱ってください。公開・二次利用を許可する場合は、意図に合うライセンスファイルを別途追加してください。オープンソース向けのライセンス（MIT など）は creative work には通常適さないので、選ぶ前に一度検討することを勧めます。
