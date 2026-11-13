---
name: crud-matrix
description: Maak of herzie de CRUD-matrix (BPMN-processtap × Dataverse-tabel) voor het IOK-datamodel, om ontbrekende en overbodige tabellen te vinden.
---

# CRUD-matrix

**Invoer:** `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md` (finaal, incl. D4), `01_context/datamodel_v2/IOK_erd_v2.md`, `BESLISSINGEN.md`.
**Uitvoer:** `02_werk/crud_matrix.md`

## Werkwijze
1. Maak een lijst van alle processtappen met ID (D1.1, D1.2, …, D4.x) en de lane (Inspecteur / Systeem / Beheerder / extern).
2. Rijen = processtappen, kolommen = tabellen (standaardtabellen én `iok_`-tabellen). Cel = combinatie van **C**reate, **R**ead, **U**pdate, **D**elete (of deactiveren = **X**).
3. Noteer per stap ook of een flow (systeem) of de gebruiker het doet.
4. Markeer onder de matrix:
   - **Ontbrekend**: een stap heeft gegevens nodig waarvoor geen tabel/kolom bestaat → kandidaat-tabel of -kolom
   - **Overbodig**: tabel zonder C of zonder R in enig proces
   - **Wees**: tabel die alleen gecreëerd en nooit gelezen wordt (of omgekeerd)
   - **Open**: hangt af van een V-vraag (V1–V11) → zet in `02_werk/open_vragen.md`
5. Bron vermelden per bevinding.

## Formaat
```markdown
| ID | Stap | Lane | Wie | account | iok_speelterrein | iok_speeltoestel | … |
|---|---|---|---|---|---|---|---|
| D1.1 | Bestuur, terrein en scope kiezen | Inspecteur | gebruiker | R | R | R | |
```
Houd de tabelkolommen in een vaste volgorde: stamgegevens → sjablonen → inspectie → communicatie → standaardtabellen. Begin met de 13 tabellen van v2 en voeg kandidaat-tabellen toe als aparte kolommen (gemarkeerd `nieuw?`).
