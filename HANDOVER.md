# Handover

_Laatst bijgewerkt: 2026-11-13 (voorbereiding, nog geen opencode-sessie gedaan)_

## Stand van zaken
- Map opgezet voor opencode: `AGENTS.md`, skills, commando's, `opencode.json`.
- Alle bronnen omgezet naar `01_context/` (Excel/Word, keuzelijsten, BPMN, PDF's, datamodel v2 uit draw.io).
- Feedback IOK van 13/11 verwerkt: `01_context/feedback/feedback_IOK_2026-11-13.md`, beslissingen B04–B09, startprompt bijgewerkt.
- Finaal BPMN = `IOK_02_ToBe_uitgeklapt_aangepast`; datamodel v2 = `IOK_erd_v2.drawio` (13 tabellen).

## Ontbreekt nog (niet blokkerend)
- [x] Datamodel v2 → `01_context/datamodel_v2/IOK_erd_v2.md`
- [x] Finaal procesmodel → `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md`
- [x] Feedback IOK 13 november → `01_context/feedback/`
- [ ] Transcriptie kick-off → `01_context/feedback/`
- [ ] Cursus les 4b (Dataverse), 4c, 4d → `01_context/cursus/` (nodig voor stap 5)
- Na het toevoegen van bronnen: `python tools/bronnen_naar_md.py` / `python tools/bpmn_naar_md.py` opnieuw draaien.

## MCP-servers aanzetten (wanneer nodig)
Zet in `opencode.json` `"enabled": true` en herstart opencode. Controleer met `opencode mcp list`.
- **drawio** (stap 6): vereist Node.js 18+. Geen account nodig.
- **dataverse** (stap 4–6, enkel lezen): vervang `JOUWORG.crm4.dynamics.com` door de URL van je eigen ontwikkelomgeving (Power Platform admin center → omgeving → Omgevings-URL). Eerst in het **Power Platform admin center** bij die omgeving: Dataverse MCP aanzetten en de client **"Dataverse CLI"** toestaan (app-ID `0c412cc3-0dd6-449b-987f-05b053db9457`). Lukt dat niet in de studenttenant (beheerdersrechten), dan sla je deze MCP gewoon over.

## Open vragen
Zie `02_werk/open_vragen.md`.

## Volgende sessie
Start opencode in deze map, Plan-agent (Tab), plak `Startprompt_ERD_herziening.md` als eerste bericht en typ daarna `/intake`. Begin dus met stap 0 (intake).
