#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""knowledge-src/ の原稿から knowledge/ の docx・xlsx・pdf を生成する。

使い方: python3 scripts/build_knowledge.py
"""
import csv
import subprocess
import sys
from pathlib import Path

import docx
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn
from docx.shared import Pt, Cm
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "knowledge-src"
OUT = ROOT / "knowledge"

JP_FONT = "Yu Gothic"
ASCII_FONT = "Yu Gothic"

# (原稿, 出力, 文書のタイトル プロパティ)
DOCX_JOBS = [
    ("hr/年次有給休暇規程.md", "hr/年次有給休暇規程.docx",
     "年次有給休暇規程 (付与日数・半日・時間単位・繰越・退職時の取扱い)"),
    ("soumu/会議室利用規程.md", "soumu/会議室利用規程.docx",
     "会議室利用規程 (予約・取消・優先順位・設置備品)"),
    ("it/業務用PC貸与および持出基準.md", "it/業務用PC貸与および持出基準.docx",
     "業務用 PC 貸与および持出基準 (貸与・持ち出し・VPN・紛失時の初動)"),
]

# 原稿は docx を経由して PDF にする (通達類)
PDF_JOBS = [
    ("hr/通勤手当支給細則.md", "hr/通勤手当支給細則.pdf",
     "通勤手当支給細則 (支給額・上限・在宅勤務日の取扱い)"),
    ("soumu/社員証取扱要領.md", "soumu/社員証取扱要領.pdf",
     "社員証取扱要領 (紛失時の連絡・再発行・手数料・一時入館証)"),
]

# (出力, タイトル, [(シート名, 原稿 csv, 注記)])
XLSX_JOBS = [
    ("hr/年次有給休暇付与日数表.xlsx",
     "年次有給休暇付与日数表 (勤続年数別・比例付与)",
     [("第1表 一般", "hr/付与日数表_第1表.csv",
       "出典: 年次有給休暇規程 第 3 条。週所定労働日数が 5 日以上の者に適用する。"),
      ("第2表 比例付与", "hr/付与日数表_第2表.csv",
       "出典: 年次有給休暇規程 第 4 条。週所定労働日数が 4 日以下の者に適用する。単位は日。")]),
    ("soumu/貸与備品一覧.xlsx",
     "貸与備品一覧 (申請区分・貸与期間・自宅への持ち出しの可否)",
     [("貸与備品", "soumu/貸与備品一覧.csv",
       "出典: 会議室利用規程 第 6 条第 3 項。PC とスマートフォンは対象外 (業務用 PC 貸与および持出基準による)。")]),
    ("it/アカウント発行削除手順と権限一覧.xlsx",
     "アカウント発行削除手順と権限一覧 (申請者・承認者・所要日数・退職時の扱い)",
     [("発行と削除の手順", "it/アカウント手順_発行削除.csv",
       "所要日数は承認後の営業日数。0 は当日対応。"),
      ("権限一覧", "it/アカウント手順_権限一覧.csv",
       "棚卸しは情報システム部が実施する。")]),
]


# 表を本文形式で持つ文書。SharePoint をナレッジ ソースにする経路はセマンティック検索で、
# xlsx のセルを引けないため (Microsoft Learn の Quotas and limits / code interpreter を参照)、
# 同じ内容を docx・pdf でも作る。published に置くのはこちらで、xlsx は参考として残す。
# (出力, タイトル, 前文, [(見出し, 原稿 csv, 注記)])
TABLEDOC_JOBS = [
    ("hr/年次有給休暇付与日数表.docx",
     "年次有給休暇付与日数表 (第 1 表 一般・第 2 表 比例付与)",
     "人事部\n\n2024 年 4 月 1 日\n\n本表は年次有給休暇規程 第 3 条および第 4 条の別表である。単位は日とする。",
     [("第 1 表 一般 (週所定労働日数が 5 日以上の者)", "hr/付与日数表_第1表.csv",
       "出典: 年次有給休暇規程 第 3 条。付与日は入社日から 6 か月を経過した日、およびその後 1 年ごとの同月同日とする。"),
      ("第 2 表 比例付与 (週所定労働日数が 4 日以下の者)", "hr/付与日数表_第2表.csv",
       "出典: 年次有給休暇規程 第 4 条。表中の数値は付与日数 (日) を表す。")]),
    ("soumu/貸与備品一覧.docx",
     "貸与備品一覧 (申請区分・貸与期間・自宅への持ち出しの可否)",
     "総務部\n\n2024 年 4 月 1 日\n\n本表は会議室利用規程 第 6 条第 3 項の別表である。",
     [("貸与備品", "soumu/貸与備品一覧.csv",
       "PC とスマートフォンは本表の対象外とし、業務用 PC 貸与および持出基準による。")]),
    ("it/アカウント発行削除手順と権限一覧.docx",
     "アカウント発行削除手順と権限一覧 (申請者・承認者・所要日数・退職時の扱い)",
     "情報システム部\n\n2024 年 4 月 1 日\n\n本表は業務用 PC 貸与および持出基準の別表である。",
     [("発行と削除の手順", "it/アカウント手順_発行削除.csv",
       "所要日数は承認後の営業日数を表す。0 は当日対応とする。"),
      ("権限一覧", "it/アカウント手順_権限一覧.csv",
       "棚卸しは情報システム部が実施する。")]),
]

XLSX_KEEP = OUT / "_xlsx-参考"


def csv_to_md_table(rows) -> str:
    head, *body = rows
    out = ["| " + " | ".join(head) + " |",
           "| " + " | ".join("---" for _ in head) + " |"]
    for row in body:
        out.append("| " + " | ".join(row) + " |")
    return "\n".join(out)


def build_tabledoc(dst: Path, title: str, preamble: str, sections) -> None:
    lines = ["# " + title.split(" (")[0], "", preamble, ""]
    for heading, csv_rel, note in sections:
        rows = list(csv.reader((SRC / csv_rel).open(encoding="utf-8")))
        lines += ["## " + heading, "", csv_to_md_table(rows), "", note, ""]
    tmp_md = dst.parent / (dst.stem + ".tmp.md")
    tmp_md.parent.mkdir(parents=True, exist_ok=True)
    tmp_md.write_text("\n".join(lines), encoding="utf-8")
    try:
        if dst.suffix == ".pdf":
            md_to_pdf(tmp_md, dst, title)
        else:
            md_to_docx(tmp_md, dst, title)
    finally:
        tmp_md.unlink(missing_ok=True)


def set_fonts(document: docx.Document) -> None:
    """既定スタイルと見出しに日本語フォントを設定する。"""
    for style_name in ("Normal", "Title", "Heading 1", "Heading 2", "Heading 3",
                       "List Bullet", "List Number"):
        try:
            style = document.styles[style_name]
        except KeyError:
            continue
        font = style.font
        font.name = ASCII_FONT
        if style_name == "Normal":
            font.size = Pt(10.5)
        rpr = style.element.get_or_add_rPr()
        rfonts = rpr.find(qn("w:rFonts"))
        if rfonts is None:
            rfonts = rpr.makeelement(qn("w:rFonts"), {})
            rpr.append(rfonts)
        rfonts.set(qn("w:eastAsia"), JP_FONT)
        rfonts.set(qn("w:ascii"), ASCII_FONT)
        rfonts.set(qn("w:hAnsi"), ASCII_FONT)


def set_page(document: docx.Document) -> None:
    for section in document.sections:
        section.orientation = WD_ORIENT.PORTRAIT
        section.page_width = Cm(21.0)
        section.page_height = Cm(29.7)
        section.top_margin = Cm(2.5)
        section.bottom_margin = Cm(2.5)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(2.5)


def md_to_docx(src: Path, dst: Path, title: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["pandoc", str(src), "-f", "gfm", "-t", "docx", "-o", str(dst)],
        check=True,
    )
    document = docx.Document(str(dst))
    set_fonts(document)
    set_page(document)
    props = document.core_properties
    props.title = title
    props.author = "総務部" if "soumu" in str(dst) else (
        "情報システム部" if "it/" in str(dst) else "人事部")
    props.category = "社内規程"
    document.save(str(dst))


def md_to_pdf(src: Path, dst: Path, title: str) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    tmp_docx = dst.with_suffix(".tmp.docx")
    md_to_docx(src, tmp_docx, title)
    subprocess.run(
        ["soffice", "--headless", "--convert-to", "pdf",
         "--outdir", str(dst.parent), str(tmp_docx)],
        check=True, capture_output=True,
    )
    produced = dst.parent / (tmp_docx.stem + ".pdf")
    produced.replace(dst)
    tmp_docx.unlink()
    try:
        from pypdf import PdfReader, PdfWriter
        reader = PdfReader(str(dst))
        writer = PdfWriter()
        for page in reader.pages:
            writer.add_page(page)
        writer.add_metadata({"/Title": title, "/Subject": "社内通達"})
        with open(dst, "wb") as handle:
            writer.write(handle)
    except ImportError:
        print("  pypdf がないため PDF のタイトル プロパティは設定しません", file=sys.stderr)


def csv_to_sheet(worksheet, rows, note: str) -> None:
    head_fill = PatternFill("solid", fgColor="DCE6F1")
    thin = Side(style="thin", color="A6A6A6")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)
    for r, row in enumerate(rows, start=1):
        for c, value in enumerate(row, start=1):
            if r > 1:
                stripped = value.strip()
                if stripped.lstrip("-").isdigit():
                    value = int(stripped)
            cell = worksheet.cell(row=r, column=c, value=value)
            cell.font = Font(name=JP_FONT, size=10, bold=(r == 1))
            cell.border = border
            cell.alignment = Alignment(vertical="center", wrap_text=(r == 1))
            if r == 1:
                cell.fill = head_fill
    widths = {}
    for row in rows:
        for c, value in enumerate(row, start=1):
            length = sum(2 if ord(ch) > 0x2E80 else 1 for ch in str(value))
            widths[c] = max(widths.get(c, 8), min(length + 3, 44))
    for c, width in widths.items():
        worksheet.column_dimensions[get_column_letter(c)].width = width
    worksheet.freeze_panes = "A2"
    note_row = len(rows) + 2
    cell = worksheet.cell(row=note_row, column=1, value=note)
    cell.font = Font(name=JP_FONT, size=9, italic=True)


def build_xlsx(dst: Path, title: str, sheets) -> None:
    dst.parent.mkdir(parents=True, exist_ok=True)
    workbook = Workbook()
    workbook.remove(workbook.active)
    for sheet_name, csv_rel, note in sheets:
        rows = list(csv.reader((SRC / csv_rel).open(encoding="utf-8")))
        worksheet = workbook.create_sheet(sheet_name)
        csv_to_sheet(worksheet, rows, note)
    workbook.properties.title = title
    workbook.properties.category = "社内規程の別表"
    workbook.save(str(dst))


def main() -> int:
    for src_rel, dst_rel, title in DOCX_JOBS:
        md_to_docx(SRC / src_rel, OUT / dst_rel, title)
        print("docx:", dst_rel)
    for src_rel, dst_rel, title in PDF_JOBS:
        md_to_pdf(SRC / src_rel, OUT / dst_rel, title)
        print("pdf :", dst_rel)
    for dst_rel, title, preamble, sections in TABLEDOC_JOBS:
        build_tabledoc(OUT / dst_rel, title, preamble, sections)
        print("表文書:", dst_rel)
    XLSX_KEEP.mkdir(parents=True, exist_ok=True)
    for dst_rel, title, sheets in XLSX_JOBS:
        name = Path(dst_rel).name
        build_xlsx(XLSX_KEEP / name, title, sheets)
        print("xlsx (参考):", "_xlsx-参考/" + name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
