# Handover

_Laatst bijgewerkt: 2026-11-13 (einde sessie stap 0 – intake)_

## Stand van zaken
- **Stap 0 (intake) is af en de sessie is afgesloten op 2026-11-13.** Vier vraagrondes + teach-back, bevestigd met "klopt"; na B26 zijn er geen nieuwe beslissingen genomen.
- Vastgelegd: `02_werk/opdrachtbegrip.md` (doel, scope, buiten scope, 5 ontwerpspanningen), **B10–B26** in `BESLISSINGEN.md`, **Q01–Q09** in `02_werk/open_vragen.md`.
- Nog niets getekend of gespecificeerd: er bestaat nog geen CRUD-matrix, velddekking of v3-model.
- Let op: **B15 vervangt de vaste eis over foto's** ("elk toestel heeft een foto"). `AGENTS.md` vermeldt die oude eis nog; pas ze aan zodra IOK B15 bevestigt (Q02).

## Bestanden deze sessie
- Nieuw: `02_werk/opdrachtbegrip.md`
- Gewijzigd: `BESLISSINGEN.md` (B10–B26), `02_werk/open_vragen.md` (Q01–Q09), `HANDOVER.md`

## Open binnen stap 0
- Niets blokkerends. Q01–Q08 wachten op IOK/lector en mogen pas in stap 3–5 beantwoord worden; Q09 wacht op de cursusbestanden.

## Ontbreekt nog (niet blokkerend)
- [x] Datamodel v2 → `01_context/datamodel_v2/IOK_erd_v2.md`
- [x] Finaal procesmodel → `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md`
- [x] Feedback IOK 13 november → `01_context/feedback/`
- [ ] Transcriptie kick-off → `01_context/feedback/`
- [ ] Cursus les 4b (Dataverse), 4c, 4d → `01_context/cursus/` (nodig voor stap 5)
- [ ] Na het toevoegen van bronnen: `python tools/bronnen_naar_md.py` / `python tools/bpmn_naar_md.py` opnieuw draaien.

## MCP-servers aanzetten (wanneer nodig)
Zet in `opencode.json` `"enabled": true` en herstart opencode. Controleer met `opencode mcp list`.
- **drawio** (stap 6): vereist Node.js 18+. Geen account nodig.
- **dataverse** (stap 4–6, enkel lezen): vervang `JOUWORG.crm4.dynamics.com` door de URL van je eigen ontwikkelomgeving. Eerst in het **Power Platform admin center** bij die omgeving Dataverse MCP aanzetten en de client **"Dataverse CLI"** toestaan (app-ID `0c412cc3-0dd6-449b-987f-05b053db9457`). Lukt dat niet in de studenttenant, dan sla je deze MCP over.

## Volgende sessie — stap 1: CRUD-matrix (maken)
Start opencode in deze map, kies de **Build-agent**, plak als eerste bericht:

> Lees `HANDOVER.md`, `BESLISSINGEN.md` (zeker B10–B26) en `02_werk/opdrachtbegrip.md`. Laad de skill `crud-matrix` en maak `02_werk/crud_matrix.md`: per BPMN-stap (hoofdproces, D1, D2, D3, D4) welke gegevens gelezen, aangemaakt en gewijzigd worden, met per cel de verwijzing naar de BPMN-stap. Markeer wat ontbreekt t.o.v. datamodel v2 en wat overbodig is. Nog niets in Dataverse bouwen.

Sluit die sessie af met `/handover`.
