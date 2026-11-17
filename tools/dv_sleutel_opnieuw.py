"""Laat Dataverse de index van hangende of mislukte alternatieve sleutels opnieuw opbouwen (ReactivateEntityKey).
Wijzigt geen tabellen, kolommen of gegevens. Gebruik:  python tools/dv_sleutel_opnieuw.py --url https://<org>... --uitvoeren"""
import sys, time
from dv_gemeen import Dv, DvFout, laad_spec

def toestand(dv, spec):
    uit = []
    for t in spec["tabellen"]:
        if t.get("alternatieve_sleutels"):
            for k in dv.get("EntityDefinitions(LogicalName='%s')/Keys" % t["schema"])["value"]:
                if k["EntityKeyIndexStatus"] != "Active": uit.append((t["schema"], k["LogicalName"], k["EntityKeyIndexStatus"], k.get("AsyncJob")))
    return uit

def main():
    spec = laad_spec(); uitvoeren = "--uitvoeren" in sys.argv
    dv = Dv(schrijven=uitvoeren)
    hangend = toestand(dv, spec)
    print("Niet-actieve sleutels: %d" % len(hangend))
    for tabel, sleutel, status, _ in hangend: print(" - %s.%s (%s)" % (tabel, sleutel, status))
    if not hangend or not uitvoeren:
        if hangend: print("Proefdraai: voeg --uitvoeren toe om de index opnieuw te laten opbouwen.")
        return 0
    for tabel, sleutel, status, _ in hangend:
        try:
            dv.vraag("POST", "ReactivateEntityKey", {"EntityLogicalName": tabel, "EntityKeyLogicalName": sleutel})
            print("  opnieuw gestart: %s.%s" % (tabel, sleutel), flush=True)
        except DvFout as e: print("  ! %s.%s -> %s" % (tabel, sleutel, e), flush=True)
    print("Wachten (max. 4 minuten)...", flush=True)
    for i in range(16):
        time.sleep(15)
        hangend = toestand(dv, spec)
        print("  na %3d s: %s" % ((i + 1) * 15, ", ".join("%s=%s" % (s, st) for _, s, st, _ in hangend) or "alles actief"), flush=True)
        if not hangend or all(st == "Failed" for _, _, st, _ in hangend): break
    for tabel, sleutel, status, job in hangend:
        if job:
            a = dv.get("asyncoperations(%s)?$select=statuscode,message,friendlymessage" % job, mag_404=True) or {}
            print(" - %s: %s | job status %s | %s" % (sleutel, status, a.get("statuscode"), (a.get("friendlymessage") or a.get("message") or "-")[:700]))
    return 1 if hangend else 0

if __name__ == "__main__":
    try: sys.exit(main())
    except DvFout as e: sys.exit("FOUT %s" % e)
