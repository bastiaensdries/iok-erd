"""Controleert de twee formulekolommen op iok_resultaat. ALLEEN-LEZEN.
Gebruik:  python tools/dv_formule.py --url https://<org>.crm17.dynamics.com"""
import sys
from dv_gemeen import Dv, DvFout

VERWACHT = [
    ("iok_risicoscore",  "Decimal", ["iok_impact", "iok_kans", "iok_blootstelling", "IsBlank", "Blank"]),
    ("iok_risicoklasse", "String",  ["iok_risicoscore", "Licht", "Mogelijk", "Substantieel", "Hoog", "Zeer hoog"]),
]

def main():
    dv = Dv(schrijven=False)
    w = dv.wie()
    print("Omgeving: %s" % w["organisatie"])
    pad = ("EntityDefinitions(LogicalName='iok_resultaat')/Attributes"
           "?$select=LogicalName,AttributeType,SourceType,MetadataId")
    alle = dv.get(pad)["value"]
    per_naam = {a["LogicalName"]: a for a in alle}

    fouten = 0
    for naam, type_verwacht, brokken in VERWACHT:
        a = per_naam.get(naam)
        if a is None:
            print("ONTBREEKT  %s  -- kolom bestaat niet" % naam)
            fouten += 1
            continue

        regels = []
        soort = a.get("AttributeType")
        if soort != type_verwacht:
            regels.append("type is %s, verwacht %s" % (soort, type_verwacht))

        bron = a.get("SourceType")
        if bron in (None, 0):
            regels.append("is geen formulekolom (SourceType=%s)" % bron)

        formule = ""
        for cast in ("Microsoft.Dynamics.CRM.DecimalAttributeMetadata",
                     "Microsoft.Dynamics.CRM.StringAttributeMetadata",
                     "Microsoft.Dynamics.CRM.MoneyAttributeMetadata",
                     "Microsoft.Dynamics.CRM.IntegerAttributeMetadata"):
            try:
                d = dv.get("EntityDefinitions(LogicalName='iok_resultaat')/Attributes(%s)/%s"
                           "?$select=LogicalName,FormulaDefinition" % (a["MetadataId"], cast), mag_404=True)
            except DvFout:
                d = None
            if d and d.get("FormulaDefinition"):
                formule = d["FormulaDefinition"]
                break

        if not formule:
            regels.append("geen formule gevonden")
        else:
            mist = [b for b in brokken if b not in formule]
            if mist:
                regels.append("formule mist: %s" % ", ".join(mist))

        if regels:
            print("FOUT       %s" % naam)
            for r in regels:
                print("             - %s" % r)
            if formule:
                print("             formule: %s" % formule.replace("\n", " ")[:300])
            fouten += 1
        else:
            print("OK         %-18s %s" % (naam, soort))

    print()
    print("Berekende waarden in de proefdata:")
    rijen = dv.alle("iok_resultaats?$select=iok_naam,iok_impact,iok_kans,iok_blootstelling,"
                    "iok_risicoscore,iok_risicoklasse&$orderby=iok_naam")
    verwacht = {"K.1": [126.0, 54.0], "1.1": [9.0], "G.2.6.2": [27.0], "A.1.1": [18.0], "E.1.3": [27.0], "G.2.3": [None]}
    print("  %-9s %6s %6s %6s %10s  %s" % ("punt", "impact", "kans", "bloot", "score", "klasse"))
    leeg_ok = True
    for r in rijen:
        sc, kl = r.get("iok_risicoscore"), r.get("iok_risicoklasse")
        getal = lambda v: "-" if v is None else ("%g" % float(v))
        print("  %-9s %6s %6s %6s %10s  %s" % (r.get("iok_naam"), getal(r.get("iok_impact")), getal(r.get("iok_kans")),
                                               getal(r.get("iok_blootstelling")), getal(sc), kl or "-"))
        if r.get("iok_blootstelling") is None and (sc is not None or kl):
            leeg_ok = False
    print()
    if not rijen:
        print("Geen resultaatrecords gevonden; laad eerst de proefdata.")
    elif leeg_ok:
        print("De test op leeg werkt: een bevinding zonder blootstelling krijgt geen score en geen klasse.")
    else:
        print("FOUT: een bevinding zonder blootstelling kreeg toch een score. De IsBlank-test in de formule klopt niet.")
        fouten += 1

    print()
    print("Fouten: %d" % fouten)
    return 1 if fouten else 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except DvFout as e:
        print("Fout %s: %s" % (e.code, e.args[-1]))
        sys.exit(2)
