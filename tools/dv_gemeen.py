"""Gedeelde code voor de Dataverse-scripts (dv_controle, dv_bouw, dv_laden). Alleen de standaardbibliotheek.

Omgeving:  --url https://<org>.crm4.dynamics.com   of omgevingsvariabele DV_URL   of het bestand .dv_omgeving
Aanmelden: device code (je krijgt een code en een link, je logt in in de browser). Het token staat in
           .dv_token.json (staat in .gitignore; niet delen). Alternatief: omgevingsvariabele DV_TOKEN.
           Client-ID: de app-registratie die Microsoft voor voorbeeldcode publiceert; eigen app via DV_CLIENT_ID.
"""
import json, os, sys, time, urllib.error, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CLIENT_ID = os.environ.get("DV_CLIENT_ID", "51f81489-12ee-4a9e-aaae-a2591f45987d")
TOKENBESTAND = ROOT / ".dv_token.json"
LOGIN = "https://login.microsoftonline.com/organizations/oauth2/v2.0/"
API = "/api/data/v9.2/"

class DvFout(Exception):
    def __init__(self, status, tekst):
        super().__init__("%s: %s" % (status, tekst)); self.status = status; self.tekst = tekst

def laad_spec():
    j = ROOT / "03_output/spec.json"
    if j.exists(): return json.loads(j.read_text(encoding="utf-8"))
    import yaml
    return yaml.safe_load((ROOT / "03_output/spec.yaml").read_text(encoding="utf-8"))

def arg(naam, standaard=None):
    return sys.argv[sys.argv.index(naam) + 1] if naam in sys.argv and sys.argv.index(naam) + 1 < len(sys.argv) else standaard

def omgeving():
    url = arg("--url") or os.environ.get("DV_URL")
    f = ROOT / ".dv_omgeving"
    if not url and f.exists(): url = f.read_text(encoding="utf-8").strip()
    if not url: raise SystemExit("Geen omgeving. Geef --url https://<org>.crm4.dynamics.com (of zet de URL in het bestand .dv_omgeving).")
    url = url.rstrip("/")
    if not url.startswith("https://") or ".dynamics.com" not in url: raise SystemExit("Dit lijkt geen Dataverse-URL: " + url)
    return url

def _post(url, data):
    req = urllib.request.Request(url, data=urllib.parse.urlencode(data).encode(), headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r: return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read() or b"{}")

def token(url):
    if os.environ.get("DV_TOKEN"): return os.environ["DV_TOKEN"]
    scope = url + "/user_impersonation offline_access"
    cache = json.loads(TOKENBESTAND.read_text(encoding="utf-8")) if TOKENBESTAND.exists() else {}
    c = cache.get(url, {})
    if c.get("access_token") and c.get("verloopt", 0) > time.time() + 120: return c["access_token"]
    t = None
    if c.get("refresh_token"):
        t = _post(LOGIN + "token", {"grant_type": "refresh_token", "client_id": CLIENT_ID, "refresh_token": c["refresh_token"], "scope": scope})
        if "access_token" not in t: t = None
    if not t:
        d = _post(LOGIN + "devicecode", {"client_id": CLIENT_ID, "scope": scope})
        if "device_code" not in d: raise SystemExit("Aanmelden kan niet starten: %s" % d.get("error_description", d))
        print("\n" + d.get("message", "Ga naar %s en geef de code %s in." % (d.get("verification_uri"), d.get("user_code"))) + "\n", flush=True)
        einde, wacht = time.time() + int(d.get("expires_in", 900)), int(d.get("interval", 5))
        while time.time() < einde:
            time.sleep(wacht)
            t = _post(LOGIN + "token", {"grant_type": "urn:ietf:params:oauth:grant-type:device_code", "client_id": CLIENT_ID, "device_code": d["device_code"]})
            if "access_token" in t: break
            if t.get("error") == "slow_down": wacht += 5
            elif t.get("error") != "authorization_pending": raise SystemExit("Aanmelden mislukt: %s" % t.get("error_description", t))
        else:
            raise SystemExit("Aanmelden verlopen: niet op tijd ingelogd.")
    cache[url] = {"access_token": t["access_token"], "refresh_token": t.get("refresh_token", c.get("refresh_token")), "verloopt": time.time() + int(t.get("expires_in", 3600))}
    TOKENBESTAND.write_text(json.dumps(cache), encoding="utf-8")
    return t["access_token"]

class Dv:
    """Kleine Web API-client. Met schrijven=False weigert hij alles behalve GET."""
    def __init__(self, url=None, schrijven=False, solution=None):
        self.url = url or omgeving(); self.schrijven = schrijven; self.solution = solution
        self.aantal_schrijf = 0

    def vraag(self, methode, pad, body=None, headers=None, mag_404=False):
        if methode != "GET" and not self.schrijven: raise DvFout(0, "alleen-lezen: %s %s geweigerd" % (methode, pad))
        volledig = pad if pad.startswith("http") else self.url + API + pad
        volledig = urllib.parse.quote(volledig, safe=":/?&=$(),'@+*;!~-._%")   # spaties e.d. in $filter coderen
        h = {"Authorization": "Bearer " + token(self.url), "Accept": "application/json", "OData-MaxVersion": "4.0", "OData-Version": "4.0",
             "Content-Type": "application/json; charset=utf-8"}
        if self.solution and methode != "GET": h["MSCRM.SolutionUniqueName"] = self.solution
        h.update(headers or {})
        data = json.dumps(body).encode("utf-8") if body is not None else None
        for poging in range(6):
            req = urllib.request.Request(volledig, data=data, headers=h, method=methode)
            try:
                with urllib.request.urlopen(req, timeout=300) as r:
                    if methode != "GET": self.aantal_schrijf += 1
                    inhoud = r.read()
                    return (json.loads(inhoud) if inhoud else None), dict(r.headers)
            except urllib.error.HTTPError as e:
                inhoud = e.read().decode("utf-8", "replace")
                if e.code == 404 and mag_404: return None, {}
                if e.code in (429, 503) and poging < 5:
                    time.sleep(int(e.headers.get("Retry-After", 5 * (poging + 1)))); continue
                try: tekst = json.loads(inhoud)["error"]["message"]
                except Exception: tekst = inhoud[:500]
                raise DvFout(e.code, tekst)
            except urllib.error.URLError as e:
                if poging < 5: time.sleep(5 * (poging + 1)); continue
                raise DvFout(0, "geen verbinding: %s" % e.reason)

    def get(self, pad, mag_404=False):
        return self.vraag("GET", pad, mag_404=mag_404)[0]

    def alle(self, pad):
        uit, d = [], self.get(pad)
        while d:
            uit += d.get("value", [])
            d = self.get(d["@odata.nextLink"]) if d.get("@odata.nextLink") else None
        return uit

    def wie(self):
        w = self.get("WhoAmI")
        o = self.get("organizations?$select=name,languagecode")["value"][0]
        u = self.get("systemusers(%s)?$select=fullname" % w["UserId"])
        return {"gebruiker": u["fullname"], "userid": w["UserId"], "organisatie": o["name"], "taal": o["languagecode"]}

def label(tekst, taal):
    return {"@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": tekst, "LanguageCode": taal}]}

def kolomnaam(k):
    """Weergavenaam van een kolom uit spec.yaml: 'weergavenaam' als die er is (B93),
    anders afgeleid uit de schemanaam (zonder iok_, een lookup zonder 'id', eerste letter hoofdletter)."""
    if k.get("weergavenaam"): return k["weergavenaam"]
    s = k["schema"][4:] if k["schema"].startswith("iok_") else k["schema"]
    if k.get("type") == "lookup" and s.endswith("id"): s = s[:-2]
    return s[:1].upper() + s[1:]

def label_tekst(l):
    if not l: return ""
    if l.get("UserLocalizedLabel"): return l["UserLocalizedLabel"].get("Label", "")
    return (l.get("LocalizedLabels") or [{}])[0].get("Label", "")
