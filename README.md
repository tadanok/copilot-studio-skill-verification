# Copilot Studio スキル差し替え検証キット

Microsoft Copilot Studio (GitHub Copilot ハーネス) で、エージェントの振る舞いの変更をスキル (`SKILL.md`) の差し替えだけで完結できるかを確かめるための一式です。
ハブと 3 つの部門エージェントの構成で、スキルの差し替えがどこまで効くかを、検証 A から G で確かめます。

> [!NOTE]
> 2026 年 10 月時点の情報です。
> Copilot Studio の画面と挙動は変わりやすく、この検証で使った機能にはプレビュー段階のものが含まれます。

## 対応する記事

Qiita の連載 (全 4 回) の詳細を、このリポジトリで補っています。
検証の記録と結果は、連載の進行に合わせて追加します。

1. [第 1 回 設計とキット](https://qiita.com/tadanok/items/df45c82b3cb3348a94f3)
2. [第 2 回 検証 A から E](https://qiita.com/tadanok/items/754a5097ea26418227f8)
3. [第 3 回 検証 F と G](https://qiita.com/tadanok/items/535d23fc1aaf9fd8cdc8)
4. 第 4 回 運用に持ち込むなら (公開後にリンクします)

## 中身

| 場所 | 中身 | 使いどころ |
| --- | --- | --- |
| `手順書.md` | 検証の進め方 (図入り) | 最初に読む |
| `キットの補足.md` | アップロード用ファイルの扱いと、原稿からの作り直しかた | キットを直すとき |
| `README-versions.md` | スキルの版 v1 から v4 と、検証 F の目印のスキルの対応表 | どの版を使うかの確認 |
| `agents/*/instructions.md` | ハブと 3 部門の指示 | フェーズ 1 と検証 D |
| `agents/*/description.md` | 接続エージェントの説明文 | フェーズ 1 と検証 D |
| `skills/` | 共通スキル 3 つの原稿。v1 (差し替え前) | 正本の管理とレビュー |
| `skills-v2/` | v2。検証 A から D で使用 | 正本の管理とレビュー |
| `skills-v3/` | v3。E-01 と E-03 の途中経過。`hr-tone` を含む | 正本の管理とレビュー |
| `skills-v4/` | v4。運用で使う版。`hr-tone` は廃止 | 正本の管理とレビュー |
| `skills-f/` | 検証 F の目印のスキル。運用には使わない | 検証 F |
| `upload/v1/` から `upload/v4/`、`upload/f/` | 各版をスキル名の `.md` にしたもの | アップロードはここから |
| `knowledge/hr/`、`knowledge/soumu/`、`knowledge/it/` | SharePoint に置く文書 (docx、pdf) | フェーズ 0 と検証 D |
| `knowledge/_xlsx-参考/` | 同じ表を xlsx にしたもの | 登録しない |
| `knowledge-src/` | 文書の原稿 (Markdown と CSV) | 文書を直すとき |
| `tests/検証テストセットと記録シート.xlsx` | 質問、変更依頼、記録欄、判定表 (検証 A から E の記録入り) | 全フェーズ |
| `tests/testset.csv`、`tests/change-requests.csv` | テストセットと変更依頼の原稿 | テストセットを直すとき |
| `tests/検証F-計画.md` | 検証 F の設計と手順 | 検証 F |
| `tests/records/` | 検証 A から G の詳細記録 | 結果の見直し |
| `scripts/` | 原稿から文書、検証ブック、アップロード用ファイルを作り直すスクリプト | キットを直すとき |
| `figures/` | 実画面のスクリーンショット | 手順の確認 |

## 始め方

1. `手順書.md` の「この検証で確かめること」と「前提」を読みます。
2. 「フェーズ 0: 準備」から順に進めます。スキルは `upload/` の各版のフォルダーからドロップします。
3. 結果は `tests/検証テストセットと記録シート.xlsx` に記録し、`tests/records/` の記録と見比べます。

## 前提と課金の注意

- Copilot Studio で GitHub Copilot ハーネスのエージェントを作成、公開できる権限と、ナレッジを置く SharePoint のサイトが必要です。
- GitHub Copilot ハーネスのエージェントは、**作り始めた時点から Copilot クレジットを消費します**。公開後に課金が始まる標準ハーネスとは違い、公開前の **[プレビュー]** での試行や評価の作成も課金の対象です。
- Copilot クレジットを割り当てた環境が必要です。Microsoft 365 Copilot のライセンスでは賄われません。
- 動かす前に、消費量の見方を確認してください。詳しくは「[使用率に基づく請求の概要](https://learn.microsoft.com/ja-jp/microsoft-copilot-studio/agents-experience/billing-credit-overview)」と「[GitHub Copilotハーネスを使用してエージェントのコストを管理する](https://learn.microsoft.com/ja-jp/power-platform/admin/manage-usage-github-copilot-harness)」を参照してください。

## ライセンスと免責

このリポジトリは、中身の種類によって 2 つのライセンスを使い分けています。

| 対象 | ライセンス |
| --- | --- |
| `scripts/` | [MIT](LICENSE) |
| `skills/` から `skills-v4/`、`skills-f/`、`upload/` (SKILL.md) | [MIT](LICENSE) |
| `agents/` (指示と説明文) | [MIT](LICENSE) |
| `手順書.md`、`README.md`、`キットの補足.md`、`README-versions.md`、`tests/` (テストセット、記録シート、記録) | [CC BY 4.0](LICENSE-docs) |
| `knowledge/`、`knowledge-src/` (架空の文書) | [CC BY 4.0](LICENSE-docs) |
| `figures/` (スクリーンショット) | **対象外**。Microsoft の製品画面です。Used with permission from Microsoft. |

SKILL.md と指示は、ご自身のエージェントにそのまま組み込んで使えるよう MIT にしています。
文章を転載、改変して使う場合は、出典 (このリポジトリへのリンクと著作者名) を表示してください。

- このリポジトリは個人の検証の記録です。Microsoft とは関係がなく、Microsoft が承認、保証したものではありません。
- `knowledge/` と `knowledge-src/` の文書 (規程、細則、要領、一覧) は、検証のために作った**架空のもの**です。実在の組織の規程ではありません。文中のメール アドレスは例示用のドメイン (`example.com`) です。
- 記録の内容は、2026 年 9 月から 10 月に 1 つの検証用テナントで観測したものです。ほかの環境や、機能が更新された後に同じ結果になるとは限りません。
