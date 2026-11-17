"""NIET MEER NODIG (B88): de drie sleutels zijn vanzelf actief geworden. Dit script laat actieve sleutels altijd staan.
Verwijdert de drie hangende sleutels op de naamkolom (B87). Enkel deze drie, en enkel als ze NIET actief zijn.
Gebruik:  python tools/dv_sleutel_weg.py --url https://<org>.crm4.dynamics.com            (toont wat er zou gebeuren)
          python tools/dv_sleutel_weg.py --url https://<org>.crm4.dynamics.com --uitvoeren"""
import sys
from dv_gemeen import Dv, DvFout

WEG = {"iok_terreingroep": "iok_ak_terreingroep_bestuurid_naam", "iok_checklist": "iok_ak_checklist_naam_versie",
       "iok_checklistonderdeel": "iok_ak_checklistonderdeel_checklistid_naam"}

def main():
    uitvoeren = "--uitvoeren" in sys.argv
    dv = Dv(schrijven=uitvoeren, solution="IOK_Speelterreinen"); w = dv.wie()
    print("Omgeving: %s (%s)\nAangemeld als: %s\n" % (w["organisatie"], dv.url, w["gebruiker"]))
    fouten = 0
    for tabel, sleutel in WEG.items():
        keys = dv.get("EntityDefinitions(LogicalName='%s')/Keys" % tabel)["value"]
        k = next((x for x in keys if x["LogicalName"] == sleutel), None)
        if not k: print("  bestaat niet (meer): %s" % sleutel); continue
        if k["EntityKeyIndexStatus"] == "Active": print("  ! %s is actief: blijft staan" % sleutel); continue
        if not uitvoeren: print("  zou verwijderen: %s (%s)" % (sleutel, k["EntityKeyIndexStatus"])); continue
        try:
            dv.vraag("DELETE", "EntityDefinitions(LogicalName='%s')/Keys(%s)" % (tabel, k["MetadataId"]))
            print("  verwijderd: %s" % sleutel, flush=True)
        except DvFout as e: fouten += 1; print("  ! %s niet verwijderd -> %s" % (sleutel, e), flush=True)
    if not uitvoeren: print("\nProefdraai: voeg --uitvoeren toe om te verwijderen.")
    return 1 if fouten else 0

if __name__ == "__main__":
    try: sys.exit(main())
    except DvFout as e: sys.exit("FOUT %s" % e)
