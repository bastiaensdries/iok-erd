"""Stap 6: leest 03_output/datamodel_v3.md en maakt daaruit
  03_output/spec.yaml, 03_output/ERD_v3.md (Mermaid) en 03_output/IOK_erd_v3.drawio,
en controleert daarna datamodel, spec en ERD op verschillen.

Gebruik:  python tools/stap6_genereer.py          (genereren + controleren)
          python tools/stap6_genereer.py --check  (enkel controleren)

Het datamodel is de bron. Wat niet in de tabellen van het datamodel staat
(weergavenamen, keuzewaarden van doelgroep/categorie, statusredenen, formules,
rechten per rol, werkwoorden op de relaties) staat hieronder in AANVULLING.
"""
import re, sys, json, html
from pathlib import Path
import xml.etree.ElementTree as ET
import yaml

ROOT = Path(__file__).resolve().parent.parent
DM = ROOT / "03_output/datamodel_v3.md"
SPEC = ROOT / "03_output/spec.yaml"
ERD = ROOT / "03_output/ERD_v3.md"
DRAWIO = ROOT / "03_output/IOK_erd_v3.drawio"

# ---------------------------------------------------------------- AANVULLING
WEERGAVE = {
    "iok_terreingroep": ("Terreingroep", "Terreingroepen"), "iok_speelterrein": ("Speelterrein", "Speelterreinen"),
    "iok_speeltoestel": ("Speeltoestel", "Speeltoestellen"), "iok_toestelcode": ("Toestelcode", "Toestelcodes"),
    "iok_toesteltype": ("Toesteltype", "Toesteltypes"), "iok_checklist": ("Checklist", "Checklists"),
    "iok_checklistonderdeel": ("Checklistonderdeel", "Checklistonderdelen"), "iok_controlepunt": ("Controlepunt", "Controlepunten"),
    "iok_standaardtekst": ("Standaardtekst", "Standaardteksten"), "iok_inspectiedossier": ("Inspectiedossier", "Inspectiedossiers"),
    "iok_beoordeling": ("Beoordeling", "Beoordelingen"), "iok_resultaat": ("Resultaat", "Resultaten"),
    "iok_maatregel": ("Maatregel", "Maatregelen"), "iok_hicmeting": ("HIC-meting", "HIC-metingen"),
    "iok_foto": ("Foto", "Foto's"), "iok_rapportversie": ("Rapportversie", "Rapportversies"), "iok_document": ("Document", "Documenten"),
}
STATUS = {  # (actief, inactief); standaard Actief / Inactief
    "iok_speeltoestel": (["In gebruik"], ["Buiten gebruik"]),
    "iok_checklist": (["Concept", "Actief"], ["Vervangen"]),
    "iok_inspectiedossier": (["Concept", "In uitvoering"], ["Afgerond", "Geannuleerd"]),
    "iok_rapportversie": (["Concept"], ["Definitief", "Verzonden", "Vervangen"]),
    "iok_document": (["Concept"], ["Definitief", "Mislukt", "Vervangen"]),
}
KEUZE_OPTIES = {  # lijsten die het datamodel enkel beschrijft
    "iok_doelgroep": ["3 jaar", "6 jaar", "9 jaar", "van 1 tot 6 jaar", "van 1 tot 14 jaar", "van 1 tot 18 jaar",
                      "van 2,5 tot 4 jaar", "van 2,5 tot 6 jaar", "van 3 tot 9 jaar", "van 6 tot 9 jaar", "van 6 tot 12 jaar",
                      "van 12 tot 14 jaar", "vanaf 6 jaar", "vanaf 9 jaar", "vanaf 12 jaar"],
    "iok_categorie": ["Zandbak", "Wip", "Schommel", "Glijbaan", "Draaitoestel", "Sporttoestel", "Combinatietoestel",
                      "Evenwichtstoestel", "Kabelbaan", "Skate", "Speelhuisje", "Andere", "Zitelementen", "Activiteitpaneel",
                      "Water", "Klimmen"],
}
HERGEBRUIKT = {  # standaardkolommen die het model gebruikt: (naam, type, sleutelcel)
    "account": [("name", "Tekst", ""), ("address1_line1", "Tekst", ""), ("address1_postalcode", "Tekst", ""),
                ("address1_city", "Tekst", ""), ("emailaddress1", "Tekst", ""), ("primarycontactid", "Lookup → contact", "")],
    "contact": [("fullname", "Tekst", ""), ("emailaddress1", "Tekst", ""), ("telephone1", "Tekst", ""),
                ("parentcustomerid", "Lookup → account", "FK")],
    "systemuser": [("fullname", "Tekst", "")],
    "sharepointdocumentlocation": [("regardingobjectid", "Lookup → iok_inspectiedossier", "FK")],
}
STD_PK = {"account": "accountid", "contact": "contactid", "systemuser": "systemuserid",
          "sharepointdocumentlocation": "sharepointdocumentlocationid"}
STD_REL = {"parentcustomerid": "contact_customer_accounts", "regardingobjectid": "iok_inspectiedossier_SharePointDocumentLocations"}
FORMAAT = {("iok_inspectiedossier", "iok_dossiernummer"): "DOS-{DATETIMEUTC:yyyy}-{SEQNUM:5}"}
FORMULE = {
    ("iok_resultaat", "iok_risicoscore"): "If(IsBlank(iok_impact) || IsBlank(iok_kans) || IsBlank(iok_blootstelling), Blank(), iok_impact * iok_kans * iok_blootstelling)",
    ("iok_resultaat", "iok_risicoklasse"): 'If(IsBlank(iok_risicoscore), Blank(), iok_risicoscore <= 20, "Licht", iok_risicoscore <= 70, "Mogelijk", iok_risicoscore <= 160, "Substantieel", iok_risicoscore <= 320, "Hoog", "Zeer hoog")',
}
ONZEKER = {
    "iok_doelgroep": "Q14 (waarden en bewoording; skate-lijst wijkt af)", "iok_bestuursoort": "Q01 (private uitbaters)",
    "iok_categorie": "Q15 (officiele lijst van types)",
    ("iok_speelterrein", "iok_eenheden"): "Q12 (telt het terrein zelf eenheden?)",
    ("iok_speelterrein", "iok_terreingroepid"): "Q20 (is een bronrij een groep van locaties?)",
    ("iok_speelterrein", "iok_uitbaterid"): "Q01",
    ("iok_speeltoestel", "iok_serienummer"): "Q19 (gebruikt IOK dit veld?)",
    ("iok_beoordeling", "iok_serienummer"): "Q19",
    ("iok_controlepunt", "iok_nokbepaalthoofdstuk"): "Q18 (zijn M en N een uitzondering?)",
    ("iok_resultaat", "iok_risicoklasse"): "Q24 (precies 70 = Mogelijk of Substantieel?)",
    ("iok_resultaat", "iok_impact"): "Q08 (gebruikt IOK de score in de praktijk?)",
    ("iok_foto", "iok_isovergenomen"): "Q02 (foto's niet verplicht, laatste foto hernemen)",
    ("iok_hicmeting", "iok_peak"): "Q03 (drempels: harde validatie of richtwaarde?)",
    "iok_toesteltype_onderdeel": "Q21 (welk type hoort bij welk Deel 2-blad?)",
    "iok_besluit": "Q26 (telt een toestel met Niet beoordeeld mee in de eenheden?)",
}
WERKWOORD = {
    ("account", "contact", "parentcustomerid"): "heeft contactpersoon", ("account", "iok_terreingroep", "iok_bestuurid"): "heeft groep",
    ("account", "iok_speelterrein", "iok_bestuurid"): "beheert", ("account", "iok_speelterrein", "iok_uitbaterid"): "baat uit",
    ("account", "iok_inspectiedossier", "iok_bestuurid"): "is bestuur in (kopie)", ("systemuser", "iok_inspectiedossier", "iok_inspecteurid"): "inspecteert",
    ("iok_terreingroep", "iok_speelterrein", "iok_terreingroepid"): "groepeert", ("iok_speelterrein", "iok_speeltoestel", "iok_speelterreinid"): "bevat",
    ("iok_speelterrein", "iok_inspectiedossier", "iok_speelterreinid"): "wordt gecontroleerd in", ("iok_toesteltype", "iok_speeltoestel", "iok_toesteltypeid"): "typeert",
    ("iok_speeltoestel", "iok_toestelcode", "iok_speeltoestelid"): "draagt", ("iok_speeltoestel", "iok_beoordeling", "iok_speeltoestelid"): "wordt beoordeeld in",
    ("iok_checklist", "iok_checklist", "iok_vorigeversieid"): "volgt op", ("iok_checklist", "iok_checklistonderdeel", "iok_checklistid"): "bestaat uit",
    ("iok_checklist", "iok_beoordeling", "iok_checklistid"): "wordt gebruikt in", ("iok_checklistonderdeel", "iok_controlepunt", "iok_onderdeelid"): "bevat",
    ("iok_controlepunt", "iok_controlepunt", "iok_ouderid"): "is ouder van", ("iok_controlepunt", "iok_controlepunt", "iok_hoofdstukid"): "is hoofdstuk van",
    ("iok_controlepunt", "iok_standaardtekst", "iok_controlepuntid"): "heeft zinnen", ("iok_controlepunt", "iok_resultaat", "iok_controlepuntid"): "wordt beantwoord in",
    ("iok_inspectiedossier", "iok_beoordeling", "iok_inspectiedossierid"): "bevat", ("iok_inspectiedossier", "iok_rapportversie", "iok_inspectiedossierid"): "heeft versie",
    ("iok_inspectiedossier", "sharepointdocumentlocation", "regardingobjectid"): "heeft archiefmap", ("iok_beoordeling", "iok_beoordeling", "iok_bronbeoordelingid"): "is bron van",
    ("iok_beoordeling", "iok_resultaat", "iok_beoordelingid"): "heeft resultaat", ("iok_beoordeling", "iok_maatregel", "iok_beoordelingid"): "leidt tot",
    ("iok_beoordeling", "iok_hicmeting", "iok_beoordelingid"): "heeft meting", ("iok_beoordeling", "iok_foto", "iok_beoordelingid"): "heeft foto",
    ("iok_resultaat", "iok_maatregel", "iok_resultaatid"): "onderbouwt", ("iok_resultaat", "iok_foto", "iok_resultaatid"): "toont gebrek van",
    ("iok_standaardtekst", "iok_resultaat", "iok_standaardtekstid"): "is herkomst van opmerking", ("iok_standaardtekst", "iok_maatregel", "iok_standaardtekstid"): "is herkomst van maatregel",
    ("iok_standaardtekst", "iok_beoordeling", "iok_besluitstandaardtekstid"): "is herkomst van besluit",
    ("iok_standaardtekst", "iok_inspectiedossier", "iok_algemeenbesluitstandaardtekstid"): "is herkomst van algemeen besluit",
    ("iok_rapportversie", "iok_document", "iok_rapportversieid"): "omvat",
    "iok_toesteltype_onderdeel": "vraagt", "iok_beoordeling_onderdeel": "gebruikt",
}
PRIV = ["maken", "lezen", "wijzigen", "verwijderen", "toevoegen", "toevoegen_aan", "toewijzen", "delen"]
def _p(**kw):
    return {k: kw.get(k, "geen") for k in PRIV}
O = "org"
ROLLEN = {  # per tabel: (inspecteur, bevoegde beheerder); niveaus org | eigen | geen
    "account": (_p(lezen=O, toevoegen_aan=O), _p(maken=O, lezen=O, wijzigen=O, toevoegen=O, toevoegen_aan=O, toewijzen=O)),
    "contact": (_p(lezen=O), _p(maken=O, lezen=O, wijzigen=O, toevoegen=O, toevoegen_aan=O, toewijzen=O)),
    "systemuser": (_p(lezen=O, toevoegen_aan=O), _p(lezen=O, toevoegen_aan=O)),
    "sharepointdocumentlocation": (_p(maken=O, lezen=O, toevoegen=O, toevoegen_aan=O), _p(lezen=O)),
}
for t in ["iok_terreingroep", "iok_speelterrein", "iok_speeltoestel", "iok_toestelcode"]:
    ROLLEN[t] = (_p(lezen=O, toevoegen_aan=O), _p(maken=O, lezen=O, wijzigen=O, toevoegen=O, toevoegen_aan=O, toewijzen=O))
for t in ["iok_toesteltype", "iok_checklist", "iok_standaardtekst"]:
    ROLLEN[t] = (_p(lezen=O, toevoegen_aan=O), _p(maken=O, lezen=O, wijzigen=O, toevoegen=O, toevoegen_aan=O))
ROLLEN["iok_checklistonderdeel"] = (_p(lezen=O, toevoegen=O, toevoegen_aan=O), _p(maken=O, lezen=O, wijzigen=O, verwijderen=O, toevoegen=O, toevoegen_aan=O))
ROLLEN["iok_controlepunt"] = (_p(lezen=O, toevoegen_aan=O), _p(maken=O, lezen=O, wijzigen=O, verwijderen=O, toevoegen=O, toevoegen_aan=O))
for t in ["iok_inspectiedossier", "iok_beoordeling"]:
    ROLLEN[t] = (_p(maken=O, lezen=O, wijzigen=O, toevoegen=O, toevoegen_aan=O, toewijzen=O), _p(lezen=O, verwijderen=O))
for t in ["iok_resultaat", "iok_maatregel", "iok_hicmeting", "iok_foto"]:
    ROLLEN[t] = (_p(maken=O, lezen=O, wijzigen=O, verwijderen="eigen", toevoegen=O, toevoegen_aan=O, toewijzen=O), _p(lezen=O, verwijderen=O))
for t in ["iok_rapportversie", "iok_document"]:
    ROLLEN[t] = (_p(maken=O, lezen=O, wijzigen=O, toevoegen=O, toevoegen_aan=O, toewijzen=O), _p(lezen=O))
ROL_ONZEKER = {"iok_speelterrein": "Q06 (mag de inspecteur terreinen en toestellen aanmaken?)", "iok_speeltoestel": "Q06", "iok_toestelcode": "Q06"}

# ---------------------------------------------------------------- datamodel lezen
def cellen(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]

def bt(s):
    return re.findall(r"`([^`]+)`", s)

def parse_type(t):
    d = {}
    if "primaire kolom" in t: d["primair"] = True
    if "**sleutel**" in t: d["sleutel"] = True
    m = re.match(r"formulekolom \((decimaal|tekst)(?:, (\d+) decimalen)?\)", t)
    if m:
        d["formule"] = True
        if m.group(1) == "decimaal": d.update(type="decimal", precisie=int(m.group(2)))
        else: d.update(type="text")
        return d
    m = re.match(r"meerregelige tekst \((\d+)\)", t)
    if m: return dict(d, type="memo", lengte=int(m.group(1)))
    m = re.match(r"tekst \((\d+)\)", t)
    if m: return dict(d, type="text", lengte=int(m.group(1)))
    m = re.match(r"URL \((\d+)\)", t)
    if m: return dict(d, type="text", lengte=int(m.group(1)), formaat="url")
    if t.startswith("geheel getal"):
        d["type"] = "int"
        m = re.search(r"standaard (\d+)", t)
        if m: d["standaard"] = int(m.group(1))
        return d
    m = re.match(r"decimaal \((\d+) decima", t)
    if m: return dict(d, type="decimal", precisie=int(m.group(1)))
    if t.startswith("datum (alleen datum)"): return dict(d, type="date", gedrag="dateonly")
    if t.startswith("datum en tijd"): return dict(d, type="datetime")
    m = re.match(r"keuze `([a-z_]+)`", t)
    if m: return dict(d, type="choice", keuzelijst=m.group(1))
    if t.startswith("ja/nee"):
        d["type"] = "bool"
        m = re.search(r"standaard (ja|nee)", t)
        if m: d["standaard"] = (m.group(1) == "ja")
        return d
    m = re.match(r"lookup → `([a-z_]+)`", t)
    if m: return dict(d, type="lookup", doel=m.group(1))
    if t.startswith("autonummer"): return dict(d, type="autonumber")
    raise ValueError("onbekend kolomtype: " + t)

def lees_datamodel():
    lines = DM.read_text(encoding="utf-8").splitlines()
    m = {"tabellen": {}, "volgorde": [], "keuzelijsten": {}, "relaties": [], "nn": [], "sleutels": [], "info": {}}
    sec, tab, groep, intabel = None, None, None, False
    for ln in lines:
        h = re.match(r"^## (\d+)\.", ln)
        if h: sec, tab = int(h.group(1)), None; continue
        h = re.match(r"^### \d+\.\d+ `([a-z_]+)`", ln)
        if h:
            tab = h.group(1); m["tabellen"].setdefault(tab, []); intabel = False; continue
        if not ln.startswith("|"):
            intabel = False; continue
        c = cellen(ln)
        if set(ln.strip()) <= set("|-: "): continue
        if sec == 1 and len(c) == 5 and c[1].startswith("`"):
            if c[0]: groep = c[0]
            m["info"][bt(c[1])[0]] = {"groep": groep, "soort": c[2], "eigenaarschap": c[3]}
            m["volgorde"].append(bt(c[1])[0])
        elif sec == 3 and c[0].startswith("`"):
            m["keuzelijsten"][bt(c[0])[0]] = c[1]
        elif sec == 8 and len(c) == 5 and c[0].startswith("`"):
            if "↔" in c[0]:
                a, b = bt(c[0]); m["nn"].append({"schema": bt(c[2])[0], "tabellen": [a, b]})
            else:
                m["relaties"].append({"van": bt(c[0])[0], "naar": bt(c[1])[0], "lookup": bt(c[2])[0], "vo": c[3], "gedrag": c[4].replace("*", "")})
        elif sec == 9 and len(c) == 3 and c[0].startswith("`"):
            m["sleutels"].append({"tabel": bt(c[0])[0], "kolommen": bt(c[1])})
        elif tab and sec in (4, 5, 6, 7):
            if c[0] in ("Kolom", "Eigen kolom"): intabel = True; continue
            if intabel and c[0].startswith("`"):
                namen = bt(c[0])
                assert len(namen) == 1, ("meer dan een kolom per rij", ln)
                k = parse_type(c[1]); k["schema"] = namen[0]; k["verplicht"] = (c[2] == "V"); k["kopie"] = "**kopie**" in c[3]
                m["tabellen"][tab].append(k)
    return m

def kort(n):
    return n[4:] if n.startswith("iok_") else n

def rel_schema(r):
    if r["lookup"] in STD_REL: return STD_REL[r["lookup"]]
    return "iok_%s_%s_%s" % (kort(r["van"]), kort(r["naar"]), kort(r["lookup"]))

GEDRAG = {"beperken": "restrict", "koppeling verwijderen": "removelink", "parental": "cascade", "standaard": "standaard"}

def model():
    m = lees_datamodel()
    nn_namen = {n["schema"] for n in m["nn"]}
    m["entiteiten"] = [t for t in m["volgorde"] if t not in nn_namen]
    for r in m["relaties"]:
        r["schema"] = rel_schema(r); r["verwijderen"] = GEDRAG[r["gedrag"]]
    for s in m["sleutels"]:
        s["schema"] = "iok_ak_%s_%s" % (kort(s["tabel"]), "_".join(kort(k) for k in s["kolommen"]))
    return m

# ---------------------------------------------------------------- spec.yaml
def q(v):
    if isinstance(v, bool): return "true" if v else "false"
    if isinstance(v, int): return str(v)
    if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", v) and v not in ("true", "false", "null", "yes", "no", "ja", "nee"): return v
    return json.dumps(v, ensure_ascii=False)

def flow(d):
    return "{ " + ", ".join("%s: %s" % (k, q(v) if not isinstance(v, list) else "[" + ", ".join(q(x) for x in v) + "]") for k, v in d.items()) + " }"

def schrijf_spec(m):
    o = ["# Specificatie IOK-datamodel v3 - GEGENEREERD uit 03_output/datamodel_v3.md",
         "# door tools/stap6_genereer.py. Niet met de hand wijzigen: pas het datamodel aan en genereer opnieuw.",
         "# Weergavenamen, keuzewaarden van doelgroep/categorie, statusredenen, formules en rollen",
         "# staan in het script (AANVULLING). Er is niets gebouwd in Dataverse.",
         "# Beslissingen: BESLISSINGEN.md (B01-B84). # ONZEKER: = hangt af van een open vraag (02_werk/open_vragen.md).",
         "publisher: { prefix: iok, naam: IOK }",
         "solution: { naam: IOK_Speelterreinen, versie: 1.0.0 }",
         "globale_keuzelijsten:"]
    for naam, waarden in m["keuzelijsten"].items():
        opties = KEUZE_OPTIES.get(naam) or [w.strip() for w in waarden.split("·")]
        o.append("  - schema: %s%s" % (naam, "   # ONZEKER: " + ONZEKER[naam] if naam in ONZEKER else ""))
        o.append("    opties:")
        for i, lab in enumerate(opties):
            o.append("      - " + flow({"label": lab, "waarde": 100000000 + i}))
    o.append("tabellen:")
    for t in m["entiteiten"]:
        info, kol = m["info"][t], m["tabellen"].get(t, [])
        std = info["soort"] == "standaard"
        o.append("  - schema: %s" % t)
        o.append("    bestaand: %s" % q(std))
        if std:
            o.append("    hergebruikt: [%s]   # standaardkolommen die het model gebruikt" % ", ".join(h[0] for h in HERGEBRUIKT[t]))
        else:
            e, mv = WEERGAVE[t]
            o.append("    weergavenaam: " + flow({"enkelvoud": e, "meervoud": mv}))
            o.append("    eigenaarschap: %s            # niet meer te wijzigen" % ("organization" if info["eigenaarschap"] == "organisatie" else "user"))
            pk = [k for k in kol if k.get("primair")][0]
            d = {"schema": pk["schema"]}
            if pk["type"] == "autonumber": d.update(type="autonumber", formaat=FORMAAT[(t, pk["schema"])])
            else: d["lengte"] = pk["lengte"]
            o.append("    primaire_kolom: " + flow(d))
            o.append("    notities: false                # niet meer uit te zetten")
            o.append("    activiteiten: false")
            if t == "iok_inspectiedossier": o.append("    documentbeheer: true           # SharePoint-map per dossier (B60)")
            a, i = STATUS.get(t, (["Actief"], ["Inactief"]))
            o.append("    statusredenen: { actief: [%s], inactief: [%s] }" % (", ".join(q(x) for x in a), ", ".join(q(x) for x in i)))
        rest = [k for k in kol if not k.get("primair")]
        o.append("    kolommen:" + (" []" if not rest else ""))
        for k in rest:
            d = {"schema": k["schema"], "type": k["type"]}
            for key in ("lengte", "precisie", "formaat", "gedrag", "keuzelijst", "doel"):
                if key in k: d[key] = k[key]
            if k.get("formule"): d["formule"] = FORMULE[(t, k["schema"])]
            else: d["verplicht"] = k["verplicht"]
            if "standaard" in k: d["standaard"] = k["standaard"]
            if k.get("kopie"): d["kopie"] = True
            oz = ONZEKER.get((t, k["schema"]))
            o.append("      - " + flow(d) + ("   # ONZEKER: " + oz if oz else ""))
        sl = [s for s in m["sleutels"] if s["tabel"] == t]
        if sl:
            o.append("    alternatieve_sleutels:")
            for s in sl: o.append("      - " + flow({"schema": s["schema"], "kolommen": s["kolommen"]}))
    o.append("relaties:")
    for r in m["relaties"]:
        d = {"schema": r["schema"], "type": "1N", "van": r["van"], "naar": r["naar"], "lookup": r["lookup"]}
        if r["lookup"] in STD_REL: d["bestaand"] = True
        else: d.update(verplicht=(r["vo"] == "V"), verwijderen=r["verwijderen"])
        o.append("  - " + flow(d))
    for n in m["nn"]:
        oz = ONZEKER.get(n["schema"])
        o.append("  - " + flow({"schema": n["schema"], "type": "NN", "tabellen": n["tabellen"]}) + ("   # ONZEKER: " + oz if oz else ""))
    o.append("rollen:   # niveaus: org | eigen | geen. De voorwaarden (dossier actief, checklist in Concept) dwingt een synchrone controle af, niet de rol (B74, B75, B77).")
    for idx, rol in enumerate(["Inspecteur", "Bevoegde beheerder"]):
        o.append("  - naam: %s" % q(rol))
        o.append("    rechten:")
        for t in m["entiteiten"]:
            oz = ROL_ONZEKER.get(t) if idx == 0 else None
            o.append("      - " + flow(dict({"tabel": t}, **ROLLEN[t][idx])) + ("   # ONZEKER: " + oz if oz else ""))
    SPEC.write_text("\n".join(o) + "\n", encoding="utf-8")
    # zelfde inhoud als JSON, zodat de dv_-scripts zonder PyYAML werken
    SPEC.with_suffix(".json").write_text(json.dumps(yaml.safe_load(SPEC.read_text(encoding="utf-8")), ensure_ascii=False, indent=1), encoding="utf-8")

# ---------------------------------------------------------------- Mermaid
MTYPE = {"text": "string", "memo": "string", "int": "int", "decimal": "decimal", "date": "date", "datetime": "datetime",
         "choice": "choice", "bool": "bool", "lookup": "lookup", "autonumber": "string"}

def pk_naam(t):
    return STD_PK.get(t, t + "id")

def rel_regel(r):
    return '    %s %s %s : "%s"' % (r["van"], "||--o{" if r["vo"] == "V" else "|o--o{", r["naar"], WERKWOORD.get((r["van"], r["naar"], r["lookup"]), "heeft"))

def nn_regel(n):
    return '    %s }o--o{ %s : "%s"' % (n["tabellen"][0], n["tabellen"][1], WERKWOORD.get(n["schema"], "heeft"))

def entiteit_blok(m, t):
    uk = {k for s in m["sleutels"] if s["tabel"] == t for k in s["kolommen"]}
    o = ["    %s {" % t, "        guid %s PK" % pk_naam(t)]
    if t in HERGEBRUIKT:
        for naam, typ, key in HERGEBRUIKT[t]:
            o.append("        %s %s%s" % ("lookup" if typ.startswith("Lookup") else "string", naam, " FK" if key else ""))
    for k in m["tabellen"].get(t, []):
        keys = [x for x, c in (("FK", k["type"] == "lookup"), ("UK", k["schema"] in uk)) if c]
        if keys or k.get("primair") or t in HERGEBRUIKT:
            o.append("        %s %s%s%s" % (MTYPE[k["type"]], k["schema"], " " + ", ".join(keys) if keys else "", ' "primaire kolom"' if k.get("primair") else ""))
    o.append("    }")
    return o

def schrijf_erd(m):
    groepen = ["Stamgegevens", "Sjablonen", "Inspectie", "Communicatie"]
    ent = m["entiteiten"]
    o = ["# ERD datamodel v3 – IOK", "",
         "_Gegenereerd uit `03_output/datamodel_v3.md` door `tools/stap6_genereer.py` (stap 6). Niet met de hand wijzigen._", "",
         "%d tabellen (%d standaard, %d eigen), %d relaties 1:N en %d native N:N. Volledige kolomlijsten staan in `datamodel_v3.md`; de diagrammen tonen de sleutel (PK), alternatieve sleutels (UK), lookups (FK) en de primaire kolom. Hetzelfde model met alle kolommen: `IOK_erd_v3.drawio`."
         % (len(ent), sum(1 for t in ent if m["info"][t]["soort"] == "standaard"), sum(1 for t in ent if m["info"][t]["soort"] == "eigen"), len(m["relaties"]), len(m["nn"])), "",
         "Notatie: `||--o{` = verplichte lookup (1 : 0..N), `|o--o{` = optionele lookup (0..1 : 0..N), `}o--o{` = native N:N. Bekijken: VS Code (Markdown Preview Mermaid Support) of mermaid.live.", "",
         "## 1. Overzicht (alle tabellen en relaties)", "", "```mermaid", "erDiagram"]
    for g in groepen + ["Platform"]:
        o.append("    %% " + g)
        for r in m["relaties"]:
            if m["info"][r["naar"]]["groep"] == g: o.append(rel_regel(r))
        for n in m["nn"]:
            if m["info"][n["tabellen"][0]]["groep"] == g: o.append(nn_regel(n))
    o += ["```", ""]
    for i, g in enumerate(groepen, 2):
        leden = [t for t in ent if m["info"][t]["groep"] == g]
        o += ["## %d. %s" % (i, g), "", "Tabellen van deze groep met hun sleutels en lookups; tabellen uit andere groepen staan er enkel als naam bij.", "", "```mermaid", "erDiagram", "    %% " + g]
        for r in m["relaties"]:
            if r["van"] in leden or r["naar"] in leden: o.append(rel_regel(r))
        for n in m["nn"]:
            if set(n["tabellen"]) & set(leden): o.append(nn_regel(n))
        for t in leden: o += entiteit_blok(m, t)
        o += ["```", ""]
    o += ["## 6. Platform", "", "`systemuser` en `sharepointdocumentlocation` zijn standaardtabellen zonder eigen kolommen; ze staan in het overzicht en in de groepen Inspectie en Communicatie.", ""]
    ERD.write_text("\n".join(o), encoding="utf-8")

# ---------------------------------------------------------------- draw.io (stijl van IOK_erd_v2.drawio)
S_TABLE = "shape=table;startSize=30;container=1;collapsible=1;childLayout=tableLayout;fixedRows=1;rowLines=0;fontStyle=1;align=center;resizeLast=1;html=1;"
S_ROW = "shape=tableRow;horizontal=0;startSize=0;swimlaneHead=0;swimlaneBody=0;fillColor=none;collapsible=0;dropTarget=0;points=[[0,0.5],[1,0.5]];portConstraint=eastwest;top=0;left=0;right=0;bottom=%d;"
S_KEY = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;fontStyle=%d;overflow=hidden;whiteSpace=wrap;html=1;"
S_VAL = "shape=partialRectangle;connectable=0;fillColor=none;top=0;left=0;bottom=0;right=0;align=left;spacingLeft=6;fontStyle=%d;overflow=hidden;whiteSpace=wrap;html=1;"
S_EDGE = "edgeStyle=entityRelationEdgeStyle;rounded=0;html=1;startArrow=%s;endArrow=%s;startFill=0;endFill=0;startSize=10;endSize=10;fontSize=10;labelBackgroundColor=default;"
S_SELF = "edgeStyle=orthogonalEdgeStyle;rounded=0;html=1;startArrow=%s;endArrow=%s;startFill=0;endFill=0;startSize=10;endSize=10;fontSize=10;labelBackgroundColor=default;exitX=1;exitY=0.5;entryX=1;entryY=0.5;"
KOLOMMEN_LAYOUT = [["account", "contact", "systemuser", "sharepointdocumentlocation"],
                   ["iok_terreingroep", "iok_speelterrein", "iok_speeltoestel", "iok_toestelcode", "iok_toesteltype"],
                   ["iok_checklist", "iok_checklistonderdeel", "iok_controlepunt", "iok_standaardtekst"],
                   ["iok_inspectiedossier", "iok_rapportversie", "iok_document"],
                   ["iok_beoordeling"],
                   ["iok_resultaat", "iok_maatregel", "iok_hicmeting", "iok_foto"]]
W, KW, RH = 400, 60, 30

def dtype(k):
    t = k["type"]
    s = {"text": "Tekst(%s)" % k.get("lengte"), "memo": "Tekst lang(%s)" % k.get("lengte"), "int": "Geheel getal", "decimal": "Decimaal(%s)" % k.get("precisie"),
         "date": "Datum", "datetime": "Datum/tijd", "choice": "Keuze(%s)" % k.get("keuzelijst"), "bool": "Ja/Nee",
         "lookup": "Lookup → %s" % k.get("doel"), "autonumber": "Autonummer"}[t]
    if k.get("formaat") == "url": s = "URL(%s)" % k["lengte"]
    if k.get("formule"): s = "Formule(%s)" % ("decimaal" if t == "decimal" else "tekst")
    return s + (" {V}" if k.get("verplicht") else "") + (" (kopie)" if k.get("kopie") else "")

def tabel_rijen(m, t):
    """[(sleutelcel, tekst, kolomnaam)] - eerste rij is de PK."""
    uk = {k for s in m["sleutels"] if s["tabel"] == t for k in s["kolommen"]}
    rijen = [("PK", "%s: GUID {V}" % pk_naam(t), pk_naam(t))]
    for naam, typ, key in HERGEBRUIKT.get(t, []):
        rijen.append((key, "%s: %s (standaard)" % (naam, typ), naam))
    for k in m["tabellen"].get(t, []):
        keys = [x for x, c in (("FK", k["type"] == "lookup"), ("UK", k["schema"] in uk)) if c]
        rijen.append((",".join(keys), "%s: %s" % (k["schema"], dtype(k)) + (" · primaire kolom" if k.get("primair") else ""), k["schema"]))
    return rijen

def schrijf_drawio(m):
    x = lambda s: html.escape(s, quote=True)
    c = []
    geplaatst = [t for kol in KOLOMMEN_LAYOUT for t in kol]
    assert sorted(geplaatst) == sorted(m["entiteiten"]), "layout mist tabellen"
    for ci, kol in enumerate(KOLOMMEN_LAYOUT):
        y = 80
        for t in kol:
            rijen = tabel_rijen(m, t)
            h = RH * (len(rijen) + 1)
            c.append('<mxCell id="t_%s" parent="1" style="%s" value="%s" vertex="1"><mxGeometry height="%d" width="%d" x="%d" y="%d" as="geometry" /></mxCell>' % (t, S_TABLE, x(t), h, W, 40 + ci * (W + 160), y))
            for ri, (key, tekst, naam) in enumerate(rijen):
                rid = "r_%s_%s" % (t, naam)
                pk = ri == 0
                c.append('<mxCell id="%s" parent="t_%s" style="%s" value="" vertex="1"><mxGeometry height="%d" width="%d" y="%d" as="geometry" /></mxCell>' % (rid, t, S_ROW % (1 if pk else 0), RH, W, RH * (ri + 1)))
                c.append('<mxCell id="%s_k" parent="%s" style="%s" value="%s" vertex="1"><mxGeometry height="%d" width="%d" as="geometry"><mxRectangle height="%d" width="%d" as="alternateBounds" /></mxGeometry></mxCell>' % (rid, rid, S_KEY % (1 if pk else 0), x(key), RH, KW, RH, KW))
                c.append('<mxCell id="%s_v" parent="%s" style="%s" value="%s" vertex="1"><mxGeometry height="%d" width="%d" x="%d" as="geometry"><mxRectangle height="%d" width="%d" as="alternateBounds" /></mxGeometry></mxCell>' % (rid, rid, S_VAL % (5 if pk else 0), x(tekst), RH, W - KW, KW, RH, W - KW))
            y += h + 70
    for i, r in enumerate(m["relaties"]):
        start = "ERmandOne" if r["vo"] == "V" else "ERzeroToOne"
        st = (S_SELF if r["van"] == r["naar"] else S_EDGE) % (start, "ERzeroToMany")
        lab = ("1" if r["vo"] == "V" else "0..1") + " : 0..M"
        c.append('<mxCell id="e_%d" edge="1" parent="1" source="r_%s_%s" style="%s" target="r_%s_%s" value="%s"><mxGeometry relative="1" as="geometry" /></mxCell>' % (i, r["van"], pk_naam(r["van"]), st, r["naar"], r["lookup"], x(lab)))
    for i, n in enumerate(m["nn"]):
        a, b = n["tabellen"]
        c.append('<mxCell id="n_%d" edge="1" parent="1" source="r_%s_%s" style="%s" target="r_%s_%s" value="%s"><mxGeometry relative="1" as="geometry" /></mxCell>' % (i, a, pk_naam(a), S_EDGE % ("ERzeroToMany", "ERzeroToMany"), b, pk_naam(b), x("N : M · %s" % n["schema"])))
    c.append('<mxCell id="legende" parent="1" style="text;html=1;align=left;verticalAlign=top;whiteSpace=wrap;fontSize=12;" value="%s" vertex="1"><mxGeometry height="50" width="1400" x="40" y="10" as="geometry" /></mxCell>' % x("<b>IOK datamodel v3 (Dataverse)</b> – gegenereerd uit datamodel_v3.md. PK = GUID-sleutel · UK = alternatieve sleutel · FK = lookup · {V} = verplicht · (kopie) = bevroren kopiekolom (B57) · (standaard) = bestaande kolom van een standaardtabel. Lijnen met N : M zijn native N:N-koppelingen."))
    out = ('<mxfile host="app.diagrams.net">\n  <diagram id="erd3" name="ERD IOK v3">\n    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="3400" pageHeight="2400" math="0" shadow="0">\n      <root>\n        <mxCell id="0" />\n        <mxCell id="1" parent="0" />\n        '
           + "\n        ".join(c) + "\n      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n")
    DRAWIO.write_text(out, encoding="utf-8")

# ---------------------------------------------------------------- controle
def controleer(m):
    f = []
    ent, tab = set(m["entiteiten"]), m["tabellen"]
    # A. datamodel intern
    if set(tab) - {t for t in tab if not tab[t]} - ent: f.append("A1 tabel met kolommen ontbreekt in §1: %s" % (set(tab) - ent))
    for t in ent:
        if m["info"][t]["soort"] == "eigen" and not tab.get(t): f.append("A1 eigen tabel zonder kolomtabel: " + t)
    rel = {(r["van"], r["naar"], r["lookup"]): r for r in m["relaties"]}
    if len(rel) != len(m["relaties"]): f.append("A2 dubbele relatie in §8")
    for t in ent:
        namen = [k["schema"] for k in tab.get(t, [])]
        if len(namen) != len(set(namen)): f.append("A3 dubbele kolomnaam in " + t)
        for k in tab.get(t, []):
            if not k["schema"].startswith("iok_"): f.append("A4 kolom zonder iok_: %s.%s" % (t, k["schema"]))
            if k["type"] == "lookup":
                r = rel.get((k["doel"], t, k["schema"]))
                if not r: f.append("A5 lookup zonder relatie in §8: %s.%s → %s" % (t, k["schema"], k["doel"]))
                elif (r["vo"] == "V") != k["verplicht"]: f.append("A6 V/O verschilt tussen kolom en §8: %s.%s" % (t, k["schema"]))
            if k["type"] == "choice" and k["keuzelijst"] not in m["keuzelijsten"]: f.append("A7 keuzelijst ontbreekt in §3: " + k["keuzelijst"])
        if m["info"][t]["soort"] == "eigen" and sum(1 for k in tab[t] if k.get("primair")) != 1: f.append("A8 niet precies een primaire kolom: " + t)
    for r in m["relaties"]:
        for t in (r["van"], r["naar"]):
            if t not in ent: f.append("A9 relatie naar onbekende tabel: " + t)
        if r["lookup"] not in STD_REL and r["lookup"] not in [k["schema"] for k in tab.get(r["naar"], []) if k["type"] == "lookup" and k["doel"] == r["van"]]:
            f.append("A10 relatie zonder lookupkolom: %s → %s (%s)" % (r["van"], r["naar"], r["lookup"]))
    gebruikt = {k["keuzelijst"] for t in ent for k in tab.get(t, []) if k["type"] == "choice"}
    for kl in m["keuzelijsten"]:
        if kl not in gebruikt: f.append("A11 keuzelijst niet gebruikt: " + kl)
    for t in ent:
        par = [r for r in m["relaties"] if r["naar"] == t and r["gedrag"] == "parental"]
        if len(par) > 1: f.append("A12 meer dan een parental-relatie: " + t)
    enkel = {(s["tabel"], s["kolommen"][0]) for s in m["sleutels"] if len(s["kolommen"]) == 1}
    for s in m["sleutels"]:
        for k in s["kolommen"]:
            if k not in [c["schema"] for c in tab.get(s["tabel"], [])]: f.append("A13 sleutelkolom bestaat niet: %s.%s" % (s["tabel"], k))
    for t in ent:
        for k in tab.get(t, []):
            if k.get("sleutel") != ((t, k["schema"]) in enkel or None) and (k.get("sleutel") or (t, k["schema"]) in enkel):
                f.append("A14 '**sleutel**' in de kolomtabel en §9 verschillen: %s.%s" % (t, k["schema"]))
    alle = [t for t in ent] + [n["schema"] for n in m["nn"]] + [r["schema"] for r in m["relaties"]] + [s["schema"] for s in m["sleutels"]] + list(m["keuzelijsten"])
    if len(alle) != len(set(alle)): f.append("A15 dubbele schemanaam: %s" % sorted({a for a in alle if alle.count(a) > 1}))
    for t, (a, i) in STATUS.items():
        tekst = DM.read_text(encoding="utf-8")
        for lab in a + i:
            if "**%s**" % lab not in tekst: f.append("A16 statusreden niet in het datamodel: %s.%s" % (t, lab))
    # B. spec.yaml
    s = yaml.safe_load(SPEC.read_text(encoding="utf-8"))
    st = {t["schema"]: t for t in s["tabellen"]}
    if set(st) != ent: f.append("B1 tabellen verschillen: enkel datamodel %s, enkel spec %s" % (sorted(ent - set(st)), sorted(set(st) - ent)))
    for t in ent & set(st):
        dm = {k["schema"]: k for k in tab.get(t, [])}
        sp = {k["schema"]: k for k in st[t]["kolommen"]}
        if "primaire_kolom" in st[t]: sp[st[t]["primaire_kolom"]["schema"]] = dict(st[t]["primaire_kolom"], primair=True)
        if set(dm) != set(sp): f.append("B2 kolommen verschillen in %s: enkel datamodel %s, enkel spec %s" % (t, sorted(set(dm) - set(sp)), sorted(set(sp) - set(dm))))
        for n in set(dm) & set(sp):
            a, b = dm[n], sp[n]
            if b.get("primair"):
                if a["type"] != b.get("type", "text") or a.get("lengte") != b.get("lengte"): f.append("B3 primaire kolom verschilt: %s.%s" % (t, n))
                continue
            for key in ("type", "lengte", "precisie", "keuzelijst", "doel"):
                if a.get(key) != b.get(key): f.append("B3 %s verschilt: %s.%s (%s / %s)" % (key, t, n, a.get(key), b.get(key)))
            if not a.get("formule") and a["verplicht"] != b.get("verplicht"): f.append("B4 verplicht verschilt: %s.%s" % (t, n))
        sk = {tuple(x["kolommen"]) for x in st[t].get("alternatieve_sleutels", [])}
        dk = {tuple(x["kolommen"]) for x in m["sleutels"] if x["tabel"] == t}
        if sk != dk: f.append("B5 sleutels verschillen in " + t)
    sr = {(r["van"], r["naar"], r["lookup"]) for r in s["relaties"] if r["type"] == "1N"}
    if sr != set(rel): f.append("B6 relaties verschillen: %s" % sorted(sr ^ set(rel)))
    snn = {(r["schema"], tuple(r["tabellen"])) for r in s["relaties"] if r["type"] == "NN"}
    if snn != {(n["schema"], tuple(n["tabellen"])) for n in m["nn"]}: f.append("B7 N:N verschilt")
    if set(x["schema"] for x in s["globale_keuzelijsten"]) != set(m["keuzelijsten"]): f.append("B8 keuzelijsten verschillen")
    for x in s["globale_keuzelijsten"]:
        w = [o["waarde"] for o in x["opties"]]
        if w != list(range(100000000, 100000000 + len(w))): f.append("B9 keuzewaarden niet doorlopend: " + x["schema"])
        if x["schema"] not in KEUZE_OPTIES and [o["label"] for o in x["opties"]] != [v.strip() for v in m["keuzelijsten"][x["schema"]].split("·")]: f.append("B10 opties verschillen: " + x["schema"])
    for rol in s["rollen"]:
        if {r["tabel"] for r in rol["rechten"]} != ent: f.append("B11 rol dekt niet alle tabellen: " + rol["naam"])
    # C. Mermaid
    txt = ERD.read_text(encoding="utf-8")
    blokken = re.findall(r"```mermaid\n(.*?)```", txt, flags=re.S)
    pat = re.compile(r'^\s*(\w+) (\|\|--o\{|\|o--o\{|\}o--o\{) (\w+) : "(.*)"\s*$', re.M)
    ov = pat.findall(blokken[0])
    verwacht = sorted([(r["van"], "||--o{" if r["vo"] == "V" else "|o--o{", r["naar"], WERKWOORD.get((r["van"], r["naar"], r["lookup"]), "heeft")) for r in m["relaties"]]
                      + [(n["tabellen"][0], "}o--o{", n["tabellen"][1], WERKWOORD.get(n["schema"], "heeft")) for n in m["nn"]])
    if sorted(ov) != verwacht: f.append("C1 relaties in het overzichtsdiagram verschillen (%d / %d)" % (len(ov), len(verwacht)))
    if {a for a, _, b, _ in ov} | {b for a, _, b, _ in ov} != ent: f.append("C2 tabellen in het overzichtsdiagram verschillen")
    if len(set(verwacht)) != len(verwacht): f.append("C3 twee relaties met hetzelfde label tussen dezelfde tabellen")
    blokt = {}
    for b in blokken[1:]:
        for naam, body in re.findall(r"^    (\w+) \{\n(.*?)^    \}", b, flags=re.S | re.M):
            blokt[naam] = [l.split()[1] for l in body.strip().splitlines()]
    eigen = {t for t in ent if m["info"][t]["groep"] != "Platform"}
    if set(blokt) != eigen: f.append("C4 tabelblokken in de deeldiagrammen verschillen: %s" % sorted(set(blokt) ^ eigen))
    for t in set(blokt) & eigen:
        fk = {k["schema"] for k in tab.get(t, []) if k["type"] == "lookup"}
        if not fk <= set(blokt[t]): f.append("C5 lookup ontbreekt in het diagram: %s %s" % (t, sorted(fk - set(blokt[t]))))
    # D. draw.io
    root = ET.parse(DRAWIO).getroot()
    cells = {c.get("id"): c for c in root.iter("mxCell")}
    dt = {c.get("value"): cid for cid, c in cells.items() if "shape=table;" in (c.get("style") or "")}
    if set(dt) != ent: f.append("D1 tabellen in draw.io verschillen: %s" % sorted(set(dt) ^ ent))
    for t in set(dt) & ent:
        rows = [cid for cid, c in cells.items() if c.get("parent") == dt[t]]
        namen = {html.unescape(cells[r + "_v"].get("value")).split(":")[0] for r in rows}
        verw = {pk_naam(t)} | {h[0] for h in HERGEBRUIKT.get(t, [])} | {k["schema"] for k in tab.get(t, [])}
        if namen != verw: f.append("D2 kolommen in draw.io verschillen voor %s: %s" % (t, sorted(namen ^ verw)))
    edges = [c for c in cells.values() if c.get("edge") == "1"]
    for e in edges:
        if e.get("source") not in cells or e.get("target") not in cells: f.append("D3 lijn zonder begin of einde: " + e.get("id"))
    def _rel(e):
        van, naar = cells[e.get("source")].get("parent")[2:], cells[e.get("target")].get("parent")[2:]
        return (van, naar, e.get("target")[len("r_" + naar + "_"):])
    de = sorted(_rel(e) for e in edges if e.get("id").startswith("e_"))
    if de != sorted(rel): f.append("D4 relaties in draw.io verschillen (%d / %d)" % (len(de), len(rel)))
    if len([e for e in edges if e.get("id").startswith("n_")]) != len(m["nn"]): f.append("D5 N:N in draw.io verschilt")
    return f, s

def main():
    m = model()
    if "--check" not in sys.argv:
        schrijf_spec(m); schrijf_erd(m); schrijf_drawio(m)
    f, s = controleer(m)
    ent = m["entiteiten"]
    print("Datamodel: %d tabellen (%d standaard, %d eigen) + %d N:N, %d kolommen in de kolomtabellen, %d relaties 1:N, %d alternatieve sleutels, %d keuzelijsten"
          % (len(ent), sum(1 for t in ent if m["info"][t]["soort"] == "standaard"), sum(1 for t in ent if m["info"][t]["soort"] == "eigen"), len(m["nn"]),
             sum(len(v) for v in m["tabellen"].values()), len(m["relaties"]), len(m["sleutels"]), len(m["keuzelijsten"])))
    print("spec.yaml: %d tabellen, %d kolommen (+ primaire kolommen), %d relaties" % (len(s["tabellen"]), sum(len(t["kolommen"]) for t in s["tabellen"]), len(s["relaties"])))
    print("Verschillen: %d" % len(f))
    for x in f: print(" -", x)
    return 1 if f else 0

if __name__ == "__main__":
    sys.exit(main())
