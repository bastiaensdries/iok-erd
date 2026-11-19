# Handover

_Laatst bijgewerkt: 2026-11-19 20:10 (takenbord op GitHub met 10 issues; dossierformulier nog half af)_

## Stand van zaken

- **Takenbord (2026-11-19).** GitHub Project **"IOK – app bouwen"** (bordweergave: Todo · In Progress · Done), gekoppeld aan de repo `bastiaensdries/iok-erd` met automatische import van open issues. **10 issues** aangemaakt door opencode: acht met label `formulier` (in de bouwvolgorde: Inspectiedossier — enkel koptekst, tab Beoordelingen en tab Verslag —, Beoordeling, Resultaat, Maatregel, Speelterrein, Speeltoestel, HIC-meting, Foto) en twee met label `specificatie` ("Specificatie tweede ronde formulieren", "Specificatie flows"). De kaarten verwijzen naar `02_werk/app_formulieren_views.md`; de details staan daar, niet in de issues. Subrasters gebruiken voorlopig de standaardview; elke kaart noemt de lookup waarmee het subraster gekoppeld wordt. Flows worden pas gebouwd nadat ze uitgeschreven en beslist zijn.
  - **Nog te doen vóór het team kaarten oppakt:** (1) teamgenoten toevoegen aan de Power Platform-omgeving **met een rol**; (2) teamgenoten als collaborator op de repo (de repo bevat echte IOK-documenten in `00_bronnen/`); (3) teamgenoten toegang geven tot het Project — apart, via de instellingen van het Project (Manage access).
  - **Werkafspraken team:** één persoon per formulier tegelijk; eerst pullen, kleine commits; B-nummers via één persoon of op de kaart vermelden zodat twee agents niet hetzelfde nummer uitdelen.
  - **Let op:** `gh` staat niet op de pc van Dries; opencode gebruikte daarom het GitHub-token uit de Windows-credentialmanager en de REST API. Een agent op die pc kan dus met de volledige GitHub-rechten van Dries handelen, ook in Plan-modus: de Plan-agent van opencode blokkeert enkel bestandswijzigingen, geen shellopdrachten. De schrijvende Dataverse-scripts vragen wel altijd `--uitvoeren` plus een getypte bevestiging.

- **Stap 9 is begonnen (2026-11-17): de app.** Formulieren en views volgen `02_werk/app_formulieren_views.md` (B91, aanvaard als B92). De app **IOK Speelterreinen** bestaat in de solution, met de groep Inspectie (Inspectiedossiers, Speelterreinen, Speeltoestellen); het dossierformulier is in opbouw: **tab Algemeen is af** (17/11, 21:06; sectie `sectie_dossier` met dossiernummer alleen-lezen, speelterrein, controledatum, soort controle, inspecteur, eigenaar). **Tab "Bevroren gegevens" is af** (`tab_bevroren`, secties Bestuur, Uitbater, Terrein, Inspecteur, labels zichtbaar). **Volgende stap (niet uitgevoerd op 17/11):** tab Beoordelingen op het dossierformulier: 1-column tab (`tab_beoordelingen`), sectie `sectie_beoordelingen` met verborgen label, daarin een subgrid (Show related records, tabel Beoordelingen (Inspectiedossier), voorlopig de standaardview), label Beoordelingen, naam `subraster_beoordelingen`. Daarna de view "Beoordelingen van dossier" maken (kolommen en sortering op volgorde: zie de specificatie) en aan het subraster koppelen; dan de tab Verslag. Terrein en toestellen staan samen in dat ene subraster (terrein = beoordeling met volgorde 0). **Werkwijze die goed liep:** formulierdesigner en app in twee browsertabbladen; na **Save and publish** F5 in de app. Teamgenoten moeten nog toegang krijgen tot de omgeving (gebruiker + rol) vóór ze formulieren kunnen bouwen; één persoon per formulier tegelijk. Naamgeving op formulieren: `tab_…`, `sectie_…`, `subraster_…`; veldlabels niet overschrijven (B93). **B93:** kolommen krijgen leesbare weergavenamen via `KOLOMNAAM` in `stap6_genereer.py`; `dv_bouw.py` werkt nu ook de weergavenaam van bestaande kolommen bij (stap 6b) en `dv_controle.py` controleert ze. **Uitgevoerd op 17/11 om 20:59** door Dries: `dv_bouw.py --uitvoeren` zette 36 weergavenamen, 0 fouten; `dv_controle.py`: 0 verschillen (nu ook op weergavenamen). De agent kan de omgeving niet bereiken vanuit zijn shell; scripts tegen Dataverse draait Dries. Eerste dossier kreeg nummer `DOS-2026-01000`: de autonummerreeks begint standaard bij 1000.

> **Het datamodel is af en operationeel. Wat nu volgt is het bouwen van de app, geen modelwerk meer.**
> Enige voorbehoud: het model is nooit getoetst aan les 4b (zie "Ontbreekt nog").

- **Afgewerkt op 2026-11-17.**
  - **De twee formulekolommen bestaan en werken.** `iok_risicoscore` (Decimal) en `iok_risicoklasse` (String) op `iok_resultaat`, met de hand gemaakt in de maker-portal via de solution. Gecontroleerd met het nieuwe `tools/dv_formule.py` (alleen-lezen): type, formule en berekende waarden. **De zes berekende scores komen exact overeen met de cijfers in het echte verslag** (126 Substantieel, 9 Licht, 54 Mogelijk, 27 Mogelijk, 18 Licht, 27 Mogelijk), en de zevende bevinding blijft leeg omdat haar blootstelling leeg is — de `IsBlank`-test van B82 werkt dus.
  - **Drie gaten in de proefdata gedicht**, na vergelijking met de PDF van `C_2026` (13 pagina's, regel voor regel):
    1. **BOA 5 "Klimrots" ontbrak.** Oorzaak: `bronnen_naar_md.py` las van `.docx` enkel alinea's en tabellen, geen **tekstvakken**; de kop van dat toestel stond in een tekstvak en viel stil weg. **Script gerepareerd** (functie `tekstvak()`); de hernieuwde conversie voegt exact één regel toe en verandert verder niets. **Nagekeken:** het hele document bevat precies twee tekstvakken met tekst, beide dezelfde kop, en géén enkel Excel-bestand heeft tekst in tekeningen. Dit was dus het enige gat; de velddekking van stap 2 staat op een volledige bron.
    2. **De risicocijfers zijn nu overgenomen** uit het verslag: `iok_impact`, `iok_kans` en `iok_blootstelling` staan in `iok_resultaat.csv`, als expliciete waarden in `BEVINDINGEN` in `csv_maken.py`.
    3. **Foto's blijven ontbreken** — daarvoor zijn de bestanden zelf nodig.
  - **`dv_laden.py` heeft nu `--bijwerken`**: werkt bestaande records bij uit de CSV's in plaats van ze over te slaan. Optioneel met een tabellijst, bv. `--bijwerken iok_resultaat`. Overschrijft handmatige wijzigingen in Dataverse; dat is de bedoeling (de CSV is de bron) maar het is geen samenvoeging.
  - **De omgeving bevat nu 1.046 records + 19 N:N-koppelingen** (was 1.043 + 18): BOA 5, zijn toestelcode, zijn beoordeling en één koppeling kwamen erbij, en de 7 resultaten zijn bijgewerkt. `dv_controle.py`: 0 verschillen.
  - **Q28** toegevoegd: bij BOA 35 punt G.2.3 staat in het verslag de kop "Impact Kans Resultaat" boven drie getallen — er is een kolom weggevallen en het valt niet uit te maken of 3,0 de blootstelling of het resultaat is. De blootstelling blijft daarom leeg.
  - **`tools/maak_verslag.py`** (nieuw, alleen-lezen) bouwt uit de CSV's een leesbare HTML-weergave van het voorbeelddossier: `03_output/verslag_voorbeeld.html`. Handig om naast het echte verslag te leggen.
  - **B89 en B90** vastgelegd: de apparchitectuur (model-driven met canvas custom page) en offline buiten scope, met wat offline zou kosten als de eis terugkomt.
  - **Het project staat op GitHub**: `https://github.com/bastiaensdries/iok-erd`, **private** (in `00_bronnen/` staan echte IOK-documenten). Stappen 4 tot en met 8 zijn in één commit gegaan; daarvoor stonden er zes commits tot stap 3. `README.md` toegevoegd. Teamgenoten moeten nog als collaborator toegevoegd worden.
  - **Nog te doen, geen van alle blokkerend:** documentbeheer (SharePoint) op `iok_inspectiedossier` — vraagt een SharePoint-site; de twee beveiligingsrollen Inspecteur en Bevoegde beheerder (rechten in `spec.yaml` onder `rollen`; overwogen om te scripten in plaats van ~270 vinkjes per rol te klikken); foto's; teamgenoten toevoegen aan de omgeving **én** aan de GitHub-repo.

- **Stap 8 is af: de gedeelde omgeving staat klaar** (2026-11-16). Reden: `orged88419c` is van het type **Developer** — die heeft één eigenaar en is **niet te delen**, ook niet met teamgenoten in dezelfde tenant. Een Sandbox kon niet: de tenant heeft geen 1 GB vrije databasecapaciteit. Daarom een **Trial**.
  - **Nieuwe omgeving:** `trial-eu-d03fb080`, regio Zwitserland, URL `https://orgb2056d46.crm17.dynamics.com`. Werd aangemaakt **zonder** Dataverse-database; die is er daarna bij gezet met "+ Add Dataverse" op de omgevingspagina. Een Trial loopt ~30 dagen en is te verlengen, en wijst gebruikers **niet** automatisch toe: teamgenoten moeten met de hand toegevoegd worden **én** een beveiligingsrol krijgen (System Customizer voor wie bouwt).
  - **Schema gebouwd** met `dv_bouw.py --url https://orgb2056d46.crm17.dynamics.com --uitvoeren` (20:33). `dv_controle.py` geeft **13 verschillen, allemaal de indexstatus van de sleutels** — tabellen, kolommen, relaties, keuzelijsten en statusredenen kloppen. De 13 sleutels zijn in één keer aanvaard: de correctie van de naamkolommen loopt nu vóór het aanmaken van de sleutels.
  - **Data geladen op 2026-11-16 om 20:25**: 1.043 records, **0 fouten**, 1.700 schrijfaanvragen. Zelfde inhoud als in `orged88419c` (2 besturen, 128 types, 3 checklists, 25 onderdelen, 739 controlepunten met 636 zelfverwijzingen, 33 standaardteksten, 55 terreinen, 16 toestellen + 17 codes, 1 dossier, 17 beoordelingen, 7 resultaten, 18 N:N).
  - De 13 sleutels waren de volgende dag alle 13 **Active**, zonder ingrijpen. Bevestigt B88: wachten is het enige wat nodig is.
  - `04_data/_geladen.json` van de run in `orged88419c` is hernoemd naar `_geladen_orged88419c.json`; de nieuwe `_geladen.json` hoort bij deze omgeving.
  - **Aanvulling op B88:** het is **niet** de indexgrootte die de vertraging veroorzaakt. `iok_ak_speelterrein_code` heeft een index van 40 bytes en bleef ook op Pending. De asynchrone jobs melden "geslaagd" binnen de twee minuten; het platform zet de status pas ruim een uur later op Active. Niet ingrijpen, gewoon wachten.
  - ~~**Nog te doen:** (1) het handwerk — de 2 formulekolommen op `iok_resultaat`, documentbeheer op `iok_inspectiedossier`, de 2 beveiligingsrollen.~~ *(formulekolommen zijn op 17/11 gemaakt; zie bovenaan)* (2) Teamgenoten toevoegen aan de omgeving (Power Platform admin center → Manage → Environments → Settings → Users + permissions → Users → + Add user) **én een rol geven**: System Administrator voor wie meebouwt. Een Trial wijst gebruikers niet automatisch toe. (3) Daarna de app.
  - **Appkeuze** (op 16/11 vastgelegd als **B89**): model-driven als ruggengraat, met het invulscherm van een beoordeling als **custom page** (canvas) erin. Valt dat te traag uit op een tablet, dan een losse canvas-app naast de model-driven app; het datamodel verandert daar niet door.
  - **Document voor de teamgenoten:** https://claude.ai/artifact/WMC6iDW7hoN2TgRAikDwdJ — bedoeling, model, tien vormgevende beslissingen, wat er in Dataverse staat, wat er nog bij moet, wat bewust niet in zit, wat nog niet beslist is.
  - `orged88419c` blijft staan als eigen dev-omgeving; die is nu een tweede kopie, geen bron.
- **Stap 7 is uitgevoerd op 2026-11-15** in de omgeving `https://orged88419c.crm4.dynamics.com` (dev-omgeving van Dries), door Dries zelf, stap voor stap met Claude.
  - **Schema:** `dv_controle.py` geeft **0 verschillen** met `spec.yaml`: solution `IOK_Speelterreinen` (prefix `iok_`), 14 keuzelijsten, 17 tabellen, alle kolommen, 35 relaties, 2 N:N, statusredenen, 13 sleutels actief.
  - **Data:** `dv_laden.py` laadde 1.043 records zonder fouten (2 besturen, 128 types, 3 checklists, 25 onderdelen, 739 controlepunten met ouder/hoofdstuk, 33 standaardteksten, 55 terreinen van Geel, 16 toestellen + 17 codes van De Bogaard, 1 dossier, 17 beoordelingen, 7 resultaten) + 18 N:N-koppelingen. `04_data/_geladen.json` onthoudt welke rij welk record werd (niet in git).
  - **Nog met de hand:** de 2 formulekolommen op `iok_resultaat` (formules in `datamodel_v3.md` §6.4), documentbeheer op `iok_inspectiedossier`, de 2 beveiligingsrollen, het voorbeelddossier op Afgerond zetten, en daarna formulieren, views, app, flows.
  - **Geleerd (B88):** Dataverse maakt de naamkolom altijd met 850 tekens aan; `dv_bouw.py` corrigeert lengte en verplichtstelling. Sleutels met de naamkolom + een tweede kolom bleven ruim een uur op Pending en werden dan vanzelf actief. B86 (afbreken) en B87 (`iok_uniekenaam`) zijn **niet** uitgevoerd en vervallen.
  - Hulpscripts die bleven staan: `dv_sleutels.py` (toestand van de sleutels, alleen-lezen), `dv_proef.py` (wegwerptabellen), `dv_sleutel_opnieuw.py` en `dv_sleutel_weg.py` (niet meer nodig).
  - De regels hieronder over "klaargezet, niet uitgevoerd" beschrijven de toestand vóór deze run.
- **Stap 7 (bouwen in Dataverse) is klaargezet, niet uitgevoerd** (2026-11-15, B85). Er is nog **niets** in Dataverse aangemaakt en de scripts zijn **nog nooit tegen een echte omgeving gedraaid**: enkel offline getest (alle 193 aanvragen laten zich opbouwen; de CSV's kloppen met `spec.yaml`). Reken bij de eerste echte run op foutmeldingen die bijgestuurd moeten worden.
  - `tools/dv_gemeen.py` (aanmelden met device code, Web API), `tools/dv_controle.py` (alleen-lezen vergelijking met de spec), `tools/dv_bouw.py` (publisher, solution, 14 keuzelijsten, 17 tabellen, kolommen, 35 relaties, 2 N:N, statusredenen, 13 sleutels), `tools/dv_laden.py` (CSV's laden), `tools/csv_maken.py` (CSV's maken).
  - `04_data/`: 13 CSV's voor Geel (55 terreinen, 128 types, 739 controlepunten, 16 toestellen van De Bogaard, het dossier van 04/08/2026). Afleidingen en gaten: `04_data/LEESMIJ.md`.
  - `03_output/spec.json` = `spec.yaml` als JSON (zodat de scripts zonder PyYAML werken); wordt mee gegenereerd door `stap6_genereer.py`.
  - **Draaiboek** (op de pc van Dries, in de projectmap): (1) `python tools/dv_controle.py --url https://<org>.crm4.dynamics.com` → inloggen met de code; verwacht: alles ontbreekt. (2) `python tools/dv_bouw.py --url ...` = proefdraai; daarna met `--uitvoeren`. (3) de handmatige punten die het script oplijst (2 formulekolommen, documentbeheer, rollen). (4) `python tools/dv_controle.py --url ...` → 0 verschillen. (5) `python tools/dv_laden.py --url ... --uitvoeren`. De URL mag ook één keer in het bestand `.dv_omgeving`.
  - **Niet beslist:** eerst in een testomgeving of meteen in de dev-omgeving. **Niet in de scripts:** formulekolommen, documentbeheer, rollen, formulieren, views, app, flows, plug-in (B77).
  - `.dv_token.json` (aanmeldtoken) en `.dv_omgeving` staan in `.gitignore`; niet delen.
- **Stap 6 is af** (2026-11-14, in Claude). Alle zes de stappen hebben nu een resultaat; zie "Uitkomst stap 6" hieronder. **Niets gebouwd in Dataverse. Les 4b is nog altijd niet getoetst** (`01_context/cursus/` leeg).
- Beslissingen tot en met **B84**; open vragen tot en met **Q27**. De regels hieronder over "tot en met B75 / Q23" en "nog niets getekend" beschrijven de toestand vóór stap 6.
- **Stap 0 (intake) en stap 1 (CRUD-matrix) zijn af.** `02_werk/opdrachtbegrip.md`, `02_werk/crud_matrix.md`.
- **Stap 2 (velddekking) is inhoudelijk af**: `02_werk/velddekking.md` (deel A: lege sjablonen + keuzelijsten; deel B: ingevulde verslagen; overzichten in §16–17; correcties op deel A in §18; samenvatting in §19). "Deel C" is afgedekt door §16–17.
- Beslissingen tot en met **B75**; open vragen tot en met **Q23**. Beantwoord: Q10 (B57), Q11 (B40), Q13 (B60), Q16 (B53). Modelkant beslist, inhoud nog bij IOK: Q12, Q18, Q20, Q21, Q22.
- De hulpscripts van deel B (`_check*.py`) staan nu in `tools/_scratch_stap2/` (wegwerp, niet nodig voor het model).
- **Stap 4 (datamodel v3) is af**: `03_output/datamodel_v3.md` — 23 tabellen (4 standaard, 17 eigen, 2 N:N), kolommen, keuzelijsten, relaties met verwijdergedrag, sleutels, eigenaarschap, rollen en 16 regels buiten het model. Nog niets getekend.
- **Na te lezen door Dries**: B56–B69 zijn door Claude beslist op delegatie. Belangrijkste: B57 (bevriezen met kopiekolommen), B58 (toesteltype niet geversioneerd, herziet B26), B63 (eigenaarschap, niet meer te wijzigen na het bouwen), B67 (inspecteur mag verkeerde invoer verwijderen).
- **Stap 3 (ontwerpvragen) is af** (2026-11-14, in Claude): drie rondes, **B46–B61**, zie `02_werk/ontwerpvragen.md`. Ronde 3 (B56–B61) is door Dries gedelegeerd en nog **na te lezen**; B58 herziet B26 (toesteltype niet meer geversioneerd).

- **Stap 5 (review) is af** (2026-11-14, frisse sessie in Claude): `02_werk/review_v3.md`, **36 genummerde punten** (fout / risico / verbetering), elk met plaats, bron en voorstel. Datamodel, `BESLISSINGEN.md` en CRUD-matrix zijn **niet gewijzigd**. **Les 4b is niet getoetst**: `01_context/cursus/` is nog leeg (Q09).

## Stap 2 volledig afgesloten
- [x] **CRUD-matrix bijgewerkt** (2026-11-14, in Claude): nieuwe kolom `iok_toestelcode` (B44), contact-leesreden na B37 (niet meer in D1.1), D3.2 leest `iok_controlepunt` voor de validatie (B40/B43), H1 C+U op resultaat/maatregel (B28/B40). Samenvatting per tabel opnieuw afgeleid: 24 tabellen, 0 verschillen. Zie de sectie "Wijzigingen na stap 2" onderaan `02_werk/crud_matrix.md`.

## Uitkomst stap 5 (lees `02_werk/review_v3.md`)
- **Eerst lezen:** punt 24 (na Afgerond blijven beoordelingen, resultaten, maatregelen, HIC en foto's bewerkbaar: B57c/B67 niet gerealiseerd), punt 25 (risicoformule: lege factor = 0 → alles "Licht"), punt 8 (verwijderd/onbruikbaar toestel past niet in besluit en invulplicht).
- **De zes ⚑-punten zijn beslist op delegatie (B70–B75), nog na te lezen door Dries.** Elk is terug te draaien met een nieuw B-nummer; het datamodel is nog niet aangepast.
  - B70 – serienummer krijgt een kolom + kopie (punt 1)
  - B71 – besluit "Niet beoordeeld" voor een verwijderd/onbruikbaar toestel (punt 8, herziet B18)
  - B72 – jaarlijkse controle: voor een toestel enkel het besluit verplicht (punt 12, herziet B40/B69)
  - B73 – inspecteur als lookup + naamkopie (punt 19, herziet B63)
  - B74 – dossier op slot na Afgerond met één synchrone controle (punt 24)
  - B75 – beheerder mag sjabloononderdelen verwijderen in Concept (punt 30)
- **Overige fouten** (geen beslissing nodig, wel akkoord): 2, 7, 10, 18. **Risico's:** 3, 4, 9, 11, 14, 16, 20, 23, 26, 28, 31, 34. De rest zijn verbeteringen.
- **Nieuwe vragen voor IOK** (nog niet in `open_vragen.md` gezet): bevestiging van B72 (jaarlijks enkel het besluit, bij Q22); grens van de risicoklasse op precies 70 (punt 26, bij Q08); punt 6.5 leeg in `B_SAM` (punt 17, bij Q22); tellen de eenheden van een verwijderd toestel mee (punt 8). Q06 krijgt hoge prioriteit (punt 16).
- **Te testen in de eigen omgeving** (naast B62): onderliggende records van een inactief dossier (punt 24); `Blank()` in de risicoformule (punt 25); cascade-verwijderen met "beperken" op `iok_ouderid` (punt 30); eigenaar van records die een flow aanmaakt (punt 31); opzoeken van inactieve controlepunten (punt 34).
- **Laadregels voor later (geen model):** 635 bronrijen → 635 terreinen (B56); codes naar hoofdletters; doelgroepwaarden opschonen; controlepuntcodes normaliseren (velddekking §6.8, §14); 162 terreincodes met "/" of "+" (punt 28).

## Ontbreekt nog (niet blokkerend)
- [x] Datamodel v2 → `01_context/datamodel_v2/IOK_erd_v2.md`
- [x] Finaal procesmodel → `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md`
- [x] Feedback IOK 13 november → `01_context/feedback/`
- [x] CRUD-matrix (stap 1) → `02_werk/crud_matrix.md`
- [x] Velddekking (stap 2) → `02_werk/velddekking.md`
- [ ] Transcriptie kick-off → `01_context/feedback/`
- [ ] Cursus les 4b (Dataverse), 4c, 4d → `01_context/cursus/` (stap 5 is zonder gedaan; toetsing aan les 4b inhalen zodra de map gevuld is)
- [ ] Na het toevoegen van bronnen: `python tools/bronnen_naar_md.py` / `python tools/bpmn_naar_md.py` opnieuw draaien.
- [ ] `AGENTS.md`: de vaste eis "elk toestel heeft een foto" is door B15 vervangen (wacht op bevestiging IOK, Q02).

## MCP-servers
`drawio` (stap 6) en `dataverse` (stap 4–6, enkel lezen) staan uit in `opencode.json`; aanzetten en herstarten wanneer nodig. Dataverse MCP vereist dat je in het Power Platform admin center Dataverse MCP aanzet en de client "Dataverse CLI" toestaat.

## Modelkeuze
De gratis DeepSeek-limiet in opencode was op 2026-11-14 bereikt (reset 15-11 01:57). Voor **stap 3 en 4** (veel samenhangende beslissingen) een sterker model gebruiken.

## Uitkomst stap 6 (2026-11-14)
- **Deel 1 (overleg):** B70–B75 en de 36 reviewpunten zijn aan Dries voorgelegd met een voorstel per punt. Dries liet alles doorgaan zonder afzonderlijke opmerkingen ("check dit en ga verder") → **B76**. 35 punten verwerkt, punt 16 deels uitgesteld, niets afgewezen.
- **`03_output/datamodel_v3.md`** bijgewerkt (B70–B84): 23 tabellen (4 standaard, 17 eigen, 2 N:N), 147 kolommen, 35 relaties 1:N, 13 alternatieve sleutels, 14 keuzelijsten, 26 regels in §11.
- **`03_output/spec.yaml`**, **`03_output/ERD_v3.md`** (Mermaid: overzicht + 4 deeldiagrammen) en **`03_output/IOK_erd_v3.drawio`** (stijl van v2, alle kolommen) worden **gegenereerd uit het datamodel** met `python tools/stap6_genereer.py`. Het datamodel is de bron: pas het daar aan en genereer opnieuw; wijzig spec en ERD niet met de hand. Wat niet in de tabellen van het datamodel staat (weergavenamen, opties van doelgroep/categorie, statusredenen, formules, rechten per rol) staat bovenaan in het script.
- **Controle** (`python tools/stap6_genereer.py --check`): 0 verschillen tussen datamodel, spec en ERD. Het script controleert ook het datamodel zelf (elke lookup heeft een relatie in §8 met dezelfde V/O, sleutels in §9 bestaan, één parental per tabel, geen dubbele namen). De Mermaid-blokken zijn door de Mermaid-parser gehaald (5/5); **het draw.io-bestand is niet visueel geopend**: de tabellen staan in zes kolommen, de lijnen zijn automatisch en vragen wellicht wat schuiven.
- **`03_output/IOK_erd_v3.mdj`** (StarUML, één ER-diagram met alle 21 tabellen, 180 kolommen en 37 relaties): gemaakt met `python tools/model_naar_staruml.py [voorbeeld.png]`, zelfde bron als spec en ERD. Vaste plaatsing in vijf kolommen en rechthoekige lijnen die aankomen ter hoogte van de lookup-kolom. Op 2026-11-15 geopend en nagekeken in StarUML op de pc van Dries. `03_output/_voorbeeld_staruml.png` is een voorbeeldafbeelding van de layout en mag weg.
- **`03_output/changelog_v2_v3.md`**: v2 → v3 tabel per tabel + wat in stap 6 wijzigde.
- **`02_werk/crud_matrix.md`** bijgewerkt (sectie "Wijzigingen in stap 6"); **`02_werk/open_vragen.md`**: Q24–Q27 toegevoegd, Q06 hoge prioriteit, Q19 aangepast (serienummer heeft een kolom).

## Na te lezen door Dries
- **B77 – wijkt af van wat in deel 1 voorgesteld was.** Voorstel was een realtime workflow voor het slot (B74). Nagekeken in Microsoft Learn: een workflowvoorwaarde leest maar één stap ver (de rij zelf en haar N:1-rijen), en resultaat/maatregel/HIC/foto zitten twee stappen van het dossier. Daarom **voorlopig een plug-in** (geen modelwijziging). Wil het team geen code, dan is het alternatief een workflow per tabel + een rechtstreekse lookup naar het dossier op die vier tabellen (en naar de checklist op het controlepunt); die kolommen kunnen later nog bij.
- **B70–B75** zijn aanvaard op vertrouwen (B76), niet punt voor punt nagelezen. Belangrijkste: B72 (jaarlijks enkel het besluit; wacht op IOK, Q27) en B71 (Niet beoordeeld; Q26).
- **B78–B84**: de uitwerking van de aanvaarde reviewpunten. Let op B79 (besluit wordt niet overgenomen in D1.4) en B80 (hernomen foto blokkeert het afronden niet).
- **CRUD D3.5 leest nu `iok_controlepunt`**: stond niet in de review, maar zonder kan de PDF de checklistvragen niet drukken.

## Volgende stappen
1. **Les 4b**: zodra `01_context/cursus/` gevuld is, het model eraan toetsen (Q09). Dat is het enige onderdeel van stap 5/6 dat niet gedaan is.
2. **IOK**: Q06 en Q20 eerst; daarna Q24–Q27 en de rest. Geen van de vragen wijzigt de structuur.
3. **Testen in de eigen omgeving** vóór het bouwen: lijst in `datamodel_v3.md` §12 (slot, `Blank()` in de formules, verwijderen in Concept, eigenaar van flowrecords, sleutels).
4. **draw.io** openen en de layout nakijken; `AGENTS.md` bijwerken (vaste eis foto's, B15; stap 6 en de cursusmap).
5. Wijzigingen zijn **niet gecommit** in git.
