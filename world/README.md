# world/ — 正典

この世界について「事実である」と決めたことを置く場所。

**ここに数値を書かない。** ゲームの攻撃力も、レベルも、確率も `projects/` の担当です。ここに書いてよいのは、どの作品にしても変わらない事柄だけ。

## 最初に読むもの

[premise.md](premise.md) — この世界の骨子。すべての設定はここから派生します。前提に関わる未決事項もここに集約しています。

## 書き始める

```sh
python3 tools/new.py character aria アリア
python3 tools/new.py location north-tower 北の塔
python3 tools/new.py concept ash-magic 灰の魔術
```

書いたら検査:

```sh
python3 tools/check.py
```

## どこに置くか

| ディレクトリ | 入れるもの |
|---|---|
| `characters/` | 人物 |
| `factions/` | 勢力・組織・種族 |
| `locations/` | 土地・場所 |
| `events/` | 出来事 |
| `concepts/` | 体系・仕組み（魔法、技術、宗教、言語、暦） |
| `items/` | 物品 |

判断に迷ったら [docs/00-repository-guide.md](../docs/00-repository-guide.md)。

## 移行のとき

既に書き溜めた設定があるなら、一度に整形しようとしないでください。手が止まります。

1. まず**そのまま貼る**。1トピック1ファイル、frontmatter は `id` / `name` / `type` / `status: draft` の4つだけ埋める
2. 全部入れ終わってから、`status` を見直して固まっているものを `canon` に上げる
3. 最後に `[[参照]]` を張る。`python3 tools/check.py` が参照切れを教えてくれる

整形は後からいくらでもできますが、頭の外に出ていない設定は失われます。**移すことを優先してください。**
