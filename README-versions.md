# スキルの版

| 版 | 内容 | 差し替えたエージェント |
| --- | --- | --- |
| v1 (`skills/`) | 初期版 | ベースライン時点の全エージェント |
| v2 (`skills-v2/`) | 検証 A から D で使用。口調、エスカレーション、有給の手続きを変更 | 検証当時は全エージェント |
| v3 (`skills-v3/`) | E-01 で `tone-and-format` に受付時間の節を追加。E-03 で `hr-tone` を追加 | ハブ (tone-and-format)、人事 (hr-tone) |
| v4 (`skills-v4/`) | E-03 で `tone-and-format` に `## 部門ごとの文体` の節を追加。`hr-tone` は廃止 | ハブのみ |

**運用で使うのは v4 です。** `hr-tone` は E-03 で起動しないことが分かったため、v4 には含めていません。部門ごとの文体は `tone-and-format` の `## 部門ごとの文体` の節に集約しています。

## 検証用のマーカー スキル (`skills-f/`)

検証 F (スキルの起動は仕様か書き方か) 専用です。運用には使いません。本文は「回答の最後に固有の整理番号を 1 文で書く」だけで、版の間で違うのはスキル名と description と整理番号だけです。設計は `tests/検証F-計画.md`、記録は `tests/records/検証F.md` にあります。

| フォルダー | スキル名 | 整理番号 | 置く先 | ドロップするファイル |
| --- | --- | --- | --- | --- |
| `f1-always-run-first` | `always-run-first` | F-1-7781 | 人事 | `upload/f/1/always-run-first.md` |
| `f2a-hr-leave-note` | `hr-leave-note` | F-2A-3310 | 人事 | `upload/f/2a/hr-leave-note.md` |
| `f2b-skill-01` | `skill-01` | F-2B-6630 | 人事 | `upload/f/2b/skill-01.md` |
| `f2c-hr-leave-note-min` | `hr-leave-note` | F-2C-5560 | 人事 | `upload/f/2c/hr-leave-note.md` |
| `f2d-skill-01-min` | `skill-01` | F-2D-8840 | 人事 | `upload/f/2d/skill-01.md` |
| `f3-hub-serial` | `hub-serial` | F-3-9910 | ハブ | `upload/f/3/hub-serial.md` |
| `f4-pad-glossary` | `glossary-note` | なし | 人事 (段階 4 の水増し) | `upload/f/4/glossary-note.md` |
| `f4-pad-meeting` | `meeting-room-note` | なし | 人事 (段階 4 の水増し) | `upload/f/4/meeting-room-note.md` |
| `f4-pad-device` | `device-note` | なし | 人事 (段階 4 の水増し) | `upload/f/4/device-note.md` |

`f2a` と `f2c` は同じスキル名、`f2b` と `f2d` も同じスキル名です。入れ替えて 1 つずつ試すためで、同時には置きません。ドロップ ファイルを段階ごとのフォルダーに分けてあるのはそのためです。
