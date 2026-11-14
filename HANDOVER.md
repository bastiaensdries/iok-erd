# Handover

_Laatst bijgewerkt: 2026-11-14 (tijdens stap 2 – velddekking, deel A)_

## Stand van zaken
- **Stap 1 (CRUD-matrix) is af.** `02_werk/crud_matrix.md` bestaat; matrix en samenvatting per tabel zijn gecontroleerd (0 verschillen).
- **Stap 2 is begonnen (deel A af)**: `02_werk/velddekking.md` behandelt de vier lege sjablonen en de zes keuzelijstbestanden. Beslissingen **B32–B39** en vragen **Q14–Q17** zijn toegevoegd. Deel B (ingevulde A-/B-/C-verslagen) en deel C (overzichten) volgen.
- 23 tabelkolommen (stamgegevens → sjablonen → inspectie → communicatie → standaardtabellen) en **29 processtappen in procesvolgorde**: D1.1–D1.4, H1, D2.1–D2.6, D3.1–D3.10, H2–H4, D4.1–D4.5; cellen C/R/U/D/X.
- Nieuwe beslissingen **B27–B31**; nieuwe vragen **Q10** (bevriezen), **Q11** (lege resultaatrijen, stap 3), **Q12** (eenheden per bestuur), **Q13** (archieflocatie).
- Er is nog geen v3-model en er is nog niets getekend; de velddekking is halfweg (deel A af).

## Bestanden deze sessie
- Nieuw: `02_werk/velddekking.md` (deel A: vier lege sjablonen + keuzelijsten)
- Gewijzigd: `BESLISSINGEN.md` (B32–B39), `02_werk/open_vragen.md` (Q14–Q17), `HANDOVER.md`

## Open binnen stap 1
- Niets blokkerends. Q10 bepaalt of D3.9 later een C op snapshot-tabellen krijgt, Q11 waar de lege resultaatrijen ontstaan, Q12 of er een kolom `iok_eenheden` op Account komt. Alle drie mogen tot stap 3/4 wachten.

## Taken voor het einde van stap 2
- [ ] **CRUD-matrix bijwerken na B37 (contact).** In de matrix wordt `contact` gelezen als "verantwoordelijke" (D1.1, D3.2, D3.5, H2), maar sinds **B37** is verantwoordelijke = het **bestuur (Account)**. Nuance: in **H2** blijft `contact` waarschijnlijk nodig voor het **e-mailadres van het bestuur** (de inspecteur mailt zelf, B05) — controleer dat vóór je de leesreden schrapt. **Niet tussentijds aanpassen** (opdracht Dries, 2026-11-14).

## Voor stap 3 (ontwerpvragen beslissen)
- **(a) Q16 en HIC samen bekijken als één meetwaarde-oplossing.** De skate-*Afmetingen* en *Veiligheidszone* (Q16) en de HIC-meting (B20, Q03) zijn allebei "een getal met een eenheid en een drempel" bij een beoordeling. Beslis in stap 3 of dat één generiek patroon wordt (meetwaarde op `iok_resultaat`, of één `iok_meting` met een `iok_soort` in plaats van een aparte `iok_hicmeting`), in plaats van per meting een eigen tabel.
- **(b) Diepte van de controlepunt-hiërarchie.** Maximum in de vier lege sjablonen = **3 niveaus** (hoofdstuk → subkop → controlepunt): `A.` → `A.1` → `A.1.1` (Deel 1), `1.` → `1.1` → `1.1.1` (terrein), `H.` → `H.1` → `H.1.1` (valbescherming). Beslis of een **vaste maximumdiepte** volstaat (3, eventueel 4 als de skate-onderdelen als extra niveau tellen) of dat `iok_controlepunt.iok_ouder` **onbeperkt** zelfverwijzend blijft. Controleer in **deel B** of de ingevulde verslagen dieper gaan.

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

## Volgende sessie — stap 2, deel B: de ingevulde verslagen
Kies de **Build-agent** en plak als eerste bericht:

> Lees `HANDOVER.md`, `BESLISSINGEN.md` (zeker B10–B39), `02_werk/velddekking.md` (deel A) en `02_werk/crud_matrix.md`. Laad de skill `velddekking`. Werk **deel B** van `02_werk/velddekking.md` uit: de ingevulde voorbeelden `A_Verslaggeving Indienststelling Schommel`, `B_Indienststelling Evenwichtsparcours`, `B_risicoanalyse terrein`, `B_Samengesteld verslag nieuw speelterrein` en `C_2026 - Jaarlijkse controle De Bogaard (algemeen)`. Controleer daarbij de openstaande punten uit deel A: wijkt **toezicht** per toestel af van het terrein (B33)? Wordt **datum onderhoud** echt gebruikt (B37)? Welke **algemene standaardzinnen** (besluit, preventiesamenvatting) komen alleen in de ingevulde verslagen voor (B35)? Neem het **HIC-blok** en de **risicoscore** (impact/kans/blootstelling) mee en toets ze aan Q03/Q08/Q16. Ga ook na hoe diep de controlepunt-hiërarchie in de ingevulde verslagen werkelijk gaat (HANDOVER, stap 3b). Nog niets in Dataverse bouwen.

Sluit die sessie af met `/handover`.
