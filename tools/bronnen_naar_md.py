"""Zet de bronbestanden (xlsx/xlsm/xls/docx) om naar compacte markdown voor opencode.

Gebruik:  python tools/bronnen_naar_md.py
Leest:    00_bronnen/docs/
Schrijft: 01_context/docs/<naam>.md          (inhoud, enkel niet-lege cellen)
          01_context/keuzelijsten/<naam>.md  (Excel-keuzelijsten / data validations)
Vereist:  pip install openpyxl xlrd python-docx
"""
import re, sys, warnings
warnings.filterwarnings("ignore")
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT, KL = ROOT / "00_bronnen/docs", ROOT / "01_context/docs", ROOT / "01_context/keuzelijsten"


def clean(v):
    if v is None:
        return ""
    s = str(v).strip()
    if s.endswith(".0") and s[:-2].isdigit():
        s = s[:-2]
    return re.sub(r"\s+", " ", s)


def resolve_range(wb, ref, cur_ws):
    """Zet een verwijzing als =Lijsten!$A$1:$A$9 of een benoemd bereik om naar waarden."""
    ref = ref.lstrip("=").strip()
    if ref.startswith('"'):
        return [x.strip() for x in ref.strip('"').split(",")]
    try:
        if ref in wb.defined_names:
            dests = list(wb.defined_names[ref].destinations)
            if dests:
                sheet, rng = dests[0]
                return [clean(c.value) for row in wb[sheet][rng.replace("$", "")] for c in row if clean(c.value)]
    except Exception:
        pass
    m = re.match(r"^(?:'?([^'!]+)'?!)?(\$?[A-Z]+\$?\d+(?::\$?[A-Z]+\$?\d+)?)$", ref)
    if not m:
        return None
    ws = wb[m.group(1)] if m.group(1) and m.group(1) in wb.sheetnames else cur_ws
    cells = ws[m.group(2).replace("$", "")]
    if not isinstance(cells, tuple):
        cells = ((cells,),)
    elif cells and not isinstance(cells[0], tuple):
        cells = (cells,)
    return [clean(c.value) for row in cells for c in row if clean(c.value)]


def xlsx(path):
    import openpyxl
    wb = openpyxl.load_workbook(path, data_only=True)
    out, kl = [f"# {path.name}\n", "_Enkel niet-lege cellen. Formaat: `rij | kolom: waarde`._\n"], [f"# Keuzelijsten in {path.name}\n"]
    for ws in wb.worksheets:
        state = "" if ws.sheet_state == "visible" else f" (verborgen: {ws.sheet_state})"
        out.append(f"\n## Blad: {ws.title}{state}\n")
        for row in ws.iter_rows():
            cells = [f"{c.column_letter}: {clean(c.value)}" for c in row if clean(c.value)]
            if cells:
                out.append(f"- r{row[0].row} | " + " | ".join(cells))
        dvs = getattr(ws.data_validations, "dataValidation", [])
        if dvs:
            kl.append(f"\n## Blad: {ws.title}\n")
            seen = {}
            for dv in dvs:
                key = (dv.type, dv.formula1)
                seen.setdefault(key, []).append(str(dv.sqref))
            for (typ, f1), ranges in seen.items():
                vals = resolve_range(wb, f1, ws) if typ == "list" and f1 else None
                rs = " ".join(ranges)
                rs = rs if len(rs) < 200 else rs[:200] + " …"
                kl.append(f"- **{typ}** `{f1}` → cellen {rs}")
                if vals:
                    kl.append(f"  - waarden: {', '.join(dict.fromkeys(vals))}")
    ext = x14_validations(path, wb)
    if ext:
        kl.append("\n## Keuzelijsten in Excel-extensieformaat (x14)\n")
        kl.extend(ext)
    return "\n".join(out), ("\n".join(kl) if len(kl) > 1 else None)


def x14_validations(path, wb):
    """openpyxl slaat x14-keuzelijsten over (lijsten die naar een ander blad verwijzen); lees ze rechtstreeks uit de XML."""
    import zipfile
    z = zipfile.ZipFile(path)
    rels = z.read("xl/_rels/workbook.xml.rels").decode("utf8", "ignore")
    book = z.read("xl/workbook.xml").decode("utf8", "ignore")
    rid_target = dict(re.findall(r'Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    rid_target.update({k: v for v, k in re.findall(r'Target="([^"]+)"[^>]*Id="([^"]+)"', rels)})
    lines = []
    for name, rid in re.findall(r'<sheet [^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', book):
        target = rid_target.get(rid, "").lstrip("/")
        target = target if target.startswith("xl/") else "xl/" + target
        if target not in z.namelist():
            continue
        xml = z.read(target).decode("utf8", "ignore")
        for f1, sq in re.findall(r"<x14:dataValidation [^>]*>.*?<xm:f>(.*?)</xm:f>.*?<xm:sqref>(.*?)</xm:sqref>", xml, re.S):
            ws = wb[name] if name in wb.sheetnames else wb.active
            vals = resolve_range(wb, f1, ws)
            lines.append(f"- blad **{name}**: `{f1}` → cellen {sq}")
            if vals:
                lines.append(f"  - waarden: {', '.join(dict.fromkeys(vals))}")
    return lines


def xls(path):
    import xlrd
    wb = xlrd.open_workbook(path)
    out = [f"# {path.name}\n", "_Enkel niet-lege cellen. Oud .xls-formaat: keuzelijsten niet uitleesbaar._\n"]
    for sh in wb.sheets():
        out.append(f"\n## Blad: {sh.name}\n")
        for r in range(sh.nrows):
            cells = [f"{xlrd.colname(c)}: {clean(sh.cell_value(r, c))}" for c in range(sh.ncols) if clean(sh.cell_value(r, c))]
            if cells:
                out.append(f"- r{r+1} | " + " | ".join(cells))
    return "\n".join(out), None


def docx_(path):
    import docx
    d = docx.Document(path)
    out = [f"# {path.name}\n"]
    body = d.element.body
    for el in body.iterchildren():
        tag = el.tag.split("}")[1]
        if tag == "p":
            p = docx.text.paragraph.Paragraph(el, d)
            t = clean(p.text)
            has_img = bool(el.findall(".//{http://schemas.openxmlformats.org/drawingml/2006/main}blip"))
            if not t and not has_img:
                continue
            style = (p.style.name or "").lower()
            if style.startswith("heading") or style.startswith("kop"):
                lvl = re.findall(r"\d", style)
                out.append("\n" + "#" * (int(lvl[0]) + 1 if lvl else 2) + " " + t)
            elif t:
                out.append(t)
            if has_img:
                out.append("[foto]")
        elif tag == "tbl":
            tbl = docx.table.Table(el, d)
            for row in tbl.rows:
                vals = []
                for c in row.cells:
                    v = clean(c.text)
                    if not vals or vals[-1] != v:
                        vals.append(v)
                if any(vals):
                    out.append("| " + " | ".join(vals) + " |")
            out.append("")
    return "\n".join(out), None


HANDLERS = {".xlsx": xlsx, ".xlsm": xlsx, ".xls": xls, ".docx": docx_}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True); KL.mkdir(parents=True, exist_ok=True)
    for f in sorted(SRC.iterdir()):
        h = HANDLERS.get(f.suffix.lower())
        if not h:
            continue
        try:
            md, kl = h(f)
            (OUT / f"{f.stem}.md").write_text(md, encoding="utf-8")
            if kl:
                (KL / f"{f.stem}.md").write_text(kl, encoding="utf-8")
            print(f"OK   {f.name}  ({len(md)//1000} kB{', + keuzelijsten' if kl else ''})")
        except Exception as e:
            print(f"FOUT {f.name}: {e}", file=sys.stderr)
