# IOK — datamodel speelterreincontroles

Dataverse-datamodel en proof of concept voor de veiligheidscontroles van speelterreinen die IOK uitvoert
voor gemeenten en OCMW's. Schoolproject, Thomas More, opleidingsonderdeel Enterprise solutions.

IOK controleert speelterreinen op veiligheid volgens EN 1176 (speeltoestellen) en EN 14974 (skate). Een
inspecteur loopt ter plaatse het terrein en elk toestel na aan de hand van een checklist, noteert gebreken,
meet waar nodig de valdemping, en levert een rapport af met een besluit per toestel en een lijst
preventiemaatregelen. Dat gebeurt vandaag met Excel-sjablonen en Word-verslagen; de bedoeling is een
Power Platform-toepassing op Dataverse.

**Dit project levert het datamodel, niet de app.** De app begint nu.

## Begin hier

| Wil je weten | Lees |
|---|---|
| waar het over gaat, in detail | het [overzichtsdocument](https://claude.ai/artifact/2iUFdxJouBurMioaw5xN58) — vraag Dries om toegang |
| hoe het model eruitziet | `03_output/datamodel_v3.md` (de bron) en `03_output/ERD_v3.md` |
| waarom iets zo is | `BESLISSINGEN.md` — 90 genummerde keuzes met hun reden |
| waar we staan | `HANDOVER.md` |
| wat nog niet beslist is | `02_werk/open_vragen.md` — Q01 tot Q28 |
| waar de proefdata vandaan komt | `04_data/LEESMIJ.md` |

## Mappen

```
00_bronnen/      de aangeleverde documenten van IOK (Excel, Word, PDF) — niet wijzigen
01_context/      diezelfde bronnen omgezet naar markdown, plus BPMN en datamodel v2
02_werk/         tussenwerk: opdrachtbegrip, CRUD-matrix, velddekking, review, open vragen
03_output/       het datamodel en wat eruit gegenereerd wordt
04_data/         proefdata als CSV, plus het laadplan
tools/           de scripts
```

## De keten

Het datamodel is de enige bron. Alles eronder wordt eruit gegenereerd:

```
03_output/datamodel_v3.md
        │  python tools/stap6_genereer.py
        ├──> 03_output/spec.yaml + spec.json      (machineleesbare specificatie)
        ├──> 03_output/ERD_v3.md                  (Mermaid)
        ├──> 03_output/IOK_erd_v3.drawio          (draw.io)
        └──> 03_output/IOK_erd_v3.mdj             (StarUML, via model_naar_staruml.py)
                 │  python tools/dv_bouw.py
                 └──> Dataverse
```

Wil je iets aan het model veranderen, pas dan `datamodel_v3.md` aan en genereer opnieuw.
**Wijzig nooit met de hand:** `spec.yaml`, `spec.json`, de drie ERD-bestanden, de CSV's in `04_data/`,
of tabellen en kolommen rechtstreeks in Dataverse. Dan lopen ze uit elkaar en weet niemand nog wat klopt.

`python tools/stap6_genereer.py --check` controleert of datamodel, spec en ERD nog overeenkomen, en
controleert ook het datamodel zelf: heeft elke lookup een relatie, bestaan de kolommen in de sleutels,
heeft elke tabel hoogstens één parental-relatie, zijn er geen dubbele namen.

## Scripts

Alles in `tools/`. De `dv_*`-scripts praten met de Dataverse Web API; aanmelden gebeurt met een device
code (het script toont een code, jij logt in met je schoolaccount). Geen app-registratie nodig.

| Script | Wat |
|---|---|
| `bronnen_naar_md.py` | zet `00_bronnen/docs/` om naar markdown in `01_context/` |
| `bpmn_naar_md.py` | idem voor het procesmodel |
| `stap6_genereer.py` | genereert spec, ERD en draw.io uit het datamodel; `--check` vergelijkt |
| `model_naar_staruml.py` | genereert het StarUML-diagram |
| `csv_maken.py` | bouwt de proefdata-CSV's uit de bronnen |
| `dv_controle.py` | vergelijkt een omgeving met `spec.yaml` (ook de weergavenamen van de kolommen) — alleen-lezen |
| `dv_bouw.py` | bouwt het schema in Dataverse; zet ook de weergavenamen van bestaande kolommen goed (B93) |
| `dv_laden.py` | laadt de CSV's |
| `dv_formule.py` | controleert de twee formulekolommen en toont wat Dataverse uitrekent |
| `dv_sleutels.py` | toont de toestand van de alternatieve sleutels — alleen-lezen |
| `maak_verslag.py` | maakt een leesbaar voorbeeldverslag (HTML) uit de proefdata |

`dv_bouw.py` en `dv_laden.py` schrijven alleen met `--uitvoeren` plus een getypte bevestiging. Zonder die
vlag draaien ze een proefronde. Een agent draait ze nooit met `--uitvoeren`; zie `AGENTS.md`.

### Een omgeving opbouwen

```
python tools/dv_controle.py --url https://<org>.crm17.dynamics.com      # verwacht: alles ontbreekt
python tools/dv_bouw.py     --url https://<org>.crm17.dynamics.com --uitvoeren
python tools/dv_laden.py    --url https://<org>.crm17.dynamics.com --uitvoeren
python tools/dv_controle.py --url https://<org>.crm17.dynamics.com      # verwacht: 0 verschillen
```

Reken op een halfuur. De alternatieve sleutels kunnen na het bouwen meer dan een uur op `Pending` staan
voor ze actief worden; dat is normaal, niet ingrijpen (zie B88). Het laden kan pas als ze actief zijn.

Niet door de scripts, dus met de hand: de twee formulekolommen op `iok_resultaat`, documentbeheer
(SharePoint) op `iok_inspectiedossier`, en de twee beveiligingsrollen. `dv_controle.py` zet ze onderaan
als lijstje.

## Stand van zaken

Het model is af en draait. In de omgeving staan 17 eigen tabellen, 4 standaardtabellen en 2 N:N, met
alle kolommen, 35 relaties, 14 keuzelijsten, alle statusredenen en 13 alternatieve sleutels. `dv_controle.py`
geeft 0 verschillen met de spec. Er staan 1046 proefrecords in plus 19 N:N-koppelingen: alle
speelterreinen van Geel, de toestellen van De Bogaard, de drie checklists met 739 controlepunten, en één
echt inspectiedossier van 4 augustus 2026.

De risicoscores die Dataverse zelf uitrekent komen exact overeen met de cijfers in het echte IOK-verslag.

**Wat nog open staat:** het model is nooit getoetst aan les 4b (die lesmap was leeg); Q21 moet beantwoord
zijn voor een toestel zijn volledige Deel 2-checklist kan krijgen; documentbeheer, de twee rollen en de
foto's moeten nog; en de app zelf bestaat nog niet. Richting daarvoor staat in B89: model-driven als
ruggengraat met het invulscherm van een beoordeling als canvas custom page.

## Afspraken

- **Private repo.** `00_bronnen/` bevat echte IOK-documenten met een bestaand terrein, een adres en de
  bevindingen van een echte controle. Niet publiek maken, niet doorsturen buiten het team.
- Geen geheimen in git. `.dv_token.json` en `.dv_omgeving` staan in `.gitignore`; laat dat zo.
- Elke keuze krijgt een nummer in `BESLISSINGEN.md`, met de reden erbij. Herziet een nieuwe beslissing een
  oude, zeg dat er dan bij. Oude regels worden niet geschrapt.
