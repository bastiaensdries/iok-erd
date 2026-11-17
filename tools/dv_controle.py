"""Vergelijkt een Dataverse-omgeving met 03_output/spec.yaml. ALLEEN-LEZEN: dit script kan niets wijzigen.

Gebruik:  python tools/dv_controle.py --url https://<org>.crm4.dynamics.com
In een lege omgeving meldt het dat alles ontbreekt: dat bewijst dat aanmelden en lezen werken.
Na dv_bouw.py moet het aantal verschillen 0 zijn (op de handmatige punten na, die apart vermeld staan).
"""
import sys
from dv_gemeen import Dv, DvFout, laad_spec, label_tekst

TYPE = {"text": "String", "memo": "Memo", "int": "Integer", "decimal": "Decimal", "date": "DateTime", "datetime": "DateTime",
        "choice": "Picklist", "bool": "Boolean", "lookup": "Lookup", "autonumber": "String"}
VERWIJDEREN = {"restrict": "Restrict", "removelink": "RemoveLink", "cascade": "Cascade"}
ED = "EntityDefinitions(LogicalName='%s')"

def controleer(dv, spec):
    v, hand = [], []
    sol = spec["solution"]["naam"]
    s = dv.alle("solutions?$select=uniquename&$expand=publisherid($select=customizationprefix)&$filter=uniquename eq '%s'" % sol)
    if not s: v.append("solution ontbreekt: " + sol)
    elif s[0]["publisherid"]["customizationprefix"] != spec["publisher"]["prefix"]: v.append("solution heeft prefix %s" % s[0]["publisherid"]["customizationprefix"])
    for k in spec["globale_keuzelijsten"]:
        o = dv.get("GlobalOptionSetDefinitions(Name='%s')/Microsoft.Dynamics.CRM.OptionSetMetadata?$select=Name,Options" % k["schema"], mag_404=True)
        if not o: v.append("keuzelijst ontbreekt: " + k["schema"]); continue
        echt = {x["Value"]: label_tekst(x["Label"]) for x in o["Options"]}
        for opt in k["opties"]:
            if echt.get(opt["waarde"]) != opt["label"]: v.append("keuzelijst %s: optie %s = '%s', verwacht '%s'" % (k["schema"], opt["waarde"], echt.get(opt["waarde"]), opt["label"]))
        for w in set(echt) - {x["waarde"] for x in k["opties"]}: v.append("keuzelijst %s: extra optie %s '%s'" % (k["schema"], w, echt[w]))
    for t in spec["tabellen"]:
        naam = t["schema"]
        e = dv.get((ED % naam) + "?$select=LogicalName,OwnershipType,PrimaryNameAttribute&$expand=Attributes($select=LogicalName,AttributeType,RequiredLevel),Keys($select=SchemaName,KeyAttributes,EntityKeyIndexStatus)", mag_404=True)
        if not e: v.append("tabel ontbreekt: " + naam); continue
        att = {a["LogicalName"]: a for a in e["Attributes"]}
        kolommen = list(t["kolommen"])
        if not t["bestaand"]:
            eig = "OrganizationOwned" if t["eigenaarschap"] == "organization" else "UserOwned"
            if e["OwnershipType"] != eig: v.append("%s: eigenaarschap %s, verwacht %s (niet te wijzigen: tabel opnieuw maken)" % (naam, e["OwnershipType"], eig))
            pk = t["primaire_kolom"]
            if e["PrimaryNameAttribute"] != pk["schema"]: v.append("%s: primaire kolom %s, verwacht %s" % (naam, e["PrimaryNameAttribute"], pk["schema"]))
            kolommen.append({"schema": pk["schema"], "type": pk.get("type", "text"), "lengte": pk.get("lengte"), "verplicht": pk.get("type") != "autonumber", "formaat_auto": pk.get("formaat")})
        soorten = {k["type"] for k in kolommen}
        def cast(typ, velden, expand=""):
            return {a["LogicalName"]: a for a in dv.alle((ED % naam) + "/Attributes/Microsoft.Dynamics.CRM.%sAttributeMetadata?$select=LogicalName,%s%s" % (typ, velden, expand))}
        tekst = cast("String", "MaxLength,AutoNumberFormat") if soorten & {"text", "autonumber"} else {}
        memo = cast("Memo", "MaxLength") if "memo" in soorten else {}
        keuze = cast("Picklist", "DefaultFormValue", "&$expand=GlobalOptionSet($select=Name)") if "choice" in soorten else {}
        look = cast("Lookup", "Targets") if "lookup" in soorten else {}
        deci = cast("Decimal", "Precision") if "decimal" in soorten else {}
        datum = cast("DateTime", "Format") if soorten & {"date", "datetime"} else {}
        for k in kolommen:
            c, a = k["schema"], att.get(k["schema"])
            if k.get("formule"): hand.append("%s.%s: formulekolom, met de hand maken en nakijken" % (naam, c))
            if not a:
                if not k.get("formule"): v.append("kolom ontbreekt: %s.%s" % (naam, c))
                continue
            if a["AttributeType"] != TYPE[k["type"]]: v.append("%s.%s: type %s, verwacht %s (niet te wijzigen: kolom opnieuw maken)" % (naam, c, a["AttributeType"], TYPE[k["type"]])); continue
            if "verplicht" in k and not k.get("formule"):
                echt = a["RequiredLevel"]["Value"] in ("ApplicationRequired", "SystemRequired")
                if echt != bool(k["verplicht"]): v.append("%s.%s: verplicht = %s, verwacht %s" % (naam, c, echt, k["verplicht"]))
            if k["type"] in ("text", "autonumber") and k.get("lengte") and tekst.get(c, {}).get("MaxLength") != k["lengte"]: v.append("%s.%s: lengte %s, verwacht %s" % (naam, c, tekst.get(c, {}).get("MaxLength"), k["lengte"]))
            if k.get("formaat_auto") and tekst.get(c, {}).get("AutoNumberFormat") != k["formaat_auto"]: v.append("%s.%s: autonummer '%s', verwacht '%s'" % (naam, c, tekst.get(c, {}).get("AutoNumberFormat"), k["formaat_auto"]))
            if k["type"] == "memo" and memo.get(c, {}).get("MaxLength") != k["lengte"]: v.append("%s.%s: lengte %s, verwacht %s" % (naam, c, memo.get(c, {}).get("MaxLength"), k["lengte"]))
            if k["type"] == "choice" and ((keuze.get(c, {}).get("GlobalOptionSet") or {}).get("Name")) != k["keuzelijst"]: v.append("%s.%s: keuzelijst %s, verwacht %s" % (naam, c, (keuze.get(c, {}).get("GlobalOptionSet") or {}).get("Name"), k["keuzelijst"]))
            if k["type"] == "lookup" and look.get(c, {}).get("Targets") != [k["doel"]]: v.append("%s.%s: verwijst naar %s, verwacht %s" % (naam, c, look.get(c, {}).get("Targets"), k["doel"]))
            if k["type"] == "decimal" and not k.get("formule") and deci.get(c, {}).get("Precision") != k["precisie"]: v.append("%s.%s: precisie %s, verwacht %s" % (naam, c, deci.get(c, {}).get("Precision"), k["precisie"]))
            if k["type"] == "date" and datum.get(c, {}).get("Format") != "DateOnly": v.append("%s.%s: geen Alleen datum" % (naam, c))
        sleutels = {tuple(sorted(x["KeyAttributes"])): x for x in e["Keys"]}
        for s2 in t.get("alternatieve_sleutels", []):
            x = sleutels.get(tuple(sorted(s2["kolommen"])))
            if not x: v.append("sleutel ontbreekt: %s (%s)" % (naam, " + ".join(s2["kolommen"])))
            elif x["EntityKeyIndexStatus"] != "Active": v.append("sleutel %s op %s is nog niet actief (status %s)" % (x["SchemaName"], naam, x["EntityKeyIndexStatus"]))
        sr = t.get("statusredenen")
        if sr and (sr["actief"], sr["inactief"]) != (["Actief"], ["Inactief"]):
            o = dv.get((ED % naam) + "/Attributes(LogicalName='statuscode')/Microsoft.Dynamics.CRM.StatusAttributeMetadata?$select=LogicalName&$expand=OptionSet($select=Options)")
            echt = {(x["State"], label_tekst(x["Label"])) for x in o["OptionSet"]["Options"]}
            verwacht = {(0, l) for l in sr["actief"]} | {(1, l) for l in sr["inactief"]}
            for st, l in sorted(verwacht - echt): v.append("%s: statusreden ontbreekt: %s (%s)" % (naam, l, "actief" if st == 0 else "inactief"))
            for st, l in sorted(echt - verwacht): v.append("%s: extra statusreden: %s" % (naam, l))
        if t.get("documentbeheer"): hand.append("%s: documentbeheer (SharePoint) aanzetten" % naam)
    for r in spec["relaties"]:
        if r["type"] == "NN":
            x = dv.get("RelationshipDefinitions(SchemaName='%s')/Microsoft.Dynamics.CRM.ManyToManyRelationshipMetadata?$select=Entity1LogicalName,Entity2LogicalName" % r["schema"], mag_404=True)
            if not x: v.append("N:N ontbreekt: " + r["schema"])
            elif {x["Entity1LogicalName"], x["Entity2LogicalName"]} != set(r["tabellen"]): v.append("N:N %s koppelt andere tabellen" % r["schema"])
        elif not r.get("bestaand"):
            x = dv.get("RelationshipDefinitions(SchemaName='%s')/Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata?$select=ReferencedEntity,ReferencingEntity,ReferencingAttribute,CascadeConfiguration" % r["schema"], mag_404=True)
            if not x: v.append("relatie ontbreekt: %s (%s -> %s.%s)" % (r["schema"], r["van"], r["naar"], r["lookup"])); continue
            if (x["ReferencedEntity"], x["ReferencingEntity"], x["ReferencingAttribute"]) != (r["van"], r["naar"], r["lookup"]): v.append("relatie %s koppelt iets anders" % r["schema"])
            if x["CascadeConfiguration"]["Delete"] != VERWIJDEREN[r["verwijderen"]]: v.append("relatie %s: verwijderen = %s, verwacht %s" % (r["schema"], x["CascadeConfiguration"]["Delete"], VERWIJDEREN[r["verwijderen"]]))
    hand.append("beveiligingsrollen Inspecteur en Bevoegde beheerder: met de hand maken volgens 'rollen' in spec.yaml")
    return v, hand

def main():
    spec = laad_spec()
    dv = Dv(schrijven=False)
    w = dv.wie()
    print("Omgeving: %s (%s)\nAangemeld als: %s\n" % (w["organisatie"], dv.url, w["gebruiker"]))
    v, hand = controleer(dv, spec)
    print("Verschillen met spec.yaml: %d" % len(v))
    for x in v: print(" -", x)
    print("\nNiet door dit script gecontroleerd (handwerk): %d" % len(hand))
    for x in hand: print(" -", x)
    return 1 if v else 0

if __name__ == "__main__":
    try: sys.exit(main())
    except DvFout as e: sys.exit("FOUT %s" % e)
