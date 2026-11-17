# Startprompt — stap 9: de app bouwen

## Lees eerst

In deze volgorde, voor je iets voorstelt:

1. `AGENTS.md` — de werkafspraken van dit project
2. `HANDOVER.md` — waar we staan; begin bij "Stand van zaken"
3. `BESLISSINGEN.md` — 90 genummerde keuzes. Zeker **B89** (apparchitectuur), **B90** (offline buiten scope),
   **B40** (geen lege resultaatrijen), **B51** (checklistonderdeel), **B57** (bevriezen met kopiekolommen),
   **B77** (het slot als plug-in)
4. `03_output/datamodel_v3.md` — het model; **§11 is verplicht**: 26 regels die niet in kolommen of relaties
   zitten maar wel gebouwd moeten worden
5. `02_werk/open_vragen.md` — Q01 tot Q28, wat nog niet beslist is

## Waar we staan

Het datamodel is af, gebouwd en gevuld. In `https://orgb2056d46.crm17.dynamics.com` staat de solution
**IOK Speelterreinen** (prefix `iok_`) met 17 eigen tabellen, 4 standaardtabellen, 2 N:N, 35 relaties,
14 keuzelijsten, alle statusredenen, 13 actieve alternatieve sleutels en de twee formulekolommen.
`python tools/dv_controle.py --url ...` geeft 0 verschillen met `spec.yaml`.

Er staan 1.046 proefrecords in plus 19 N:N-koppelingen: alle speelterreinen van Geel, de 17 toestellen van
De Bogaard, de drie checklists met 739 controlepunten, en één echt inspectiedossier van 4 augustus 2026 met
17 beoordelingen en 7 bevindingen. De risicoscores die Dataverse uitrekent komen exact overeen met het
echte IOK-verslag.

**Nog niet gedaan, geen van alle blokkerend:** documentbeheer (SharePoint) op `iok_inspectiedossier`,
de twee beveiligingsrollen, foto's.

## De opdracht

**Stap 9: de toepassing bouwen.** Dit is geen modelwerk meer.

Richting ligt vast in B89: één **model-driven app** op de solution, met het invulscherm van een beoordeling
als **canvas custom page** erin. De splitsing naar een losse canvas-app blijft open tot dat scherm gebouwd
en getest is.

Doel op korte termijn: zo snel mogelijk een werkend voorbeeld waarin je het dossier van De Bogaard kan
openen en doorlopen — terrein, toestellen, beoordelingen, bevindingen.

## Harde regels

- **Het datamodel is de bron.** Wil je iets aan het model veranderen, pas `03_output/datamodel_v3.md` aan en
  draai `python tools/stap6_genereer.py`. Wijzig nooit met de hand: `spec.yaml`, de ERD-bestanden, de CSV's
  in `04_data/`, of tabellen en kolommen rechtstreeks in Dataverse.
- **Een agent draait `tools/dv_bouw.py` en `tools/dv_laden.py` nooit met `--uitvoeren`.** Die start Dries
  zelf, met bevestiging. Alleen-lezen mag wel: `dv_controle.py`, `dv_sleutels.py`, `dv_formule.py`.
- **Elke keuze krijgt een nummer** in `BESLISSINGEN.md`, met de reden erbij. We zitten aan B90.
- **Stop en vraag het als iets niet beslist is.** Verzin geen velden, geen regels en geen gegevens.
- **Verifieer twijfels over Dataverse en Power Platform in de officiële Microsoft-documentatie** en vermeld
  de bron. Niet uit het hoofd antwoorden over wat wel of niet kan.

## Werkwijze

Antwoord in het Nederlands, kort en direct. Eén stap per bericht als we aan het uitvoeren zijn, zodat ik
meteen kan terugkoppelen. Zeg erbij wat ik moet klikken en waar. Werk `HANDOVER.md` bij als er iets
wezenlijks verandert.

## Begin met

Lees de bestanden hierboven, zeg in een paar zinnen wat je begrepen hebt van de stand van zaken, en stel
dan de eerste stap voor. Bouw nog niets voor ik akkoord ben.
