"""Maakt de laad-CSV's in 04_data/ uit de bronnen in 01_context/ (proof of concept: Geel).

Gebruik:  python tools/csv_maken.py
Er wordt niets verzonnen: wat niet in een bron staat, blijft leeg. Afleidingen (bv. welk
toesteltype bij een toestel hoort) staan in de kolom _opmerking en in 04_data/LEESMIJ.md.
Kolommen die met _ beginnen worden niet geladen; _sleutel is de unieke naam van de rij
waarmee andere bestanden naar die rij verwijzen (in de lookup-kolommen).
"""
import csv, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "01_context/docs"
UIT = ROOT / "04_data"
GEMEENTE = "Geel"
meldingen = []

def rijen(bestand, blad):
    """[(rijnummer, {kolom: waarde})] van een blad uit een bron-markdown."""
    uit, actief = [], False
    for ln in (DOCS / bestand).read_text(encoding="utf-8").splitlines():
        if ln.startswith("## Blad:"):
            actief = ln[8:].strip().lower() == blad.strip().lower(); continue
        m = re.match(r"- r(\d+) \| (.*)", ln)
        if actief and m:
            cel = {}
            for deel in re.split(r" \| (?=[A-Z]{1,2}: )", m.group(2)):
                k, _, v = deel.partition(": ")
                cel[k] = v.strip()
            uit.append((int(m.group(1)), cel))
    if not uit: raise SystemExit("blad niet gevonden: %s / %s" % (bestand, blad))
    return uit

def schrijf(naam, kolommen, data):
    with open(UIT / naam, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=kolommen, extrasaction="raise")
        w.writeheader()
        for r in data: w.writerow({k: r.get(k, "") for k in kolommen})
    return len(data)

# ---------------------------------------------------------------- checklists
CODE = r"(?:[A-Z]|\d+)(?:\.\d+)+"

def lees_onderdeel(bestand, blad):
    items, laatste_a, sub = [], None, []
    for nr, cel in rijen(bestand, blad):
        cel = {k: v for k, v in cel.items() if k != "G"}          # G = Status-kolom, geen inhoud
        a, b = cel.get("A", ""), cel.get("B", "")
        if b.rstrip(" :").lower() == "opmerkingen" or a.rstrip(" :").lower() == "opmerkingen": continue
        if a:
            if re.match(r"^[A-Z]\. \d", a):                         # "H. 1 Algemeen" -> "H.1 Algemeen"
                meldingen.append("%s / %s r%d: code '%s' genormaliseerd naar '%s'" % (bestand, blad, nr, a[:4], a[:2] + a[3:4]))
                a = a[:2] + a[3:]
            m1 = re.match(r"^([A-Z]|\d+)\s*[.,]\s*(\S.*)$", a)
            m2 = re.match(r"^(%s)\.?\s*(.*)$" % CODE, a)
            if m2:
                rest = m2.group(2).rstrip(" :").strip()
                tekst = b if b else rest
                it = {"code": m2.group(1), "tekst": tekst, "toel": [], "rij": nr}
                extra = [v for k, v in sorted(cel.items()) if k not in ("A", "B")]
                if b and rest: it["toel"].append(rest)
                it["toel"] += extra
            elif m1:
                it = {"code": m1.group(1), "tekst": m1.group(2).rstrip(" :").strip(), "toel": [v for k, v in sorted(cel.items()) if k != "A"], "rij": nr}
            else:
                continue                                            # kopregels van het blad
            items.append(it); laatste_a = it
        elif items:
            tekst = " ".join(v for k, v in sorted(cel.items()) if v)
            ms = re.match(r"^(%s)\s+(.+)$" % CODE, b)
            if ms and ms.group(1).count(".") >= 2:
                sub.append((laatste_a, ms.group(1), ms.group(2), nr, tekst))
            elif tekst:
                items[-1]["toel"].append(tekst)
    # subregels met een eigen code (4 niveaus, velddekking §14) worden een eigen controlepunt
    for ouder, code, tekst, nr, vol in sub:
        aantal = sum(1 for o, c, *_ in sub if o is ouder and c == code)
        goed = code if code.startswith(ouder["code"] + ".") else ouder["code"] + "." + code.split(".")[-1]
        if aantal > 1:                                             # dezelfde code twee keer: geen eigen punt, toelichting bij de ouder
            ouder["toel"].append(vol)
            meldingen.append("%s / %s r%d: subregel %s komt %d keer voor onder %s en staat als toelichting bij %s" % (bestand, blad, nr, code, aantal, ouder["code"], ouder["code"]))
            continue
        if goed != code:
            meldingen.append("%s / %s r%d: code %s staat onder %s en is geladen als %s (velddekking §14)" % (bestand, blad, nr, code, ouder["code"], goed))
        items.append({"code": goed, "tekst": tekst, "toel": [], "rij": nr})
    items.sort(key=lambda i: i["rij"])
    codes = [i["code"] for i in items]
    dubbel = sorted({c for c in codes if codes.count(c) > 1})
    if dubbel: raise SystemExit("dubbele codes in %s / %s: %s" % (bestand, blad, dubbel))
    return items

CHECKLISTS = [
    {"naam": "Speeltoestellen EN 1176", "versie": "2022", "soort": "Toestel", "norm": "EN 1176", "bestand": "Indienststelling versie 2022.md",
     "bladen": [("Algemeen", "Deel 1 Algemeen", True)] + [(b, b.strip().capitalize(), False) for b in
                ["schommels", "Glijbaan", "Kabelbaan", "Draaitoestel", "Wip ", "Doelen", "zandbak", "Water", "springkasteel", "Zware balken", "Springtoestel"]]},
    {"naam": "Skatetoestellen EN 14974", "versie": "2022", "soort": "Toestel", "norm": "EN 14974", "bestand": "risicoanalyse skate toestellen versie 2022.md",
     "bladen": [("Algemeen", "Deel 1 Skate algemeen", True)] + [(b, b, False) for b in
                ["Curbs", "Rail", "Bank", "Jump-ramp", "Coping-ramp", "Spine-ramp", "Wall-ramp", "Fun-box", "Pyramide", "Mini-pipe", "Half-pipe"]]},
    {"naam": "Speelterrein", "versie": "2022", "soort": "Terrein", "norm": "", "bestand": "risicoanalyse terrein versie 2022.md",
     "bladen": [("terrein", "Terrein", True)]},
]

def maak_checklists():
    cl, od, cp = [], [], []
    for c in CHECKLISTS:
        ck = "%s|%s" % (c["naam"], c["versie"])
        cl.append({"_sleutel": ck, "iok_naam": c["naam"], "iok_versie": c["versie"], "iok_soort": c["soort"], "iok_norm": c["norm"], "statuscode": "Actief"})
        for vol, (blad, naam, altijd) in enumerate(c["bladen"], 1):
            ok = "%s|%s" % (ck, naam)
            od.append({"_sleutel": ok, "iok_naam": naam, "iok_checklistid": ck, "iok_altijdvantoepassing": "ja" if altijd else "nee", "iok_volgorde": vol * 10})
            items = lees_onderdeel(c["bestand"], blad)
            aanwezig = {i["code"] for i in items}
            for n, i in enumerate(items, 1):
                segs = i["code"].split(".")
                ouder = next((".".join(segs[:k]) for k in range(len(segs) - 1, 0, -1) if ".".join(segs[:k]) in aanwezig), "")
                hoofd = segs[0] if segs[0] in aanwezig and segs[0] != i["code"] else ""
                if len(segs) > 1 and not ouder: meldingen.append("%s / %s: %s heeft geen ouder in het blad" % (c["bestand"], blad, i["code"]))
                cp.append({"_sleutel": "%s|%s" % (ok, i["code"]), "iok_naam": ("%s %s" % (i["code"], i["tekst"]))[:200], "iok_code": i["code"],
                           "iok_tekst": i["tekst"], "iok_toelichting": "\n".join(t for t in i["toel"] if t), "iok_onderdeelid": ok,
                           "iok_ouderid": "%s|%s" % (ok, ouder) if ouder else "", "iok_hoofdstukid": "%s|%s" % (ok, hoofd) if hoofd else "",
                           "iok_volgorde": n * 10, "iok_nokbepaalthoofdstuk": "ja", "_bron": "%s / %s r%d" % (c["bestand"], blad, i["rij"])})
    return cl, od, cp

# ---------------------------------------------------------------- stamgegevens
def maak_toesteltypes():
    uit, cat = [], None
    for nr, cel in rijen("Overzicht soorten speeltoestellen.md", "Blad1"):
        if nr < 3: continue
        if "A" in cel: cat = cel["A"]
        if "B" in cel:
            c = "Zitelementen" if cat == "Zitelemeneten" else cat
            uit.append({"_sleutel": cel["B"], "iok_naam": cel["B"], "iok_categorie": c, "iok_eenheden": cel["C"],
                        "iok_norm": "EN 14974" if c == "Skate" else "EN 1176"})
    return uit

def maak_terreinen():
    acc, ter = {}, []
    for nr, cel in rijen("Overzicht bestaande speelterreinen.md", "Overzicht speelterreinen"):
        if nr == 1 or cel.get("D") != GEMEENTE: continue
        bestuur = ("Stad %s" if cel["E"] == "Gemeente" else "OCMW %s") % GEMEENTE
        acc[bestuur] = {"_sleutel": bestuur, "name": bestuur, "address1_city": GEMEENTE, "iok_soort": cel["E"]}
        code = cel.get("B", "").strip().upper()
        if not code: meldingen.append("terrein zonder code overgeslagen: r%d %s" % (nr, cel.get("C"))); continue
        op = []
        if cel.get("F") not in ("1", None): op.append("bron: %s locaties in deze rij (Q20)" % cel.get("F"))
        if "/" in code or "+" in code: op.append("code bevat / of + (B84)")
        ter.append({"_sleutel": code, "iok_naam": cel["C"], "iok_code": code, "iok_bestuurid": bestuur,
                    "iok_legacyid": cel["A"], "_toestellen_in_bron": cel.get("G", ""), "_opmerking": "; ".join(op)})
    codes = [t["iok_code"] for t in ter]
    if len(codes) != len(set(codes)): raise SystemExit("dubbele terreincodes in %s" % GEMEENTE)
    return list(acc.values()), ter

# De 16 toestellen van De Bogaard uit het verslag C_2026: (naam, hoofdcode, extra codes, weergave, type, type letterlijk in de lijst?)
BOGAARD = [
    ("Metalen doelen", "BOA 1", ["BOA 2"], "BOA 1 + BOA 2", "Metalen doel(en)", True),
    ("Skatepark", "BOA 03", [], "", "Skatepark", True),
    ("Klimrots", "BOA 5", [], "", "Klimmuur / Klimrots", False),
    ("Galaxy", "BOA 04", [], "", "Klimtoestel", False),
    ("Evenwichtsbalken", "BOA 7", [], "", "Evenwichtstoestel", False),
    ("Zelf remmende veerwip", "BOA 11", [], "", "Veertoestel enkel", False),
    ("Ringenschommel", "BOA 13", [], "", "Ringenschommel", True),
    ("Draai wip", "BOA 17", [], "", "Draaitoestel", False),
    ("Klimtoren met netten", "BOA 24", [], "", "Klimnetten", False),
    ("Vogelnestschommel", "BOA 29", [], "", "Vogelnestschommel", True),
    ("Trampoline", "BOA 30", [], "", "Trampoline", True),
    ("Volleybalterrein", "BOA 32", [], "", "Volleybalterrein", True),
    ("Toren met glijbaan", "BOA 35", [], "", "Klimtoren met glijbaan", False),
    ("Kabelbaan", "BOA 36", [], "", "Kabelbaan", True),
    ("Dubbele veerwip paard", "BOA 38", [], "", "Veertoestel dubbel", False),
    ("Fitnesstoestellen", "BOA 45", [], "", "Fitnesstoestel", False),
    ("Contactschommel", "BOA 34", [], "", "Contactschommel", True),
]
VERSLAG = "C_2026 - Jaarlijkse controle De Bogaard (algemeen).md"

# Toestellen die wel in de PDF van het verslag staan (pagina 4) maar die de md-conversie heeft laten vallen.
# Hun kop ontbreekt in VERSLAG; gegevens overgenomen uit de PDF. Zie 04_data/LEESMIJ.md.
UIT_PDF = {"BOA 5": {"besluit": "Conform", "besluittekst": "Het toestel is conform de norm."}}

def maak_toestellen(types):
    tekst = (DOCS / VERSLAG).read_text(encoding="utf-8")
    eenh = {t["iok_naam"]: t["iok_eenheden"] for t in types}
    toe, codes = [], []
    for naam, code, extra, weergave, typ, zeker in BOGAARD:
        kop = "%s %s" % (naam, weergave or code)
        if kop not in tekst and code not in UIT_PDF: raise SystemExit("toestel niet gevonden in het verslag: " + kop)
        if typ not in eenh: raise SystemExit("toesteltype bestaat niet: " + typ)
        toe.append({"_sleutel": code, "iok_naam": naam, "iok_code": code, "iok_codeweergave": weergave, "iok_speelterreinid": "BOA",
                    "iok_toesteltypeid": typ, "iok_eenheden": eenh[typ],
                    "_opmerking": ("ontbreekt in de md-conversie van het verslag, overgenomen uit de PDF p.4; " if code in UIT_PDF else "")
                                   + ("" if zeker else "toesteltype afgeleid uit de naam, niet in de bron: te bevestigen (Q15)")})
        for c in [code] + extra:
            codes.append({"_sleutel": c, "iok_code": c, "iok_speeltoestelid": code, "iok_ishoofdcode": "ja" if c == code else "nee"})
    return toe, codes

# ---------------------------------------------------------------- standaardteksten
def lijsten(bestand, blad):
    """{lijstnaam: [zinnen]} uit een blad Standaardlijsten (kop, dan de waarden, gescheiden door een lege rij)."""
    uit, naam, vorige = {}, None, -9
    for nr, cel in rijen(bestand, blad):
        a = cel.get("A", "")
        if not a: continue
        if nr - vorige > 1: naam = a; uit[naam] = []
        else: uit[naam].append(a)
        vorige = nr
    return uit

def maak_standaardteksten():
    uit = []
    def voeg(lijst, zinnen, soort, cp="", bron=""):
        for n, z in enumerate(zinnen, 1):
            uit.append({"_sleutel": "%s %d" % (lijst, n), "iok_naam": "%s %d" % (lijst, n), "iok_tekst": z, "iok_soort": soort, "iok_controlepuntid": cp, "_lijst": lijst, "_bron": bron})
    overslaan = {"keuze", "bevestiging", "doelgroep", "toestellen", "ra uitgevoerd door :", "danny frederix"}   # namenlijsten vervallen (B37)
    d1 = "Speeltoestellen EN 1176|2022|Deel 1 Algemeen|"
    ind = lijsten("Indienststelling versie 2022.md", "Standaardlijsten")
    for lijst, zinnen in ind.items():
        if lijst.lower() in overslaan or not zinnen: continue
        cp = {"Markeringen": d1 + "M", "Inlichtingen": d1 + "N"}.get(lijst, "")
        voeg(lijst, zinnen, "Opmerking bij controlepunt", cp, "Indienststelling versie 2022 / Standaardlijsten")
    for lijst, zinnen in lijsten("risicoanalyse skate toestellen versie 2022.md", "Standaardlijsten").items():
        if lijst.lower() in overslaan or lijst in ind or not zinnen: continue
        voeg("Skate " + lijst, zinnen, "Opmerking bij controlepunt", "", "risicoanalyse skate toestellen versie 2022 / Standaardlijsten")
    for lijst, zinnen in lijsten("risicoanalyse terrein versie 2022.md", "standaardlijsten").items():
        if lijst.lower() in overslaan or not zinnen: continue
        voeg("Terrein " + lijst, zinnen, "Opmerking bij controlepunt", "", "risicoanalyse terrein versie 2022 / standaardlijsten")
    c = (DOCS / VERSLAG).read_text(encoding="utf-8")
    besluit = ["Het toestel is conform de norm.", "Het terrein is conform de norm.", "Het toestel is momenteel onbruikbaar.", "Het toestel is verwijderd van het terrein."]
    for z in besluit:
        if z.rstrip(".") not in c: raise SystemExit("besluitzin niet in het verslag: " + z)
    voeg("Besluit", besluit, "Besluit beoordeling", "", VERSLAG)
    alg = re.search(r"ALGEMEEN BESLUIT:\n(.+)", c).group(1).strip()
    voeg("Algemeen besluit", [alg], "Algemeen besluit", "", VERSLAG)
    return uit, alg

# ---------------------------------------------------------------- voorbeelddossier (C_2026)
# bevindingen: (toestelcode, onderdeel, code in het sjabloon, begin van de regel in het verslag,
#               impact, kans, blootstelling) -- de drie cijfers komen uit de risicotabel onder elke bevinding in de
#               PDF van het verslag; "" = niet af te leiden. Zie 04_data/LEESMIJ.md.
BEVINDINGEN = [
    ("BOA 11", "Deel 1 Algemeen", "K.1", "K.1 ", "7", "6", "3"),
    ("BOA 11", "Wip", "1.1", "1.5 Beweging van de wip", "1", "3", "3"),
    ("BOA 24", "Deel 1 Algemeen", "K.1", "K.1 ", "3", "6", "3"),
    ("BOA 30", "Deel 1 Algemeen", "G.2.6.2", "G.2.6.2 ", "3", "3", "3"),
    ("BOA 35", "Deel 1 Algemeen", "A.1.1", "A.1.1 ", "3", "2", "3"),
    ("BOA 35", "Deel 1 Algemeen", "E.1.3", "E.1.3", "3", "3", "3"),
    # p.11: de kop luidt "Impact Kans Resultaat" met drie getallen -- er is een kolom weggevallen. Of 3/1,0/3,0 nu
    # impact/kans/resultaat is (blootstelling 1,0) of impact/kans/blootstelling (resultaat 9,0) valt niet uit te
    # maken, dus blijft de blootstelling leeg en rekent de formulekolom niets uit (Q28).
    ("BOA 35", "Deel 1 Algemeen", "G.2.3", "G.2.3 ", "3", "1", ""),
]
NIET_BEOORDEELD = {"BOA 29": "Het toestel is momenteel onbruikbaar.", "BOA 32": "Het toestel is verwijderd van het terrein.", "BOA 38": "Het toestel is verwijderd van het terrein."}

def maak_dossier(toestellen, types, cps, alg):
    c = (DOCS / VERSLAG).read_text(encoding="utf-8")
    blokken = c.split("JAARLIJKSE CONTROLE:\n")[1:]
    dk = "BOA|2026-08-04"
    dossier = [{"_sleutel": dk, "iok_speelterreinid": "BOA", "iok_controledatum": "2026-08-04", "iok_soortcontrole": "Jaarlijkse controle",
                "iok_inspecteurid": "@ik", "iok_inspecteurnaam": "@ik", "iok_bestuurid": "Stad Geel", "iok_bestuurnaam": "Stad Geel",
                "iok_terreinnaam": "De Bogaard Algemeen", "iok_terreincode": "BOA", "iok_algemeenbesluit": alg,
                "_opmerking": "inspecteur = de gebruiker die laadt; status blijft Concept (zelf op Afgerond zetten)"}]
    eenh = {t["iok_naam"]: t["iok_eenheden"] for t in types}
    cpset = {x["_sleutel"] for x in cps}
    beo, res, nn = [], [], []
    en, sk, te = "Speeltoestellen EN 1176|2022", "Skatetoestellen EN 14974|2022", "Speelterrein|2022"
    beo.append({"_sleutel": dk + "|TERREIN", "iok_naam": "BOA 2026-08-04 Terrein", "iok_inspectiedossierid": dk, "iok_soort": "Terrein", "iok_checklistid": te,
                "iok_beoordelingsbasis": "Jaarlijkse controle", "iok_besluit": "Conform", "iok_besluittekst": "Het terrein is conform de norm.", "iok_volgorde": 0})
    nn.append({"iok_beoordeling": dk + "|TERREIN", "iok_checklistonderdeel": te + "|Terrein"})
    for vol, t in enumerate(toestellen, 1):
        code = t["iok_code"]; bk = "%s|%s" % (dk, code); skate = t["iok_toesteltypeid"] == "Skatepark"
        kop = "%s %s" % (t["iok_naam"], t["iok_codeweergave"] or code)
        blok = next((b for b in blokken if b.startswith(kop)), None)
        if blok is None and code in UIT_PDF:
            blok = UIT_PDF[code]["besluittekst"]          # enkel in de PDF: besluit overgenomen uit UIT_PDF
        elif blok is None:
            raise SystemExit("blok niet gevonden in het verslag: " + kop)
        b = {"_sleutel": bk, "iok_naam": "BOA 2026-08-04 %s" % code, "iok_inspectiedossierid": dk, "iok_soort": "Toestel", "iok_speeltoestelid": code,
             "iok_checklistid": sk if skate else en, "iok_norm": "EN 14974" if skate else "EN 1176", "iok_beoordelingsbasis": "Jaarlijkse controle",
             "iok_volgorde": vol, "iok_toestelcode": t["iok_codeweergave"] or code, "iok_toestelnaam": t["iok_naam"], "iok_typenaam": t["iok_toesteltypeid"],
             "iok_eenheden": eenh[t["iok_toesteltypeid"]]}
        if code in NIET_BEOORDEELD:
            b["iok_besluit"], b["iok_besluittekst"] = "Niet beoordeeld", NIET_BEOORDEELD[code]
            m = re.search(r"Opmerkingen:\n(.*?)\Z", blok, flags=re.S)
            if m: b["iok_opmerking"] = " ".join(m.group(1).split())
        elif "Het toestel is conform de norm." in blok:
            b["iok_besluit"], b["iok_besluittekst"] = "Conform", "Het toestel is conform de norm."
        else:
            b["_opmerking"] = "het verslag noemt bevindingen maar geen besluit: besluit leeg gelaten"
        beo.append(b)
        nn.append({"iok_beoordeling": bk, "iok_checklistonderdeel": (sk + "|Deel 1 Skate algemeen") if skate else (en + "|Deel 1 Algemeen")})
        for tc, onderdeel, cpcode, begin, impact, kans, bloot in BEVINDINGEN:
            if tc != code: continue
            regels = blok.split("\n")
            i = next(k for k, r in enumerate(regels) if r.startswith(begin))
            j, op = i + 1, []
            while j < len(regels) and regels[j] != "[foto]" and not re.match(r"^([A-Z]\.|\d+\.\d|Specifieke onderdelen|[A-Z]\. )", regels[j]) and not re.match(r"^%s[ .]" % CODE, regels[j]):
                op.append(regels[j]); j += 1
            cpk = "%s|%s|%s" % (en, onderdeel, cpcode)
            if cpk not in cpset: raise SystemExit("controlepunt bestaat niet: " + cpk)
            if onderdeel != "Deel 1 Algemeen" and {"iok_beoordeling": bk, "iok_checklistonderdeel": en + "|" + onderdeel} not in nn:
                nn.append({"iok_beoordeling": bk, "iok_checklistonderdeel": en + "|" + onderdeel})
            afw = "" if regels[i].startswith(cpcode) else "het verslag noemt code %s; in het sjabloon 2022 heeft dezelfde tekst code %s" % (begin.split()[0], cpcode)
            if afw: meldingen.append("%s: %s" % (code, afw))
            if not bloot: afw = (afw + "; " if afw else "") + "blootstelling niet af te leiden uit het verslag (Q28)"
            res.append({"_sleutel": "%s|%s" % (bk, cpk), "iok_naam": cpcode, "iok_beoordelingid": bk, "iok_controlepuntid": cpk, "iok_antwoord": "NOK",
                        "iok_opmerking": " ".join(" ".join(op).split()),
                        "iok_impact": impact, "iok_kans": kans, "iok_blootstelling": bloot, "_opmerking": afw})
    return dossier, beo, res, nn

# ---------------------------------------------------------------- laadplan + controle
def main():
    UIT.mkdir(exist_ok=True)
    types = maak_toesteltypes(); acc, ter = maak_terreinen(); toe, codes = maak_toestellen(types)
    cl, od, cp = maak_checklists(); st, alg = maak_standaardteksten()
    dos, beo, res, nn = maak_dossier(toe, types, cp, alg)
    K = lambda *k: ["_sleutel"] + list(k)
    plan = [
        ("account", "account.csv", K("name", "address1_city", "iok_soort"), acc, {}),
        ("iok_toesteltype", "iok_toesteltype.csv", K("iok_naam", "iok_categorie", "iok_eenheden", "iok_norm"), types, {}),
        ("iok_checklist", "iok_checklist.csv", K("iok_naam", "iok_versie", "iok_soort", "iok_norm", "statuscode"), cl, {}),
        ("iok_checklistonderdeel", "iok_checklistonderdeel.csv", K("iok_naam", "iok_checklistid", "iok_altijdvantoepassing", "iok_volgorde"), od, {"iok_checklistid": "iok_checklist"}),
        ("iok_controlepunt", "iok_controlepunt.csv", K("iok_naam", "iok_code", "iok_tekst", "iok_toelichting", "iok_onderdeelid", "iok_ouderid", "iok_hoofdstukid", "iok_volgorde", "iok_nokbepaalthoofdstuk", "_bron"), cp,
         {"iok_onderdeelid": "iok_checklistonderdeel", "iok_ouderid": "iok_controlepunt", "iok_hoofdstukid": "iok_controlepunt"}),
        ("iok_standaardtekst", "iok_standaardtekst.csv", K("iok_naam", "iok_tekst", "iok_soort", "iok_controlepuntid", "_lijst", "_bron"), st, {"iok_controlepuntid": "iok_controlepunt"}),
        ("iok_speelterrein", "iok_speelterrein.csv", K("iok_naam", "iok_code", "iok_bestuurid", "iok_legacyid", "_toestellen_in_bron", "_opmerking"), ter, {"iok_bestuurid": "account"}),
        ("iok_speeltoestel", "iok_speeltoestel.csv", K("iok_naam", "iok_code", "iok_codeweergave", "iok_speelterreinid", "iok_toesteltypeid", "iok_eenheden", "_opmerking"), toe,
         {"iok_speelterreinid": "iok_speelterrein", "iok_toesteltypeid": "iok_toesteltype"}),
        ("iok_toestelcode", "iok_toestelcode.csv", K("iok_code", "iok_speeltoestelid", "iok_ishoofdcode"), codes, {"iok_speeltoestelid": "iok_speeltoestel"}),
        ("iok_inspectiedossier", "iok_inspectiedossier.csv", K("iok_speelterreinid", "iok_controledatum", "iok_soortcontrole", "iok_inspecteurid", "iok_inspecteurnaam", "iok_bestuurid", "iok_bestuurnaam", "iok_terreinnaam", "iok_terreincode", "iok_algemeenbesluit", "_opmerking"), dos,
         {"iok_speelterreinid": "iok_speelterrein", "iok_bestuurid": "account", "iok_inspecteurid": "systemuser"}),
        ("iok_beoordeling", "iok_beoordeling.csv", K("iok_naam", "iok_inspectiedossierid", "iok_soort", "iok_speeltoestelid", "iok_checklistid", "iok_norm", "iok_beoordelingsbasis", "iok_besluit", "iok_besluittekst", "iok_opmerking", "iok_volgorde", "iok_toestelcode", "iok_toestelnaam", "iok_typenaam", "iok_eenheden", "_opmerking"), beo,
         {"iok_inspectiedossierid": "iok_inspectiedossier", "iok_speeltoestelid": "iok_speeltoestel", "iok_checklistid": "iok_checklist"}),
        ("iok_resultaat", "iok_resultaat.csv", K("iok_naam", "iok_beoordelingid", "iok_controlepuntid", "iok_antwoord", "iok_opmerking",
                                                  "iok_impact", "iok_kans", "iok_blootstelling", "_opmerking"), res,
         {"iok_beoordelingid": "iok_beoordeling", "iok_controlepuntid": "iok_controlepunt"}),
    ]
    sleutels, fouten, laadplan = {}, [], []
    for tabel, bestand, kol, data, lookups in plan:
        ks = [r["_sleutel"] for r in data]
        if len(ks) != len(set(ks)): fouten.append("dubbele _sleutel in " + bestand)
        sleutels[tabel] = set(ks)
    for tabel, bestand, kol, data, lookups in plan:
        for r in data:
            for lk, doel in lookups.items():
                v = r.get(lk, "")
                if v and v != "@ik" and v not in sleutels[doel]: fouten.append("%s: %s verwijst naar onbekende %s '%s'" % (bestand, lk, doel, v))
        n = schrijf(bestand, kol, data)
        laadplan.append({"tabel": tabel, "bestand": bestand, "rijen": n, "lookups": lookups,
                         "tweede_pas": [k for k, d in lookups.items() if d == tabel]})
    for r in nn:
        if r["iok_beoordeling"] not in sleutels["iok_beoordeling"] or r["iok_checklistonderdeel"] not in sleutels["iok_checklistonderdeel"]: fouten.append("N:N verwijst naar een onbekende rij: %s" % r)
    n = schrijf("iok_beoordeling_onderdeel.csv", ["iok_beoordeling", "iok_checklistonderdeel"], nn)
    laadplan.append({"nn": "iok_beoordeling_onderdeel", "bestand": "iok_beoordeling_onderdeel.csv", "rijen": n, "tabellen": ["iok_beoordeling", "iok_checklistonderdeel"]})
    (UIT / "laadplan.json").write_text(json.dumps(laadplan, ensure_ascii=False, indent=2), encoding="utf-8")
    (UIT / "_meldingen.txt").write_text("\n".join(meldingen) + "\n", encoding="utf-8")
    for s in laadplan: print("%-34s %5d rijen" % (s["bestand"], s["rijen"]))
    print("meldingen: %d (04_data/_meldingen.txt); fouten: %d" % (len(meldingen), len(fouten)))
    for f in fouten: print(" -", f)
    return 1 if fouten else 0

if __name__ == "__main__":
    sys.exit(main())
