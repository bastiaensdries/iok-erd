# Handover

_Laatst bijgewerkt: 2026-11-14 (stap 2 volledig af, incl. CRUD-matrix; afgerond in Claude omdat de gratis opencode-limiet bereikt was)_

## Stand van zaken
- **Stap 0 (intake) en stap 1 (CRUD-matrix) zijn af.** `02_werk/opdrachtbegrip.md`, `02_werk/crud_matrix.md`.
- **Stap 2 (velddekking) is inhoudelijk af**: `02_werk/velddekking.md` (deel A: lege sjablonen + keuzelijsten; deel B: ingevulde verslagen; overzichten in §16–17; correcties op deel A in §18; samenvatting in §19). "Deel C" is afgedekt door §16–17.
- Beslissingen tot en met **B45**; open vragen tot en met **Q22**. Q11 is beantwoord door B40.
- De hulpscripts van deel B (`_check*.py`) staan nu in `tools/_scratch_stap2/` (wegwerp, niet nodig voor het model).
- Nog geen v3-model, nog niets getekend.

## Stap 2 volledig afgesloten
- [x] **CRUD-matrix bijgewerkt** (2026-11-14, in Claude): nieuwe kolom `iok_toestelcode` (B44), contact-leesreden na B37 (niet meer in D1.1), D3.2 leest `iok_controlepunt` voor de validatie (B40/B43), H1 C+U op resultaat/maatregel (B28/B40). Samenvatting per tabel opnieuw afgeleid: 24 tabellen, 0 verschillen. Zie de sectie "Wijzigingen na stap 2" onderaan `02_werk/crud_matrix.md`.

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

## Volgende sessie — stap 3 (ontwerpvragen)
Denksessie (opencode: **Plan-agent**, `/hervat 3`; of in Claude met Fable). Begin met **Q20** (basiseenheid speelterrein), daarna de punten uit "Voor stap 3". Vragen in rondes van max. 5, met opties, voor- en nadelen, voorstel en bron. Schrijf pas na akkoord: `BESLISSINGEN.md`, `02_werk/ontwerpvragen.md`, `HANDOVER.md`.
