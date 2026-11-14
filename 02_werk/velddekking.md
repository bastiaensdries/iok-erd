# Velddekking v3 — Deel A: de vier lege sjablonen en de keuzelijsten

_Datum: 2026-11-14. Stap 2 (maken), deel A van 3. Bronnen: `01_context/docs/*.md` en `01_context/keuzelijsten/*.md` (de markdownversies, niet de originelen). Steunt op `BESLISSINGEN.md` B01–B39 en `02_werk/crud_matrix.md`._

**Afbakening van deel A:** de vier lege sjablonen (`Indienststelling versie 2022`, `Risicoanalyse toestellen versie 2022`, `risicoanalyse skate toestellen versie 2022`, `risicoanalyse terrein versie 2022`) en de zes keuzelijstbestanden. **Controlepunten worden als structuur beschreven**, niet punt per punt (skill `velddekking`, werkwijze 3). De ingevulde A-, B- en C-verslagen en de overzichten (`Overzicht bestaande speelterreinen`, `Overzicht soorten speeltoestellen`) komen in deel B en C.

**Statuswaarden:** `gedekt` = v2 had al een kolom en v3 houdt ze · `nieuw` = kolom bestaat nog niet in v2 · `weggelaten` = bewust niet gemodelleerd (reden staat erbij) · `open` = beslissing of bron ontbreekt.

**Afkortingen in de bronkolom:** **IND** = `Indienststelling versie 2022.md` · **RAT** = `Risicoanalyse toestellen versie 2022.md` · **SKT** = `risicoanalyse skate toestellen versie 2022.md` · **TER** = `risicoanalyse terrein versie 2022.md`. Celnotatie `r5/A` = rij 5, kolom A van het genoemde blad.

---

## 1. De vier sjablonen: opbouw en omvang

| Sjabloon | Bladen | Hoofdstukken (niveau 1) | Code-rijen met tekst | Waarvan inleidende rij | Waarvan OK/NOK-punt |
|---|---|---|---|---|---|
| **IND** / **RAT** (identiek, B38) | 13: Algemeen + 11 Deel 2-bladen + Standaardlijsten | 14 (A–N) + 40 over de 11 Deel 2-bladen | **399** (153 + 246) | 25 | 374 |
| **SKT** | 13: Algemeen + 11 onderdelen + Standaardlijsten | 10 (Deel 1) + 31 (11 onderdelen) | **93** (59 + 34) | 3 | 90 |
| **TER** | 2: terrein + standaardlijsten | 8 | **55** | 7 | 48 |

Per blad, zodat de omvang meetbaar blijft:

| Blad | H1 | Code-rijen | Waarvan inleiding |
|---|---|---|---|
| **Deel 1 – Algemeen** (IND/RAT) | 14 (A–N, plus subkop "H. 1 Algemeen") | 153 | 3 (C.2, H.4.9, I.1.7) |
| schommels | 6 | 31 | 1 (2.3) |
| Glijbaan | 8 | 41 | 4 (2.10, 3.4, 4.4, 5.3) |
| Kabelbaan | 4 | 23 | 0 |
| Draaitoestel | 6 | 39 | 0 |
| Wip | 7 | 36 | 2 (3.3, 4.3) |
| Doelen | 3 | 7 | 1 (3.1) |
| zandbak | 1 | 9 | 0 |
| Water | 2 | 30 | 10 |
| springkasteel | 1 | 9 | 0 |
| Zware balken | 1 | 7 | 0 |
| Springtoestel | 1 | 14 | 4 |
| **Skate – Deel 1 – Algemeen** | 10 (A–H, M, N) | 59 | 1 (D.5) |
| Curbs | 3 | 1 | 0 |
| Rail | 3 | 4 | 0 |
| Bank | 3 | 2 | 0 |
| Jump-ramp | 2 | **0** | 0 |
| Coping-ramp | 3 | 1 | 0 |
| Spine-ramp | 2 | **0** | 0 |
| Wall-ramp | 3 | 3 | 0 |
| Fun-box | 3 | 9 | 0 |
| Pyramide | 3 | 3 | 0 |
| Mini-pipe | 3 | 4 | 1 |
| Half-pipe | 3 | 7 | 1 |
| **Terrein** | 8 | 55 | 7 |

_Telling: rijen met een code in kolom A én een vraagtekst in kolom B. Een "inleidende rij" is een code-rij waarvan de tekst op ":" eindigt (een groepje deelvragen). De telling is een **bovengrens**: welke rijen echt beantwoordbaar zijn, volgt uit de `bevestiging`-validatie in de bron; die cellijsten zijn in de keuzelijstbestanden afgekapt (`G12 …`)._

---

## 2. Structuur van een checklist (zoals ze in de sjablonen staat)

De sjablonen hebben vier niveaus, en dat is precies de ruggengraat van v3:

| Niveau in het sjabloon | Voorbeeld (IND · schommels) | v3 |
|---|---|---|
| **Formulier / checklist** | werkmap "Indienststelling", blad "schommels" = `Deel 2 : Specifieke toestellen : Schommels EN 1176-2/2017` | `iok_checklist` (B19: `soort` + `deel` + `versie`, B38: één reeks) |
| **Hoofdstuk** (niveau 1) | "2. Valhoogte / valruimte" | `iok_controlepunt` met `iok_ouder` leeg (hoofdstuk) |
| **Subkop** (soms) | "A.1 Hout :" in Deel 1, "H. 1 Algemeen :" | `iok_controlepunt` met `iok_ouder` = hoofdstuk |
| **Controlepunt** | "2.1 Schokabsorberende eigenschappen van de ondergrond aangepast aan valhoogte?" | `iok_controlepunt` met `iok_ouder` = subkop of hoofdstuk, plus `iok_code` en `iok_tekst` |
| **Beoordeling** | kolom G "Status": OK / NOK / nvt | `iok_resultaat` (B36) |
| **Opmerking / maatregel** | vrije rij onder het punt, soms met standaardzin | `iok_maatregel` + `iok_standaardtekst` (B18/B35) |
| **Foto** | cel "foto" op het Algemeen-blad | `iok_foto` (B15/B37) |

Drie afwijkingen op dat patroon, die het model moeten opvangen:

1. **Het terreinblad heeft beantwoordbare niveau-2-rijen.** "1.1 Voldoende afscheiding tov. verkeer" is zowel een kop boven 1.1.1–1.1.2 als een rij met eigen tekst; de `bevestiging`-lijst geldt voor G26 én G27. In de toestelbladen is niveau 1 nooit beantwoordbaar, in het terreinblad dus soms wel. → De hiërarchie moet willekeurig diep kunnen (`iok_ouder`), een punt op elk niveau mag een `iok_resultaat` krijgen.
2. **De skate-onderdelen zijn deels een meetformulier.** Elk onderdeel heeft drie vaste hoofdstukken: *1. Afmetingen* (min./max. in mm), *2. Veiligheidszone* (lengte/breedte, bv. 5000 × 2000 mm) en *3. Bijkomende eisen* (de eigenlijke OK/NOK-punten, 0–9 per onderdeel). In *Afmetingen* en *Veiligheidszone* staat de norm in kolom C/D/F naast het label, niet in een vraagzin. → Naast OK/NOK/nvt zijn **meetwaarden** nodig (zie §7, Q16).
3. **Deel 1 geldt altijd, Deel 2 per toesteltype.** "Deel 1 : Speeltoestellen algemeen EN 1176-1/2017" staat in dezelfde werkmap als de 11 Deel 2-bladen, maar is één checklist die bij elk toestel hoort; een Deel 2-blad hoort bij één of meer toesteltypes (B26: N:N type → checklist). Een skatepark is één toestel met één EN 14974-checklist waarin Deel 1 en de 11 onderdelen samen zitten (B39).

---

## 3. Kopvelden van het Algemeen-blad (18 velden + titel en 2 sectiekoppen) en van het terreinblad (11 velden + titel en sectiekop)

### 3.1 Toestel-sjablonen (IND, RAT, SKT — dezelfde cellen, enkele verschillen)

| Bron | Label in bron | Voorbeeldwaarde | → Tabel.kolom | Type | Status |
|---|---|---|---|---|---|
| IND/RAT/SKT · Algemeen · r2/A | Documenttitel ("Indienststelling Speeltoestellen" / "Risicoanalyse Speeltoestellen" / "Risicoanalyse Skatetoestellen EN 14974") | — | — (vaste tekst in het PDF-sjabloon) | — | weggelaten |
| IND/RAT/SKT · Algemeen · r5/A | Omschrijving toestel | — (C5 = "0") | `iok_speeltoestel.iok_naam` (primaire kolom) | tekst | gedekt (v2 `SPEELTOESTEL.omschrijving`) |
| IND/RAT · Algemeen · r8/A | Adres speelterrein | — | `iok_speelterrein` → straat, postcode, plaats (of de standaard adreskolommen van een eigen tabel) | tekst (3 kolommen) | gedekt (v2 `SPEELTERREIN.straat_nr/postcode/plaats`) |
| IND/RAT/SKT · Algemeen · r8/E | Verantwoordelijke | — | `iok_speelterrein.iok_bestuur` → `account` | lookup (Account) | gedekt (v2 `BESTUUR.naam`), B37 |
| IND/RAT · Algemeen · r8/F | "Gemeentebestuur van de gemeente" | vaste tekst | — | — | weggelaten (vaste tekst in de PDF) |
| IND/RAT/SKT · Algemeen · r11/A | Uitbater | — | `iok_speelterrein.iok_uitbater` → `account` | lookup (Account) | open (Q01: private uitbaters) |
| IND/RAT · Algemeen · r11/E + r12/F | RA Uitgevoerd door + "IOK Antwerpseweg 1, 2440 Geel" | namenlijst / vast adres | — (PDF: vaste tekst + naam van de ingelogde gebruiker) | — | weggelaten, B37 |
| IND/RAT/SKT · Algemeen · r14/A | Algemene kenmerken | sectiekop | — | — | weggelaten (opmaak) |
| IND/RAT/SKT · Algemeen · r15/E | Codenummer toestel | — (C6 = "0") | `iok_speeltoestel.iok_code` | tekst, uniek (B25) | gedekt (v2 `SPEELTOESTEL.code`) |
| IND/RAT/SKT · Algemeen · r17/A | Doelgroep | — | `iok_speelterrein.iok_doelgroep` én `iok_speeltoestel.iok_doelgroep` | keuze (globaal) | gedekt (v2 bij beide), B32 + Q14 |
| IND/RAT/SKT · Algemeen · r17/E | Datum controle | — | `iok_inspectiedossier.iok_controledatum` | datum | gedekt (v2 `CONTROLE.datum`) |
| IND/RAT/SKT · Algemeen · r18/A | Toezicht | — | `iok_speelterrein.iok_toezicht` | keuze (globaal) | gedekt (v2 `SPEELTERREIN.toezicht`), B33 |
| IND/RAT/SKT · Algemeen · r18/E | Datum onderhoud | — | nog te bepalen | datum | open (B37: in deel B) |
| IND/RAT/SKT · Algemeen · r20/A | foto | — | `iok_foto` (fotoType = overzicht, koppeling aan de beoordeling) | koppeling + SharePoint-link | gedekt (v2 `FOTO`), B15/B37 |
| IND/RAT/SKT · Algemeen · r20/E | Gegevens toestellen | sectiekop | — | — | weggelaten (opmaak) |
| IND/RAT/SKT · Algemeen · r20/F | Leverancier | — | `iok_speeltoestel.iok_leverancier` | tekst | gedekt |
| IND/RAT/SKT · Algemeen · r21/F | Type toestel (fabrikanttype) | — | `iok_speeltoestel.iok_type_fabrikant` | tekst | gedekt |
| IND/RAT/SKT · Algemeen · r22/F | Serienummer | — | `iok_speeltoestel.iok_serienummer` | tekst | gedekt |
| IND/RAT/SKT · Algemeen · r23/F | Bouwjaar | — | `iok_speeltoestel.iok_bouwjaar` | geheel getal | gedekt |
| IND/RAT/SKT · Algemeen · r24/F | Attest | — | `iok_speeltoestel.iok_attest` | tekst | gedekt, maar Q08 (conformiteitsdocument) |

_Toelichting:_ "Type toestel" (r21/F) is **niet** hetzelfde als het toesteltype in de opzoektabel (B26/B34): het eerste is de fabrikantbenaming, het tweede de soort. Beide blijven bestaan.

### 3.2 Terrein-sjabloon (TER)

| Bron | Label in bron | Voorbeeldwaarde | → Tabel.kolom | Type | Status |
|---|---|---|---|---|---|
| TER · terrein · r2/A | "Risicoanalyse Deel omgeving en zonering" | — | — (vaste tekst in de PDF) | — | weggelaten |
| TER · terrein · r5/A | Benaming speelterrein | — | `iok_speelterrein.iok_naam` | tekst | gedekt (v2 `SPEELTERREIN.naam`) |
| TER · terrein · r8/A | Adres speelterrein | — | `iok_speelterrein` → straat, postcode, plaats | tekst (3 kolommen) | gedekt |
| TER · terrein · r8/E | Verantwoordelijke | — | `iok_speelterrein.iok_bestuur` → `account` | lookup | gedekt, B37 |
| TER · terrein · r8/F | "Gemeentebestuur van de gemeente" | vaste tekst | — | — | weggelaten |
| TER · terrein · r11/A | Uitbater | — | `iok_speelterrein.iok_uitbater` | lookup | open (Q01) |
| TER · terrein · r11/E + r12/F | "RA Uitgevoerd door : IOK" + adres | vaste tekst | — | — | weggelaten, B37 |
| TER · terrein · r16/A | Algemene kenmerken | sectiekop | — | — | weggelaten (opmaak) |
| TER · terrein · r17/A | Doelgroep | — | `iok_speelterrein.iok_doelgroep` | keuze (globaal) | gedekt, B32 |
| TER · terrein · r17/E | Datum controle | — | `iok_inspectiedossier.iok_controledatum` | datum | gedekt |
| TER · terrein · r18/A | Toezicht | — | `iok_speelterrein.iok_toezicht` | keuze (globaal) | gedekt, B33 |
| TER · terrein · r18/E | Datum onderhoud | — | nog te bepalen | datum | open (B37) |
| TER · terrein · r22/B | Code terrein | — | `iok_speelterrein.iok_code` | tekst, uniek (B25) | gedekt (v2 `SPEELTERREIN.code`) |

_Twee opmerkingen:_ (a) het terreinblad heeft **geen fotoveld**, het toestelblad wel; (b) het terreinblad heeft **geen eenhedenveld**, v2 had `SPEELTERREIN.eenheden` → Q12.

---

## 4. Keuzelijsten: wat wordt een keuzelijst, een opzoektabel of een standaardzin?

| Bestand · lijst | Waarden | Aantal | → Bestemming in v3 | Soort | Status |
|---|---|---|---|---|---|
| IND/RAT/A_/B_ · `bevestiging` (alle bladen) | OK, NOK, nvt | 3 | `iok_resultaat.iok_antwoord` | **globale keuzelijst** | gedekt (v2 `RESULTAAT.status`), B36 |
| IND/RAT/A_/B_/TER · `Doelgroep` / `doelgroep` | 11 waarden (toestel) / 10 (terrein) | 12 samen | `iok_speelterrein.iok_doelgroep`, `iok_speeltoestel.iok_doelgroep` | **globale keuzelijst** | gedekt, B32 + Q14 |
| IND/RAT/A_/B_/TER · `keuze` | Geen toezicht, Sociale controle, Regelmatige controle, Constant toezicht | 4 | `iok_speelterrein.iok_toezicht` | **globale keuzelijst** | gedekt, B33 |
| IND/RAT/A_/B_ · `toestellen` | 27 namen, per werkmap verschillend | 27 | `iok_toesteltype` | **opzoektabel** | gedekt (v2 `TOESTELTYPE`), B34 + Q15 |
| IND/RAT · `Markeringen` (B542:F542) | 4 zinnen over het aanbrengen van de code | 4 | `iok_standaardtekst` (soort = markering, controlepunt M.6) | **standaardzinnen-tabel** | nieuw, B35 |
| IND/RAT · `Inlichtingen` (B549:F549) | 4 zinnen over schema's/logboek/keuringsbewijzen | 4 | `iok_standaardtekst` (soort = inlichting, controlepunt N.4) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `Informatie` (B105–B124) | 7 zinnen over borden en codes op het terrein | 7 | `iok_standaardtekst` (soort = inlichting, controlepunt 6.1–6.6.5) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `AREI` (B96) | 2 zinnen over elektrische installaties | 2 | `iok_standaardtekst` (controlepunt 5.2) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `Schema` (B146–B150) | 1 zin over schema's | 1 | `iok_standaardtekst` (controlepunt 8.2) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `Meubilair` (B94) | **geen waarden** | 0 | `iok_standaardtekst` (controlepunt 5.1) — lijst is leeg | — | open (zie §6) |
| TER · `$I$131:$I$131`, `$I$118:$I$120` | **geen waarden, geen naam** | 0 | — | — | open (zie §6) |
| TER · `standaardlijsten!$A$49` (x14) | 1 zin over een bank in het looppad | 1 | `iok_standaardtekst` (controlepunt 5.4) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `standaardlijsten!$A$47:$A$48` (x14) | 2 zinnen over ontbrekende banken | 2 | `iok_standaardtekst` (controlepunt 5.3) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `standaardlijsten!$A$70:$A$71` (x14) | 2 zinnen over bomenonderhoud | 2 | `iok_standaardtekst` (controlepunt 4.3) | **standaardzinnen-tabel** | nieuw, B35 |
| IND/RAT · `Standaardlijsten!$A$77:$A$78` (x14) | Danny Frederix, Marc Lemmens | 2 | — (PDF: naam van de ingelogde gebruiker) | — | weggelaten, B37 |
| IND/RAT · blad `Standaardlijsten` | bevat de lijsten hierboven plus 4 toezicht, 3 bevestigingen, 11 doelgroepen, 27 toestellen | 43 rijen | — (vervalt als blad) | — | weggelaten (verdeeld over de lijsten hierboven) |
| SKT · blad `Standaardlijsten` | 23 rijen; keuzelijsten niet uitleesbaar (.xls) | 23 | — | — | open (niet uitleesbaar) |

**Conclusie voor het model:** de lijsten in de bronnen vallen uiteen in **4 keuzelijsten of opzoektabellen** (`iok_resultaat.iok_antwoord`, `iok_doelgroep` op terrein en toestel, `iok_toezicht`, `iok_toesteltype`), **9 standaardzinnenlijsten** (waarvan `Meubilair` leeg is) en **3 lijsten die vervallen** (de namenlijst van de inspecteurs en de twee naamloze lijsten). Er is **geen enkele lijst** die een eigen tabel nodig heeft buiten `iok_toesteltype` en `iok_standaardtekst` — dat bevestigt B02 (standaardtabel of `iok_`-tabel, geen lijstentabellen).

---

## 5. Standaardzinnen: van losse cellen naar één tabel

De zinnen staan in de sjablonen op de **opmerkingsrij direct onder het controlepunt** (soms een samengevoegde cel over B:F). Daarmee is de band met het controlepunt impliciet: de lijst is alleen geldig voor dat punt. In v3 wordt dat expliciet:

| Kolom in `iok_standaardtekst` | Herkomst | Verplicht? |
|---|---|---|
| `iok_tekst` | de zin, letterlijk overgenomen | ja |
| `iok_soort` | markering / inlichting / maatregel / besluit (B35) | ja |
| `iok_controlepunt` | het controlepunt waaronder de zin in het sjabloon staat; **leeg = algemene zin** | nee (B35) |
| `iok_versie` | versie van de tekstenset, zodat oude dossiers de oude zinnen houden (B07/B19) | ja |
| `iok_actief` | state; beheerder deactiveert in plaats van te verwijderen (B08) | ja |

Algemene zinnen die **niet** aan een controlepunt hangen (en dus met een lege verwijzing moeten kunnen): het besluit ("Het toestel is conform de norm"), de kop- en voetteksten van het verslag, en de inleidende zinnen van de preventiesamenvatting (B11/B18). Die staan in deel A nog niet in de bronnen; ze komen uit de ingevulde verslagen (deel B).

---

## 6. Inconsistenties tussen de bronnen (deel A)

1. **Doelgroep verschilt per formulier.** Terrein: 10 waarden met "van 1 tot 18 jaar", zonder "van 1 tot 14 jaar" en "van 2,5 tot 4 jaar". Toestel: 11 waarden met die twee, zonder "van 1 tot 18 jaar". → B32 (één lijst), Q14 (is het verschil bewust?).
2. **Waarden bevatten opmaak.** De doelgroepwaarden beginnen met een opsommingsteken ("- 3 jaar") en de laatste eindigt op een punt ("van 6 tot 9 jaar."). Bij het laden opschonen.
3. **Volgorde van toezicht verschilt.** Toestel: Geen / Sociale / Regelmatige / Constant. Terrein: Geen / Regelmatige / Sociale / Constant. Zelfde waarden, andere volgorde.
4. **De lijst `toestellen` verschilt per werkmap** (27 namen): "Vogelnestschommel" alleen in A_, "Evenwichtsparcours" alleen in B_, "Combinatietoestel glijbaan, glijstang en tuimelrek" alleen in de sjablonen. → B34, Q15.
5. **`Meubilair` (TER, B94) heeft geen waarden**, terwijl de cel wel een validatie heeft. Mogelijk een lege lijst in het origineel.
6. **Twee naamloze lijsten in TER** (`$I$131:$I$131`, `$I$118:$I$120`) met celverwijzingen A48/I131 en A54:A55, zonder waarden. Niet te interpreteren zonder het origineel; in het .md-bestand staat geen inhoud.
7. **Twee skate-onderdelen hebben geen OK/NOK-punten**: Jump-ramp en Spine-ramp hebben alleen *Afmetingen* en *Veiligheidszone*. Een inspecteur kan daar niets beoordelen, tenzij de meting zelf de beoordeling is. → Q17.
8. **Nummering is niet consequent**: "1.Toegang" (geen spatie, Glijbaan), "3, Bijkomende eisen" (komma, Curbs), "H. 1 Algemeen" (spatie, Deel 1). Bij het laden normaliseren; de code blijft de bron van de volgorde.
9. **De skate-chapters springen van H naar M/N** (Deel 1: A–H, dan M. Markeringen, N. Inlichtingen, met dezelfde nummering als EN 1176-1). Niet fout, maar bij het laden moet de code niet als volgnummer worden gebruikt.
10. **Het skate-sjabloon is een ouder .xls-bestand**: er is geen `bevestiging`-keuzelijst uitleesbaar en r8/F ("Gemeentebestuur van de gemeente") en de IOK-adresregel ontbreken. De kop is dus niet identiek aan IND/RAT.
11. **"Uitbater" en "Verantwoordelijke" wijzen in de praktijk beide naar het bestuur**, maar staan als twee velden in de kop. Zolang Q01 (private uitbaters) open is, blijven het twee velden.

---

## 7. Wat deel A oplevert en wat nog open is

**Beslist en verwerkt:** B32–B39 (doelgroep, toezicht, toesteltype, standaardtekst, antwoord/status, kopvelden, één checklistreeks, skate als één toestel).

**Open na deel A:**

| Nr | Punt | Voor wie |
|---|---|---|
| Q14 | Doelgroep: zijn de verschillen bewust, en volstaat één waarde? | IOK |
| Q15 | Officiële namen en volledigheid van de toesteltypes (27 vs 145) | IOK |
| Q16 | **Meetwaarden in de skate-checklist**: *Afmetingen* en *Veiligheidszone* zijn min./max.-waarden in mm, geen OK/NOK. Komen die als numerieke velden op `iok_resultaat` (bv. `iok_meetwaarde`, `iok_eenheid`) of als aparte `iok_meting`-tabel naast `iok_hicmeting`? Samen met HIC bekijken (HANDOVER, stap 3). | Dries (stap 3/4) |
| Q17 | Jump-ramp en Spine-ramp zonder beoordelingspunten (§6.7): is de meting daar de beoordeling of ontbreken er punten? | IOK |
| — | "Datum onderhoud" (B37) | Dries, deel B |
| — | Toezicht per toestel afwijkend van het terrein (B33) | controle in deel B |

**Nog niet gedekt (deel B en C):** de ingevulde verslagen (`A_`, `B_`, `C_`) met hun echte waarden, het HIC-blok, de risicoscore (impact/kans/blootstelling) en de standaardzinnen die alleen daar voorkomen; daarna de overzichten (`Overzicht bestaande speelterreinen` met de 31 dubbele codes, `Overzicht soorten speeltoestellen` met de 145 types).
