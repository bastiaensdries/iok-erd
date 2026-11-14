# Handover

_Laatst bijgewerkt: 2026-11-14 (einde stap 2 – velddekking; afgerond in Claude nadat de gratis opencode-limiet bereikt was)_

## Stand van zaken
- **Stap 0 (intake) en stap 1 (CRUD-matrix) zijn af.** `02_werk/opdrachtbegrip.md`, `02_werk/crud_matrix.md`.
- **Stap 2 (velddekking) is inhoudelijk af**: `02_werk/velddekking.md` (deel A: lege sjablonen + keuzelijsten; deel B: ingevulde verslagen; overzichten in §16–17; correcties op deel A in §18; samenvatting in §19). "Deel C" is afgedekt door §16–17.
- Beslissingen tot en met **B45**; open vragen tot en met **Q22**. Q11 is beantwoord door B40.
- De hulpscripts van deel B (`_check*.py`) staan nu in `tools/_scratch_stap2/` (wegwerp, niet nodig voor het model).
- Nog geen v3-model, nog niets getekend.

## Nog te doen om stap 2 volledig af te sluiten (eerste taak volgende sessie)
- [ ] **CRUD-matrix bijwerken** in één keer (was bewust uitgesteld, zie velddekking §19.3):
  - **contact na B37**: verantwoordelijke = bestuur (Account). In **H2** blijft `contact` waarschijnlijk nodig voor het e-mailadres van het bestuur (de inspecteur mailt zelf, B05); pas enkel de leesreden aan waar nodig.
  - nieuwe tabel **`iok_toestelcode`** (B44) als kolom; nieuwe velden `iok_beoordeling.iok_opmerking` (B42) en `iok_controlepunt.iok_hoofdstuk` (B43) in de opmerkingen;
  - **D3.2** krijgt de validatie "1 NOK = hoofdstuk NOK" en de invulplicht per beoordelingsbasis (B40); D1.3 maakt **geen** lege resultaatrijen (B40).
  - daarna de samenvatting per tabel opnieuw afleiden en controleren (0 verschillen), zoals in stap 1.

## Voor stap 3 (ontwerpvragen beslissen)
- **Q20 – wat is een rij in "Overzicht bestaande speelterreinen"?** (hoogste prioriteit) 635 rijen, kolom F telt op tot 879 ≈ ±850 terreinen: een rij is waarschijnlijk een groepering, geen terrein. Bepaalt de basiseenheid (`iok_speelterrein`) en "één verslag per terrein". Ontwerpvraag: groepering boven `iok_speelterrein`? Hangt samen met de 31 dubbele codes en B25/B44.
- **Q16 + HIC als één meetwaarde-patroon** (meetwaarde op `iok_resultaat` of één `iok_meting` met soort i.p.v. aparte `iok_hicmeting`).
- **Q21** kardinaliteit type → checklist (0..N?), **Q22** terreinchecklist of enkel terreinoordeel bij jaarlijkse controle, **Q18** hoofdstuk M/N en de validatieregel van B40.
- **Q10** bevriezen: kopiëren of onveranderlijke versies (B14/B19).
- De hiërarchievraag (oude punt b) is beslist in **B43** (onbeperkt + `iok_hoofdstuk`).

## Voor stap 4 (datamodel v3)
- **Risicoscore (B45)**: R = I×K×B en de risicoklasse zijn **berekend**, geen invoervelden. Dataverse-keuzewaarden zijn **gehele getallen**, kans/blootstelling hebben decimale factoren (0,2 / 0,5) → opzoektabel (label + factor) of decimaal veld met vaste waarden.
- Nieuwe elementen uit stap 2: `iok_hoofdstuk`, `iok_toestelcode`, `iok_beoordeling.iok_opmerking`, validatieregels (B40), standaardzinnen (5 besluiten + gebruikte lijsten).
- Ontwerpregel: de SharePoint-archieflocatie wordt aangemaakt bij het aanmaken van een dossier, ongeacht hoe het ontstaat (Q13); nagaan of de standaard SharePoint-integratie van Dataverse dat al doet (mslearn).

## Ontbreekt nog (niet blokkerend)
- [x] Datamodel v2 → `01_context/datamodel_v2/IOK_erd_v2.md`
- [x] Finaal procesmodel → `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md`
- [x] Feedback IOK 13 november → `01_context/feedback/`
- [x] CRUD-matrix (stap 1) → `02_werk/crud_matrix.md`
- [x] Velddekking (stap 2) → `02_werk/velddekking.md`
- [ ] Transcriptie kick-off → `01_context/feedback/`
- [ ] Cursus les 4b (Dataverse), 4c, 4d → `01_context/cursus/` (nodig voor stap 5)
- [ ] Na het toevoegen van bronnen: `python tools/bronnen_naar_md.py` / `python tools/bpmn_naar_md.py` opnieuw draaien.
- [ ] `AGENTS.md`: de vaste eis "elk toestel heeft een foto" is door B15 vervangen (wacht op bevestiging IOK, Q02).

## MCP-servers
`drawio` (stap 6) en `dataverse` (stap 4–6, enkel lezen) staan uit in `opencode.json`; aanzetten en herstarten wanneer nodig. Dataverse MCP vereist dat je in het Power Platform admin center Dataverse MCP aanzet en de client "Dataverse CLI" toestaat.

## Modelkeuze
De gratis DeepSeek-limiet in opencode was op 2026-11-14 bereikt (reset 15-11 01:57). Voor **stap 3 en 4** (veel samenhangende beslissingen) een sterker model gebruiken.

## Volgende sessie — afronding stap 2 + start stap 3
Kies eerst de **Build-agent** en plak:

> Lees `HANDOVER.md`, `BESLISSINGEN.md` (zeker B27–B45) en `02_werk/velddekking.md` §19. Voer de taak "Nog te doen om stap 2 volledig af te sluiten" uit: werk `02_werk/crud_matrix.md` in één keer bij en controleer de samenvatting per tabel opnieuw (0 verschillen). Toon me daarna de wijzigingen kort.

Daarna `/new`, **Plan-agent**, `/hervat 3`: ontwerpvragen, te beginnen met **Q20**.
