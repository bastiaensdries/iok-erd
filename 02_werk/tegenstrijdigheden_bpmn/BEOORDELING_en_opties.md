# Beoordeling van "Tegenstrijdigheden tussen BPMN, IOK-feedback en datamodel v3"

_2026-11-19. Nagekeken door Claude tegen `00_bronnen/BPMN/IOK_02_ToBe_uitgeklapt_aangepast.bpmn` (met de toelichtingen per taak), `03_output/datamodel_v3.md`, `02_werk/crud_matrix.md` en `03_output/spec.yaml`. **Er is niets beslist en niets gewijzigd.** Het team beslist op 20/11; elke aanvaarde keuze krijgt een B-nummer vanaf **B94** (B89–B93 zijn intussen gebruikt, het brondocument spreekt nog van "vanaf B89")._

Brondocument: `TEGENSTRIJDIGHEDEN_en_voorstellen.md` in deze map (16/11). De puntnummers hieronder volgen dat document.

## Voor agents die hierop gezet worden

- **Alleen lezen en voorstellen.** Geen wijzigingen aan `datamodel_v3.md`, `spec.yaml`, `BESLISSINGEN.md`, `open_vragen.md`, de scripts of Dataverse. Geen B-nummers uitdelen.
- Schrijf je bevindingen in een **eigen bestand in deze map**, bv. `agent_<naam>_<onderwerp>.md`, zodat meerdere agents elkaar niet overschrijven.
- Steun elke bewering op een bron (pad + regel, B-nummer, BPMN-taak). Lees de BPMN **in het `.bpmn`-bestand**, niet enkel in `01_context/bpmn/`: zie punt 0.
- Twijfel over wat Dataverse of Power Platform kan → Microsoft Learn, met bron.
- Per punt: **opties** met gevolg (structuur? rollen? enkel een regel? enkel tekst?) en een aanbeveling. De keuze is aan het team.

---

## 0. Belangrijker dan het document zelf: de BPMN-toelichtingen ontbreken in de markdownversie

- **Vaststelling:** `tools/bpmn_naar_md.py` neemt de `<bpmn:documentation>`-elementen niet mee. Het `.bpmn`-bestand bevat er 35, met onder meer verwijzingen naar het interview met IOK (S11) en de klantfeedback van 13/11. `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md` bevat enkel taaknamen en beslissingen. Het datamodel is gebouwd op die markdownversie.
- **Vergelijkbaar met** het gat van de tekstvakken in `bronnen_naar_md.py` (HANDOVER, 17/11).
- **Opties:**
  - A. Script herstellen (toelichting per taak meenemen), conversie opnieuw draaien, daarna alle toelichtingen één keer tegen het model leggen en de afwijkingen oplijsten. *Aanbevolen: dit is de basis voor de rest van deze lijst.*
  - B. Enkel de toelichtingen die het brondocument citeert behandelen. Risico: andere afwijkingen blijven onopgemerkt.

## 1. Jaarlijkse controle: alle punten of enkel het besluit? — **klopt, echte tegenstrijdigheid**

- BPMN (toelichting bij "Jaarlijks alle toepasselijke controlepunten beoordelen", S01 p.8, S11 00:36): "Jaarlijks opnieuw alle toepasselijke punten beoordelen, ook bij overgenomen gegevens."
- Model: B72 / regel 1 → bij jaarlijks enkel het besluit verplicht. Het echte verslag `C_2026` volgt B72 (enkel "Het toestel is conform de norm.").
- Q27 bestaat al (bevestiging van B72).
- **Opties:**
  - A. Q27 aanvullen met het BPMN-citaat en de vraag "bekijken of vastleggen?" aan IOK stellen; tot dan B72 laten staan. *Aanbevolen.*
  - B. Nu al regel 1 voor jaarlijks gelijkstellen aan indienststelling (elk hoofdstuk of punt een antwoord). Gevolg: enkel regel 1 en de invulplicht in het invulscherm; geen structuurwijziging. Overgenomen resultaten moeten dan bevestigd worden (dat doet regel 9 al).

## 2. Moment waarop het dossier op slot gaat — **klopt niet**

- Het model doet al wat het voorstel vraagt: het slot gaat dicht bij **D3.9** ("Definitieve PDF … bewaren" = `D3_archive`), niet bij het genereren van de PDF. Tijdens nakijken en corrigeren (D3.7–D3.8) blijft het dossier In uitvoering. Bronnen: CRUD-matrix D3.8 en D3.9, B57 (c), B74.
- **Opties:** geen modelwijziging. Hooguit de formulering in het overzichtsdocument voor het team verduidelijken.

## 3. Rechten van de inspecteur op stamgegevens — **klopt, belangrijk**

- BPMN (toelichting bij "Toestel, norm en beoordelingsbasis vaststellen", S11 00:34–00:39): "de inspecteur kan zo nodig een nieuw toestel registreren; beschermde norm- en standaardteksten blijven bij bevoegd stamgegevensbeheer."
- Model: inspecteur enkel lezen op terrein, toestel en toestelcode (`spec.yaml`, rollen, met `# ONZEKER: Q06`).
- Dit beantwoordt Q06 voor de **toestellen**, met het interview als bron. De rollen zijn nog niet gebouwd, dus nu beslissen is goedkoop.
- Spanning met **B08** ("enkel één bevoegde beheerder wijzigt stamgegevens"): de BPMN zegt *registreren*, niet *wijzigen*.
- **Opties:**
  - A. Inspecteur: **maken** op `iok_speeltoestel` en `iok_toestelcode`; **wijzigen** enkel voor de beheerder. Gevolg: de inspecteur kan een tikfout in een net aangemaakt toestel niet zelf verbeteren.
  - B. Inspecteur: **maken en wijzigen** (Org) op toestel en toestelcode. Ruimer dan B08; vraagt een nieuwe beslissing die B08 voor toestellen verfijnt.
  - C. Maken + wijzigen op **Eigen** niveau (enkel toestellen die hij zelf aanmaakte). Let op: eigenaarschap van toestellen is gebruiker/team (B63); te controleren of dat praktisch werkt.
  - Terrein en terreingroep: blijven alleen-lezen tot IOK antwoordt (punt 9).
- Gevolg in alle gevallen: enkel `rollen` in `spec.yaml` (via het datamodel §10 en `stap6_genereer.py`), geen structuur. Q06 deels beantwoord.

## 4. Preventiesamenvatting: apart bestand of deel van het rapport? — **klopt, geen modelwijziging nodig**

- BPMN: presentatie nog niet bevestigd, geen verplicht apart PDF-bestand. Ook: de samenvatting wordt **altijd** gemaakt; zonder maatregelen vermeldt ze dat expliciet.
- Model: `iok_documenttype` (Rapport / Preventiesamenvatting) laat beide toe.
- **Opties:** de vraag aan IOK bundelen; de regel "altijd maken, ook zonder maatregelen" meenemen bij de specificatie van de PDF-flow (kaart "Specificatie flows").

## 5. Foto's valideren — **klopt, vraag voor IOK**

- BPMN: D3 valideert "verplichte gegevens, risico's en foto's"; bij een tekortkoming "één of meer foto's".
- Model: B15 / Q02 → foto's niet verplicht.
- **Opties:** Q02 aanvullen met deze twee BPMN-citaten. Gevolg van het antwoord: enkel een validatieregel (D3.2), geen structuur.

## 6. Tekortkoming zonder controlepunt — **klopt, belangrijkste vraag voor IOK**

- BPMN: lus over tekortkomingen, risico per tekortkoming.
- Model: risicokolommen op `iok_resultaat`, dat een controlepunt verplicht maakt.
- Is het antwoord "niet elke tekortkoming hangt aan een controlepunt", dan raakt dat de **structuur** (risico op `iok_maatregel`, of `iok_controlepuntid` optioneel + aanpassing van de sleutel `iok_beoordelingid` + `iok_controlepuntid`).
- **Opties:** nieuwe Q aan IOK, hoge prioriteit, vóór het invulscherm gebouwd wordt.

## 7. Risicodrempels — **klopt, al gedekt**

- De drempels komen uit de legende van het echte verslag `C_2026` (B45). Q24 (grens 70) en Q08 zijn open.
- **Opties:** bij Q08/Q24 vermelden dat de BPMN ook om bevestiging vraagt. Geen andere actie.

## 8. Status van het attest — **deels**

- De uitkomst "conform / niet conform" wordt al vastgelegd: ze bepaalt de **beoordelingsbasis** (conform → Indienststelling, niet conform → Risicoanalyse; B21). "Onduidelijk" is volgens de BPMN (O6) een tussenfase: eerst bewijsstukken opvragen en beoordelen, dan kiezen.
- **Opties:**
  - A. Geen kolom; de vraag "welke bewijsstukken gelden en wie beslist" aan IOK stellen. *Aanbevolen.*
  - B. Keuzekolom `iok_attestbeoordeling` (Conform / Niet conform / Onduidelijk) als IOK de tussenfase wil bijhouden. Structuurwijziging (nieuwe kolom), klein.

## 9. Mag de inspecteur een terrein of terreingroep aanmaken? — **klopt, vraag voor IOK**

- BPMN noemt enkel een toestel. Hoort bij Q06. Tot dan alleen-lezen.

## 10. Code van een nieuw toestel — **klopt, maar pas na punt 3**

- Enkel relevant als de inspecteur toestellen mag aanmaken. De sleutel is hoofdletterongevoelig (nog te testen, B62), dus uniekheid is gedekt; hoofdletters en het aanmaken van de hoofdcode (regel 11) vragen een flow of plug-in.
- **Opties:** meenemen in "Specificatie flows" als punt 3 aanvaard wordt.

## 11. Verzendproblemen — **al gedekt** (B83). Geen actie.

## 12. Correctie na verzending — **al gedekt** (B12/V6, regel 15). Enkel in het overzichtsdocument vermelden dat de BPMN dit niet beschrijft.

## 13. Controleomvang — **al gedekt** (regel 10: de scope is een parameter, geen kolom). Geen actie.

## 14. Stamgegevensversie (D4) — **al gedekt** (B57, B58). Hooguit de uitleg in het overzichtsdocument.

## 15. Financieel overzicht — **klopt, kleine aanvulling**

- Regel 16 zegt niet dat enkel **Afgeronde** dossiers tellen. BPMN: "alleen uitgevoerde controles, met de eenheden die toen golden".
- **Opties:** regel 16 aanvullen met "enkel dossiers met status Afgerond, gefilterd op `iok_controledatum`"; Q26 (Niet beoordeeld) blijft open. Beslissen wanneer de views D4.3/D4.5 gebouwd worden.

## 16. Rechten op checklistonderdeel — **klopt niet**

- `spec.yaml` geeft de inspecteur al Toevoegen (Org) op `iok_checklistonderdeel` (B84). Enkel de samengevatte tabel in het overzichtsdocument laat het weg.

## 17–22. Overzichtsdocument voor het team

- Correcties aan het teamdocument (aantal tabellen in de tekening, kolomtelling `iok_beoordeling` = 23 in §6.2, sectienummering, tenant per teamlid). Geen gevolg voor het model. Meenemen bij de volgende versie van dat document.
- **19 (HIC enkel bij een toestel):** terecht; een bedrijfsregel, mee te nemen bij het beoordelingsformulier of het invulscherm.

## 23. Tablet / "voorlopig advies: canvas-app" — **achterhaald**

- B89 (16/11) koos model-driven met een custom page voor het invulscherm; de splitsing naar een losse canvas-app blijft open tot dat scherm getest is. Het tabletmodel staat al in `AGENTS.md`.

---

## Samenvatting voor de beslissing op 20/11

| Wat | Voorstel | Wie / wanneer |
|---|---|---|
| Punt 0: BPMN-script herstellen en toelichtingen nalezen | doen, eerst | agent, daarna team |
| Punt 3: rechten inspecteur op toestellen | kiezen tussen A, B, C → B94 | team, vóór de rollen gebouwd worden |
| Vragen voor IOK: 1, 5, 6, 8, 9 (+ 4) | bundelen in `open_vragen.md` (Q27 en Q02 aanvullen, nieuwe Q's vanaf Q29) | team |
| Punt 15: enkel Afgeronde dossiers tellen | aanvullen bij regel 16 | bij de views |
| 4, 10, 19 | meenemen in "Specificatie flows" / formulieren | later |
| 2, 7, 11–14, 16, 23 | geen actie op het model | – |
| 17–22 | volgende versie van het overzichtsdocument | – |
