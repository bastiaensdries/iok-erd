import csv, io, os, sys, html
DATA = os.path.join(os.environ["HOME"], "mnt", "ERD", "04_data")
def lees(n):
    with io.open(os.path.join(DATA, n + ".csv"), encoding="utf-8-sig") as f: return list(csv.DictReader(f))
def e(t): return html.escape(t or "")
def datum_nl(iso):
    m = ["januari","februari","maart","april","mei","juni","juli","augustus","september","oktober","november","december"]
    try:
        j, mm, d = iso.split("-"); return "%d %s %s" % (int(d), m[int(mm)-1], j)
    except Exception: return iso

dos = lees("iok_inspectiedossier")[0]
beoordelingen = lees("iok_beoordeling"); resultaten = lees("iok_resultaat")
toestellen = {r["_sleutel"]: r for r in lees("iok_speeltoestel")}
punten = {r["_sleutel"]: r for r in lees("iok_controlepunt")}
onderdelen = {r["_sleutel"]: r for r in lees("iok_checklistonderdeel")}
besturen = {r["_sleutel"]: r for r in lees("account")}
bestuur = besturen.get(dos["iok_bestuurid"], {})
per_beo = {}
for r in resultaten: per_beo.setdefault(r["iok_beoordelingid"], []).append(r)
beo = sorted(beoordelingen, key=lambda b: int(b["iok_volgorde"] or 0))
n_toe = sum(1 for b in beo if b["iok_soort"] == "Toestel")
n_nb = sum(1 for b in beo if b["iok_besluit"] == "Niet beoordeeld")

S = []; A = S.append
A("<!DOCTYPE html><html lang='nl'><head><meta charset='utf-8'>")
A("<meta name='viewport' content='width=device-width, initial-scale=1'>")
A("<title>Verslag %s - %s</title>" % (e(dos["iok_terreincode"]), e(datum_nl(dos["iok_controledatum"]))))
A("""<style>
*{box-sizing:border-box}
body{margin:0;background:#f4f4f2;color:#1b1b1a;font:16px/1.55 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
.blad{max-width:820px;margin:0 auto;background:#fff;padding:32px 28px 56px;min-height:100vh}
h1{font-size:25px;line-height:1.25;margin:0 0 4px;font-weight:650;letter-spacing:-.01em}
.sub{color:#6b6b68;font-size:15px;margin:0 0 26px}
h2{font-size:13px;letter-spacing:.07em;text-transform:uppercase;color:#6b6b68;font-weight:650;margin:38px 0 14px;padding-bottom:7px;border-bottom:1px solid #e3e3df}
dl{display:grid;grid-template-columns:150px 1fr;gap:7px 18px;margin:0}
dt{color:#6b6b68;font-size:14px}
dd{margin:0}
.cijfers{display:flex;gap:10px;flex-wrap:wrap;margin:20px 0 0}
.cijfer{flex:1;min-width:104px;border:1px solid #e3e3df;border-radius:9px;padding:12px 13px;background:#fafaf8}
.cijfer b{display:block;font-size:26px;font-weight:650;line-height:1.1;letter-spacing:-.02em}
.cijfer span{font-size:12.5px;color:#6b6b68}
.toestel{border:1px solid #e3e3df;border-radius:9px;margin:0 0 11px;overflow:hidden}
.kop{display:flex;align-items:baseline;gap:11px;padding:13px 15px;flex-wrap:wrap}
.kop .code{font-weight:650;font-size:16px;letter-spacing:-.01em}
.kop .naam{color:#54544f;font-size:14.5px;flex:1;min-width:120px}
.vlag{font-size:12px;font-weight:600;padding:3px 9px;border-radius:999px;white-space:nowrap}
.ok{background:#e4f0e6;color:#20572c}
.nb{background:#ececea;color:#5a5a56}
.nokv{background:#fbe6e2;color:#8a2d1c}
.leeg{background:#fff4df;color:#7a5410}
.tekst{padding:0 15px 13px;color:#54544f;font-size:14.5px}
.bev{border-top:1px solid #eeeeea;padding:13px 15px;background:#fcfcfa}
.bev h3{margin:0 0 9px;font-size:12px;letter-spacing:.05em;text-transform:uppercase;color:#8a2d1c;font-weight:650}
.punt{margin:0 0 13px}
.punt:last-child{margin-bottom:0}
.punt .pk{font-size:13px;color:#6b6b68;margin-bottom:3px}
.punt .pk code{background:#f0f0ec;padding:1px 5px;border-radius:4px;font-size:12px}
.punt .po{font-size:14.5px}
.risico{display:flex;gap:14px;flex-wrap:wrap;margin-top:7px;font-size:12.5px;color:#6b6b68}
.risico b{color:#1b1b1a;font-weight:650}
.risico .sc{border-left:1px solid #e3e3df;padding-left:14px}
.slot{border:1px solid #e3e3df;border-radius:9px;padding:15px;background:#fafaf8;font-size:14.5px}
.voet{margin-top:40px;padding-top:16px;border-top:1px solid #e3e3df;color:#8c8c88;font-size:12.5px}
.voet code{background:#f0f0ec;padding:1px 5px;border-radius:4px}
@media(max-width:560px){.blad{padding:22px 16px 40px}dl{grid-template-columns:1fr;gap:1px 0}dt{margin-top:9px}h1{font-size:21px}}
</style></head><body><div class='blad'>""")
A("<h1>Veiligheidscontrole speelterrein</h1>")
A("<p class='sub'>%s &middot; %s &middot; %s</p>" % (e(dos["iok_terreinnaam"]), e(dos["iok_soortcontrole"].lower()), e(datum_nl(dos["iok_controledatum"]))))
A("<h2>Dossier</h2><dl>")
rijen = [("Terrein", "%s (%s)" % (dos["iok_terreinnaam"], dos["iok_terreincode"])),
         ("Bestuur", dos["iok_bestuurnaam"]), ("Gemeente", bestuur.get("address1_city", "")),
         ("Soort controle", dos["iok_soortcontrole"]), ("Controledatum", datum_nl(dos["iok_controledatum"])),
         ("Inspecteur", dos["iok_inspecteurnaam"])]
for lab, w in rijen:
    if w == "@ik": A("<dt>%s</dt><dd><em>de gebruiker die de proefdata laadde</em></dd>" % e(lab))
    elif w: A("<dt>%s</dt><dd>%s</dd>" % (e(lab), e(w)))
A("</dl>")
A("<div class='cijfers'>")
A("<div class='cijfer'><b>%d</b><span>toestellen beoordeeld</span></div>" % n_toe)
A("<div class='cijfer'><b>%d</b><span>bevindingen</span></div>" % len(resultaten))
A("<div class='cijfer'><b>%d</b><span>niet beoordeeld</span></div>" % n_nb)
A("</div>")
terr = [b for b in beo if b["iok_soort"] == "Terrein"]
if terr:
    b = terr[0]
    A("<h2>Het terrein</h2><div class='toestel'><div class='kop'><span class='code'>Terrein</span>")
    A("<span class='naam'>%s</span>" % e(dos["iok_terreinnaam"]))
    A("<span class='vlag ok'>%s</span></div>" % e(b["iok_besluit"] or "-"))
    if b["iok_besluittekst"]: A("<div class='tekst'>%s</div>" % e(b["iok_besluittekst"]))
    A("</div>")
A("<h2>De toestellen</h2>")
for b in beo:
    if b["iok_soort"] != "Toestel": continue
    bev = per_beo.get(b["_sleutel"], []); besluit = b["iok_besluit"]
    klasse = "ok" if besluit == "Conform" else ("nb" if besluit == "Niet beoordeeld" else "leeg")
    etiket = besluit or "besluit ontbreekt"
    toestel = toestellen.get(b["iok_speeltoestelid"], {})
    code = b["iok_toestelcode"] or toestel.get("iok_code", "")
    A("<div class='toestel'><div class='kop'><span class='code'>%s</span>" % e(code))
    A("<span class='naam'>%s</span>" % e(b["iok_toestelnaam"] or toestel.get("iok_naam", "")))
    if bev: A("<span class='vlag nokv'>%d bevinding%s</span>" % (len(bev), "" if len(bev) == 1 else "en"))
    A("<span class='vlag %s'>%s</span></div>" % (klasse, e(etiket)))
    if b["iok_besluittekst"]: A("<div class='tekst'>%s</div>" % e(b["iok_besluittekst"]))
    if bev:
        A("<div class='bev'><h3>Vastgesteld</h3>")
        for r in bev:
            p = punten.get(r["iok_controlepuntid"], {}); ond = onderdelen.get(p.get("iok_onderdeelid", ""), {})
            A("<div class='punt'><div class='pk'><code>%s</code> %s &middot; %s</div>" % (
                e(p.get("iok_code", "?")), e(p.get("iok_tekst", "")), e(ond.get("iok_naam", ""))))
            if r["iok_opmerking"]: A("<div class='po'>%s</div>" % e(r["iok_opmerking"]))
            i, k, b = r.get("iok_impact",""), r.get("iok_kans",""), r.get("iok_blootstelling","")
            if i or k or b:
                if i and k and b:
                    sc = float(i.replace(',','.')) * float(k.replace(',','.')) * float(b.replace(',','.'))
                    kl = ('Licht' if sc <= 20 else 'Mogelijk' if sc <= 70 else 'Substantieel' if sc <= 160 else 'Hoog' if sc <= 320 else 'Zeer hoog')
                    sct = '%g' % sc
                else:
                    sct, kl = '&mdash;', 'blootstelling ontbreekt in het verslag'
                A("<div class='risico'><span>impact <b>%s</b></span><span>kans <b>%s</b></span>"
                  "<span>blootstelling <b>%s</b></span><span class='sc'>risico <b>%s</b> &middot; %s</span></div>"
                  % (e(i) or '&mdash;', e(k) or '&mdash;', e(b) or '&mdash;', sct, e(kl) if kl.islower() else kl))
            A("</div>")
        A("</div>")
    A("</div>")
if dos["iok_algemeenbesluit"]:
    A("<h2>Algemeen besluit</h2><div class='slot'>%s</div>" % e(dos["iok_algemeenbesluit"]))
A("<div class='voet'>Gemaakt uit de proefdata in <code>04_data/</code> met <code>tools/maak_verslag.py</code>. ")
A("Dit is geen echt IOK-verslag en geen rapportsjabloon: het toont dat het datamodel alle gegevens draagt die een verslag nodig heeft. De lay-out van het echte rapport moet nog ontworpen worden.</div>")
A("</div></body></html>")
uit = os.path.join(os.environ["HOME"], "mnt", "ERD", "03_output", "verslag_voorbeeld.html")
with io.open(uit, "w", encoding="utf-8") as f: f.write("\n".join(S))
print("geschreven:", uit, len("\n".join(S)), "tekens")
print("%d beoordelingen, %d bevindingen, %d niet beoordeeld" % (len(beo), len(resultaten), n_nb))
