"""PDF 마스킹 일괄 제거기

Acrobat에서 넣은 강조, 교정(Redact) 표시(적용 전), 사각형 주석을 한 번에 지운 사본을 만든다.
원본은 건드리지 않고 같은 폴더에 '<원래이름>_마스킹제거.pdf'로 저장한다.

사용법
  - PDF 파일이나 폴더(여러 개 가능)를 exe 아이콘 위로 끌어다 놓기
  - 또는 exe를 그냥 실행하면 폴더 선택 창이 뜨고, 그 폴더 안의 PDF를 모두 처리한다
"""
import sys
from pathlib import Path

from pypdf import PdfReader, PdfWriter
from pypdf.generic import ArrayObject, NameObject

# 지울 주석 종류. 원이나 펜 마스킹도 지우려면 "/Circle", "/Ink"를 추가한다.
MASK_SUBTYPES = {"/Redact", "/Square", "/Highlight"}
SUFFIX = "_마스킹제거"


def pick_folder():
    import tkinter as tk
    from tkinter import filedialog

    root = tk.Tk()
    root.withdraw()
    path = filedialog.askdirectory(title="마스킹을 지울 PDF가 있는 폴더 선택")
    root.destroy()
    return [path] if path else []


def collect_pdfs(paths):
    """폴더는 그 안의 PDF(하위 폴더 제외)로 펼치고, 이미 처리한 결과 파일은 건너뛴다."""
    pdfs = []
    for p in paths:
        if p.is_dir():
            pdfs += sorted(f for f in p.iterdir() if f.is_file() and f.suffix.lower() == ".pdf")
        else:
            pdfs.append(p)
    return [p for p in pdfs if not p.stem.endswith(SUFFIX)]


def unmask(src: Path) -> tuple[Path, int]:
    reader = PdfReader(src)
    if reader.is_encrypted:
        reader.decrypt("")
    writer = PdfWriter(clone_from=reader)

    removed = 0
    for page in writer.pages:
        if "/Annots" not in page:
            continue
        annots = page["/Annots"].get_object()
        masks = [a for a in annots if a.get_object().get("/Subtype") in MASK_SUBTYPES]
        if not masks:
            continue
        mask_ids = {id(a.get_object()) for a in masks}
        kept = ArrayObject()
        for a in annots:
            obj = a.get_object()
            if id(obj) in mask_ids:
                continue
            # 지운 마스킹에 딸린 팝업 메모도 함께 지운다
            parent = obj.get("/Parent")
            if obj.get("/Subtype") == "/Popup" and parent is not None and id(parent.get_object()) in mask_ids:
                continue
            kept.append(a)
        removed += len(masks)
        if kept:
            page[NameObject("/Annots")] = kept
        else:
            del page["/Annots"]

    dst = src.with_name(f"{src.stem}{SUFFIX}{src.suffix}")
    with open(dst, "wb") as f:
        writer.write(f)
    return dst, removed


def main():
    paths = collect_pdfs([Path(p) for p in (sys.argv[1:] or pick_folder())])
    if not paths:
        print("처리할 PDF가 없습니다.")
    for p in paths:
        try:
            dst, n = unmask(p)
            print(f"[완료] {p.name}: 마스킹 {n}개 제거 -> {dst.name}")
            if n == 0:
                print("       (지울 마스킹이 없습니다. 이미 '적용'된 교정이거나 'PDF 편집'으로 그린 도형일 수 있습니다.)")
        except Exception as e:
            print(f"[실패] {p.name}: {e}")
    input("\n엔터를 누르면 창이 닫힙니다...")


if __name__ == "__main__":
    main()
