# Velddekking v3

_Datum: 2026-11-14. Stap 2 (maken). Bronnen: `01_context/docs/*.md` en `01_context/keuzelijsten/*.md` (de markdownversies, niet de originelen). Steunt op `BESLISSINGEN.md` B01–B45 en `02_werk/crud_matrix.md`._

**Deel A = §1–§7** (de vier lege sjablonen en de zes keuzelijstbestanden). **Deel B = §8–§19** (de vijf ingevulde voorbeelden en de twee overzichten). Deel C was de resterende bron: de overzichten zijn in deel B meegenomen, zodat alleen de vragen Q15/Q20/Q21 nog openstaan.

**Afbakening van deel A:** de vier lege sjablonen (`Indienststelling versie 2022`, `Risicoanalyse toestellen versie 2022`, `risicoanalyse skate toestellen versie 2022`, `risicoanalyse terrein versie 2022`) en de zes keuzelijstbestanden. **Controlepunten worden als structuur beschreven**, niet punt per punt (skill `velddekking`, werkwijze 3). De ingevulde A-, B- en C-verslagen en de overzichten (`Overzicht bestaande speelterreinen`, `Overzicht soorten speeltoestellen`) komen in deel B en C.

**Statuswaarden:** `gedekt` = v2 had al een kolom en v3 houdt ze · `nieuw` = kolom bestaat nog niet in v2 · `weggelaten` = bewust niet gemodelleerd (reden staat erbij) · `open` = beslissing of bron ontbreekt.

**Afkortingen in de bronkolom:** **IND** = `Indienststelling versie 2022.md` · **RAT** = `Risicoanalyse toestellen versie 2022.md` · **SKT** = `risicoanalyse skate toestellen versie 2022.md` · **TER** = `risicoanalyse terrein versie 2022.md`. Celnotatie `r5/A` = rij 5, kolom A van het genoemde blad.

---

## 1. De vier sjablonen: opbouw en omvang

| Sjabloon | Bladen | Hoofdstukken (niveau 1) | Code-rijen met tekst | Waarvan inleidende rij | Waarvan OK/NOK-punt |
|---|---|---|---|---|---|
| **IND** / **RAT** (identiek, B38) | 13: Algemeen + 11 Deel 2-bladen + Standaardlijsten | 14 (A–N) + 40 over de 11 Deel 2-bladen | **417** (168 + 249) | 26 | 391 |
| **SKT** | 13: Algemeen + 11 onderdelen + Standaardlijsten | 10 (Deel 1) + 31 (11 onderdelen) | **93** (59 + 34) | 3 | 90 |
| **TER** | 2: terrein + standaardlijsten | 8 | **55** | 7 | 48 |

Per blad, zodat de omvang meetbaar blijft:

| Blad | H1 | Code-rijen | Waarvan inleiding |
|---|---|---|---|
| **Deel 1 – Algemeen** (IND/RAT) | 14 (A–N, plus subkop "H. 1 Algemeen") | 168 | 4 (C.2, E.1.8., H.4.9, I.1.7) |
| schommels | 6 | 31 | 1 (2.3) |
| Glijbaan | 8 | 41 | 4 (2.10, 3.4, 4.4, 5.3) |
| Kabelbaan | 4 | 23 | 0 |
| Draaitoestel | 6 | 42 | 0 |
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

_Herzien bij de eindcontrole van stap 2 (2026-11-14): de eerste telling gaf 399 code-rijen (153 + 246), 25 inleidende rijen en 374 punten. Een letterlijke hertelling met de regel hierboven geeft **417** (168 + 249), **26** en **391**: 15 rijen op het Algemeen-blad en 3 op Draaitoestel waren niet meegeteld (o.a. de codes met een punt: `4.3.`, `4.4.`, `4.5.`, en `E.1.8.` als vierde inleidende rij). De tabellen hierboven zijn aangepast; de **verhoudingen** en alle conclusies in §2–§7 veranderen daardoor niet._

---

## 2. Structuur van een checklist (zoals ze in de sjablonen staat)

De sjablonen hebben vier niveaus, en dat is precies de ruggengraat van v3 (voor de codes gaat het in de praktijk tot vier niveaus; zie §14):

| Niveau in het sjabloon | Voorbeeld (IND · schommels) | v3 |
|---|---|---|
| **Formulier / checklist** | werkmap "Indienststelling", blad "schommels" = `Deel 2 : Specifieke toestellen : Schommels EN 1176-2/2017` | `iok_checklist` (B19: `soort` + `deel` + `versie`, B38: één reeks) |
| **Hoofdstuk** (niveau 1) | "2. Valhoogte / valruimte" | `iok_controlepunt` met `iok_ouder` leeg (hoofdstuk) |
| **Subkop** (soms) | "A.1 Hout :" in Deel 1, "H. 1 Algemeen :" | `iok_controlepunt` met `iok_ouder` = hoofdstuk |
| **Controlepunt** | "2.1 Schokabsorberende eigenschappen van de ondergrond aangepast aan valhoogte?" | `iok_controlepunt` met `iok_ouder` = subkop of hoofdstuk, plus `iok_code` en `iok_tekst` |
| **Beoordeling** | kolom G "Status": OK / NOK / nvt | `iok_resultaat` (B36, aangevuld door B40) |
| **Opmerking / maatregel** | vrije rij onder het punt, soms met standaardzin | `iok_maatregel` + `iok_standaardtekst` (B18/B35) |
| **Foto** | cel "foto" op het Algemeen-blad | `iok_foto` (B15/B37) |

Drie afwijkingen op dat patroon, die het model moeten opvangen:

1. **Het terreinblad heeft beantwoordbare niveau-2-rijen.** "1.1 Voldoende afscheiding tov. verkeer" is zowel een kop boven 1.1.1–1.1.2 als een rij met eigen tekst; de `bevestiging`-lijst geldt voor G26 én G27. In de toestelbladen is niveau 1 nooit beantwoordbaar, in het terreinblad dus soms wel. → De hiërarchie moet willekeurig diep kunnen (`iok_ouder`), een punt op elk niveau mag een `iok_resultaat` krijgen.
2. **De skate-onderdelen zijn deels een meetformulier.** Elk onderdeel heeft drie vaste hoofdstukken: *1. Afmetingen* (min./max. in mm), *2. Veiligheidszone* (lengte/breedte, bv. 5000 × 2000 mm) en *3. Bijkomende eisen* (de eigenlijke OK/NOK-punten, 0–9 per onderdeel). In *Afmetingen* en *Veiligheidszone* staat de norm in kolom C/D/F naast het label, niet in een vraagzin. → Naast OK/NOK/nvt zijn **meetwaarden** nodig (zie §7, Q16).
3. **Deel 1 geldt altijd, Deel 2 per toesteltype.** "Deel 1 : Speeltoestellen algemeen EN 1176-1/2017" staat in dezelfde werkmap als de 11 Deel 2-bladen, maar is één checklist die bij elk toestel hoort; een Deel 2-blad hoort bij één of meer toesteltypes (B26: N:N type → checklist). Een skatepark is één toestel met één EN 14974-checklist waarin Deel 1 en de 11 onderdelen samen zitten (B39).

---

## 3. Kopvelden: het Algemeen-blad (18 velden + titel en 2 sectiekoppen) en het terreinblad (titel en sectiekop + dezelfde kopvelden, zonder foto)

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
| IND/RAT/SKT · Algemeen · r18/E | Datum onderhoud | — (altijd leeg) | — (geen kolom) | — | **vervallen in B41** (§10) |
| IND/RAT/SKT · Algemeen · r20/A | foto | — | `iok_foto` (fotoType = overzicht, koppeling aan de beoordeling) | koppeling + SharePoint-link | gedekt (v2 `FOTO`), B15/B37 |
| IND/RAT/SKT · Algemeen · r20/E | Gegevens toestellen | sectiekop | — | — | weggelaten (opmaak) |
| IND/RAT/SKT · Algemeen · r20/F | Leverancier | — | `iok_speeltoestel.iok_leverancier` | tekst | gedekt |
| IND/RAT/SKT · Algemeen · r21/F | Type toestel (fabrikanttype) | — | `iok_speeltoestel.iok_type_fabrikant` | tekst | gedekt |
| IND/RAT/SKT · Algemeen · r22/F | Serienummer | — | `iok_speeltoestel.iok_serienummer` | tekst | gedekt |
| IND/RAT/SKT · Algemeen · r23/F | Bouwjaar | — | `iok_speeltoestel.iok_bouwjaar` | geheel getal | gedekt |
| IND/RAT/SKT · Algemeen · r24/F | Attest | **"EN 1176/2017"** (de norm) | `iok_speeltoestel.iok_attest` voor het **document**; de norm zelf hoort op `iok_beoordeling` (B21) | tekst | gedekt + Q08; zie §10 en §15.9 |

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
| TER · terrein · r18/E | Datum onderhoud | — (altijd leeg) | — (geen kolom) | — | **vervallen in B41** (§10) |
| TER · terrein · r22/B | Code terrein | — | `iok_speelterrein.iok_code` | tekst, uniek (B25) | gedekt (v2 `SPEELTERREIN.code`) |

_Twee opmerkingen:_ (a) het terreinblad heeft **geen fotoveld**, het toestelblad wel; (b) het terreinblad heeft **geen eenhedenveld**, v2 had `SPEELTERREIN.eenheden` → Q12.

---

## 4. Keuzelijsten: wat wordt een keuzelijst, een opzoektabel of een standaardzin?

| Bestand · lijst | Waarden | Aantal | → Bestemming in v3 | Soort | Status |
|---|---|---|---|---|---|
| IND/RAT/A_/B_/SKT · `bevestiging` (alle bladen) | OK, NOK, nvt | 3 | `iok_resultaat.iok_antwoord` | **globale keuzelijst** | gedekt (v2 `RESULTAAT.status`), B36/B40 |
| IND/RAT/A_/B_/TER/SKT · `Doelgroep` / `doelgroep` | 11 waarden (toestel) / 10 (terrein) / 3 (skate: "vanaf 6, 9 en 12 jaar") | **15 strings** (12 in IND/RAT/TER, 3 alleen in SKT) | `iok_speelterrein.iok_doelgroep`, `iok_speeltoestel.iok_doelgroep` | **globale keuzelijst** | gedekt, B32 + Q14 |
| IND/RAT/A_/B_/TER · `keuze` | Geen toezicht, Sociale controle, Regelmatige controle, Constant toezicht | 4 | `iok_speelterrein.iok_toezicht` | **globale keuzelijst** | gedekt, B33 |
| IND/RAT/A_/B_ · `toestellen` | 27 namen, per werkmap verschillend (SKT heeft een eigen lijst met de **11 skate-onderdelen**) | 27 (+11) | `iok_toesteltype` | **opzoektabel** | gedekt (v2 `TOESTELTYPE`), B34 + Q15 |
| IND/RAT · `Markeringen` (B542:F542) | 4 zinnen over het aanbrengen van de code | 4 | `iok_standaardtekst` (soort = markering, controlepunt M.6) | **standaardzinnen-tabel** | nieuw, B35 |
| IND/RAT · `Inlichtingen` (B549:F549) | 4 zinnen over schema's/logboek/keuringsbewijzen | 4 | `iok_standaardtekst` (soort = inlichting, controlepunt N.4) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `Informatie` (B105–B124) | 7 zinnen over borden en codes op het terrein | 7 | `iok_standaardtekst` (soort = inlichting, controlepunt 6.1–6.6.5) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `AREI` (B96) | 2 zinnen over elektrische installaties | 2 | `iok_standaardtekst` (controlepunt 5.2) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `Schema` (B146–B150) | 1 zin over schema's | 1 | `iok_standaardtekst` (controlepunt 8.2) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `Meubilair` (B94) | **geen waarden** | 0 | `iok_standaardtekst` (controlepunt 5.1) — lijst is leeg | — | open (zie §6; **gecorrigeerd in §18.1**: de lijst heeft één zin) |
| TER · `$I$131:$I$131`, `$I$118:$I$120` | **geen waarden, geen naam** | 0 | — | — | open (zie §6) |
| TER · `standaardlijsten!$A$49` (x14) | 1 zin over een bank in het looppad | 1 | `iok_standaardtekst` (controlepunt 5.4) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `standaardlijsten!$A$47:$A$48` (x14) | 2 zinnen over ontbrekende banken | 2 | `iok_standaardtekst` (controlepunt 5.3) | **standaardzinnen-tabel** | nieuw, B35 |
| TER · `standaardlijsten!$A$70:$A$71` (x14) | 2 zinnen over bomenonderhoud | 2 | `iok_standaardtekst` (controlepunt 4.3) | **standaardzinnen-tabel** | nieuw, B35 |
| IND/RAT · `Standaardlijsten!$A$77:$A$78` (x14) | Danny Frederix, Marc Lemmens | 2 | — (PDF: naam van de ingelogde gebruiker) | — | weggelaten, B37 |
| IND/RAT · blad `Standaardlijsten` | bevat de lijsten hierboven plus 4 toezicht, 3 bevestigingen, 11 doelgroepen, 27 toestellen | 43 rijen | — (vervalt als blad) | — | weggelaten (verdeeld over de lijsten hierboven) |
| SKT · blad `Standaardlijsten` | **39 rijen, wél leesbaar**: `keuze` (4), `bevestiging` (3), `Doelgroep` (3, andere bewoording), `toestellen` (de 11 skate-onderdelen), `Markeringen` (4), `Inlichtingen` (4), **`Gebruik` (3)** | 39 | `iok_standaardtekst` voor `Gebruik` (soort = inlichting); de rest gelijk aan IND/RAT | **standaardzinnen-tabel** + Q14 | nieuw, B35; `Doelgroep` → Q14 |

**Conclusie voor het model:** de lijsten in de bronnen vallen uiteen in **4 keuzelijsten of opzoektabellen** (`iok_resultaat.iok_antwoord`, `iok_doelgroep` op terrein en toestel, `iok_toezicht`, `iok_toesteltype`), **10 standaardzinnenlijsten** (waarvan `Meubilair` volgens deel B toch één zin bevat, §18.1, en `Gebruik` alleen in het skate-sjabloon staat) en **3 lijsten die vervallen** (de namenlijst van de inspecteurs en de twee naamloze lijsten). Er is **geen enkele lijst** die een eigen tabel nodig heeft buiten `iok_toesteltype` en `iok_standaardtekst` — dat bevestigt B02 (standaardtabel of `iok_`-tabel, geen lijstentabellen).

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

Algemene zinnen die **niet** aan een controlepunt hangen (en dus met een lege verwijzing moeten kunnen): het besluit ("Het toestel is conform de norm"), de kop- en voetteksten van het verslag, en de inleidende zinnen van de preventiesamenvatting (B11/B18). Die staan in de vier sjablonen niet in de bronnen; ze komen uit het ingevulde verslag `C_` (zie §12.3).

---

## 6. Inconsistenties tussen de bronnen (deel A)

1. **Doelgroep verschilt per formulier.** Terrein: 10 waarden met "van 1 tot 18 jaar", zonder "van 1 tot 14 jaar" en "van 2,5 tot 4 jaar". Toestel: 11 waarden met die twee, zonder "van 1 tot 18 jaar". Skate: **3 waarden in een andere bewoording** ("vanaf 6 jaar", "vanaf 9 jaar", "vanaf 12 jaar"); die hebben in de andere lijsten geen exacte tegenhanger (daar staat "- 3 jaar", "- 6 jaar", "- 9 jaar", wat evengoed "tot … jaar" kan betekenen). → B32 (één lijst), Q14 (is het verschil bewust, en welke bewoording is de officiële?).
2. **Waarden bevatten opmaak.** De doelgroepwaarden beginnen met een opsommingsteken ("- 3 jaar") en de laatste eindigt op een punt ("van 6 tot 9 jaar."). Bij het laden opschonen.
3. **Volgorde van toezicht verschilt.** Toestel: Geen / Sociale / Regelmatige / Constant. Terrein: Geen / Regelmatige / Sociale / Constant. Zelfde waarden, andere volgorde.
4. **De lijst `toestellen` verschilt per werkmap** (27 namen): "Vogelnestschommel" alleen in A_, "Evenwichtsparcours" alleen in B_, "Combinatietoestel glijbaan, glijstang en tuimelrek" alleen in de sjablonen. → B34, Q15.
5. **`Meubilair` (TER, B94) heeft geen waarden**, terwijl de cel wel een validatie heeft. Mogelijk een lege lijst in het origineel. → **Correctie in deel B (§18.1):** de lijst heeft één zin, die in `B_TER` 5.1 wordt gebruikt.
6. **Twee naamloze lijsten in TER** (`$I$131:$I$131`, `$I$118:$I$120`) met celverwijzingen A48/I131 en A54:A55, zonder waarden. Niet te interpreteren zonder het origineel; in het .md-bestand staat geen inhoud.
7. **Twee skate-onderdelen hebben geen OK/NOK-punten**: Jump-ramp en Spine-ramp hebben alleen *Afmetingen* en *Veiligheidszone*. Een inspecteur kan daar niets beoordelen, tenzij de meting zelf de beoordeling is. → Q17.
8. **Nummering is niet consequent**: "1.Toegang" (geen spatie, Glijbaan), "3, Bijkomende eisen" (komma, Curbs), "H. 1 Algemeen" (spatie, Deel 1). Bij het laden normaliseren; de code blijft de bron van de volgorde.
9. **De skate-chapters springen van H naar M/N** (Deel 1: A–H, dan M. Markeringen, N. Inlichtingen, met dezelfde nummering als EN 1176-1). Niet fout, maar bij het laden moet de code niet als volgnummer worden gebruikt.
10. **Het skate-sjabloon is een ouder .xls-bestand, maar het blad `Standaardlijsten` is wél leesbaar** (39 rijen, zeven lijsten, §4) — alleen de **data validations** zijn niet uitleesbaar. Wat ten opzichte van IND/RAT ontbreekt: r8/F ("Gemeentebestuur van de gemeente"), de IOK-adresregel bij "RA Uitgevoerd door" en de norm in de titel ("Deel 1 : Skatetoestellen algemeen :"). De kop is dus niet identiek aan IND/RAT.
11. **"Uitbater" en "Verantwoordelijke" wijzen in de praktijk beide naar het bestuur**, maar staan als twee velden in de kop. Zolang Q01 (private uitbaters) open is, blijven het twee velden.

---

## 7. Wat deel A oplevert en wat nog open is

**Beslist en verwerkt:** B32–B39 (doelgroep, toezicht, toesteltype, standaardtekst, antwoord/status, kopvelden, één checklistreeks, skate als één toestel).

**Open na deel A:**

| Nr | Punt | Voor wie |
|---|---|---|
| Q14 | Doelgroep: zijn de verschillen bewust, en volstaat één waarde? | IOK |
| Q15 | Officiële namen en volledigheid van de toesteltypes (27 vs **128** — zie §17.1) | IOK |
| Q16 | **Meetwaarden in de skate-checklist**: *Afmetingen* en *Veiligheidszone* zijn min./max.-waarden in mm, geen OK/NOK. Komen die als numerieke velden op `iok_resultaat` (bv. `iok_meetwaarde`, `iok_eenheid`) of als aparte `iok_meting`-tabel naast `iok_hicmeting`? Samen met HIC bekijken (HANDOVER, stap 3). | Dries (stap 3/4) |
| Q17 | Jump-ramp en Spine-ramp zonder beoordelingspunten (§6.7): is de meting daar de beoordeling of ontbreken er punten? | IOK |
| — | ~~"Datum onderhoud" (B37)~~ → **afgehandeld in deel B: B41** (veld vervalt, §10) | — |
| — | ~~Toezicht per toestel afwijkend van het terrein (B33)~~ → **afgehandeld: geen afwijking gevonden**; B33 blijft (§10) | — |

**Afgehandeld in deel B (§8–§19):** de ingevulde verslagen (`A_`, `B_IND`, `B_TER`, `B_SAM`, `C_`) met hun echte waarden, het HIC-blok en de risicoscore (§13), de standaardzinnen die alleen in het verslag staan (§12.3) en de twee overzichten (§16–§17, met de 31 dubbele codes en de **128** types).

---
---

# Deel B: de vijf ingevulde voorbeelden en de twee overzichten

_Datum: 2026-11-14. Stap 2 (maken), deel B. Zelfde bronnen en statuswaarden als deel A. Steunt op B01–B45._

**Afkortingen:** **A_** = `A_Verslaggeving Indienststelling Schommel.md` · **B_IND** = `B_Indienststelling Evenwichtsparcours.md` · **B_TER** = `B_risicoanalyse terrein.md` · **B_SAM** = `B_Samengesteld verslag nieuw speelterrein.md` · **C_** = `C_2026 - Jaarlijkse controle De Bogaard (algemeen).md` · **OVT** = `Overzicht bestaande speelterreinen.md` · **OST** = `Overzicht soorten speeltoestellen.md`. Celnotatie `r18/E` = rij 18, kolom E.

## 8. Bronnen, methode en afbakening

| Bron | Wat het is | Hoe gelezen |
|---|---|---|
| **A_** | Ingevulde werkmap *Indienststelling* voor één schommel (3 bladen) | volledig |
| **B_IND** | Ingevulde werkmap *Indienststelling* voor een evenwichtsparcours (2 bladen) | volledig |
| **B_TER** | Ingevulde werkmap *Risicoanalyse terrein* voor hetzelfde terrein (3 bladen) | volledig |
| **B_SAM** | De **gegenereerde PDF** van datzelfde dossier (terrein + één toestel) | volledig |
| **C_** | Een **voorbeeldverslag** van een jaarlijkse controle (geen echte inspectie: r43 "Voorbeeld :") | volledig |
| **OVT** | 635 bestaande speelterreinregels (879 terreinen) | kolomkoppen, alle codes (voor de duplicaten) en alle F/G-tellingen |
| **OST** | 128 soorten speeltoestellen met standaardeenheden | volledig |

**Methode.** Per bestand zijn de **statuswaarden** in kolom G geteld en is per blad nagegaan welke velden een waarde hebben. De honderden controlepunten zijn niet één per één overgenomen (skill `velddekking`, werkwijze 3): alleen de **structuur**, de **totalen** en de **afwijkingen** staan hier. De tellingen zijn met een script op de markdownbestanden gedaan, niet met de hand.

**Wat deel B niet doet:** geen Dataverse-ontwerp en geen definitieve kolomnamen (B01); de CRUD-matrix wordt niet tussentijds aangepast (afspraak Dries, 2026-11-14).

## 9. De vijf voorbeelden: wat ze zijn en hoeveel er echt ingevuld is

| Bestand | Bladen | Statuswaarden in kolom G | Waarvan hoofdstuk | Waarvan controlepunt | Opmerkingen |
|---|---|---|---|---|---|
| **A_** | Algemeen, **schommels**, Standaardlijsten | **47** | 16 | 31 | 1 standaardzin (M.6) |
| **B_IND** | Algemeen, Standaardlijsten | **14** | **14** | **0** | geen Deel 2-blad aanwezig |
| **B_TER** | terrein, standaardlijsten, **Verslag** | **46** | **0** | **46** | 5 opmerkingen: 1 vrije tekst (1.2) + 4 uit de standaardlijsten (`Meubilair` bij 5.1, `Schema's` bij 8.2.1–8.2.3) |
| **B_SAM** | (PDF) terrein p.1-4 + Algemeen p.1-2 | — | — | — | zelfde dossier als B_IND + B_TER |
| **C_** | (docx) cover + **1 terreinblok** + 16 toestelblokken | — | — | — | 22 foto's, 1 "Opmerkingen" |

Per blad, zodat het invulpatroon zichtbaar wordt:

- **A_ · Algemeen:** 13 hoofdstukstatus (A–L, N; **M ontbreekt**) + 7 puntstatus (G.2.5 en M.1–M.6). Hoofdstuk M staat op **OK** in het verslag, maar heeft zelf geen status; M.5 en M.6 zijn **NOK**. Van de 391 beoordeelbare punten in de sjablonen (§1) hebben er **31** een status (7 op Algemeen, 24 op schommels); de rest is leeg of hoort bij bladen die deze werkmap niet bevat.
- **A_ · schommels:** 3 hoofdstukstatus (3, 4 en 6 = nvt) + 24 puntstatus (1.1–1.17, 2.1–2.4, 5.1–5.3). Hoofdstuk 2 heeft geen status; zijn punten zijn wél ingevuld.
- **B_IND · Algemeen:** 14 hoofdstukstatus, **nul** controlepuntstatus. Er is **geen Deel 2-blad**: het toesteltype "Evenwichtsparcours" heeft er geen, en de PDF (`B_SAM`) bevat dan ook alleen "Algemeen"-pagina's.
- **B_TER · terrein:** 46 puntstatus (22 OK, 19 nvt, 5 NOK: 1.2, 5.1, 8.2.1, 8.2.2, 8.2.3), **nul** hoofdstukstatus. Punt **6.5 is leeg** en wordt in de PDF zonder status afgedrukt.
- **B_SAM:** het terrein wordt **volledig** afgedrukt (ook het lege 6.5); het toestel alleen als **hoofdstukken** A–N (omdat B_IND alleen hoofdstukken heeft ingevuld).
- **C_:** 1 terreinblok + **16 toestelblokken**. 9 toestellen conform (10 "conform"-zinnen: "Galaxy BOA 04" staat er tweemaal), 4 met bevindingen (Zelf remmende veerwip, Klimtoren met netten, Trampoline, Toren met glijbaan), 1 onbruikbaar (Vogelnestschommel), 2 verwijderd (Volleybalterrein, Dubbele veerwip paard).

## 10. Kopvelden: wat wordt echt ingevuld en wat blijft altijd leeg

| Kopveld | A_ (schommel) | B_IND (evenwichtsparcours) | B_TER (terrein) | C_ (jaarlijks) | Conclusie |
|---|---|---|---|---|---|
| Omschrijving / benaming | Schommel | Evenwichtsparcours | Speelterrein Collin Brownstraat | "De Bogaard" + 16 toestelnamen | gedekt |
| Adres | Diestseweg, 2440 Geel | Collin Brownstraat, 2440 Geel | Collin Brownstraat, 2440 Geel | — | gedekt |
| Verantwoordelijke | Stadsbestuur van de stad **+ Mevr. Greet Verwerft** | idem | idem | Stad Geel | **het veld is het bestuur (Account); de naam ernaast is de primaire contactpersoon (Contact)** → B16/B37 |
| Uitbater | Stad Geel (Werft 20) | Stad Geel (Werft 17) | Stad Geel (Werft 17) | Stad Geel | gedekt (Q01) |
| Codenummer | **BOA 34** | **SCB 01 -> SCB 04** | SCB (terrein) | BOA 1 + BOA 2, BOA 03, … | **meerdere codes per toestel** → B44 |
| Doelgroep | van 1 tot 14 jaar | van 1 tot 14 jaar | **van 1 tot 18 jaar** | — | beide lijsten in gebruik → Q14 |
| Datum controle | 19/01/2026 | 14/08/2025 | 14/08/2025 | 04/08/2026 | gedekt (B06) |
| **Toezicht** | Geen toezicht | Sociale controle | Sociale controle | — | **geen afwijking per toestel gevonden** → B33 |
| **Datum onderhoud** | **leeg** | **leeg** | **leeg** | — (veld ontbreekt) | **altijd leeg** → B41 |
| Leverancier | Kompan | Kompan | — | — | gedekt |
| Type toestel (fabrikant) | M97801-3517 | NRO811-821-871-209 | — | — | gedekt |
| **Serienummer** | **leeg** | **leeg** | — | — | **altijd leeg** → Q19 |
| Bouwjaar | 2026 | 2025 | — | — | gedekt |
| **Attest** | **EN 1176/2017** | **EN 1176/2017** | — | — | het veld "Attest" bevat de **norm**, geen document → B21 + Q08 |
| Foto | cel leeg | cel leeg | geen veld | **22× [foto]** | foto is een afbeelding, geen celwaarde → B15/B37 |
| RA uitgevoerd door | Danny Frederix | Danny Frederix | IOK + adres + Danny | — | vaste tekst + `systemuser` (B37) |
| **Opmerkingen** | leeg | leeg | leeg | **1×** (Vogelnestschommel) | → B42 |

**De drie handover-punten, kort:**

1. **Toezicht per toestel (B33).** In het enige dossier met zowel een terrein- als een toestelblad (B_, Collin Brownstraat) staat op beide **"Sociale controle"**. A_ heeft alleen een toestelblad en zegt "Geen toezicht"; C_ toont het veld niet. **Geen enkel voorbeeld wijkt per toestel af van het terrein.** B33 blijft staan, met de nuance dat het veld fysiek op het toestelblad staat en dus in een los toestelformulier (A_) de enige toezichtwaarde is.
2. **Datum onderhoud (B37).** **5 van 5 keer leeg.** Wordt geen kolom (B41); samen met serienummer een vraag aan IOK (Q19).
3. **Algemene standaardzinnen (B35).** Ze staan **niet** in de sjablonen, alleen in C_ (§12). Daarmee is de open plek uit deel A §5 (de algemene zinnen **zonder** controlepunt) ingevuld.

## 11. Antwoorden en status: het invulpatroon

De voorbeelden laten **twee invulstijlen** zien, en die zijn allebei geldig:

| Stijl | Waar | Wat de inspecteur doet |
|---|---|---|
| **Hoofdstukgestuurd** | A_ (Algemeen), B_IND | hoofdstukresultaat invullen; alleen afwijkende punten (M.5/M.6) hebben een status |
| **Puntgestuurd** | A_ (schommels), B_TER | elk controlepunt een status geven; de hoofdstukken blijven leeg |

Daaruit volgt **B40**:

- Een `iok_resultaat` ontstaat **pas** wanneer de inspecteur iets vastlegt (NOK, nvt of een opmerking). **Geen lege resultaatrijen vooraf** → **Q11 is beantwoord**.
- Bij **indienststelling en jaarlijkse controle**: hoofdstukresultaat verplicht, punten enkel bij afwijking. Bij **risicoanalyse**: alle punten verplicht.
- **Leeg punt = "niet afzonderlijk beoordeeld, gedekt door het hoofdstuk"**, niet "OK".
- Het hoofdstukresultaat is een **opgeslagen waarde** (resultaat op het hoofdstukcontrolepunt), **niet berekend**. "1 NOK = hoofdstuk NOK" wordt een **validatieregel in D3.2**. Daarmee is de tegenspraak in A_ (hoofdstuk M = OK met M.5/M.6 = NOK) een **datacontrole**, geen rekenregel; of M/N een uitzondering zijn, vraagt IOK (Q18).

Invulplicht per basis, zoals de bronnen ze tonen:

| Beoordelingsbasis | Toestel | Terrein |
|---|---|---|
| **Indienststelling** | hoofdstukresultaat verplicht; punten enkel bij NOK/nvt/opmerking (A_, B_IND) | **geen voorbeeld**: B_TER is een risicoanalyse; of het terrein bij een indienststelling volledig wordt beoordeeld, is niet bewezen → **Q22** |
| **Jaarlijkse controle** | idem (C_ toont per toestel enkel de bevindingen, geen volledige lijst) | **onduidelijk**: C_ toont bij "TERREIN" alleen een oordeel, geen checklist → **Q22** |
| **Risicoanalyse** | alle punten verplicht (B40; geen ingevuld toestelvoorbeeld) | alle punten verplicht (B_TER) |

**Wat verder opvalt:**

- **`nvt` is een volwaardig antwoord**, geen leegte: in B_TER 19 van 46, in A_ (schommels) 14 van 27. Het wordt gebruikt voor hele secties (A_ hoofdstuk 3, 4, 6) en voor losse punten.
- **Een leeg punt komt ook in een volledig ingevuld rapport voor** (B_TER 6.5) en wordt in de PDF **zonder status** afgedrukt. Een lege cel is dus nooit stilzwijgend "OK".
- **Hoofdstukken zijn soms beantwoordbaar, soms niet**: in het terreinblad zijn het koppen (geen status), in de toestelbladen niet. Dat is precies de wisselende diepte uit §14.

## 12. Opmerkingen en standaardzinnen

### 12.1 Eén vrije opmerking per blad

Elk blad eindigt op **"Opmerkingen:"**: de 12 IND/RAT-bladen (Algemeen + 11 Deel 2), het terreinblad (1×) en de 12 skate-bladen (Algemeen + 11 onderdelen). In de voorbeelden is het bijna altijd leeg; C_ gebruikt het één keer:

> "Momenteel is het nest verwijderd van het toestel. Hierdoor is het toestel onbruikbaar. De constructie levert geen direct gevaar op zonder het nest." (C_ r103-105, onder Vogelnestschommel BOA 29)

→ **B42:** één veld `iok_beoordeling.iok_opmerking`. Bij een combinatietoestel met meerdere checklists komt de tekst van alle bladen in dat ene veld; de PDF print ze één keer onderaan.

### 12.2 Welke standaardzinnenlijsten worden echt gebruikt

| Lijst in het sjabloon | Waarde in de bron | Gebruikt in | Status |
|---|---|---|---|
| `Markeringen` (4 zinnen) | "Gegevens van het toestel zijn gedeeltelijk aanwezig …" (r65) | **A_** M.6 | bevestigd |
| `Meubilair` (1 zin) | "Geen afvalbakken aanwezig op het terrein. Eventueel enkele bakken aan te brengen …" (r60) | **B_TER** 5.1 | bevestigd — **de lijst is niet leeg** (correctie op deel A) |
| `Schema's` (1 zin) | "De uitbater is momenteel niet in de bezit van de nodige schema's …" (r75) | **B_TER** 8.2.1, 8.2.2, 8.2.3 | bevestigd |
| `Inlichtingen` (4 zinnen) | — | nergens | niet gebruikt in de voorbeelden |
| `Informatie` (7 zinnen) | — | nergens | niet gebruikt |
| `AREI` (2 zinnen) | — | nergens | niet gebruikt |
| `Banken`, `Bomen`, `Belgacom`, `Gebruik` (SKT) | — | nergens | niet gebruikt |

**Niet elke opmerking komt uit een lijst.** De opmerking onder B_TER 1.2 ("Er zijn nog geen borden aangebracht in de buurt van het speelterrein …") staat **niet** in de lijst `Informatie`; het is vrije tekst. Dat bevestigt B18: een maatregel is **standaardtekst óf vrije tekst**.

**Eén tekst, geen twee.** In de formulieren bevat de opmerking onder een punt zowel de **bevinding** als de **maatregel** ("Er zijn nog geen borden … Eventueel enkele borden aanbrengen."). In v3 kan die tekst als `iok_maatregel` (gekoppeld aan het resultaat, B18) worden bewaard; `iok_beoordeling.iok_opmerking` (B42) blijft voor een korte toelichting bij het geheel. De PDF print ze onder het controlepunt.

### 12.3 De algemene zinnen die alleen in het verslag staan

C_ levert de **algemene** standaardzinnen die in geen enkel sjabloon staan. Ze horen in `iok_standaardtekst` met **soort = besluit** en **zonder controlepunt** (B35):

| Zin (letterlijk) | Bron | Wanneer |
|---|---|---|
| "Het terrein is conform de norm." | C_ r47 | terrein conform |
| "Het toestel is conform de norm." | C_ r51, 55, 59, 61, 65, 84, 88, 152, 160, 164 | toestel conform |
| "Het toestel is momenteel onbruikbaar." | C_ r102 | bevinding (B18/B24) |
| "Het toestel is verwijderd van het terrein" (r122, zonder punt) / "… terrein." (r156, met punt) | C_ r122, 156 | bevinding verwijdering (B12/V4) — **normaliseren bij het laden** |
| "ALGEMEEN BESLUIT: Gezien de inbreuken in het verslag dienen de nodige maatregelen genomen te worden opdat het speelterrein aan de algemene veiligheidsverplichting van periodieke controle speelterrein en speeltoestellen overeenkomstig het KB 28 maart 2001 zou voldoen." | C_ r165-166 | slottekst met inbreuken |

**Ontbreekt:** de **conforme variant** van het algemeen besluit (een verslag zonder inbreuken). Geen enkel voorbeeld vult die in → open punt voor IOK, geen aanname.

**Layout, geen data:** "JAARLIJKSE CONTROLE:", "TERREIN.", "Algemeen:" en "Specifieke onderdelen:" zijn koppen in de PDF. "Specifieke onderdelen" verwijst naar de Deel 2-checklists; het model heeft daarvoor `iok_checklist.iok_deel` (B19/B26). De titel per blad is **niet betrouwbaar**: in de IND-template staat op het Algemeen-blad "Indienststelling", op alle 11 Deel 2-bladen "Risicoanalyse" (B38). De **beoordelingsbasis** (B21) bepaalt de titel, niet de tekst in de cel.

### 12.4 Het blad "Verslag" is een view, geen tabel

B_TER heeft een derde blad **"Verslag"**: uitsluitend de **5 NOK-punten** met hun koppen en opmerkingen (1.1/1.2, 5.1, 8.2/8.2.1–8.2.3). Dat is een **gefilterde lijst van de beoordeling**, geen aparte gegevenstabel → bevestigt **B10** (geen eigen overzichtstabellen; views/exports). Het is ook de basis voor "maatregelen en tekortkomingen per bestuur" (D4.3).

## 13. HIC-blok en risicoscore

### 13.1 HIC: de legende bestaat, de meting niet

C_ r8-17 bevat de legende **"HIC-waarde metingen"** met precies de vijf velden van B20:

| Legendeveld | Betekenis | Drempel | B20-veld |
|---|---|---|---|
| **No.** | nummer van de meting | — | volgnummer |
| **Peak** | G-waarde (de klap die de hersenen ondervinden) | **< 200** | Peak (G-waarde) |
| **HIC** | head injury criterion | **< 1000** | HIC-waarde |
| **Cm** | valhoogte van de test, "bij benadering gelijk aan de valhoogte van het toestel" | — | valhoogte (cm) |
| **Datum / Time** | moment van de meting | — | datum/tijd |

**Geen enkel voorbeeld vult een meting in.** B20 blijft dus ongewijzigd (5 velden, optioneel, alleen bij een niet-conforme valondergrond); de drempels zijn nu bronvast (B45), alleen "wanneer verplicht?" blijft open (Q03).

### 13.2 Risicoscore: de volledige tabel is bekend, niemand vult ze in

C_ r18-41 geeft de **volledige scoretabel**:

| Impact | | Kans/frequentie | | Blootstelling | |
|---|---|---|---|---|---|
| Eerste hulp vereist | 1 | Vrijwel onmogelijk | 0,2 | Zeer zelden in gebruik | 0,5 |
| Blijvend letsel | 3 | Zeer onwaarschijnlijk | 0,5 | Zelden in gebruik | 1 |
| Blijvend ongeschikt | 7 | Op lange termijn | 1 | Regelmatig in gebruik | 2 |
| Zeer ernstig, één dode | 15 | Ongewoon maar mogelijk | 3 | Meestal in gebruik | 3 |
| Catastrofaal, meerdere doden | 40 | Goed mogelijk | 6 | Steeds in gebruik | 6 |
| | | Kan worden verwacht | 10 | Heel de tijd in gebruik | 10 |

**R = impact × kans × blootstelling**, met vijf klassen: **R ≤ 20 Licht** ("misschien aanvaardbaar") · **20 < R < 70 Mogelijk** · **70 < R < 160 Substantieel** · **160 < R < 320 Hoog** · **R > 320 Zeer hoog** ("overweeg stopzetting").

→ **B45:** de tabel is bronvast; `iok_resultaat` behoudt de drie **optionele** velden impact, kans en blootstelling (v2 had ze al). **Geen enkel voorbeeld vult een score in** (ook B_TER niet), dus of IOK ze in de praktijk gebruikt en op welk niveau, blijft **Q08**. De legende wordt in het jaarverslag **altijd** afgedrukt (C_ p.1), ook als er geen score is ingevuld; dat is rapportopmaak, geen veld.

**Interpretatie voor stap 4:** de R en de klasse kunnen **berekend** worden (formule/berekend veld) en hoeven niet bewaard; alleen de drie factoren worden ingevuld. Dat is nog geen beslissing.

## 14. Diepte van de hiërarchie

De HANDOVER (stap 3b) vroeg of de ingevulde verslagen dieper gaan dan de 3 niveaus van de lege sjablonen. **Ja, tot 4.**

| Code | Diepte | Waar | Bewijs |
|---|---|---|---|
| `1.1.1` | 3 | B_TER r27 | beantwoord (OK) |
| `A.1.1` | 3 | A_ Algemeen r36 | aanwezig, niet beantwoord |
| **`G.2.6.2`** | **4** | **C_ r113-117** | **bevinding op een 4-niveau-code** ("De bodem mag geen gevaar opleveren voor struikelen") |
| `I.2.9.1` | 4 | IND r416 | subregel in kolom B (geen eigen statuscel) |
| `J.1.1.1` | 4 | IND r457 | idem |
| `E.5.1.1` | 4 | IND r241-242 | **foutieve code**: staat onder F.5.1 (moet F.5.1.1 zijn) |

**Conclusie:**

- **Beantwoordbare rijen** gaan in de sjablonen max. **3** niveaus diep; de **codes** gaan tot **4**. De 4-niveau-codes staan in kolom B als subregel, niet als aparte rij met een statuscel. C_ laat zien dat er in de praktijk **wel** op zo'n code wordt beoordeeld → het model moet ze kunnen adresseren.
- **B43:** `iok_controlepunt.iok_ouder` blijft **onbeperkt zelfverwijzend**; elk controlepunt krijgt een tweede lookup **`iok_hoofdstuk`** naar het bovenste niveau, gevuld bij het aanmaken van de checklistversie en daarna onveranderlijk (B19). Zo is "1 NOK = hoofdstuk NOK" in één stap te valideren (B40) zonder de ouderketen te volgen.
- **Normaliseren bij het laden:** `E.5.1.1` → `F.5.1.1`; "1.Toegang" → "1. Toegang"; "3, Bijkomende eisen" → "3. Bijkomende eisen" (deel A §6.8).
- **`iok_hoofdstuk` is geen vervanging van `iok_ouder`**: de ouder blijft nodig voor de volgorde en de weergave van de boom; `iok_hoofdstuk` is de directe ingang voor de validatie.

## 15. Nieuwe velden, tabellen en regels die deel B oplevert

| # | Wat | Type | Bron | Beslissing | Gevolg |
|---|---|---|---|---|---|
| 1 | `iok_beoordeling.iok_opmerking` | tekst | "Opmerkingen:" op elk blad; C_ r103-105 | **B42** | nieuwe kolom op een bestaande tabel |
| 2 | `iok_controlepunt.iok_hoofdstuk` | lookup → `iok_controlepunt` | G.2.6.2 (C_), I.2.9.1, J.1.1.1 | **B43** | nieuwe kolom, onveranderlijk |
| 3 | `iok_toestelcode` | **nieuwe tabel**, N:1 → `iok_speeltoestel` | "SCB 01 -> SCB 04", "BOA 1 + BOA 2" | **B44** | nieuwe tabel + alternatieve sleutel; `iok_speeltoestel.iok_code` = hoofdcode |
| 4 | Hoofdstukresultaat | `iok_resultaat` op het hoofdstukpunt | A_ (13 hoofdstukstatus), B_IND (14) | **B40** | geen kolom; semantiek + validatie in D3.2 |
| 5 | Algemene besluitzinnen (5 unieke) | `iok_standaardtekst`, soort = besluit, controlepunt leeg | C_ r47-166 | **B35** | inhoud, geen kolom (§12.3 telt 6 citaten: de verwijderingszin heeft twee schrijfwijzen) |
| 6 | Standaardzinnen per controlepunt | `iok_standaardtekst` | Markeringen r65, Meubilair r60, Schema's r75 | **B35** | inhoud; `Meubilair` is niet leeg |
| 7 | Versiedatum in de PDF-voettekst | **geen nieuw veld** | B_SAM "Versie d.d. :28/11/2025" | voorstel stap 4 | de generatiedatum is het onveranderlijke aanmaakmoment van `iok_rapportversie`; de controledatum blijft de versiesleutel (B06) |
| 8 | Standaardeenheden per type | `iok_toesteltype.iok_eenheden` | OST kolom C (1–9) | **B26** | bestaande afspraak, nu met bron |
| 9 | Norm in het veld "Attest" | `iok_beoordeling.iok_norm` | A_/B_IND r24 "EN 1176/2017" | **B21** | `iok_attest` blijft voor het document; het formulier gebruikt "Attest" voor de norm |
| 10 | Contactpersoon náást "Verantwoordelijke" | `contact` (primair) | A_/B_IND r10 "Mevr. Greet Verwerft" | **B16/B37** | geen extra veld; het veld zelf blijft het bestuur, de PDF print de primaire contactpersoon erbij |

**Geen nieuwe tabel voor:** het "Verslag"-blad (§12.4), de HIC-meting (B20), de risicoscore (B45) en de algemene besluiten (B35).

## 16. Overzicht bestaande speelterreinen

### 16.1 Kolomkoppen (letterlijk)

| Kolom | Kop |
|---|---|
| A | `ID_speelterrein` |
| B | `Code_speelterrein` |
| C | `Naam_speelterrein` |
| D | `Gemeente` |
| E | `Bestuur` |
| F | `Gecontroleerdetsperrein_terreinen` (**typo** voor "Gecontroleerde terreinen") |
| G | `Gecontroleerde_toestellen` |

### 16.2 Wat de 635 rijen bevatten

| Kenmerk | Waarde |
|---|---|
| Rijen | **635** (r2–r636, ononderbroken; geen lege tussenrijen) |
| Unieke `ID_speelterrein` | **635**, geen dubbele ID; bereik **1–761** met gaten (legacy) |
| Rijen **zonder** code | **31** — waarvan **alle 21 rijen van Oud-Turnhout**, plus Arendonk r13, Herentals r292 en 8 rijen in Heist-op-den-Berg (r207, r219–r225) |
| Codes | **604** ingevuld, **574** uniek (exact) |
| **Dubbele codes** | **31** na normalisatie naar hoofdletters, **30** exact (alleen `SPORT`/`Sport` verschilt) → bevestigt de vaste eis en B25 |
| Gemeenten | **26** (Arendonk … Westerlo) |
| `Bestuur` | **620 "Gemeente"**, **15 "OCMW"** — dus een **soort**, geen naam |
| F (gecontroleerde terreinen) | **2 rijen leeg**; 0–15; **6× nul**, **561× één**, **68× meer dan één**; **som 879** |
| G (gecontroleerde toestellen) | **3 rijen leeg**; 0–83; 7× nul; **som 5.177** |

**De sommen zijn de projectvolumes.** 879 ≈ ±850 terreinen en 5.177 ≈ ±5.250 toestellen (projectopdracht r339-340). Een rij is dus **geen terrein maar een groepering**: 68 rijen dekken meer dan één locatie (uiterste: "Onthaalmoeders OCMW", Laakdal, F = 15, G = 42). Dat botst met "één `iok_speelterrein` per code" en met "één verslag per terrein" → **Q20** (hoge prioriteit, ontwerpvraag voor stap 3). **Geen kolom voor F/G in v3**: het blijven tellingen (view/export).

**Twee datakwaliteitsproblemen in dezelfde tabel:**

1. **31 rijen hebben geen code** — één volledige gemeente (Oud-Turnhout, 21 terreinen) en 10 losse rijen. Zonder code kan B25 (code verplicht en uniek) niet worden toegepast; dit is een migratie- en niet een modelvraag, maar het moet samen met Q20 worden beslist.
2. **Drie rijen hebben geen telling**: r413 (Mol, Paviljoenstraat, alleen F), r569 (Rijkevorsel, Donk) en r597 (Vosselaar, Gemeenteschool centrum overdekt). De sommen zijn dus een **ondergrens**.


### 16.3 De 31 dubbele codes

De codes zijn hier **zonder onderscheid tussen hoofd- en kleine letters** vergeleken. Exact vergeleken zijn het er **30**: `SPORT` (r410, Sporthal Den Uyt, Mol) en `Sport` (r395, Skatepark, Meerhout) verschillen alleen in schrijfwijze. Omdat de vaste eis van 31 dubbele codes uitgaat, is normaliseren naar hoofdletters bij het laden de juiste aanname — maar dat is een **laadregel**, geen modelregel.

| Code | Record 1 (rij · ID · naam · gemeente) | Record 2 |
|---|---|---|
| `NP` | r300 · 455 · Speelterrein Netepark · Herentals | r296 · 501 · Speelterrein Netepark zwembad · Herentals |
| `DD` | r299 · 457 · Speelterrein Diependaal-oud · Herentals | r291 · 420 · Speelterrein Diependaal · Herentals |
| `HO.B6` | r286 · 115 · Veldstraat · Hoogstraten | r261 · 120 · Buizelhoek · Hoogstraten |
| `SK` | r306 · 438 · Skateterrein Herenthoutseweg · Herentals | r94 · 343 · 't Sonneveld · Baarle-Hertog |
| `E` | r323 · 708 · BKO Hulshout · Hulshout | r206 · 101 · Winterstraat · Heist-op-den-Berg |
| `C` | r322 · 707 · Speelplein Site Schoolstraat Houtvenne · Hulshout | r213 · 100 · Ganzenakker · Heist-op-den-Berg |
| `I` | r320 · 713 · School Strepestraat · Hulshout | r212 · 96 · Rashoeve · Heist-op-den-Berg |
| `HO.B10` | r282 · 625 · ZOC Hoogstraten · Hoogstraten | r254 · 415 · Speelterrein Jaak Aertslaan · Hoogstraten |
| `AC` | r226 · 537 · Moerenloopstraat · Heist-op-den-Berg | r9 · 402 · Speelterrein Academie · Arendonk |
| `N` | r209 · 110 · Blokstraat · Heist-op-den-Berg | r47 · 320 · Kruisblokken · Balen |
| `SBR` | r138 · 505 · Brabantsblok · Geel | r114 · 370 · Sportcentrum Brasel · Dessel |
| `SHE` | r235 · 611 · Heide · Herselt | r140 · 384 · Speelplein Helleblok · Geel |
| `HO.B14` | r269 · 532 · Eligius Van Den Akerplein · Hoogstraten | r253 · 510 · E.Van Den Akerplein · Hoogstraten |
| `SW` | r243 · 725 · BKO Varenwinkel · Herselt | r237 · 617 · Varenwinkel · Herselt |
| `SAS` | r242 · 699 · Skatepark De Mixx · Herselt | r108 · 381 · Speelterrein Sas 4 · Dessel |
| `F` | r324 · 709 · BKO Westmeerbeek · Hulshout | r216 · 105 · Heivelden · Heist-op-den-Berg |
| `KER` | r523 · 491 · Kerkakker · Ravels | r119 · 49 · Kerkstraat Witgoor · Dessel |
| `SKP` | r522 · 235 · Skate-terrein Poppel · Ravels | r127 · 578 · Speelterrein de Korte Plek · Geel |
| `GBR` | r521 · 230 · Basisschool Ravels · Ravels | r378 · 680 · Speelbos Brulens · Lille |
| `GKL` | r525 · 233 · Basisschool Klimop · Ravels | r387 · 467 · Klaprooslaan · Lille |
| `RI.G/0.12` | r565 · 314 · Molenakkers · Rijkevorsel | r551 · 237 · Kinderclub Chalet · Rijkevorsel |
| `RI.G/0.02` | r559 · 524 · Heibraak · Rijkevorsel | r557 · 242 · Varenvelden · Rijkevorsel |
| `SHO` | r541 · 518 · Skate terrein · Retie | r147 · 350 · Holvenseheide · Geel |
| `STA` | r512 · 217 · Weelde Statie · Ravels | r165 · 534 · Stadspark · Geel |
| `KRUI` | r403 · 564 · Kruiwagenstraat · Mol | r31 · 745 · Kruierie · Balen |
| `HH` | r326 · 712 · Sportpark Joris Verhaegen · Hulshout | r10 · 495 · Het Hof · Arendonk |
| `G` | r325 · 710 · BKO Houtvenne · Hulshout | r204 · 111 · Dophei · Heist-op-den-Berg |
| `SPORT` | r410 · 636 · Sporthal Den Uyt · Mol | r395 · 714 · Skatepark · Meerhout |
| `BRA` | r510 · 215 · De Braak · Ravels | r236 · 623 · BKO Ramsel · Herselt |
| `PAR` | r500 · 389 · Park Ravels · Ravels | r400 · 569 · Kinderopvang Pardoes · Mol |
| `BOS` | r418 · 752 · Bosveld · Mol | r17 · 751 · Bosvelden · Arendonk |

**Wat dit leert:**

1. **B25 klopt**: de code is niet uniek, en **23 van de 31** duplicaten overschrijden een gemeentegrens (SK, E, C, I, AC, N, SBR, SHE, SAS, F, KER, SKP, GBR, GKL, SHO, STA, KRUI, HH, G, SPORT, BRA, PAR, BOS). De 31 zijn dus **geen binnen-gemeentelijke nummering** maar een echt probleem; de andere 8 (NP, DD, HO.B6, HO.B10, HO.B14, SW, RI.G/0.12, RI.G/0.02) blijven binnen één gemeente.
2. **`Bestuur` is een soort, geen bestuur**: "Gemeente" (620) of "OCMW" (15) is niet te koppelen aan één `account`. De kolom `Gemeente` + `Bestuur` samen wijzen wel het bestuur aan (B16: één Account per gemeente/OCMW).
3. **`ID_speelterrein`** is een **legacy sleutel** (635 uniek, bereik 1–761 met gaten). Niet overnemen als `iok_code`; wel bruikbaar als migratiesleutel.
4. **31 rijen hebben geen code**, waaronder **alle 21 Oud-Turnhout-rijen** (§16.2). Een terrein zonder code kan niet aan B25 voldoen; dat is een migratiepunt, geen ontwerpvraag.
5. **Geen adres, doelgroep, toezicht of eenheden** in dit overzicht: die komen uit de sjablonen/dossier, niet hiervandaan.
6. **F/G zijn tellingen** (§16.2), geen stamgegevens.

## 17. Overzicht soorten speeltoestellen

### 17.1 Omvang: 128 types in 16 categorieën

| Categorie | Types | Eenheden (aantal types per waarde) |
|---|---|---|
| Zandbak | 4 | 1×1, 2×1, 3×1, 4×1 |
| Wip | 8 | 1×8 |
| Schommel | 8 | 1×6, 2×2 |
| Glijbaan | 8 | 1×6, 2×1, 3×1 |
| Draaitoestel | 5 | 1×5 |
| Sporttoestel | 19 | 1×16, 2×1, 3×2 |
| Combinatietoestel | 7 | 2, 3, 4, 5, 6, 7, 9 (elk 1) |
| Evenwichtstoestel | 8 | 1×5, 2×2, 3×1 |
| Kabelbaan | 2 | 1×2 |
| Skate | 2 | 1×2 |
| Speelhuisje | 6 | 1×4, 2×1, 3×1 |
| Andere | 12 | 1×12 |
| Zitelemeneten (typo) | 8 | 1×8 |
| Activiteitpaneel | 13 | 1×13 |
| Water | 5 | 1×3, 2×1, 3×1 |
| Klimmen | 13 | 1×6, 2×4, 3×1, 4×1, 5×1 |
| **Totaal** | **128** | **196 eenheden** als je alle types optelt |

**Correctie op B26:** er staan **128** types in de bron, niet 145. Die 145 is het **laatste rijnummer** (r145), geen aantal: tussen r3 en r145 staan **128** types en **15** rijen die alleen een categoriekop zijn (`Zandbak` op r3 is zowel kop als type). De **beslissing B26 blijft ongewijzigd** (type = eigen versieerbare opzoektabel, categorie = keuzelijst, type → checklist N:N); alleen het **aantal** en de **categorie-indeling** zijn gecorrigeerd. Er zijn **16** categorieën, niet 15.

**Structuur van het blad:** de categorie staat **alleen op de eerste rij** van elk blok (kolom A), de types staan in kolom B en de eenheden in kolom C. Bij het laden moet de categorie dus **naar beneden worden doorgetrokken**. Er zijn **geen dubbele typenamen**.

**Eenheden zijn een standaardwaarde, geen vaste regel:** "Evenwichtsparcours 4 elementen" = 2 eenheden, "Combinatietoestel 9 eenheden" = 9, "Zandbak met 3 spelelementen" = 4. → `iok_toesteltype.iok_eenheden` als **default** op het type (B26), per dossier bevroren (B14). Dat sluit aan op Q12 (het financiële overzicht) maar beantwoordt het niet.

### 17.2 De 27 namen uit de sjablonen tegenover de 128 types

| | Aantal | Voorbeelden |
|---|---|---|
| **Exacte match** | **10** | Vogelnestschommel, Draaitoestel, Glijbaan, Houten doel(en), Kabelbaan, Klimnetten, Metalen doel(en), Springkasteel, Tuimelrek, Zandbak |
| **Geen exacte match** | **17** | Basketpaal (→ Basketbalpaal), Klimtoren (→ Klimtoren met glijbaan / Bandenklimtoren), Rioolbuis (→ Tunnel), Schommel (→ Schommel enkel/dubbel), Wip (→ Wip 2/4 zitjes), Veertoestel eekhoorn/hond/moto/paard (→ Veertoestel enkel/dubbel/meerdere zitjes), Evenwichtsparcours (→ 2/3/4/6/12 elementen), Houten klimrek/klimtoren/schuilhut/trein, Schommel met platform/twee zitjes, Toren met glijbaan |

**Conclusie:** de lijst van 27 en de lijst van 128 zijn **twee verschillende vocabulaires**. De 27 is een **legacy-vrije lijst** per werkmap (A_ en B_ verschillen: "Vogelnestschommel" vs "Evenwichtsparcours"); de 128 is de **officiële types-met-eenheden**. Dat scherpt **Q15** aan: welke namen zijn leidend, en hoe mapt de oude lijst op de nieuwe?

### 17.3 Type → checklist is 0..N, niet 1..N

Er zijn **11 Deel 2-bladen** (schommels, Glijbaan, Kabelbaan, Draaitoestel, Wip, Doelen, zandbak, Water, springkasteel, Zware balken, Springtoestel) tegenover **128 types**. Niet elk type heeft dus een Deel 2-checklist:

- **B_IND bewijst het:** "Evenwichtsparcours" heeft geen Deel 2-blad; het verslag bevat alleen Deel 1 (Algemeen).
- De bladen **"Zware balken"** en **"Springtoestel"** hebben **geen gelijknamig type** (vermoedelijk "Evenwichtsbalken" en "Trampoline"/"Springkasteel", maar dat is niet bewezen).

→ **Q21:** is de N:N type → checklist **0..N**? En welke types horen bij welk blad? B26 blijft inhoudelijk staan, maar de kardinaliteit moet worden bijgesteld. Voor de vocabulairekloof: C_ bevat "Trampoline", "Volleybalterrein" en "Fitnesstoestel(len)", die als type in OST bestaan, maar **"Evenwichtsbalken" bestaat in OST niet** — die naam komt alleen voor in het Deel 2-blad *Zware balken* en in C_. Precies daarom is de mapping niet te gokken.

### 17.4 Naamgeving en kwaliteit van de lijst

- **Typo's in de types:** "Zitelemeneten" (→ Zitelementen), "Klimcombiantie" (2×, → Klimcombinatie), "1 Puntschommel" (→ 1-puntschommel), "schommelwip", "fietscarousel" (kleine letter). In de **sjabloonlijst van 27** (§17.2) staat bovendien "veertoestel paard" met een kleine letter; dat is een andere lijst en telt hier niet mee.
- **Nieuwe/atypische types:** "Teqball-tafel", "Pana-installatie", "Monkeybars", "Indoor speeltoestel", "Beweegbank", "Chillzone". Geen bewijs of die onder EN 1176 vallen → niet zelf interpreteren (Q15/Q21).
- **Categorie "Andere"** is een restgroep van 12 types; bij het laden als keuzelijst behouden (B26).

## 18. Correcties op deel A

1. **`Meubilair` is niet leeg.** Deel A §4 en §6.5 zeggen "geen waarden"; de bron heeft **1 waarde** (TER r60: "Geen afvalbakken aanwezig op het terrein. Eventueel enkele bakken aan te brengen op of naast het terrein."), en B_TER gebruikt ze bij 5.1. Daarmee blijft `Meubilair` een lijst met inhoud — en komt het aantal standaardzinnenlijsten op **10**, omdat het skate-sjabloon er een tiende bij heeft (`Gebruik`, §4).
2. **128 types, niet 145.** B26 noemt 145; de bron telt **128** in **16** categorieën (§17.1). B26's beslissing zelf verandert niet.
3. **De hiërarchie gaat tot 4, niet 3.** Deel A §2 en de HANDOVER gaan uit van max. 3 niveaus (hoofdstuk → subkop → controlepunt). Dat klopt voor de **beantwoordbare rijen**, maar **niet voor de codes**: G.2.6.2, I.2.9.1 en J.1.1.1 zijn 4 niveaus en C_ beoordeelt op G.2.6.2 → B43.
4. **Toezicht (B33) is bevestigd.** Geen enkel voorbeeld wijkt per toestel af van het terrein. De enige nuance: A_ is een los toestelformulier zonder terreinblad, dus daar is de toestelwaarde de enige.
5. **De algemene standaardzinnen bestaan wél**, maar alleen in het verslag (C_), niet in de sjablonen → §12.3. De open plek uit deel A §5 (zinnen zonder controlepunt) is daarmee ingevuld.
6. **De titel per blad is onbetrouwbaar.** In de IND-template staat "Indienststelling" op Algemeen en "Risicoanalyse" op alle 11 Deel 2-bladen. Niet als veld modelleren; de beoordelingsbasis (B21) stuurt de titel.

## 19. Wat deel B oplevert en wat nog open is

### 19.1 Beslist en verwerkt

**B40–B45:** invulregel en hoofdstukresultaat (B40, beantwoordt Q11) · datum onderhoud vervalt (B41) · `iok_opmerking` op de beoordeling (B42) · onbeperkte hiërarchie + `iok_hoofdstuk` (B43) · `iok_toestelcode` (B44) · risicoscore en HIC-drempels (B45).

**Bevestigd zonder wijziging:** B15/B37 (foto), B16/B37 (verantwoordelijke = bestuur, contactpersoon apart), B18 (maatregel = standaardtekst of vrije tekst), B19 (checklistversie), B20 (HIC), B21 (norm/basis; "Attest" bevat de norm), B23 (terreinbesluit), B24 (onbruikbaar = bevinding), B25 (code uniek — nu via B44), B26 (type/eenheden), B33 (toezicht op terrein), B35 (standaardtekst), B38 (één checklistreeks), B10 (geen overzichtstabellen).

### 19.2 Open na deel B

| Nr | Punt | Voor wie | Status |
|---|---|---|---|
| Q03 | HIC: **wanneer** verplicht (drempels zijn bekend: G < 200, HIC < 1000)? | IOK | smaller |
| Q08 | Risicoscore: gebruikt IOK ze, en op welk niveau? (tabel is bekend) | IOK | smaller |
| Q14 | Doelgroep: één waarde, en zijn de verschillen bewust? (A_ 1–14, B_TER 1–18) | IOK | open |
| Q15 | Officiële namen: 27 vs **128** types; 10 exacte matches | IOK | aangescherpt |
| Q16 | Meetwaarden skate (Afmetingen/Veiligheidszone) vs HIC: één patroon? | Dries | stap 3 |
| Q17 | Jump-ramp en Spine-ramp zonder beoordelingspunten | IOK | open |
| **Q18** | Hoofdstuk M = OK met M.5/M.6 = NOK: vergissing of uitzondering? | IOK | **nieuw** |
| **Q19** | Datum onderhoud en serienummer: gebruikt IOK ze? | IOK | **nieuw** |
| **Q20** | Wat is een rij in OVT? 635 rijen, 879 terreinen, 31 dubbele codes (31 rijen zonder code) | IOK (hoog) | **nieuw** |
| **Q21** | Type → checklist: 0..N? Welk type bij welk Deel 2-blad? | IOK | **nieuw** |
| **Q22** | Jaarlijkse controle: terreinchecklist of enkel een terreinoordeel? | IOK | **nieuw** |

**Niet door deel B geraakt:** Q01, Q02, Q04–Q07, Q09, Q10 en Q13 blijven open zoals ze in `02_werk/open_vragen.md` staan. Q11 is beantwoord (B40); Q12 blijft open, maar het deel "standaardeenheden per type" is nu gedekt (§17.1).

### 19.3 Gevolgen voor de andere stappen (niet nu uitvoeren)

- **CRUD-matrix (stap 1):** `iok_toestelcode` (B44), `iok_beoordeling.iok_opmerking` (B42) en `iok_controlepunt.iok_hoofdstuk` (B43) zijn nieuwe rijen/kolommen; **D3.2** krijgt de validatie "1 NOK = hoofdstuk NOK" en de invulplicht per basis (B40). Net als het contact-punt van de HANDOVER **niet tussentijds aanpassen**.
- **Stap 3 (ontwerpvragen):** Q20 (groepering boven `iok_speelterrein`?), Q21 (kardinaliteit type → checklist), Q16 (meetwaarden), Q18 (M/N), Q22 (terrein bij jaarlijkse controle). Q11 is afgehandeld.
- **Stap 4 (datamodel v3):** `iok_hoofdstuk`, `iok_toestelcode`, `iok_opmerking`, de validatieregels en de standaardzinnen (5 besluiten + de gebruikte lijsten).
- **Stap 4, risicoscore (B45):** (1) **R = I×K×B en de risicoklasse zijn berekend**, geen invoervelden (berekende kolom). (2) **Dataverse-keuzewaarden zijn gehele getallen**, terwijl kans en blootstelling decimale factoren hebben (0,2 / 0,5): kies tussen een **opzoektabel met label + decimale factor** of een **decimaal veld met vaste toegelaten waarden**. Geen gewone keuzelijst met de factor als waarde.
- **Stap 5 (review):** les 4b/4c/4d ontbreekt nog in `01_context/cursus/`; Q09 blijft wachten.

**Deel C:** inhoudelijk afgedekt door §16–§17. Wat resteert is het **antwoord op Q20** (betekenis van een rij en van F/G) en de **definitieve mapping** van Q15/Q21; daarna kan het ERD in stap 6 zonder open bronvragen worden getekend.
