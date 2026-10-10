#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""skills/ と skills-v2/ の各版から、アップロード用のファイルを作る。

Copilot Studio の [スキルの追加] が受け付けるのは、YAML フロントマターと
Markdown の指示を持つ .md か、SKILL.md を含む zip。今回のスキルは SKILL.md
1 枚だけなので .md で足りる。スキルの識別はフロントマターの name で行われ、
ファイル名では行われない。SKILL.md のままでも製品側では衝突しないが、Finder
からどれを掴むか分かりにくいので、スキル名を付けた .md を出す。

zip は出さない。補助ファイルを同梱する必要が出たら、ここで zipfile を使って
SKILL.md を直下に入れた zip を作る。

各版は 1 つの完全な一式です。前の版から変わっていないスキルも含めて出すので、
その版だけを見てドロップできます。

使い方: python3 scripts/build_upload.py
"""
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
JOBS = (
    ("v1", "skills"),
    ("v2", "skills-v2"),
)


def main() -> None:
    for version, src_name in JOBS:
        out_dir = ROOT / "upload" / version
        out_dir.mkdir(parents=True, exist_ok=True)
        for skill_dir in sorted((ROOT / src_name).iterdir()):
            if not skill_dir.is_dir():
                continue
            md = out_dir / f"{skill_dir.name}.md"
            shutil.copyfile(skill_dir / "SKILL.md", md)
            print(f"{version}/{md.name}  {md.stat().st_size} バイト")



if __name__ == "__main__":
    main()
