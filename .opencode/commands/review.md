---
description: Kritische nalezing van een opgeleverd bestand in een frisse sessie (argument = bestand)
---
Je hebt dit werk **niet** gemaakt. Lees het kritisch na als een strenge lector en als de IOK-jury.

Te controleren: $ARGUMENTS (geen argument = `03_output/datamodel_v3.md`).

Lees eerst AGENTS.md, BESLISSINGEN.md, `02_werk/opdrachtbegrip.md`, `02_werk/crud_matrix.md` en de skill `dataverse-modellering`. Controleer:
1. Strijdig met een vaste eis of een beslissing (B-nummer)?
2. Elke processtap uit het finale BPMN heeft de gegevens die hij nodig heeft (CRUD-matrix)? Tabellen zonder C of zonder R?
3. Dataverse-correctheid: standaardtabel waar mogelijk (B02), prefix `iok_` (B01), types en lengtes, verwijdergedrag, één parental-relatie per tabel, N:N-keuze, alternatieve sleutels voor unieke codes, eigenaarschap. Twijfel → verifiëren via mslearn.
4. Dubbele paden, relaties in twee richtingen, overbodige tabellen of kolommen.
5. Is het verdedigbaar op het examen? Waar zou een lector "waarom?" vragen zonder dat er een motivering staat?
6. Interne consistentie tussen datamodel_v3.md, ERD en spec.yaml (als die al bestaan).

Uitvoer: een genummerde lijst, gesorteerd van ernstig naar klein, met per punt: wat, waar (bestand/tabel), waarom fout, voorstel. **Pas niets aan.** Vraag aan het einde welke punten ik wil laten verbeteren.
