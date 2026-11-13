"""Zet een draw.io-ERD (tabellen als shape=table) om naar markdown: tabellen, kolommen, relaties, notities."""
import re, sys, html
import xml.etree.ElementTree as ET
from pathlib import Path

def txt(v):
    v = html.unescape(v or "")
    v = re.sub(r"<br\s*/?>|</div>|</p>", "\n", v, flags=re.I)
    v = re.sub(r"<[^>]+>", "", v)
    v = html.unescape(v).replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", v).strip()

def card(style, end):
    m = re.search(end + r"Arrow=([A-Za-z]+)", style or "")
    return {"ERmandOne": "1", "ERone": "1", "ERzeroToOne": "0..1", "ERoneToMany": "1..N",
            "ERzeroToMany": "0..N", "ERmany": "N", "none": "-"}.get(m.group(1), m.group(1)) if m else "?"

def convert(path):
    root = ET.parse(path).getroot()
    out = [f"# Datamodel v2 (uit {Path(path).name})\n", "_Automatisch omgezet uit draw.io. Kolommen per tabel in diagramvolgorde: sleutel | naam | (type/opmerking)._\n"]
    for dia in root.iter("diagram"):
        cells = {c.get("id"): c for c in dia.iter("mxCell")}
        kids = {}
        for c in cells.values():
            kids.setdefault(c.get("parent"), []).append(c)
        def y(c):
            g = c.find("mxGeometry"); return float(g.get("y", 0)) if g is not None else 0
        def x(c):
            g = c.find("mxGeometry"); return float(g.get("x", 0)) if g is not None else 0
        tables = [c for c in cells.values() if "shape=table;" in (c.get("style") or "")]
        out.append(f"\n## Diagram: {dia.get('name')} — {len(tables)} tabellen\n")
        owner = {}
        for t in sorted(tables, key=lambda t: txt(t.get("value"))):
            name = txt(t.get("value"))
            owner[t.get("id")] = name
            out.append(f"\n### {name}\n")
            for row in sorted(kids.get(t.get("id"), []), key=y):
                owner[row.get("id")] = name
                vals = [txt(c.get("value")) for c in sorted(kids.get(row.get("id"), []), key=x)]
                for c in kids.get(row.get("id"), []):
                    owner[c.get("id")] = name
                vals = [v.replace("\n", " / ") for v in vals]
                if any(vals):
                    out.append("- " + " | ".join(v if v else "·" for v in vals))
        edges = [c for c in cells.values() if c.get("edge") == "1"]
        out.append(f"\n## Relaties ({len(edges)})\n")
        out.append("Notatie: bron [kardinaliteit bij bron] — [kardinaliteit bij doel] doel : label\n")
        rels = []
        for e in edges:
            s, t = owner.get(e.get("source"), e.get("source")), owner.get(e.get("target"), e.get("target"))
            lab = txt(e.get("value"))
            for k in kids.get(e.get("id"), []):
                if txt(k.get("value")):
                    lab = (lab + " " + txt(k.get("value"))).strip()
            rels.append(f"- {s} [{card(e.get('style'),'start')}] — [{card(e.get('style'),'end')}] {t}" + (f" : {lab}" if lab else ""))
        out += sorted(rels)
        notes = [c for c in cells.values() if c.get("vertex") == "1" and c.get("id") not in owner
                 and c.get("parent") in ("1", None) and txt(c.get("value"))]
        if notes:
            out.append("\n## Overige tekst in het diagram (notities, groepstitels, legende)\n")
            for n in sorted(notes, key=lambda n: (y(n), x(n))):
                out.append("- " + txt(n.get("value")).replace("\n", " / "))
    return "\n".join(out)

if __name__ == "__main__":
    md = convert(sys.argv[1]); Path(sys.argv[2]).write_text(md, encoding="utf-8"); print(len(md))
