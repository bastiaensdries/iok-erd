"""Bouwt het schema uit 03_output/spec.yaml in een Dataverse-omgeving (B85).

Gebruik:  python tools/dv_bouw.py --url https://<org>.crm4.dynamics.com            (proefdraai: toont wat er zou gebeuren)
          python tools/dv_bouw.py --url https://<org>.crm4.dynamics.com --uitvoeren (bouwt echt, na bevestiging)
          python tools/dv_bouw.py --offline                                        (geen netwerk: test enkel of alle aanvragen opgebouwd kunnen worden)

Maakt: publisher, solution, globale keuzelijsten, tabellen, kolommen, relaties (lookups), N:N, statusredenen, alternatieve sleutels.
Maakt NIET (handwerk, staat aan het einde opgelijst): formulekolommen, documentbeheer, beveiligingsrollen, formulieren, views, app, flows.
Herhaalbaar: wat al bestaat, wordt overgeslagen. Er wordt nooit iets verwijderd. Het enige dat gewijzigd wordt, is de primaire
kolom van de eigen tabellen (lengte en verplicht), omdat Dataverse die bij het aanmaken anders instelt dan gevraagd.
"""
import json, sys, time
from dv_gemeen import Dv, DvFout, laad_spec, label, label_tekst
import dv_controle

ED = "EntityDefinitions(LogicalName='%s')"
UITVOEREN, OFFLINE = "--uitvoeren" in sys.argv, "--offline" in sys.argv
gemaakt, bestond, fouten, plan = [], [], [], []

class Stub:
    url, solution, aantal_schrijf = "offline", None, 0
    def get(self, pad, mag_404=False): return None
    def alle(self, pad): return []
    def vraag(self, methode, pad, body=None, headers=None, mag_404=False):
        json.dumps(body); self.aantal_schrijf += 1; return None, {"OData-EntityId": "x(00000000-0000-0000-0000-000000000000)"}

def weergave(schema, lookup=False):
    s = schema[4:] if schema.startswith("iok_") else schema
    if lookup and s.endswith("id"): s = s[:-2]
    return s[:1].upper() + s[1:]

def verplicht(k):
    return {"Value": "ApplicationRequired" if k.get("verplicht") else "None", "CanBeChanged": True, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"}

def kolom(k, taal, optie_id):
    L = lambda x: label(x, taal)
    p = {"SchemaName": k["schema"], "DisplayName": L(weergave(k["schema"])), "RequiredLevel": verplicht(k)}
    t = k["type"]
    def soort(naam, typ): p.update({"@odata.type": "Microsoft.Dynamics.CRM.%sAttributeMetadata" % naam, "AttributeType": typ, "AttributeTypeName": {"Value": typ + "Type"}})
    if t in ("text", "autonumber"):
        soort("String", "String"); p.update({"MaxLength": k.get("lengte") or 100, "FormatName": {"Value": "Url" if k.get("formaat") == "url" else "Text"}})
        if t == "autonumber": p["AutoNumberFormat"] = k["formaat"]
    elif t == "memo": soort("Memo", "Memo"); p.update({"Format": "TextArea", "MaxLength": k["lengte"]})
    elif t == "int": soort("Integer", "Integer"); p.update({"Format": "None", "MinValue": -2147483648, "MaxValue": 2147483647})
    elif t == "decimal": soort("Decimal", "Decimal"); p.update({"Precision": k["precisie"], "MinValue": -100000000000, "MaxValue": 100000000000})
    elif t == "date": soort("DateTime", "DateTime"); p.update({"Format": "DateOnly", "DateTimeBehavior": {"Value": "DateOnly"}})
    elif t == "datetime": soort("DateTime", "DateTime"); p.update({"Format": "DateAndTime", "DateTimeBehavior": {"Value": "UserLocal"}})
    elif t == "bool":
        soort("Boolean", "Boolean")
        p.update({"DefaultValue": bool(k.get("standaard", False)), "OptionSet": {"@odata.type": "Microsoft.Dynamics.CRM.BooleanOptionSetMetadata", "OptionSetType": "Boolean",
                  "TrueOption": {"Value": 1, "Label": L("Ja")}, "FalseOption": {"Value": 0, "Label": L("Nee")}}})
    elif t == "choice":
        soort("Picklist", "Picklist"); p["GlobalOptionSet@odata.bind"] = "/GlobalOptionSetDefinitions(%s)" % optie_id(k["keuzelijst"])
    else: raise ValueError(t)
    return p

def cascade(soort, kind_org):
    c = dict.fromkeys(["Assign", "Delete", "Merge", "Reparent", "Share", "Unshare", "RollupView"], "NoCascade")
    if soort == "restrict": c["Delete"] = "Restrict"
    elif soort == "removelink": c["Delete"] = "RemoveLink"
    elif soort == "cascade":
        c["Delete"] = "Cascade"
        if not kind_org: c.update({"Assign": "Cascade", "Reparent": "Cascade", "Share": "Cascade", "Unshare": "Cascade"})
    return c

def doe(wat, bestaat, maak):
    try:
        if bestaat(): bestond.append(wat); return
        if not (UITVOEREN or OFFLINE): plan.append(wat); return
        maak(); gemaakt.append(wat)
        if UITVOEREN: print("  + " + wat, flush=True)
    except DvFout as e:
        fouten.append("%s -> %s" % (wat, e)); print("  ! " + wat + " -> " + str(e), flush=True)

def main():
    spec = laad_spec()
    sol, prefix = spec["solution"]["naam"], spec["publisher"]["prefix"]
    if OFFLINE: dv, w = Stub(), {"organisatie": "offline", "gebruiker": "-", "taal": 1043}
    else:
        dv = Dv(schrijven=UITVOEREN); w = dv.wie()
    taal = w["taal"]; L = lambda x: label(x, taal)
    print("Omgeving: %s (%s)\nAangemeld als: %s\nSolution: %s, prefix %s_\n" % (w["organisatie"], dv.url, w["gebruiker"], sol, prefix))
    if UITVOEREN and "--ja" not in sys.argv:
        if input("Dit maakt tabellen en kolommen aan in bovenstaande omgeving. Typ BOUW om door te gaan: ").strip() != "BOUW": return 2
    tab = {t["schema"]: t for t in spec["tabellen"]}
    # 1. publisher en solution (zonder solution-header)
    pub = {}
    def pub_bestaat():
        r = dv.alle("publishers?$select=publisherid,uniquename&$filter=customizationprefix eq '%s'" % prefix)
        if r: pub["id"] = r[0]["publisherid"]
        return bool(r)
    def pub_maak():
        _, h = dv.vraag("POST", "publishers", {"uniquename": prefix, "friendlyname": spec["publisher"]["naam"], "customizationprefix": prefix, "customizationoptionvalueprefix": 10000})
        pub["id"] = h["OData-EntityId"].split("(")[-1].rstrip(")")
    doe("publisher %s" % prefix, pub_bestaat, pub_maak)
    doe("solution %s" % sol, lambda: bool(dv.alle("solutions?$select=solutionid&$filter=uniquename eq '%s'" % sol)),
        lambda: dv.vraag("POST", "solutions", {"uniquename": sol, "friendlyname": sol.replace("_", " "), "version": spec["solution"]["versie"] + ".0", "publisherid@odata.bind": "/publishers(%s)" % pub["id"]}))
    if fouten: print("Publisher of solution mislukt: gestopt."); return 1
    dv.solution = sol
    # 2. globale keuzelijsten
    opt = {}
    def optie_id(naam):
        if naam not in opt:
            o = dv.get("GlobalOptionSetDefinitions(Name='%s')" % naam, mag_404=True)
            opt[naam] = o["MetadataId"] if o else "00000000-0000-0000-0000-000000000000"
        return opt[naam]
    for k in spec["globale_keuzelijsten"]:
        doe("keuzelijst %s" % k["schema"], lambda k=k: bool(dv.get("GlobalOptionSetDefinitions(Name='%s')" % k["schema"], mag_404=True)),
            lambda k=k: dv.vraag("POST", "GlobalOptionSetDefinitions", {"@odata.type": "Microsoft.Dynamics.CRM.OptionSetMetadata", "Name": k["schema"], "DisplayName": L(weergave(k["schema"])),
                                 "IsGlobal": True, "OptionSetType": "Picklist", "Options": [{"Value": o["waarde"], "Label": L(o["label"])} for o in k["opties"]]}))
    # 3. tabellen (met hun primaire kolom)
    for t in spec["tabellen"]:
        if t["bestaand"]: continue
        pk = t["primaire_kolom"]
        pkk = {"schema": pk["schema"], "type": pk.get("type", "text"), "lengte": pk.get("lengte"), "formaat": pk.get("formaat"), "verplicht": pk.get("type") != "autonumber"}
        prim = kolom(pkk, taal, optie_id); prim["IsPrimaryName"] = True
        body = {"@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata", "SchemaName": t["schema"], "DisplayName": L(t["weergavenaam"]["enkelvoud"]),
                "DisplayCollectionName": L(t["weergavenaam"]["meervoud"]), "Description": L(t["weergavenaam"]["enkelvoud"] + " (IOK datamodel v3)"),
                "OwnershipType": "OrganizationOwned" if t["eigenaarschap"] == "organization" else "UserOwned",
                "IsActivity": False, "HasNotes": bool(t.get("notities")), "HasActivities": bool(t.get("activiteiten")), "Attributes": [prim]}
        doe("tabel %s" % t["schema"], lambda t=t: bool(dv.get((ED % t["schema"]) + "?$select=LogicalName", mag_404=True)), lambda body=body: dv.vraag("POST", "EntityDefinitions", body))
    # 3b. primaire kolommen nakijken: Dataverse maakt ze bij het aanmaken van de tabel met lengte 850 en niet-verplicht aan,
    #     wat de aanvraag ook zegt (vastgesteld bij de eerste bouw, 2026-11-15). Te lang voor een sleutel (max. 1700 bytes).
    for t in spec["tabellen"]:
        if t["bestaand"]: continue
        pk = t["primaire_kolom"]; wil_len = pk.get("lengte"); wil_req = "None" if pk.get("type") == "autonumber" else "ApplicationRequired"
        pad = (ED % t["schema"]) + "/Attributes(LogicalName='%s')" % pk["schema"]
        def pk_goed(pad=pad, wil_len=wil_len, wil_req=wil_req):
            a = dv.get(pad + "/Microsoft.Dynamics.CRM.StringAttributeMetadata?$select=MaxLength,RequiredLevel", mag_404=True)
            return a is None or ((wil_len is None or a["MaxLength"] == wil_len) and a["RequiredLevel"]["Value"] == wil_req)
        def pk_zet(pad=pad, wil_len=wil_len, wil_req=wil_req):
            a = dv.get(pad + "/Microsoft.Dynamics.CRM.StringAttributeMetadata")
            a = {k: v for k, v in a.items() if not k.startswith("@odata.")}
            a["@odata.type"] = "Microsoft.Dynamics.CRM.StringAttributeMetadata"
            if wil_len: a["MaxLength"] = wil_len
            a["RequiredLevel"]["Value"] = wil_req
            dv.vraag("PUT", pad, a, headers={"MSCRM.MergeLabels": "true"})
        doe("primaire kolom %s.%s bijwerken (lengte %s, %s)" % (t["schema"], pk["schema"], wil_len or "ongewijzigd", "verplicht" if wil_req != "None" else "niet verplicht"), pk_goed, pk_zet)
    # 4. kolommen (geen lookups, geen formules)
    hand = []
    def kol_bestaat(t, c):
        return bool(dv.get((ED % t) + "/Attributes(LogicalName='%s')?$select=LogicalName" % c, mag_404=True))
    for t in spec["tabellen"]:
        for k in t["kolommen"]:
            if k["type"] == "lookup": continue
            if k.get("formule"):
                hand.append("formulekolom %s.%s (%s%s) = %s" % (t["schema"], k["schema"], k["type"], ", %s decimalen" % k["precisie"] if k.get("precisie") else "", k["formule"])); continue
            doe("kolom %s.%s" % (t["schema"], k["schema"]), lambda t=t, k=k: kol_bestaat(t["schema"], k["schema"]),
                lambda t=t, k=k: dv.vraag("POST", (ED % t["schema"]) + "/Attributes", kolom(k, taal, optie_id)))
    # 5. relaties 1:N (maken de lookupkolom aan) en N:N
    for r in spec["relaties"]:
        if r.get("bestaand"): continue
        if r["type"] == "NN":
            a, b = r["tabellen"]
            menu = lambda x: {"Behavior": "UseCollectionName", "Group": "Details", "Order": 10000}
            body = {"@odata.type": "Microsoft.Dynamics.CRM.ManyToManyRelationshipMetadata", "SchemaName": r["schema"], "IntersectEntityName": r["schema"],
                    "Entity1LogicalName": a, "Entity2LogicalName": b, "Entity1AssociatedMenuConfiguration": menu(a), "Entity2AssociatedMenuConfiguration": menu(b)}
        else:
            kind = tab[r["naar"]]
            lk = {"@odata.type": "Microsoft.Dynamics.CRM.LookupAttributeMetadata", "AttributeType": "Lookup", "AttributeTypeName": {"Value": "LookupType"},
                  "SchemaName": r["lookup"], "DisplayName": L(weergave(r["lookup"], True)), "RequiredLevel": verplicht(r)}
            body = {"@odata.type": "Microsoft.Dynamics.CRM.OneToManyRelationshipMetadata", "SchemaName": r["schema"], "ReferencedEntity": r["van"], "ReferencingEntity": r["naar"],
                    "CascadeConfiguration": cascade(r["verwijderen"], kind.get("eigenaarschap") == "organization"),
                    "AssociatedMenuConfiguration": {"Behavior": "UseCollectionName", "Group": "Details", "Order": 10000}, "Lookup": lk}
        doe("relatie %s" % r["schema"], lambda r=r: bool(dv.get("RelationshipDefinitions(SchemaName='%s')?$select=SchemaName" % r["schema"], mag_404=True)),
            lambda body=body: dv.vraag("POST", "RelationshipDefinitions", body))
    # 6. statusredenen: eerste actieve/inactieve hernoemt de standaardwaarde (1 / 2), de rest wordt toegevoegd
    for t in spec["tabellen"]:
        sr = t.get("statusredenen")
        if not sr or (sr["actief"], sr["inactief"]) == (["Actief"], ["Inactief"]): continue
        def huidig(t=t):
            o = dv.get((ED % t["schema"]) + "/Attributes(LogicalName='statuscode')/Microsoft.Dynamics.CRM.StatusAttributeMetadata?$select=LogicalName&$expand=OptionSet($select=Options)", mag_404=True)
            return {(x["State"], label_tekst(x["Label"])) for x in o["OptionSet"]["Options"]} if o else set()
        for staat, labels in ((0, sr["actief"]), (1, sr["inactief"])):
            for i, lab in enumerate(labels):
                if i == 0:
                    maak = lambda t=t, staat=staat, lab=lab: dv.vraag("POST", "UpdateOptionValue", {"EntityLogicalName": t["schema"], "AttributeLogicalName": "statuscode", "Value": staat + 1, "Label": L(lab), "MergeLabels": False, "SolutionUniqueName": sol})
                else:
                    maak = lambda t=t, staat=staat, lab=lab: dv.vraag("POST", "InsertStatusValue", {"EntityLogicalName": t["schema"], "AttributeLogicalName": "statuscode", "Label": L(lab), "StateCode": staat, "SolutionUniqueName": sol})
                doe("statusreden %s: %s" % (t["schema"], lab), lambda staat=staat, lab=lab, huidig=huidig: (staat, lab) in huidig(), maak)
    # 7. alternatieve sleutels (index wordt op de achtergrond gemaakt)
    for t in spec["tabellen"]:
        for s in t.get("alternatieve_sleutels", []):
            def sl_bestaat(t=t, s=s):
                e = dv.get((ED % t["schema"]) + "/Keys?$select=SchemaName,KeyAttributes", mag_404=True)
                return any(sorted(x["KeyAttributes"]) == sorted(s["kolommen"]) for x in (e or {}).get("value", []))
            doe("sleutel %s" % s["schema"], sl_bestaat, lambda t=t, s=s: dv.vraag("POST", (ED % t["schema"]) + "/Keys", {"SchemaName": s["schema"], "DisplayName": L(" + ".join(weergave(k) for k in s["kolommen"])), "KeyAttributes": s["kolommen"]}))
    if UITVOEREN:
        try: dv.vraag("POST", "PublishAllXml", {})
        except DvFout as e: fouten.append("publiceren -> %s" % e)
        print("\nWachten tot de sleutels actief zijn (max. 15 minuten)...", flush=True)
        einde = time.time() + 900
        while time.time() < einde:
            bezig = []
            for t in spec["tabellen"]:
                if t.get("alternatieve_sleutels"):
                    for x in dv.get((ED % t["schema"]) + "/Keys?$select=SchemaName,EntityKeyIndexStatus")["value"]:
                        if x["EntityKeyIndexStatus"] != "Active": bezig.append("%s (%s)" % (x["SchemaName"], x["EntityKeyIndexStatus"]))
            if not bezig or any("Failed" in b for b in bezig): break
            print("  nog niet actief: %d (%s)" % (len(bezig), time.strftime("%H:%M:%S")), flush=True)
            time.sleep(15)
        if bezig: fouten.append("sleutels niet actief: " + ", ".join(bezig))
    print("\nBestond al: %d · %s: %d · fouten: %d" % (len(bestond), "aangemaakt" if UITVOEREN else ("aanvragen opgebouwd" if OFFLINE else "zou aanmaken"), len(gemaakt) if (UITVOEREN or OFFLINE) else len(plan), len(fouten)))
    if not (UITVOEREN or OFFLINE):
        for p in plan: print("  zou aanmaken:", p)
        print("\nDit was een proefdraai: er is niets gewijzigd. Voeg --uitvoeren toe om te bouwen.")
    for f in fouten: print("  FOUT:", f)
    print("\nMet de hand te doen (dit script doet dat niet):")
    for h in hand: print(" -", h)
    print(" - documentbeheer (SharePoint) aanzetten op iok_inspectiedossier (B60)\n - beveiligingsrollen Inspecteur en Bevoegde beheerder ('rollen' in spec.yaml)\n - formulieren, views, app, flows en de regels uit datamodel_v3.md §11")
    if UITVOEREN:
        print("\nControle tegen spec.yaml:")
        v, _ = dv_controle.controleer(Dv(url=dv.url, schrijven=False), spec)
        print("Verschillen: %d" % len(v))
        for x in v: print(" -", x)
        return 1 if (v or fouten) else 0
    return 1 if fouten else 0

if __name__ == "__main__":
    try: sys.exit(main())
    except DvFout as e: sys.exit("FOUT %s" % e)
