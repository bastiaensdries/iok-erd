---
name: velddekking
description: Inventariseer alle velden uit de IOK-bronbestanden (Excel-sjablonen, ingevulde voorbeelden, Word-verslag, overzichten) en wijs elk veld toe aan een Dataverse-kolom, of markeer het als ontbrekend of bewust weggelaten.
---

# Velddekking

**Invoer:** `01_context/docs/*.md` en `01_context/keuzelijsten/*.md`. Lees de markdownversies, niet de originelen in `00_bronnen/`.
**Uitvoer:** `02_werk/velddekking.md`

## Werkwijze
1. Werk per bronbestand. Begin met de lege sjablonen (`… versie 2022`), daarna de ingevulde voorbeelden (A_, B_, C_) om te zien welke velden echt gebruikt worden.
2. Per veld één rij:

| Bron (bestand · blad · cel) | Label in bron | Voorbeeldwaarde | → Tabel.kolom | Type | Status |
|---|---|---|---|---|---|
| Indienststelling versie 2022 · Algemeen · C17 | Doelgroep | van 2,5 tot 6 jaar | iok_speeltoestel.iok_doelgroep | lookup/keuze | gedekt |

   Status = `gedekt` · `nieuw` (kolom bestaat nog niet in v2) · `weggelaten` (met reden) · `open` (vraag).
3. Herhalende controlepunten (de honderden rijen OK/NOK/nvt per hoofdstuk) niet één voor één opnemen: beschrijf de **structuur** (checklist → hoofdstuk → controlepunt → beoordeling) en tel het aantal punten per blad.
4. Keuzelijsten: noteer per lijst of het een **globale keuzelijst**, een **opzoektabel** of **standaardzinnen-tabel** wordt.
5. Signaleer inconsistenties tussen bronnen (andere labels of waarden voor hetzelfde gegeven, dubbele codes in `Overzicht bestaande speelterreinen`).
