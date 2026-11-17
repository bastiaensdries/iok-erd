"""Proef (B86): zoekt uit met welke aanvraag Dataverse de naamkolom van een nieuwe tabel op de gevraagde lengte aanmaakt.

Maakt een paar wegwerptabellen iok_zzproef<letter>, leest de werkelijke lengte (MaxLength en DatabaseLength) en
verwijdert ze weer. Raakt geen enkele andere tabel aan: het script weigert alles wat niet met iok_zzproef begint.

Gebruik:  python tools/dv_proef.py --url https://<org>.crm4.dynamics.com --uitvoeren
          python tools/dv_proef.py --url ... --opruimen     (enkel achtergebleven proeftabellen verwijderen)
"""
import sys, time
from dv_gemeen import Dv, DvFout, laad_spec, label

ED = "EntityDefinitions(LogicalName='%s')"
LENGTE = 120

def varianten(taal):
    L = lambda x: label(x, taal)
    req = lambda v: {"Value": v, "CanBeChanged": True, "ManagedPropertyLogicalName": "canmodifyrequirementlevelsettings"}
    def attr(naam, **extra):
        a = {"@odata.type": "Microsoft.Dynamics.CRM.StringAttributeMetadata", "AttributeType": "String", "AttributeTypeName": {"Value": "StringType"},
             "SchemaName": naam, "DisplayName": L("Naam"), "RequiredLevel": req("ApplicationRequired"), "MaxLength": LENGTE, "FormatName": {"Value": "Text"}, "IsPrimaryName": True}
        a.update(extra); return a
    def tabel(naam, a, **extra):
        e = {"@odata.type": "Microsoft.Dynamics.CRM.EntityMetadata", "SchemaName": naam, "DisplayName": L("Proef " + naam[-1]), "DisplayCollectionName": L("Proeven " + naam[-1]),
             "Description": L("Wegwerptabel van dv_proef.py"), "OwnershipType": "OrganizationOwned", "IsActivity": False, "HasNotes": False, "HasActivities": False, "Attributes": [a]}
        e.update(extra); return e
    return [
        ("a", "zoals dv_bouw.py het deed", tabel("iok_zzproefa", attr("iok_naam"))),
        ("b", "met PrimaryNameAttribute op de tabel", tabel("iok_zzproefb", attr("iok_naam"), PrimaryNameAttribute="iok_naam")),
        ("c", "met DatabaseLength op de kolom", tabel("iok_zzproefc", attr("iok_naam", DatabaseLength=LENGTE * 2))),
        ("d", "zoals het voorbeeld van Microsoft (hoofdletters in de schemanaam, beschrijving, niet verplicht)",
         tabel("iok_ZzProefD", attr("iok_Naam", Description=L("Naam"), RequiredLevel=req("None")), PrimaryNameAttribute="iok_naam")),
        ("e", "zonder FormatName, met Format", tabel("iok_zzproefe", {k: v for k, v in attr("iok_naam", Format="Text").items() if k != "FormatName"})),
    ]

def proeftabellen(dv):
    return [e["LogicalName"] for e in dv.alle("EntityDefinitions?$select=LogicalName") if e["LogicalName"].startswith("iok_zzproef")]

def verwijder(dv, logisch):
    assert logisch.startswith("iok_zzproef"), "dit script verwijdert enkel proeftabellen"
    dv.vraag("DELETE", ED % logisch)

def main():
    spec = laad_spec()
    if "--uitvoeren" not in sys.argv and "--opruimen" not in sys.argv:
        print("Dit script maakt 5 wegwerptabellen (iok_zzproefa..e) en verwijdert ze weer. Voeg --uitvoeren toe."); return 0
    dv = Dv(schrijven=True, solution=spec["solution"]["naam"]); w = dv.wie()
    print("Omgeving: %s (%s)\nAangemeld als: %s\n" % (w["organisatie"], dv.url, w["gebruiker"]))
    if "--opruimen" not in sys.argv:
        if input("Typ PROEF om 5 wegwerptabellen te maken en weer te verwijderen: ").strip() != "PROEF": return 2
        for letter, wat, body in varianten(w["taal"]):
            logisch = body["SchemaName"].lower()
            try:
                dv.vraag("POST", "EntityDefinitions", body)
                a = dv.get((ED % logisch) + "/Attributes(LogicalName='iok_naam')/Microsoft.Dynamics.CRM.StringAttributeMetadata?$select=MaxLength,DatabaseLength,RequiredLevel")
                goed = a["DatabaseLength"] is not None and a["DatabaseLength"] <= LENGTE * 2 + 100
                print("%s. %-95s MaxLength %s, DatabaseLength %s, verplicht %s  %s" % (letter, wat, a["MaxLength"], a["DatabaseLength"], a["RequiredLevel"]["Value"], "<== GOED" if goed else ""), flush=True)
            except DvFout as e:
                print("%s. %-95s geweigerd: %s" % (letter, wat, str(e)[:300]), flush=True)
    print("\nOpruimen...", flush=True)
    for logisch in proeftabellen(dv):
        for poging in range(3):
            try: verwijder(dv, logisch); print("  verwijderd: " + logisch, flush=True); break
            except DvFout as e:
                if poging == 2: print("  ! %s niet verwijderd: %s" % (logisch, str(e)[:300]), flush=True)
                else: time.sleep(10)
    over = proeftabellen(dv)
    print("Proeftabellen die er nog staan: %s" % (", ".join(over) or "geen"))
    return 0

if __name__ == "__main__":
    try: sys.exit(main())
    except DvFout as e: sys.exit("FOUT %s" % e)
