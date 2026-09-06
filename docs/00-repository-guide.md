# どこに何を書くか

迷ったときの判断基準を一枚にまとめたもの。

## 1. 最初の分岐：それは「世界の事実」か「作品の都合」か

書きたいことを見て、こう自問する。

> **この記述は、この世界を舞台にした別の作品でもそのまま通用するか？**

- **通用する** → `world/` に書く（正典）
  - 「北の塔は 300 年前に封鎖された」
  - 「彼女は妹の死を自分の責任だと思っている」
  - 「この国では鉄より塩が高い」
- **通用しない、特定の作品でしか意味がない** → `projects/<作品>/` に書く
  - 「HP 320、素早さ 12」
  - 「チュートリアルはここで終わる」
  - 「第3章の視点人物は彼女」

判断がつかないときは `world/` に**書かない**。後から正典に昇格させるのは簡単だが、正典から取り除くのは、既に他所から参照された後だと面倒になる。

## 2. `world/` の中のどこか

まず `world/premise.md` が世界の骨子を持つ。**前提そのもの**（この世界を一言で言うと何か、それに関わる未決事項）はそこに書き、個別の項目は下の表に従って振り分ける。

| ディレクトリ | 入れるもの | 目安 |
|---|---|---|
| `characters/` | 個人。名前を持つ人・存在 | 「その人が何をしたか」より「その人がどういう人か」。**書き方の型は `docs/03-character-density.md`** |
| `factions/` | 国家、組織、種族、教団、家系 | 複数人が属する単位 |
| `locations/` | 大陸、都市、建物、地形 | 地図に載るもの |
| `events/` | 起きた出来事。戦争、災害、発明、死 | 日付が付けられるもの |
| `concepts/` | 体系・仕組み。魔法、技術、宗教、言語、経済、暦 | 「この世界ではどう動くか」のルール |
| `items/` | 物品。武器、書物、遺物 | 個体として名前を持つもの |

**同じ内容を二か所に書かない。** 人物の生涯における戦争は `events/` に書き、人物ファイルからは `[[event:xxx]]` で参照する。重複した記述は必ず片方が古くなる。

## 3. 粒度

1ファイル1トピック。ファイルが長くなりすぎたら分割し、`related` で繋ぐ。

逆に、**まだ数行しか書けないものにファイルを作ることをためらわない**。名前と一行だけの `status: draft` のファイルでも、ID があれば他所から参照でき、後から肉付けできる。空白を可視化するほうが、頭の中に置いておくより良い。

## 4. `projects/` の増やし方

新しい方面に展開するときは、`projects/` 直下にディレクトリを1つ作るだけでよい。

```
projects/
  game/       ゲーム
  novel/      小説（例）
  trpg/       TRPG ルールブック（例）
  wiki/       公開用 Wiki（例）
```

各 `projects/*` は `world/` を**読むだけ**。`world/` の内容を自分の都合で書き換えたくなったら、それは「設定が間違っている」のか「その作品だけの解釈」のかを切り分ける。後者なら、その作品のディレクトリ内に「この作品での解釈」として書く。

## 5. 元資料の全体像

`world/` の中身は、作者の手元にある `LIGHT` ファイル群から再構成している。**その一覧が判明したので、どこまで採ったかを記録しておく。**

**同じファイルを二度読んで同じ話を書き直す、という無駄を防ぐため。**

| 元ファイル | 扱い | 主な行き先 |
|---|---|---|
| 20 CORE | **採用済** | 親方針。ほぼ既出だった |
| 21 SUPERNATURAL | **採用済** | `concepts/shinen.md`、`concepts/core-layer.md` |
| 22 LOW_CASES | **採用済** | `concepts/youkai-samples.md` ほか |
| 23 GRADE | **採用済** | `concepts/grades.md` |
| 24 BATTLE | **採用済** | `concepts/battle.md` |
| 25 EQUIPMENT | **採用済**（書式が壊れていたので参考程度） | `concepts/jugu.md`。出所注記あり |
| 26 REIMUSHO | **採用済** | `factions/reimusho.md` |
| 27 PRIVATE | **採用済**（やや古い資料） | `concepts/taimashi.md` |
| 30 SCHOOL_CORE | **採用済** | `concepts/taimashi-school.md` |
| 31 SCHOOL_CURRICULUM | **採用済** | `concepts/school-curriculum.md` |
| 40 HISTORY | **採用済** | `events/` 三件、`characters/nostradamus.md`、`characters/bug.md` |
| 41 RELIC_HISTORY | **採用済** | `concepts/relics.md` |
| 50 CHARACTERS | **採用済** | `characters/` 各種 |
| 60 BAN_UNKNOWN | **採用済** | `docs/02-canon-policy.md`、`concepts/supernatural-war.md` |
| 80 ENEMY_TENDENCY | **採用済** | `concepts/core-layer.md`、`projects/game/design/90-source-numbers.md` |
| 90 YOKAI_SAMPLES | **採用済** | `concepts/youkai-samples.md` |
| 201 SUPERNATURAL | **採用済** | `concepts/` 各種 |
| **70 MUST_LOAD_PC_STATUS** | **未読** | PC作成・成長処理。**ゲームルールなので `projects/game/`** |
| **71 MUST_LOAD_BATTLE_RULES** | **未読** | 判定・戦闘・撤退・回復処理。**同上** |
| **72 MUST_LOAD_ITEM_RULES** | **未読** | アイテム取得・使用・活動値。**同上** |

**残っている三つは、全部ゲームのルール。** `world/` へ入れるものは、現時点で見当たらない。

**そして `projects/game/design/00-open-questions.md` は「数値は一番最後」と決めてある。** だからこの三つを読むのは、**体験の核・視点・ジャンル・システムが決まってから。** 先に読むと、そのルールの形にゲームが決まる。

**ただし、これらのファイルにも世界設定が混ざっている可能性はある。** 80 ENEMY_TENDENCY がそうだった（伝承拘束、案件のエスカレーション、誤判定の手順が数値と同居していた）。**読むときは、設定と数値を分ける。**

## 6. 将来やるかもしれないこと

- `events/` の frontmatter から `timeline.md` を自動生成する
- `world/` から Wiki / 静的サイトを生成する
- ゲームのマスタデータ（CSV / JSON）を `world/` の ID と突き合わせて検証する

いずれも `tools/check.py` と同じ場所に足せる。今はまだ中身が無いので作っていない。
