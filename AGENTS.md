# Project: Dataverse-datamodel v3 voor IOK (veiligheidsinspecties speelterreinen)

Studentenproject (Thomas More, *Enterprise solutions: M365 & Power Platform*), team van 4, proof of concept voor een IOK-jury.
Doel van dit project in opencode: het datamodel v2 herzien tot een **v3 die klaar is om te bouwen** in Dataverse.
**In stap 0–6 bouwen we niets in Dataverse**; output = documenten, ERD en een machineleesbare specificatie. **Stap 7 (B85) bouwt wél**, maar enkel met de scripts `tools/dv_*.py`, enkel door Dries zelf gestart (`--uitvoeren` + bevestiging). Een agent draait die scripts nooit met `--uitvoeren`.

## Werkwijze (altijd)
- Antwoord in het **Nederlands**.
- Stel bij elke stap eerst de belangrijke vragen en wacht op antwoord als de keuze van mij is.
- "enkel overleggen" of "nog niet tekenen" = alleen bespreken, **geen bestanden schrijven**.
- **Geen aannames.** Wat niet in de bronnen staat, is een vraag voor mij of voor IOK → zet het in `02_werk/open_vragen.md`.
- Vermeld bij elk voorstel **waarop het steunt**: BPMN-stap, bronbestand (pad in `01_context/`), cursusdia of beslissing (B-nummer).
- Lees bij de start van elke sessie eerst `HANDOVER.md` en `BESLISSINGEN.md`.
- Een beslissing die ik neem, komt in `BESLISSINGEN.md` (nieuw B-nummer, datum, bron). Herzie een eerdere beslissing nooit stilzwijgend.

## Dataverse-uitgangspunten
- **Hergebruik de ingebouwde Dataverse-tabellen** waar ze passen (o.a. Account, Contact, Gebruiker, Team, E-mail, Taak, Notitie, SharePoint-documentlocatie). Maak pas een eigen tabel als geen standaardtabel past, en motiveer dat. → B02
- **Alle eigen tabellen, kolommen en keuzelijsten krijgen het prefix `iok_`**, ook eigen kolommen die we aan een standaardtabel toevoegen (bv. `account.iok_eenheden`). → B01
- Alle gegevens in Dataverse-tabellen, geen SharePoint-lijsten. SharePoint enkel als archief voor PDF's en foto's.
- Laad de skill `dataverse-modellering` vóór je tabellen, kolommen of relaties voorstelt.

## MCP-servers (opencode.json)
- **mslearn** (aan): officiële Microsoft-documentatie. Gebruik het om Dataverse-mogelijkheden en -limieten te verifiëren; vermeld de bron.
- **drawio** (uit, aanzetten in stap 6): het ERD openen/maken in draw.io (ook vanuit Mermaid), in dezelfde stijl als `00_bronnen/datamodel_v2/IOK_erd_v2.drawio`.
- **dataverse** (uit): mijn eigen ontwikkelomgeving. **Enkel lezen** (bv. welke kolommen een standaardtabel als Account al heeft). **Nooit** tabellen, kolommen of records aanmaken, wijzigen of verwijderen, ook niet als een tool dat aanbiedt.

## Vaste eisen (uit klantgesprekken, niet zelf wijzigen)
- App op **tablet (Samsung Galaxy 5G)** en laptop. **Offline is niet nodig** en niet bepalend voor het ERD (B04).
- **Eén verslag per terrein = één PDF** + **samenvatting preventiemaatregelen** (zeer belangrijk voor IOK), automatisch gegenereerd; inspecteur kijkt na, kan de PDF aanpassen en **verstuurt zelf** (B05); verzendstatus registreren.
- **Versiebeheer = controledatum** (B06): definitieve PDF, controledatum en historische dossiergegevens bewaren.
- **Stamgegevens** wijzigen zonder terugwerkende kracht → nieuwe versie, historiek blijft (B07); enkel één bevoegde beheerder wijzigt (B08).
- Overzichten: maatregelen/tekortkomingen per bestuur; financieel overzicht (eenheden) over een **gekozen periode** naar Excel.
- **Indienststelling** als conformiteit aantoonbaar is; **risicoanalyse** zonder aantoonbare conformiteit of bij herplaatst toestel. Skate = EN 14974. Combinatietoestel = meerdere Deel 2-checklists; twee schommels = één onderdeel.
- **Eén opmerking per controlepunt**; 1 NOK maakt het hoofdstuk NOK.
- **Foto's**: elk toestel heeft een foto in het verslag (ook als conform); een nieuwe foto vervangt de oude in het verslag; de oude blijft bewaard bij het toestel.
- **Jaarlijkse controle**: gegevens van vorig jaar worden als concept overgenomen; een overgenomen antwoord is nog geen nieuwe inspectie.
- **HIC-meting** alleen bij niet-conforme valondergrond.
- **Besluiten en standaardzinnen** komen uit een tabel.
- **Codes** van terreinen en toestellen zijn uniek (oude Excel had 31 dubbele codes).
- **Kosten**: premium connectors mogen, maar minimaal. Overzicht van eenheden per bestuur.
- **Integratie**: later koppeling met besturen via de Dataverse Web API.
- Volumes: ±850 terreinen, ±5250 toestellen, ±1500 foto's per jaar (projectopdracht).

## Bestandskaart
| Pad | Inhoud | Regel |
|---|---|---|
| `00_bronnen/` | originelen (Excel, Word, PDF, BPMN) | **nooit wijzigen**, niet rechtstreeks lezen als er een .md-versie is |
| `01_context/docs/` | bronbestanden als markdown (enkel niet-lege cellen, `rij \| kolom: waarde`) | hier lezen |
| `01_context/keuzelijsten/` | Excel-keuzelijsten (data validations) → kandidaten voor keuzelijsten in Dataverse | |
| `01_context/bpmn/` | BPMN als stappenlijst. **Finaal = `IOK_02_ToBe_uitgeklapt_aangepast.md`**; `IOK_02_ToBe.md` is verouderd (offline/sync) | |
| `01_context/Projectopdracht_IOK.md` | projectopdracht | |
| `01_context/datamodel_v2/IOK_erd_v2.md` | datamodel v2 (13 tabellen, uit draw.io) = vertrekpunt | |
| `01_context/feedback/` | feedback IOK 13/11 + koppeling met BPMN | |
| `01_context/cursus/` | cursus les 4b/4c/4d | ⚠️ nog leeg. Bestaat een bron niet? Zeg het en ga niet gissen |
| `02_werk/` | CRUD-matrix, velddekking, ontwerpvragen, open vragen | werkbestanden |
| `03_output/` | datamodel v3, ERD, changelog, `spec.yaml` | eindresultaat |
| `04_data/` | proefdata voor Dataverse (Geel) als CSV + `laadplan.json`; uitleg in `04_data/LEESMIJ.md` | gemaakt door `python tools/csv_maken.py`, niet met de hand wijzigen |
| `HANDOVER.md` / `BESLISSINGEN.md` | stand van zaken / beslissingenlog | altijd eerst lezen |
| `tools/` | conversiescripts (`python tools/bronnen_naar_md.py`, `python tools/bpmn_naar_md.py`, `python tools/drawio_erd_naar_md.py <in.drawio> <uit.md>`) | opnieuw draaien als een bron wijzigt |
| `tools/dv_*.py` | praten met de Dataverse Web API. Alleen-lezen: `dv_controle.py`, `dv_sleutels.py`, `dv_formule.py`. Schrijvend: `dv_bouw.py`, `dv_laden.py` | een agent draait de schrijvende nooit met `--uitvoeren` |
| `tools/maak_verslag.py` | bouwt uit de CSV's een leesbaar voorbeeldverslag in `03_output/verslag_voorbeeld.html` | alleen-lezen |
| `README.md` | oriëntatie voor wie de repo opent (ook voor een AI-assistent) | bijwerken als de scripts of de keten wijzigen |

## Stappen (één opencode-sessie per stap, afsluiten met /handover)
De bestanden achter de pijlen bestaan nog niet: die maak je in die stap. Drie soorten sessies: **denken** (Plan-agent, vragen + beslissen), **maken** (Build-agent, enkel uitwerken wat beslist is), **controleren** (frisse sessie, Plan-agent).
0. **Intake** (denken, `/intake`) → `02_werk/opdrachtbegrip.md`
1. CRUD-matrix (maken) → `02_werk/crud_matrix.md` (skill `crud-matrix`)
2. Velddekking (maken) → `02_werk/velddekking.md` (skill `velddekking`)
3. Ontwerpvragen beslissen (denken) → `02_werk/ontwerpvragen.md` + `BESLISSINGEN.md`
4. Datamodel v3: tabel per tabel, relaties, verwijdergedrag, eigenaarschap, beveiligingsrollen (maken) → `03_output/datamodel_v3.md`
5. Review + toetsen aan les 4b (controleren, `/review`) → lijst met verbeterpunten
6. Verbeteren, technische specificatie, ERD en changelog (maken) → `03_output/` (skills `spec-yaml`, `erd-mermaid`)
7. Bouwen in Dataverse (B85): `python tools/dv_controle.py` (alleen-lezen) → `python tools/dv_bouw.py` → `python tools/dv_laden.py`. Zonder `--uitvoeren` doen ze enkel een proefdraai. Het datamodel blijft de bron: eerst `datamodel_v3.md` aanpassen, dan `python tools/stap6_genereer.py`, dan pas bouwen.
8. Verhuizen naar een deelbare omgeving (2026-11-16). **Af.** Het model is gebouwd, gevuld en gecontroleerd in `https://orgb2056d46.crm17.dynamics.com`; zie `HANDOVER.md`.
9. **Nu bezig: de app bouwen.** Richting vastgelegd in **B89** (model-driven als ruggengraat, het invulscherm van een beoordeling als canvas custom page) en **B90** (offline buiten scope). Dit is geen modelwerk meer: wijzig het datamodel alleen als er een echte reden voor is, en leg die dan vast als beslissing.
