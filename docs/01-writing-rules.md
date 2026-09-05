# 記法ルール

`tools/check.py` が機械的に検査するのはこのファイルの内容。ルールを変えたら check.py も直すこと。

## ファイル

- 拡張子は `.md`
- ファイル名は **半角英小文字・数字・ハイフン** のみ（`aria.md`, `north-tower.md`）
  - 日本語名はファイル名ではなく frontmatter の `name` に書く
  - 理由：OS やツールによる濁点の正規化ゆれ（NFC/NFD）事故を避けるため
- 1ファイル1トピック

## frontmatter

各ファイルの先頭に YAML frontmatter を置く。

```markdown
---
id: char:aria
name: アリア
type: character
status: draft
aliases: [灰の姫]
tags: [王国, 魔法]
related: [faction:ashen-court, event:tower-sealing]
updated: 2026-09-05
---

（ここから本文）
```

### 必須フィールド

| フィールド | 内容 |
|---|---|
| `id` | 世界で一意な識別子。`<type略号>:<slug>` |
| `name` | 表示名。日本語で可 |
| `type` | `character` / `faction` / `location` / `event` / `concept` / `item` |
| `status` | `draft` / `wip` / `canon` / `dropped`（→ [02-canon-policy.md](02-canon-policy.md)） |

### 任意フィールド

| フィールド | 内容 |
|---|---|
| `aliases` | 別名・通称・旧称 |
| `tags` | 自由なタグ |
| `related` | 関連する ID のリスト |
| `updated` | 最終更新日 `YYYY-MM-DD` |
| `date` | `type: event` のとき、作中世界での日付。文字列で可（`王暦 402年 春`） |

## ID

形式は `<接頭辞>:<slug>`。

| type | 接頭辞 | 例 |
|---|---|---|
| character | `char` | `char:aria` |
| faction | `faction` | `faction:ashen-court` |
| location | `loc` | `loc:north-tower` |
| event | `event` | `event:tower-sealing` |
| concept | `concept` | `concept:ash-magic` |
| item | `item` | `item:kings-blade` |

**ID は一度決めたら変えない。** 表示名（`name`）は自由に変えてよい。名前を変えたくなるのは普通のことで、そのたびに全ファイルの参照を直す羽目にならないよう、ID と名前を分けている。

どうしても ID を変えるときは、`tools/check.py` を実行して参照切れをすべて潰してからコミットすること。

## 相互参照

本文中で他の項目に触れるときは `[[id]]` で書く。

```markdown
[[char:aria]] は [[event:tower-sealing]] の後、[[loc:north-tower]] に戻っていない。
```

- 表示名を変えたいときは `[[char:aria|あの女]]` と書く
- `check.py` は `[[...]]` の参照先が実在するかを検査する
- 記法そのものを例示したいときは、バッククォートで囲む（コードブロック・コード span の中は参照として扱わない）
- 存在しないものに言及したいが、まだファイルを作っていない場合 → **ファイルを作る**。`status: draft` で名前と一行だけでよい

## 本文の書き方

- 見出しは `##` から始める（`#` はタイトル用に空けておく）
- 断定して書く。「〜かもしれない」「〜という説もある」を地の文に混ぜない
  - 作中人物にとって不確かな事柄は、`## 諸説` のような節を立ててそこに隔離する
  - 作者としてまだ決めていないことは `## 未決` 節に書く（→ 後で潰すべき宿題として可視化される）
- 数値・ゲーム的な強さを書かない（→ `projects/` の担当）

## 推奨する節構成

厳密ではないが、揃っていると読み返しやすい。

```markdown
## 概要      一段落での要約
## 詳細      本体
## 関係      他の項目との関わり
## 未決      まだ決めていないこと
```
