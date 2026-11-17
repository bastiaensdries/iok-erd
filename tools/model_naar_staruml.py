"""Maakt 03_output/IOK_erd_v3.mdj (StarUML, ER-diagram) uit 03_output/datamodel_v3.md.

Gebruik:  python tools/model_naar_staruml.py [voorbeeld.png]
Zelfde bron en aanvulling als tools/stap6_genereer.py; niet met de hand wijzigen.
De tabellen staan op vaste plaatsen (LAYOUT) en de lijnen zijn rechthoekig gerouteerd:
een lijn vertrekt aan de zijkant van de bovenliggende tabel en komt aan ter hoogte van
de lookup-kolom in de onderliggende tabel.
"""
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import stap6_genereer as g

UIT = g.ROOT / "03_output/IOK_erd_v3.mdj"
_n = [0]
def nid():
    _n[0] += 1
    return "IOKv3-%05d" % _n[0]
def ref(x):
    return {"$ref": x["_id"] if isinstance(x, dict) else x}

STYPE = {"text": "Tekst", "memo": "Tekst lang", "int": "Geheel getal", "decimal": "Decimaal", "date": "Datum", "datetime": "Datum/tijd",
         "choice": "Keuze", "bool": "Ja/Nee", "lookup": "Lookup", "autonumber": "Autonummer"}
FONT, FONTB = "Arial;13;0", "Arial;13;1"
# kolommen van links naar rechts; (tabel, extra ruimte erboven)
LAYOUT = [
    [("contact", 300), ("account", 0), ("iok_terreingroep", 0), ("iok_toestelcode", 150)],
    [("iok_speelterrein", 430), ("iok_speeltoestel", 0)],
    [("iok_toesteltype", 0), ("iok_checklist", 0), ("systemuser", 0), ("iok_inspectiedossier", 0), ("iok_rapportversie", 0), ("iok_document", 0), ("sharepointdocumentlocation", 0)],
    [("iok_checklistonderdeel", 0), ("iok_beoordeling", 120), ("iok_standaardtekst", 0)],
    [("iok_controlepunt", 0), ("iok_resultaat", 0), ("iok_maatregel", 0), ("iok_foto", 0), ("iok_hicmeting", 0)],
]
TOP, VGAP, KANAAL, LANE = 170, 70, 230, 14

def rij_y(v, i):
    return v["top"] + 28 + 15 * i + 6

def bouw(preview=None):
    m = g.model()
    project = {"_type": "Project", "_id": nid(), "name": "IOK datamodel v3", "ownedElements": []}
    dm = {"_type": "ERDDataModel", "_id": nid(), "_parent": ref(project), "name": "IOK v3 (Dataverse)", "ownedElements": []}
    project["ownedElements"].append(dm)
    dia = {"_type": "ERDDiagram", "_id": nid(), "_parent": ref(dm), "name": "ERD IOK v3", "visible": True, "defaultDiagram": True, "ownedViews": []}
    dm["ownedElements"].append(dia)
    ent, kol, kidx = {}, {}, {}
    for t in m["entiteiten"]:
        e = {"_type": "ERDEntity", "_id": nid(), "_parent": ref(dm), "name": t, "ownedElements": [], "columns": []}
        uk = {s["kolommen"][0] for s in m["sleutels"] if s["tabel"] == t and len(s["kolommen"]) == 1}
        def col(naam, typ, lengte=0, pk=False, fk=False, nullable=True, unique=False):
            c = {"_type": "ERDColumn", "_id": nid(), "_parent": ref(e), "name": naam, "type": typ, "length": int(lengte) if lengte else 0,
                 "primaryKey": pk, "foreignKey": fk, "nullable": nullable, "unique": unique}
            kidx[(t, naam)] = len(e["columns"]); e["columns"].append(c); kol[(t, naam)] = c
        col(g.pk_naam(t), "GUID", pk=True, nullable=False)
        for naam, typ, key in g.HERGEBRUIKT.get(t, []):
            col(naam, "Lookup" if typ.startswith("Lookup") else "Tekst", fk=bool(key))
        for k in m["tabellen"].get(t, []):
            typ = STYPE[k["type"]]
            if k.get("formaat") == "url": typ = "URL"
            if k.get("formule"): typ = "Formule"
            lengte = k.get("lengte") or (k.get("precisie") if k["type"] == "decimal" else 0)
            col(k["schema"], typ, lengte, fk=(k["type"] == "lookup"), nullable=not k.get("verplicht"), unique=k["schema"] in uk)
        ent[t] = e; dm["ownedElements"].append(e)
    assert sorted(t for kolom in LAYOUT for t, _ in kolom) == sorted(m["entiteiten"]), "LAYOUT mist tabellen"
    # ---- tabellen plaatsen
    def breedte(t):
        cs = ent[t]["columns"]
        return 95 + int(7.0 * max(len(c["name"]) for c in cs)) + int(7.0 * max(len(c["type"]) + (len(str(c["length"])) + 2 if c["length"] else 0) for c in cs))
    view, plek, x = {}, {}, 60
    kol_x = []
    for ci, kolom in enumerate(LAYOUT):
        w = max(breedte(t) for t, _ in kolom); kol_x.append((x, x + w)); y = TOP
        for ri, (t, extra) in enumerate(kolom):
            e = ent[t]; y += extra; h = 31 + 15 * len(e["columns"])
            v = {"_type": "ERDEntityView", "_id": nid(), "_parent": ref(dia), "model": ref(e), "subViews": [], "font": FONT,
                 "left": x, "top": y, "width": w, "height": h, "autoResize": False}
            lab = {"_type": "LabelView", "_id": nid(), "_parent": ref(v), "font": FONTB, "left": x, "top": y + 5, "width": w, "height": 13, "text": t,
                   "horizontalAlignment": 2, "verticalAlignment": 5}
            comp = {"_type": "ERDColumnCompartmentView", "_id": nid(), "_parent": ref(v), "model": ref(e), "subViews": [], "font": FONT,
                    "left": x, "top": y + 23, "width": w, "height": h - 23}
            for i, c in enumerate(e["columns"]):
                comp["subViews"].append({"_type": "ERDColumnView", "_id": nid(), "_parent": ref(comp), "model": ref(c), "font": FONT,
                                         "left": x + 5, "top": y + 28 + 15 * i, "width": w - 10, "height": 13})
            v["subViews"] = [lab, comp]; v["nameLabel"] = ref(lab); v["columnCompartment"] = ref(comp)
            dia["ownedViews"].append(v); view[t] = v; plek[t] = (ci, ri)
            y += h + VGAP
        x += w + KANAAL
    onder = max(v["top"] + v["height"] for v in view.values())
    # ---- lijnen: eerst de aankomstpoorten (rij van de lookup), dan de vertrekpoorten
    edges = []
    for r in m["relaties"]:
        fk = kol.get((r["naar"], r["lookup"]))
        fk["referenceTo"] = ref(kol[(r["van"], g.pk_naam(r["van"]))])
        edges.append({"van": r["van"], "naar": r["naar"], "rij": kidx[(r["naar"], r["lookup"])], "k1": "1" if r["vo"] == "V" else "0..1", "k2": "0..*", "naam": ""})
    for n in m["nn"]:
        edges.append({"van": n["tabellen"][0], "naar": n["tabellen"][1], "rij": None, "k1": "0..*", "k2": "0..*", "naam": n["schema"] + " (N:N)"})
    for e in edges:
        (cs, rs), (ct, rt) = plek[e["van"]], plek[e["naar"]]
        if e["van"] == e["naar"]: e["soort"], e["z1"], e["z2"] = "zij", "R", "R"
        elif cs == ct and abs(rs - rt) == 1: e["soort"] = "vert"
        elif cs == ct: e["soort"], e["z1"], e["z2"] = "zij", "R", "R"
        elif abs(cs - ct) == 1: e["soort"], e["z1"], e["z2"] = "buur", ("R" if ct > cs else "L"), ("L" if ct > cs else "R")
        else: e["soort"], e["z1"], e["z2"] = "ver", ("R" if ct > cs else "L"), ("L" if ct > cs else "R")
    bezet = {}
    def vrij(t, zij, doel_y):
        v = view[t]; n = len(ent[t]["columns"])
        kand = [rij_y(v, i) for i in range(n)] + [rij_y(v, i) + 7 for i in range(n - 1)]
        kand = [y for y in kand if y not in bezet.setdefault((t, zij), set())]
        y = min(kand, key=lambda y: abs(y - doel_y)); bezet[(t, zij)].add(y)
        return y
    for e in edges:
        if e["soort"] != "vert" and e["rij"] is not None:
            e["y2"] = rij_y(view[e["naar"]], e["rij"]); bezet.setdefault((e["naar"], e["z2"]), set()).add(e["y2"])
    for e in edges:
        if e["soort"] == "vert": continue
        if e["rij"] is None: e["y2"] = vrij(e["naar"], e["z2"], view[e["van"]]["top"] + view[e["van"]]["height"] / 2)
        if e["soort"] == "ver":
            boven = (view[e["van"]]["top"] - TOP) + (e["y2"] - TOP) <= (onder - view[e["van"]]["top"]) + (onder - e["y2"])
            e["boven"] = boven; doel = view[e["van"]]["top"] if boven else view[e["van"]]["top"] + view[e["van"]]["height"]
        else: doel = e["y2"]
        e["y1"] = vrij(e["van"], e["z1"], doel)
    # ---- banen in de kanalen (kanaal i = rechts van kolom i; -1 = links van kolom 0)
    banen = {}
    def baan(kanaal, sleutel):
        banen.setdefault(kanaal, []).append(sleutel)
    def kan(t, zij):
        return plek[t][0] if zij == "R" else plek[t][0] - 1
    for i, e in enumerate(edges):
        if e["soort"] in ("zij", "buur"): e["kan"] = [kan(e["van"], e["z1"])]
        elif e["soort"] == "ver": e["kan"] = [kan(e["van"], e["z1"]), kan(e["naar"], e["z2"])]
        else: e["kan"] = []
        for j, k in enumerate(e["kan"]): baan(k, (i, j))
    baan_x = {}
    for k, lst in banen.items():
        # lange verticale stukken buitenaan, korte binnenin: minder kruisingen
        def lengte(s):
            e = edges[s[0]]
            return abs(e["y1"] - e["y2"]) if e["soort"] != "ver" else 9999
        lst.sort(key=lengte)
        x0 = kol_x[k][1] if k >= 0 else kol_x[0][0] - KANAAL
        midden = x0 + KANAAL / 2
        for n, s in enumerate(lst):
            off = ((n + 1) // 2) * LANE * (1 if n % 2 else -1)
            baan_x[s] = int(midden + off)
        assert len(lst) * LANE < KANAAL - 40, "kanaal %d te smal voor %d lijnen" % (k, len(lst))
    snel = {"boven": 0, "onder": 0}
    vtel = {}
    for i, e in enumerate(edges):
        a, b = view[e["van"]], view[e["naar"]]
        zx = lambda v, z: v["left"] + v["width"] if z == "R" else v["left"]
        if e["soort"] == "vert":
            bovenste, onderste = (a, b) if a["top"] < b["top"] else (b, a)
            n = vtel.get((bovenste["_id"], onderste["_id"]), 0); vtel[(bovenste["_id"], onderste["_id"])] = n + 1
            x = a["left"] + a["width"] // 2 + n * 40
            p = [(x, a["top"] + a["height"] if a is bovenste else a["top"]), (x, b["top"] if a is bovenste else b["top"] + b["height"])]
        elif e["soort"] in ("zij", "buur"):
            bx = baan_x[(i, 0)]
            p = [(zx(a, e["z1"]), e["y1"]), (bx, e["y1"]), (bx, e["y2"]), (zx(b, e["z2"]), e["y2"])]
        else:
            w = "boven" if e["boven"] else "onder"
            hy = (TOP - 40 - LANE * snel[w]) if e["boven"] else (onder + 40 + LANE * snel[w]); snel[w] += 1
            p = [(zx(a, e["z1"]), e["y1"]), (baan_x[(i, 0)], e["y1"]), (baan_x[(i, 0)], hy), (baan_x[(i, 1)], hy), (baan_x[(i, 1)], e["y2"]), (zx(b, e["z2"]), e["y2"])]
        q = []
        for pt in p:
            pt = (int(pt[0]), int(pt[1]))
            if q and q[-1] == pt: continue
            if len(q) >= 2 and ((q[-2][0] == q[-1][0] == pt[0]) or (q[-2][1] == q[-1][1] == pt[1])): q[-1] = pt
            else: q.append(pt)
        e["p"] = q
        owner = ent[e["van"]]
        r = {"_type": "ERDRelationship", "_id": nid(), "_parent": ref(owner), "name": e["naam"], "identifying": False}
        r["end1"] = {"_type": "ERDRelationshipEnd", "_id": nid(), "_parent": ref(r), "reference": ref(ent[e["van"]]), "cardinality": e["k1"]}
        r["end2"] = {"_type": "ERDRelationshipEnd", "_id": nid(), "_parent": ref(r), "reference": ref(ent[e["naar"]]), "cardinality": e["k2"]}
        owner["ownedElements"].append(r)
        rv = {"_type": "ERDRelationshipView", "_id": nid(), "_parent": ref(dia), "model": ref(r), "subViews": [], "font": FONT,
              "head": ref(b), "tail": ref(a), "lineStyle": 0, "points": ";".join("%d:%d" % pt for pt in q)}
        mx, my = q[len(q) // 2]
        labs = []
        for alpha, dist, pos in ((1.5707963267948966, 15, 1), (0.5235987755982988, 30, 2), (-0.5235987755982988, 30, 0)):
            labs.append({"_type": "EdgeLabelView", "_id": nid(), "_parent": ref(rv), "visible": bool(e["naam"]) and pos == 1, "font": FONT, "left": mx, "top": my, "width": 0, "height": 13,
                         "alpha": alpha, "distance": dist, "hostEdge": ref(rv), "edgePosition": pos})
        labs[0]["text"] = e["naam"]
        rv["subViews"] = labs; rv["nameLabel"] = ref(labs[0]); rv["tailNameLabel"] = ref(labs[1]); rv["headNameLabel"] = ref(labs[2])
        dia["ownedViews"].append(rv)
    UIT.write_text(json.dumps(project, ensure_ascii=False, indent="\t"), encoding="utf-8")
    kwal = kwaliteit(edges, view)
    if preview: teken(preview, ent, view, edges, onder)
    return m, project, kwal

def segmenten(e):
    return [(e["p"][i], e["p"][i + 1]) for i in range(len(e["p"]) - 1)]

def kwaliteit(edges, view):
    """telt overlappende lijnstukken, kruisingen en lijnen die door een tabel lopen"""
    over = kruis = door = 0
    segs = [(i, s) for i, e in enumerate(edges) for s in segmenten(e)]
    for a in range(len(segs)):
        (i, ((x1, y1), (x2, y2))) = segs[a]
        for b in range(a + 1, len(segs)):
            (j, ((x3, y3), (x4, y4))) = segs[b]
            if i == j: continue
            h1, h2 = y1 == y2, y3 == y4
            if h1 and h2 and y1 == y3 and max(min(x1, x2), min(x3, x4)) < min(max(x1, x2), max(x3, x4)): over += 1
            elif not h1 and not h2 and x1 == x3 and max(min(y1, y2), min(y3, y4)) < min(max(y1, y2), max(y3, y4)): over += 1
            elif h1 != h2:
                (hx1, hy, hx2), (vx, vy1, vy2) = ((x1, y1, x2), (x3, y3, y4)) if h1 else ((x3, y3, x4), (x1, y1, y2))
                if min(hx1, hx2) < vx < max(hx1, hx2) and min(vy1, vy2) < hy < max(vy1, vy2): kruis += 1
    for i, e in enumerate(edges):
        for (x1, y1), (x2, y2) in segmenten(e):
            for v in view.values():
                l, t, r, b = v["left"], v["top"], v["left"] + v["width"], v["top"] + v["height"]
                if max(min(x1, x2), l) < min(max(x1, x2), r) and max(min(y1, y2), t) < min(max(y1, y2), b) or \
                   (x1 == x2 and l < x1 < r and max(min(y1, y2), t) < min(max(y1, y2), b)) or (y1 == y2 and t < y1 < b and max(min(x1, x2), l) < min(max(x1, x2), r)):
                    door += 1
    return {"overlappend": over, "kruisingen": kruis, "door_tabel": door}

def teken(pad, ent, view, edges, onder):
    from PIL import Image, ImageDraw
    W = max(v["left"] + v["width"] for v in view.values()) + 300; H = onder + 200
    im = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(im)
    for t, v in view.items():
        l, tp = v["left"], v["top"]
        d.rectangle([l, tp, l + v["width"], tp + v["height"]], outline="black", width=2, fill="#f6f6f6")
        d.rectangle([l, tp, l + v["width"], tp + 23], outline="black", width=2, fill="#d9e6f5")
        d.text((l + 8, tp + 6), t, fill="black")
        for i, c in enumerate(ent[t]["columns"]):
            flags = ",".join(x for x, on in (("PK", c["primaryKey"]), ("FK", c["foreignKey"]), ("N", c["nullable"]), ("U", c["unique"])) if on)
            d.text((l + 6, tp + 28 + 15 * i), "%-8s %s: %s" % (flags, c["name"], c["type"]), fill="#333333")
    kleuren = ["#c0392b", "#2471a3", "#1e8449", "#7d3c98", "#b9770e", "#117a65", "#566573", "#d81b60"]
    for i, e in enumerate(edges):
        d.line(e["p"], fill=kleuren[i % len(kleuren)], width=3)
        x, y = e["p"][-1]; d.ellipse([x - 5, y - 5, x + 5, y + 5], fill=kleuren[i % len(kleuren)])
    im.save(pad)

def controleer(m, project, kwal):
    ids, refs, stats = set(), [], {}
    def loop(o):
        if isinstance(o, dict):
            if "$ref" in o: refs.append(o["$ref"]); return
            if "_id" in o:
                assert o["_id"] not in ids, "dubbel id"; ids.add(o["_id"]); stats[o["_type"]] = stats.get(o["_type"], 0) + 1
            for v in o.values(): loop(v)
        elif isinstance(o, list):
            for v in o: loop(v)
    loop(json.loads(UIT.read_text(encoding="utf-8")))
    verw_kol = sum(1 + len(g.HERGEBRUIKT.get(t, [])) + len(m["tabellen"].get(t, [])) for t in m["entiteiten"])
    f = []
    if [r for r in refs if r not in ids]: f.append("verwijzing zonder doel")
    if stats.get("ERDEntity") != len(m["entiteiten"]): f.append("aantal tabellen verschilt")
    if stats.get("ERDColumn") != verw_kol: f.append("aantal kolommen verschilt (%s / %s)" % (stats.get("ERDColumn"), verw_kol))
    if stats.get("ERDRelationship") != len(m["relaties"]) + len(m["nn"]): f.append("aantal relaties verschilt")
    for a, b in (("ERDEntity", "ERDEntityView"), ("ERDColumn", "ERDColumnView"), ("ERDRelationship", "ERDRelationshipView")):
        if stats.get(a) != stats.get(b): f.append("niet elk %s heeft een view" % a)
    print("StarUML: %d tabellen, %d kolommen, %d relaties; verschillen met het datamodel: %d" % (stats["ERDEntity"], stats["ERDColumn"], stats["ERDRelationship"], len(f)))
    print("Lijnen: %(overlappend)d overlappende stukken, %(door_tabel)d door een tabel, %(kruisingen)d kruisingen" % kwal)
    for x in f: print(" -", x)
    return 1 if f else 0

if __name__ == "__main__":
    sys.exit(controleer(*bouw(sys.argv[1] if len(sys.argv) > 1 else None)))
