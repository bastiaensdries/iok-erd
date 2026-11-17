"""Laadt de CSV's uit 04_data/ in Dataverse, in de volgorde van 04_data/laadplan.json (B85).

Gebruik:  python tools/dv_laden.py                                   (proefdraai zonder netwerk: controleert de CSV's tegen spec.yaml)
          python tools/dv_laden.py --url https://<org>... --uitvoeren (laadt echt, na bevestiging)
          ... --uitvoeren --bijwerken                                (werkt bestaande records ook bij uit de CSV's)
          ... --uitvoeren --bijwerken iok_resultaat,iok_speeltoestel (enkel die tabellen bijwerken)

--bijwerken schrijft de CSV-waarden over wat er in Dataverse staat, ook als iemand het daar met de hand wijzigde.
Zonder die vlag blijft een record dat al bestaat onaangeroerd; nieuwe rijen worden altijd aangemaakt.

Verwijzingen lopen via de kolom _sleutel; het script onthoudt in 04_data/_geladen.json welke rij welk record werd,
zodat opnieuw draaien niets dubbel aanmaakt. Zelfverwijzingen (ouder, hoofdstuk) en statussen komen in een tweede ronde.
Kolommen die met _ beginnen worden niet geladen. "@ik" = de aangemelde gebruiker.
"""
import csv, json, sys
from dv_gemeen import Dv, DvFout, laad_spec, label_tekst, ROOT, API

DATA = ROOT / "04_data"
UITVOEREN = "--uitvoeren" in sys.argv
BIJWERKEN = "--bijwerken" in sys.argv
BIJ_TABELLEN = None                       # None = alle tabellen
if BIJWERKEN:
    _i = sys.argv.index("--bijwerken") + 1
    if _i < len(sys.argv) and not sys.argv[_i].startswith("--"):
        BIJ_TABELLEN = {x.strip() for x in sys.argv[_i].split(",") if x.strip()}

def lees(bestand):
    with open(DATA / bestand, encoding="utf-8-sig", newline="") as f: return list(csv.DictReader(f))

def main():
    spec = laad_spec()
    plan = json.loads((DATA / "laadplan.json").read_text(encoding="utf-8"))
    tab = {t["schema"]: t for t in spec["tabellen"]}
    opties = {k["schema"]: {o["label"]: o["waarde"] for o in k["opties"]} for k in spec["globale_keuzelijsten"]}
    fouten, sleutels = [], {}
    for s in plan:
        if "tabel" in s: sleutels[s["tabel"]] = {r["_sleutel"] for r in lees(s["bestand"])}

    def kolomdef(tabel, kol):
        t = tab[tabel]
        pk = t.get("primaire_kolom")
        if pk and pk["schema"] == kol: return {"type": pk.get("type", "text"), "lengte": pk.get("lengte"), "verplicht": True}
        for k in t["kolommen"]:
            if k["schema"] == kol: return k
        return {"type": "text"} if t["bestaand"] else None

    def waarde(tabel, kol, v, s, waar):
        """(sleutel, waarde) voor de aanvraag, of None als de kolom leeg is of later komt."""
        k = kolomdef(tabel, kol)
        if k is None: fouten.append("%s: kolom %s staat niet in spec.yaml" % (waar, kol)); return None
        if v == "": return None
        t = k["type"]
        try:
            if t == "lookup":
                doel = s["lookups"].get(kol)
                if not doel or doel != k["doel"]: fouten.append("%s: lookup %s wijst in het laadplan naar %s, in de spec naar %s" % (waar, kol, doel, k.get("doel"))); return None
                if v != "@ik" and v not in sleutels.get(doel, ()): fouten.append("%s: %s verwijst naar onbekende rij '%s'" % (waar, kol, v))
                return ("lookup", kol, doel, v)
            if t in ("text", "memo", "autonumber"):
                if k.get("lengte") and v != "@ik" and len(v) > k["lengte"]: fouten.append("%s: %s is %d tekens, maximum %d" % (waar, kol, len(v), k["lengte"]))
                return ("waarde", kol, v)
            if t == "int": return ("waarde", kol, int(v))
            if t == "decimal": return ("waarde", kol, float(v.replace(",", ".")))
            if t in ("date", "datetime"): return ("waarde", kol, v)
            if t == "bool":
                if v not in ("ja", "nee"): raise ValueError("ja of nee verwacht")
                return ("waarde", kol, v == "ja")
            if t == "choice":
                if v not in opties[k["keuzelijst"]]: raise ValueError("'%s' is geen waarde van %s" % (v, k["keuzelijst"]))
                return ("waarde", kol, opties[k["keuzelijst"]][v])
        except ValueError as e:
            fouten.append("%s: %s: %s" % (waar, kol, e))
        return None

    # ---- proefdraai: alles opbouwen en controleren zonder netwerk
    werk = []
    for s in plan:
        if "nn" in s:
            for r in lees(s["bestand"]):
                a, b = s["tabellen"]
                if r[a] not in sleutels[a] or r[b] not in sleutels[b]: fouten.append("%s: onbekende rij %s" % (s["bestand"], r))
            werk.append((s, lees(s["bestand"]))); continue
        tabel, rijen = s["tabel"], []
        for n, r in enumerate(lees(s["bestand"]), 2):
            waar = "%s r%d" % (s["bestand"], n)
            velden = [waarde(tabel, k, v, s, waar) for k, v in r.items() if not k.startswith("_") and k != "statuscode"]
            velden = [x for x in velden if x]
            aanwezig = {x[1] for x in velden}
            t = tab[tabel]
            for k in t["kolommen"] + ([dict(t["primaire_kolom"], verplicht=t["primaire_kolom"].get("type") != "autonumber")] if t.get("primaire_kolom") else []):
                if k.get("verplicht") and not k.get("formule") and "standaard" not in k and k["schema"] not in aanwezig:
                    fouten.append("%s: verplichte kolom %s is leeg" % (waar, k["schema"]))
            rijen.append((r["_sleutel"], velden, r.get("statuscode", "")))
        werk.append((s, rijen))
    print("Proefcontrole van de CSV's tegen spec.yaml: %d fouten" % len(fouten))
    for f in fouten[:60]: print(" -", f)
    for s, rijen in werk: print("  %-34s %5d rijen" % (s["bestand"], len(rijen)))
    if fouten: return 1
    if not UITVOEREN:
        print("\nDit was een proefdraai: er is niets geladen. Voeg --url ... --uitvoeren toe om te laden."); return 0

    # ---- echt laden
    dv = Dv(schrijven=True); w = dv.wie()
    print("\nOmgeving: %s (%s)\nAangemeld als: %s" % (w["organisatie"], dv.url, w["gebruiker"]))
    if "--ja" not in sys.argv and input("Dit maakt records aan in bovenstaande omgeving. Typ LADEN om door te gaan: ").strip() != "LADEN": return 2
    kaartbestand = DATA / "_geladen.json"
    alles = json.loads(kaartbestand.read_text(encoding="utf-8")) if kaartbestand.exists() else {}
    kaart = alles.setdefault(dv.url, {})
    bewaar = lambda: kaartbestand.write_text(json.dumps(alles, ensure_ascii=False, indent=1), encoding="utf-8")
    sets = {}
    def eset(tabel):
        if tabel not in sets: sets[tabel] = dv.get("EntityDefinitions(LogicalName='%s')?$select=EntitySetName" % tabel)["EntitySetName"]
        return sets[tabel]
    def verwijzing(doel, v):
        if v == "@ik": return "/systemusers(%s)" % w["userid"]
        return "/%s(%s)" % (eset(doel), kaart[doel][v])
    laadfouten = 0
    for s, rijen in werk:
        if "nn" in s: continue
        tabel = s["tabel"]; k = kaart.setdefault(tabel, {}); nieuw = 0
        bij = BIJWERKEN and (BIJ_TABELLEN is None or tabel in BIJ_TABELLEN); bijgewerkt = 0
        for sleutel, velden, _ in rijen:
            bestaat = sleutel in k
            if bestaat and not bij: continue
            body = {}
            for x in velden:
                if x[0] == "waarde": body[x[1]] = w["gebruiker"] if x[2] == "@ik" else x[2]
                elif x[1] not in s.get("tweede_pas", []): body[x[1] + "@odata.bind"] = verwijzing(x[2], x[3])
            try:
                if bestaat:
                    dv.vraag("PATCH", "%s(%s)" % (eset(tabel), k[sleutel]), body); bijgewerkt += 1
                    if bijgewerkt % 50 == 0: print("    %s: %d bijgewerkt..." % (tabel, bijgewerkt), flush=True)
                else:
                    _, h = dv.vraag("POST", eset(tabel), body)
                    k[sleutel] = h["OData-EntityId"].split("(")[-1].rstrip(")"); nieuw += 1
                    if nieuw % 50 == 0: bewaar(); print("    %s: %d..." % (tabel, nieuw), flush=True)
            except DvFout as e:
                laadfouten += 1; print("  ! %s '%s' -> %s" % (tabel, sleutel, e), flush=True)
                if laadfouten >= 10: bewaar(); print("Te veel fouten: gestopt."); return 1
        bewaar()
        staart = ", %5d bijgewerkt" % bijgewerkt if bij else ""
        print("  %-28s %5d nieuw, %5d bestonden al%s" % (tabel, nieuw, len(rijen) - nieuw, staart), flush=True)
        if s.get("tweede_pas"):                                    # zelfverwijzingen
            gedaan = kaart.setdefault(tabel + "#tweede_pas", {}); n = 0
            for sleutel, velden, _ in rijen:
                body = {x[1] + "@odata.bind": verwijzing(x[2], x[3]) for x in velden if x[0] == "lookup" and x[1] in s["tweede_pas"] and x[3] in k}
                if not body or sleutel in gedaan or sleutel not in k: continue
                try: dv.vraag("PATCH", "%s(%s)" % (eset(tabel), k[sleutel]), body); gedaan[sleutel] = 1; n += 1
                except DvFout as e: laadfouten += 1; print("  ! %s '%s' (ouder/hoofdstuk) -> %s" % (tabel, sleutel, e), flush=True)
            bewaar(); print("  %-28s %5d zelfverwijzingen gezet" % (tabel, n), flush=True)
    for s, rijen in werk:                                           # N:N
        if "nn" not in s: continue
        a, b = s["tabellen"]; gedaan = kaart.setdefault("nn#" + s["nn"], {}); n = 0
        for r in rijen:
            sleutel = r[a] + " <> " + r[b]
            if sleutel in gedaan: continue
            try:
                dv.vraag("POST", "%s(%s)/%s/$ref" % (eset(a), kaart[a][r[a]], s["nn"]), {"@odata.id": "%s%s%s(%s)" % (dv.url, API, eset(b), kaart[b][r[b]])})
                gedaan[sleutel] = 1; n += 1
            except (DvFout, KeyError) as e: laadfouten += 1; print("  ! %s %s -> %s" % (s["nn"], sleutel, e), flush=True)
        bewaar(); print("  %-28s %5d koppelingen" % (s["nn"], n), flush=True)
    for s, rijen in werk:                                           # statussen als laatste
        if "nn" in s or not any(st for _, _, st in rijen): continue
        tabel = s["tabel"]; gedaan = kaart.setdefault(tabel + "#status", {})
        o = dv.get("EntityDefinitions(LogicalName='%s')/Attributes(LogicalName='statuscode')/Microsoft.Dynamics.CRM.StatusAttributeMetadata?$select=LogicalName&$expand=OptionSet($select=Options)" % tabel)
        st = {label_tekst(x["Label"]): (x["State"], x["Value"]) for x in o["OptionSet"]["Options"]}
        for sleutel, _, status in rijen:
            if not status or sleutel in gedaan or sleutel not in kaart[tabel]: continue
            if status not in st: laadfouten += 1; print("  ! %s: statusreden '%s' bestaat niet" % (tabel, status)); continue
            try: dv.vraag("PATCH", "%s(%s)" % (eset(tabel), kaart[tabel][sleutel]), {"statecode": st[status][0], "statuscode": st[status][1]}); gedaan[sleutel] = 1
            except DvFout as e: laadfouten += 1; print("  ! %s '%s' status -> %s" % (tabel, sleutel, e), flush=True)
        bewaar()
    print("\nKlaar. Fouten: %d. Geschreven aanvragen: %d." % (laadfouten, dv.aantal_schrijf))
    return 1 if laadfouten else 0

if __name__ == "__main__":
    try: sys.exit(main())
    except DvFout as e: sys.exit("FOUT %s" % e)
