# Opdrachtbegrip – intake (stap 0)

_Datum: 2026-11-13. Bron: intakegesprek (4 vraagrondes + teach-back), bevestigd met "klopt"._

## Doel

Het datamodel v2 herzien tot een **Dataverse-datamodel v3** dat het finale BPMN volledig ondersteunt en klaar is om te bouwen via de Dataverse Web API. In dit traject wordt **niets gebouwd**: de output is documentatie (`03_output/datamodel_v3.md`), een ERD, een changelog en een machineleesbare `spec.yaml`.

## Scope (wat v3 dekt)

- Het volledige finale BPMN: hoofdproces, D1, D2, D3 en D4 (`01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md`).
- Eén **inspectiedossier per terrein per controledatum**, met daarin het terrein en alle toestellen van dat bezoek (B10, B11).
- Per dossier één **versie per controledatum**, met een rapport-PDF én een aparte preventiesamenvatting-PDF (B11, B06).
- Per beoordeling (terrein of toestel): beoordelingsbasis, norm, antwoorden per controlepunt, bevindingen, foto's, optioneel een HIC-meting, een besluit en preventiemaatregelen (B18, B20, B21, B23).
- Stamgegevensbeheer met versies: checklists, controlepunten, standaardzinnen, toesteltypes (B07, B08, B19, B26).
- Overzichten (maatregelen per bestuur, financieel overzicht per periode) als views/exports op bestaande gegevens (B10).

## Buiten scope

- **Offline werken** en synchronisatie (B04).
- **Acuut gevaar**: de inspecteur neemt zelf contact op, buiten het model (B12).
- **Herstelopvolging**: het bestuur beslist zelf wat het met de maatregelen doet; IOK volgt niet op (B18).
- **Automatische verzending**: de inspecteur verstuurt zelf (B05).
- **Toegang per bestuur / business units**: besturen krijgen later eventueel leesrecht op hun eigen data; nu niet (B13).
- **V1, V2, V5, V7, V8, V10** en de risicofactoren/scoretabel: nog geen plek in v3, wel in `open_vragen.md`.
- **Eigen overzichtstabellen** voor maatregelen of financiering (B10).

## Ontwerpspanningen

1. **Historiek versus actualiteit.** Dezelfde gegevens leven twee keer: actueel (stamgegeven, versieerbaar) en bevroren (in het dossier). Bewust gekozen, volgt uit B06/B07 en B14.
2. **Sjabloonbeheer.** Checklisthiërarchie (hoofdstuk → controlepunt), normverwijzingen en standaardzinnen zijn het complexste deel: versieerbaar, beheerbaar door één bevoegde beheerder, en bruikbaar voor zowel terrein als toestel.
3. **Drie beoordelingsbasissen in één structuur.** Jaarlijkse controle, indienststelling en risicoanalyse moeten dezelfde beoordelingsstructuur delen zonder de checklisthiërarchie of de Deel 1/Deel 2-opbouw te verliezen. Een combinatietoestel krijgt meerdere Deel 2-checklists; skate volgt EN 14974.
4. **Documenten buiten Dataverse.** PDF's en foto's staan in SharePoint; Dataverse bewaart metadata, versies en statussen (B03, B22).
5. **Eén controlemoment.** De inspecteur kijkt het verslag na en verstuurt; er is geen tweede goedkeurder (leesversie; B05).

## Bevestigde aannames

Zie `BESLISSINGEN.md` B10–B26. In het kort:

- v3 dekt het volledige BPMN, maar zonder eigen overzichtstabellen (B10).
- Verslag en versie hangen op het dossier; preventiesamenvatting is een apart PDF (B11).
- V4, V6 en V9 krijgen een plek; V3 niet (B12).
- Twee rollen, uitbreidbaar naar toegang per bestuur (B13).
- Alles wat in het verslag staat wordt bevroren (B14).
- Foto's zijn niet verplicht; zonder nieuwe foto wordt de meest recente toestelfoto hernomen (B15).
- Bestuur = Account, contactpersoon = Contact (B16).
- Statusmodel op dossier en op rapportversie (B17).
- Maatregelen zonder opvolging; besluit is Conform/Niet conform (B18).
- Checklistversie per geheel; dossier uniek per terrein + controledatum (B19).
- HIC-metingen hangen aan de toestelbeoordeling (B20).
- Norm en beoordelingsbasis per beoordeling (B21).
- PDF's in SharePoint, metadata in Dataverse (B22).
- Terreinbeoordeling volgt dezelfde structuur als een toestel (B23).
- Toestelstatus In gebruik/Buiten gebruik; "onbruikbaar" is een bevinding (B24).
- Codes verplicht en uniek over alle besturen (B25).
- Toesteltype versieerbaar, categorie als keuzelijst, type → checklist N:N (B26).

## Bronnen

- `01_context/Projectopdracht_IOK.md` (§3, §4, §5)
- `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md` + `01_context/bpmn/IOK_BPMN_leesversie.md`
- `01_context/feedback/feedback_IOK_2026-11-13.md`
- `01_context/datamodel_v2/IOK_erd_v2.md`
- `01_context/docs/` (A-, B- en C-verslagen, lege sjablonen, overzichten)
- `01_context/keuzelijsten/`
