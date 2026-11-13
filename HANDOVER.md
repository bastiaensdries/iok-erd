# Handover

_Laatst bijgewerkt: 2026-11-13 (einde sessie stap 1 – CRUD-matrix)_

## Stand van zaken
- **Stap 1 (CRUD-matrix) is af.** `02_werk/crud_matrix.md` bestaat; matrix en samenvatting per tabel zijn gecontroleerd (0 verschillen).
- 23 tabelkolommen (stamgegevens → sjablonen → inspectie → communicatie → standaardtabellen) en **29 processtappen in procesvolgorde**: D1.1–D1.4, H1, D2.1–D2.6, D3.1–D3.10, H2–H4, D4.1–D4.5; cellen C/R/U/D/X.
- Nieuwe beslissingen **B27–B31**; nieuwe vragen **Q10** (bevriezen), **Q11** (lege resultaatrijen, stap 3), **Q12** (eenheden per bestuur), **Q13** (archieflocatie).
- Er is nog geen velddekking en geen v3-model; er is nog niets getekend.

## Bestanden deze sessie
- Nieuw: `02_werk/crud_matrix.md`
- Gewijzigd: `BESLISSINGEN.md` (B27–B31), `02_werk/open_vragen.md` (Q10–Q13), `HANDOVER.md`

## Open binnen stap 1
- Niets blokkerends. Q10 bepaalt of D3.9 later een C op snapshot-tabellen krijgt, Q11 waar de lege resultaatrijen ontstaan, Q12 of er een kolom `iok_eenheden` op Account komt. Alle drie mogen tot stap 3/4 wachten.

## Ontbreekt nog (niet blokkerend)
- [x] Datamodel v2 → `01_context/datamodel_v2/IOK_erd_v2.md`
- [x] Finaal procesmodel → `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md`
- [x] Feedback IOK 13 november → `01_context/feedback/`
- [x] CRUD-matrix (stap 1) → `02_werk/crud_matrix.md`
- [ ] Transcriptie kick-off → `01_context/feedback/`
- [ ] Cursus les 4b (Dataverse), 4c, 4d → `01_context/cursus/` (nodig voor stap 5)
- [ ] Na het toevoegen van bronnen: `python tools/bronnen_naar_md.py` / `python tools/bpmn_naar_md.py` opnieuw draaien.
- [ ] `AGENTS.md`: de vaste eis "elk toestel heeft een foto" is door B15 vervangen (wacht op bevestiging IOK, Q02).

## MCP-servers
`drawio` (stap 6) en `dataverse` (stap 4–6, enkel lezen) staan uit in `opencode.json`; aanzetten en herstarten wanneer nodig. Dataverse MCP vereist dat je in het Power Platform admin center Dataverse MCP aanzet en de client "Dataverse CLI" toestaat.

## Volgende sessie — stap 2: velddekking (maken)
Kies de **Build-agent** en plak als eerste bericht:

> Lees `HANDOVER.md`, `BESLISSINGEN.md` (zeker B10–B31), `02_werk/opdrachtbegrip.md` en `02_werk/crud_matrix.md`. Laad de skill `velddekking`. Maak `02_werk/velddekking.md`: inventariseer alle velden uit `01_context/docs/` (A-, B- en C-verslagen, lege sjablonen, overzichten) en `01_context/keuzelijsten/`, en wijs elk veld toe aan een Dataverse-kolom uit de CRUD-matrix (standaardtabel of `iok_`-tabel). Per veld: status **toegewezen / ontbrekend / bewust weggelaten**, de Dataverse-werknaam, het type en de bron (bestand + regel). Werk de kolommen bij waar de matrix een gat toont (maatregel, standaardtekst, HIC, foto, document). Nog niets in Dataverse bouwen.

Sluit die sessie af met `/handover`.
