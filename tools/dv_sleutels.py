"""Toont de toestand van de alternatieve sleutels en hun indexjob. ALLEEN-LEZEN.
Gebruik:  python tools/dv_sleutels.py --url https://<org>.crm4.dynamics.com"""
import json, sys
from dv_gemeen import Dv, DvFout, laad_spec

def main():
    spec = laad_spec(); dv = Dv(schrijven=False)
    for t in spec["tabellen"]:
        if not t.get("alternatieve_sleutels"): continue
        naam = t["schema"]
        keys = dv.get("EntityDefinitions(LogicalName='%s')/Keys" % naam)["value"]
        for k in keys:
            status = k.get("EntityKeyIndexStatus")
            print("%-55s %s" % (k["SchemaName"], status))
            if status == "Active": continue
            job = k.get("AsyncJob")
            print("   kolommen: %s" % k.get("KeyAttributes"))
            print("   AsyncJob: %s" % json.dumps(job, ensure_ascii=False))
            jid = job.get("Id") if isinstance(job, dict) else job
            if jid:
                try:
                    a = dv.get("asyncoperations(%s)?$select=name,statecode,statuscode,message,friendlymessage,createdon,startedon,completedon,retrycount" % jid, mag_404=True)
                    STATUS = {0: "wacht op middelen", 10: "wacht", 20: "bezig", 21: "pauzeert", 22: "annuleert", 30: "geslaagd", 31: "MISLUKT", 32: "geannuleerd"}
                    if a: print("   job: %s | aangemaakt %s | gestart %s | klaar %s | pogingen %s\n   melding: %s" % (STATUS.get(a.get("statuscode"), a.get("statuscode")), a.get("createdon"), a.get("startedon"), a.get("completedon"), a.get("retrycount"), (a.get("friendlymessage") or a.get("message") or "-")[:600]))
                    else: print("   job bestaat niet meer")
                except DvFout as e: print("   job niet leesbaar: %s" % e)
            for c in k.get("KeyAttributes", []):
                try: a = dv.get("EntityDefinitions(LogicalName='%s')/Attributes(LogicalName='%s')/Microsoft.Dynamics.CRM.StringAttributeMetadata?$select=MaxLength,DatabaseLength" % (naam, c), mag_404=True)
                except DvFout: a = None
                if a: print("   %s: MaxLength %s, DatabaseLength %s" % (c, a.get("MaxLength"), a.get("DatabaseLength")))

if __name__ == "__main__":
    try: sys.exit(main())
    except DvFout as e: sys.exit("FOUT %s" % e)
