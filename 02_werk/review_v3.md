# Review datamodel v3 – stap 5

_Controlesessie 2026-11-14 (Claude, frisse sessie). Nagekeken: `03_output/datamodel_v3.md` tegen `BESLISSINGEN.md` (B01–B69), `02_werk/crud_matrix.md`, `02_werk/velddekking.md`, `02_werk/ontwerpvragen.md`, `02_werk/open_vragen.md`, het finale BPMN en de bronnen in `01_context/`. **Niets gewijzigd** aan het datamodel, de beslissingen of de CRUD-matrix._

**Niet gedaan:**
- **Les 4b: niet getoetst.** `01_context/cursus/` is leeg (Q09 blijft open).
- Niets getest in een Dataverse-omgeving. Wat ik enkel uit de documentatie afleid of niet kon bevestigen, staat erbij als "te testen".

**Ernst:** `fout` = strijdig met een bron, een beslissing of Dataverse · `risico` = werkt mogelijk niet zoals bedoeld · `verbetering` = kan beter of is onvolledig beschreven. **⚑** = een beslissing moet herzien of genomen worden: die beslis jij.

## Eerst lezen

1. **Punt 24 – "Afgerond" vergrendelt enkel het dossierrecord zelf.** Beoordelingen, resultaten, maatregelen, HIC-metingen en foto's blijven actief en dus wijzigbaar en verwijderbaar in de app. B57c en B67 zijn daardoor niet gerealiseerd.
2. **Punt 25 – de risicoformule maakt van elk resultaat zonder score een score 0, klasse "Licht".** Een lege factor telt in een formulekolom als 0.
3. **Punt 8 ⚑ – een verwijderd of onbruikbaar toestel past niet in het model.** De Bogaard heeft er drie; het besluit kent enkel Conform / Niet conform en de invulplicht eist toch alle hoofdstukken.

Daarna: 7 (historiek overnemen pakt het verkeerde dossier), 1 (serienummer), 18 (uitbateradres).

## Jouw beslissing nodig (⚑)

| Punt | Onderwerp | Raakt |
|---|---|---|
| 1 | Serienummer: kolom of bewust weglaten | B41, Q19 (er is nu geen beslissing) |
| 8 | Besluit bij verwijderd / onbruikbaar toestel | B18, B12, B24 |
| 12 | Invulplicht bij de jaarlijkse controle | B40, B69 |
| 19 | Inspecteur als eigen lookup + naamkopie | B63, B37 |
| 24 | Hoe het dossier na Afgerond echt op slot gaat | B57c, B67, B69 |
| 30 | Mag de beheerder een sjabloon in Concept verwijderen | B67, datamodel §10 |

## Oordeel over B56–B69

| B | Plek in het model | Oordeel |
|---|---|---|
| B56 | §4.3, §4.4, regel 12 | klopt |
| B57 | kopiekolommen §6.1/§6.2, statussen §5.1, regel 4–5 | (a) niet afgedwongen → 23; (b) onvolledig → 1, 18, 19, 20; (c) werkt niet voor onderliggende records → 24 |
| B58 | §4.5, §4.7, §6.2 | klopt |
| B59 | §6.2, §6.4, §6.5 | herkomst ontbreekt bij de besluitteksten → 2 |
| B60 | §7.3, regel 14 | klopt |
| B61 | §4.1, regel 16 | klopt; zie 8 voor verwijderde toestellen |
| B62 | §9, §12 | klopt met de documentatie; aanvulling in 24 en 28 |
| B63 | §1, §2 | eigenaarschapstype klopt; "eigenaar = inspecteur" is zwak → 19, 31 |
| B64 | §6.4 | formulekolommen kunnen, maar de formule is fout bij lege waarden → 25, 26, 27 |
| B65 | §5.5, regel 7 | werkt, met een neveneffect → 4 |
| B66 | §6.2, §6.4, §6.5, regel 9 | onvolledig op beoordelingsniveau → 3 |
| B67 | §10 | niet afdwingbaar met een rol alleen → 24, 31 |
| B68 | §6.1, §6.2 | klopt |
| B69 | regel 1, §7.1, §7.2 | (1) klopt, maar zie 12; (2) klopt, zie 34 |

B01–B55 hebben elk een plek; afwijkingen staan in de punten hieronder (B35 → 5, B15 → 20, B18 → 8 en 11, B40 → 12, B44 → 21).

---

## A. Beslissingen en bronnen

### 1. Serienummer is weggelaten zonder beslissing — `fout` ⚑
- **Wat:** het model schrapt serienummer "(B41, Q19)", maar B41 schrapt enkel *datum onderhoud*; serienummer is daar een vraag aan IOK. De velddekking zet `iok_speeltoestel.iok_serienummer` op "gedekt". De projectopdracht noemt het veld verplicht.
- **Waar:** §4.5 (`iok_speeltoestel`), §6.2 (kopiekolommen).
- **Bron:** `Projectopdracht_IOK.md` §4.1 ("leverancier, type toestel, serienummer, bouwjaar,… Deze info is verplicht"); velddekking §3.1 r22/F; `A_` en `B_IND` r22 (label gedrukt, waarde leeg); B41.
- **Voorstel:** `iok_speeltoestel.iok_serienummer` (tekst 60, O) + kopie op `iok_beoordeling`; nieuw B-nummer. Wil je het toch weglaten, leg dat dan vast als beslissing met Q19 als voorbehoud.

### 2. Herkomst van de besluitteksten ontbreekt — `fout` (klein)
- **Wat:** B59 zegt dat ook het besluit van de beoordeling een optionele lookup naar de herkomst krijgt. Die bestaat enkel op `iok_resultaat` en `iok_maatregel`.
- **Waar:** `iok_beoordeling.iok_besluittekst`, `iok_inspectiedossier.iok_algemeenbesluit`.
- **Bron:** B59, B68.
- **Voorstel:** twee optionele lookups naar `iok_standaardtekst` toevoegen (koppeling verwijderen), of B59 in de changelog uitdrukkelijk beperken tot resultaat en maatregel.

### 3. Overgenomen besluit is niet herkenbaar — `risico`
- **Wat:** D1.4 neemt de beoordeling over (B28). `iok_isovergenomen` staat op resultaat en maatregel, niet op de beoordeling. Een overgenomen `iok_besluit`, `iok_besluittekst` of `iok_opmerking` is dus niet te onderscheiden van een nieuw oordeel. Een conform toestel zonder resultaten (9 van de 16 in De Bogaard) heeft dan geen enkele vlag.
- **Waar:** `iok_beoordeling`; regel 9.
- **Bron:** vaste eis "een overgenomen antwoord is nog geen nieuwe inspectie"; B28, B66; `C_2026`.
- **Voorstel:** besluit, besluittekst en opmerking **niet** overnemen (leeg laten), of `iok_beoordeling.iok_isovergenomen` toevoegen en in regel 9 opnemen.

### 4. Standaardteksten verhuizen terwijl dossiers op de oude versie lopen — `risico`
- **Wat:** bij een nieuwe checklistversie wijst `iok_standaardtekst.iok_controlepuntid` naar het nieuwe controlepunt. Een dossier dat nog op de oude versie loopt, vindt bij zijn controlepunt geen zinnen meer. Wijzigt een code, dan blijft de zin zonder controlepunt achter.
- **Waar:** §5.5, regel 7.
- **Bron:** B65, B19.
- **Voorstel:** zinnen in de app zoeken op onderdeelnaam + code in plaats van op de lookup, of de regel aanvullen: "versie pas activeren als er geen dossiers In uitvoering op de oude versie staan".

### 5. `iok_standaardtekstsoort` dekt de lijsten van B35 niet — `verbetering`
- **Wat:** de waarden Markering · Inlichting · Maatregel · Besluit mengen lijstnamen met gebruik. De lijsten Informatie, AREI, Schema, Meubilair en de vier skate-lijsten hebben geen soort; de zin "Het toestel is momenteel onbruikbaar." is volgens B18 geen besluit maar zou soort Besluit krijgen (B68).
- **Waar:** §3, §5.5.
- **Bron:** B35, B18, B68; velddekking §12.2–12.3.
- **Voorstel:** indelen naar gebruik: Opmerking bij controlepunt · Maatregel · Besluit beoordeling · Algemeen besluit. De lijst volgt al uit `iok_controlepuntid`.

### 6. Kolommen zonder bron of zonder schrijvende stap — `verbetering`
- **Wat / waar:**
  - `iok_rapportversie.iok_verzendpogingen` en `iok_laatstepogingop`: geen enkele stap schrijft ze. Verzenden gebeurt buiten Dataverse (B05) en H3 is in de CRUD-matrix enkel R.
  - `iok_foto.iok_genomenop`, `iok_maatregel.iok_volgorde`, `iok_checklistonderdeel.iok_volgorde`: bron "–".
- **Bron:** AGENTS.md ("vermeld waarop het steunt"); CRUD H3, "Ontbrekend 6".
- **Voorstel:** verzendpogingen schrappen, of H3 een knop "poging mislukt" geven (U op de versie). `iok_genomenop` motiveren met B15 ("meest recente foto"); de volgordekolommen met de PDF-volgorde in `B_SAM`.

---

## B. Proces

**Dossier 1 – De Bogaard, jaarlijkse controle 04/08/2026** (`C_2026`): D1.1 → D1.2 → D1.4 → H1 → D2.x (16 toestellen) → D3 → H2–H4. Het loopt vast of wordt onduidelijk op de punten 7, 8, 9, 11, 12, 13 en 3.
**Dossier 2 – Collin Brownstraat, nieuw terrein + indienststelling 14/08/2025** (`B_SAM`): D1.1 → D1.2 → D1.3 → H1 (terrein als risicoanalyse, 46 punten) → D2.1/D2.3 (Evenwichtsparcours, enkel Deel 1) → D3. Het loopt vast op 16, 10, 11 en 18–19.

Wat goed werkt in beide: één toestel met meerdere codes (B44), toestel zonder Deel 2-onderdeel (B52), hoofdstukresultaat als resultaat op het hoofdstuk (B40), bevinding op een code van 4 niveaus (B43), skatepark op een EN 1176-terrein (norm per beoordeling, B21), terrein en toestel met een verschillende beoordelingsbasis in één dossier, twee PDF's per versie (B11).

### 7. "Historiek overnemen" pakt het verkeerde dossier — `fout`
- **Wat:** regel 9 neemt over uit "het vorige dossier". Voor De Bogaard is dat de indienststelling van de schommel BOA 34 op 19/01/2026 (`A_`), niet de jaarlijkse controle van 2025. D1.4 zou dan één toestel overnemen. Bovendien: een toestel dat sinds vorig jaar nieuw is, krijgt in D1.4 geen beoordeling, en een toestel Buiten gebruik moet overgeslagen worden.
- **Waar:** §11 regel 9 en 10; CRUD D1.4.
- **Bron:** `A_Verslaggeving Indienststelling Schommel.md` r8, r15, r17 (De Bogaard, BOA 34, 19/01/2026); `C_2026` (Contactschommel BOA 34); BPMN D1; B28.
- **Voorstel:** regel herschrijven: per toestel in gebruik de **meest recente afgeronde beoordeling van dat toestel** (ongeacht het dossier), voor het terrein de meest recente terreinbeoordeling; een toestel zonder historiek krijgt een lege beoordeling zoals in D1.3; kopiekolommen altijd vers uit de stamgegevens. Het model kan dit al (`iok_bronbeoordelingid`).

### 8. Verwijderd of onbruikbaar toestel heeft geen plek — `risico` ⚑
- **Wat:** `C_2026` bevat twee toestellen "verwijderd van het terrein" (BOA 32, BOA 38) en één "momenteel onbruikbaar" (BOA 29). Ze staan wel in het verslag, met foto en zin. In het model is het besluit verplicht bij afronden en kent het enkel Conform / Niet conform; regel 1 eist bovendien een antwoord op elk hoofdstuk. De eenheden zijn al gekopieerd en tellen mee in het financiële overzicht. De inspecteur kan het toestel niet zelf Buiten gebruik zetten (enkel de beheerder, D4.1).
- **Waar:** `iok_besluit` (§3), `iok_beoordeling.iok_besluit`, regel 1, regel 16.
- **Bron:** `C_2026` (Vogelnestschommel BOA 29, Volleybalterrein BOA 32, Dubbele veerwip BOA 38); B18, B12/V4, B24, B61.
- **Voorstel:** derde waarde in `iok_besluit`: **Niet beoordeeld** (met de bevinding in `iok_besluittekst`), die de invulplicht uitschakelt. Beslis ook: tellen de eenheden van zo'n toestel mee, en wie zet het toestel Buiten gebruik?

### 9. Het dossier weet niet welk soort controle het is — `risico`
- **Wat:** de systeembeslissing "Jaarlijkse controle?" in D1 komt ná het aanmaken van het dossier en vóór er beoordelingen bestaan. De beoordelingsbasis staat enkel per beoordeling. Ook de titel van de PDF ("Jaarlijkse controle 2026") en de lijst "uitgevoerde controles" (D4.5) hebben het nodig.
- **Waar:** `iok_inspectiedossier`.
- **Bron:** BPMN D1 (XOR "Jaarlijkse controle?", lane Systeem); `C_2026` (titel "Jaarlijkse controle 2026"); projectopdracht §3 (twee blokken van controles), §5.2.
- **Voorstel:** `iok_inspectiedossier.iok_soortcontrole` (keuze: Jaarlijkse controle · Nieuwe controle, V). De gekozen toestellen (inspectiescope) hoeven geen kolom: dat is een parameter van D1.3; zet dat erbij in §11.

### 10. `iok_beoordelingsbasis` is verplicht bij het aanmaken, maar wordt pas in D2.1 bepaald — `fout`
- **Wat:** D1.3 (systeem) maakt de beoordeling aan; de keuze indienststelling of risicoanalyse valt pas in D2 ("Eerste controle van dit toestel?", "Beoordeeld als conform?").
- **Waar:** §6.2.
- **Bron:** BPMN D2; CRUD D1.3 en D2.1.
- **Voorstel:** O bij aanmaak, verplicht bij afronden (zoals `iok_besluit`); standaardwaarde Jaarlijkse controle als het dossier jaarlijks is (punt 9).

### 11. Bevinding en maatregel: één tekst in de bron, twee velden in het model — `risico`
- **Wat:** in de verslagen staat onder een controlepunt één tekst met bevinding én maatregel. Het model heeft `iok_resultaat.iok_opmerking` en `iok_maatregel.iok_tekst`, zonder regel wat waar komt. De preventiesamenvatting (D3.4) leest enkel maatregelen: typt de inspecteur alles in de opmerking, dan is de samenvatting leeg.
- **Waar:** §6.4, §6.5, §11.
- **Bron:** `C_2026` (K.1 bij BOA 11 en BOA 24); `B_SAM` punt 1.2 en 5.1; velddekking §12.2 ("Eén tekst, geen twee"); feedback IOK ("preventiesamenvatting is zeer belangrijk").
- **Voorstel:** regel toevoegen: opmerking = wat er vastgesteld is, maatregel = wat het bestuur moet doen; een NOK zonder maatregel geeft in D3.2 een waarschuwing; de PDF drukt beide onder het controlepunt.

### 12. Invulplicht bij de jaarlijkse controle is zwaar en zwak onderbouwd — `risico` ⚑
- **Wat:** regel 1 eist bij jaarlijks per toestel een antwoord op elk hoofdstuk (14 in Deel 1, plus Deel 2). `C_2026` toont bij een conform toestel enkel "Het toestel is conform de norm." Via D1.4 komen die resultaten als overgenomen binnen en moeten ze één voor één bevestigd worden: voor De Bogaard minstens 16 × 14, per jaar ruim 70.000 rijen die enkel "OK" zeggen. De bron van B40 (projectopdracht §4.1) gaat over indienststelling, niet over jaarlijks.
- **Waar:** §11 regel 1 en 9.
- **Bron:** `C_2026`; velddekking §11 (tabel "Invulplicht per basis"); projectopdracht §4.2 en §5.1 ("met minder handelingen"); B40, B69.
- **Voorstel:** bij jaarlijks voor een toestel hetzelfde als voor het terrein (B54): enkel het besluit verplicht, punten bij afwijking. Of de regel houden en één actie "alles bevestigen" per toestel voorzien. Vraag voor IOK naast Q22.

### 13. Volgorde van de toestellen in het verslag ontbreekt — `verbetering`
- **Wat:** `C_2026` volgt een eigen volgorde (… BOA 45, dan BOA 34). Sorteren op code kan niet: "BOA 7", "BOA 11" en "BOA 03" sorteren als tekst verkeerd.
- **Waar:** `iok_beoordeling`.
- **Bron:** `C_2026`.
- **Voorstel:** `iok_beoordeling.iok_volgorde` (geheel getal, O); terrein = 0.

### 14. Een fout dossier kan niet weg — `risico`
- **Wat:** niemand verwijdert dossiers (§10) en er is geen statusreden voor annuleren. Een dossier met het verkeerde terrein of de verkeerde datum blijft bestaan en houdt de sleutel terrein + controledatum bezet.
- **Waar:** §6.1 (statusredenen), §9, §10.
- **Bron:** B17, B19; alternatieve sleutels tellen inactieve records mee (B62).
- **Voorstel:** statusreden **Geannuleerd** (inactief), en de beheerder mag een dossier zonder rapportversie verwijderen (de relatie naar `iok_rapportversie` blokkeert de rest al).

### 15. Twee ontbrekende regels — `verbetering`
- **Wat:** (a) haalt de inspecteur in D2.1 een onderdeel weg, dan blijven de resultaten op de controlepunten van dat onderdeel staan. (b) Na een dossiercorrectie in D3.8 gaat het BPMN terug naar D3.5, niet naar de validatie D3.2; het dossier wordt pas in D3.9 Afgerond.
- **Waar:** §11.
- **Bron:** CRUD D2.1 (C+D op `iok_beoordeling_onderdeel`); BPMN D3.
- **Voorstel:** (a) een onderdeel met resultaten kan niet weg, of de resultaten gaan mee weg; (b) D3.9 voert de validatie van D3.2 opnieuw uit vóór de status wijzigt.

### 16. Dossier 2 kan niet starten zonder de beheerder — `risico`
- **Wat:** een nieuw terrein, een nieuw toestel en zijn codes kan enkel de beheerder aanmaken (§10). Bij een indienststelling is het toestel per definitie nieuw. Het model zegt terecht dat Q06 geen structuur wijzigt, maar het proces staat stil tot die vraag beantwoord is.
- **Waar:** §10; CRUD "Ontbrekend 10".
- **Bron:** B08, Q06; `B_SAM`.
- **Voorstel:** Q06 hoge prioriteit geven bij IOK. Bij twijfel: de inspecteur mag terrein, toestel en toestelcode **aanmaken**, enkel de beheerder mag ze wijzigen.

### 17. Kleine waarnemingen uit de bronnen — `verbetering`
- `B_SAM` punt 6.5 heeft geen status in een risicoanalyse van het terrein. Regel 1 zou dit echte dossier blokkeren. Vermoedelijk een vergetelheid; meenemen als vraag bij Q22.
- "Galaxy BOA 04" heeft twee overzichtsfoto's. De regel "een nieuwe overzichtsfoto zet de oude op `iok_inverslag` = nee" laat er maar één toe. Voorstel: enkel foto's uit een **vorig** dossier automatisch uitzetten.
- "De Bogaard Algemeen" is in `Overzicht bestaande speelterreinen` een rij met F = 2 (r172): het gekozen voorbeelddossier is zelf een geval van Q20. Geen modelgevolg (B56), wel goed om te weten voor de demo.

---

## C. Verslagen (kopiekolommen, B57)

**Gedekt:** terreinnaam, terreincode, adres van het terrein, bestuur, contactpersoon, uitbaternaam, doelgroep (terrein en toestel apart), toezicht, controledatum, toestelnaam, code, leverancier, fabrikanttype, bouwjaar, attest, norm, typenaam, eenheden, besluittekst, opmerking per beoordeling, HIC-velden, algemeen besluit. Checklistteksten komen uit de versie (B19); legendes, titels en "IOK Antwerpseweg 1" zijn vaste tekst.

### 18. Adres van de uitbater wordt gedrukt maar niet gekopieerd — `fout`
- **Wat:** onder "Uitbater" staat naam én adres ("Stad Geel, Werft 17, 2440 Geel"; in `A_` Werft 20). Het dossier kopieert enkel `iok_uitbaternaam`. Is de uitbater leeg (= het bestuur), dan komt het adres van het bestuur uit Account en dat is evenmin gekopieerd.
- **Waar:** §6.1.
- **Bron:** `A_` r11–13; `B_IND` r11–13; `B_SAM` (terrein- en toestelblad); B14, B57.
- **Voorstel:** `iok_uitbaterstraat`, `iok_uitbaterpostcode`, `iok_uitbaterplaats` (kopie, O) op het dossier.

### 19. De naam van de inspecteur is niet bevroren — `risico` ⚑
- **Wat:** "RA uitgevoerd door: … Danny Frederix" komt van de eigenaar van het dossier. Die wijzigt bij een overname (§10 laat dat uitdrukkelijk toe) of als de gebruiker vertrekt; een PDF die later opnieuw gemaakt wordt, draagt dan een andere naam. Daarnaast kan `ownerid` niet tegelijk "wie inspecteerde" en "bij welk bestuur hoort dit" zijn, terwijl B13 het eigenaarschap net voor die latere afscherming reserveert.
- **Waar:** §2, §6.1.
- **Bron:** `A_` r13, `B_IND` r13; B13, B37, B63.
- **Voorstel:** `iok_inspectiedossier.iok_inspecteurid` (lookup → `systemuser`, V, koppeling beperken) + `iok_inspecteurnaam` (kopie). Herziet de zin "geen aparte inspecteur-lookup" in B63.

### 20. Een hernomen foto wordt buiten het dossier gelezen — `risico`
- **Wat:** zonder nieuwe foto neemt de PDF "de meest recente uit eerdere beoordelingen". Dat is strijdig met regel 5 (de PDF leest enkel het dossier) en niet bevroren: een latere foto verandert een oud verslag dat opnieuw gegenereerd wordt. In de CRUD-matrix leest D1.4 foto's maar maakt het er geen aan.
- **Waar:** §6.7, regel 5; CRUD D1.4.
- **Bron:** B15, B14, B57.
- **Voorstel:** D1.3/D1.4 maken in de nieuwe beoordeling een `iok_foto` aan die naar hetzelfde bestand wijst, met `iok_isovergenomen` = ja. De PDF leest dan enkel het dossier.

### 21. Weergave van meerdere codes heeft geen bron — `verbetering`
- **Wat:** de kopie `iok_beoordeling.iok_toestelcode` moet "BOA 1 + BOA 2" of "SCB 01 -> SCB 04" bevatten, maar geen kolom of regel zegt hoe die tekst ontstaat.
- **Waar:** §4.5, §4.6, §6.2.
- **Bron:** `C_2026`; `B_IND` r15; B44.
- **Voorstel:** `iok_speeltoestel.iok_codeweergave` (tekst 100, O; leeg = hoofdcode), door de beheerder in te vullen.

### 22. Versiedatum en handmatig aangepaste PDF — `verbetering`
- **Wat:** (a) "Versie d.d." is nu `createdon` van de rapportversie; een PDF die binnen dezelfde versie opnieuw gemaakt wordt (D3.8) heeft een latere datum. (b) De inspecteur mag de PDF zelf aanpassen (vaste eis); niets legt vast dat een PDF daarna afwijkt van de dossiergegevens.
- **Waar:** §7.1, §7.2.
- **Bron:** `B_SAM` voettekst; projectopdracht §3; vaste eis "kan de PDF aanpassen"; B57.
- **Voorstel:** (a) `createdon` van `iok_document` gebruiken; (b) `iok_document.iok_handmatigaangepast` (ja/nee, standaard nee).

### 23. Onveranderlijkheid van de sjabloonteksten is niet afgedwongen — `risico`
- **Wat:** alle gedrukte checklistteksten steunen op "enkel wijzigbaar in Concept". Dat staat in §5.1 maar niet in §11, en een rol kan het niet afdwingen: de beheerder heeft wijzigrecht op alle controlepunten, ook van een actieve versie.
- **Waar:** §5.1–5.3, §10, §11.
- **Bron:** B57a, B19.
- **Voorstel:** regel 17 toevoegen met het mechanisme (synchrone controle bij wijzigen van onderdeel of controlepunt: status van de checklist = Concept). Kiezen in stap 6.

---

## D. Dataverse

**Klopt met de documentatie:** eigenaarschapstype is achteraf niet te wijzigen; organisatie-eigendom past voor de vijf sjabloontabellen; hoogstens één parental-relatie per tabel (elke tabel in §8 voldoet); lookups, datums en tekst mogen in een alternatieve sleutel, maximaal 10 per tabel; eigen statusredenen per status kunnen; een formulekolom kan tekst en decimalen teruggeven; native N:N zonder eigen kolommen is hier verdedigbaar.

### 24. Na Afgerond blijven de onderliggende records bewerkbaar — `fout` ⚑
- **Wat:** B57c en regel 4 steunen op de status: dossier Afgerond = inactief = alleen-lezen. Een status geldt per record en gaat niet mee naar onderliggende records: het cascadegedrag van een relatie kent enkel toewijzen, delen, opnieuw koppelen, verwijderen en samenvoegen. `iok_beoordeling`, `iok_resultaat`, `iok_maatregel`, `iok_hicmeting` en `iok_foto` blijven dus actief; ze hebben in het model ook geen statusredenen. B67 ("verwijderen enkel zolang het dossier niet Afgerond is") kan een beveiligingsrol evenmin: een rol kent enkel het niveau Eigen/Org, geen voorwaarde op het bovenliggende record.
- **Waar:** §6.1–6.7, §10, §11 regel 4.
- **Bron:** Microsoft Learn, *Table relationships* (acties Assign, Reparent, Share, Delete, Unshare, Merge) en *Security roles and privileges*; B57, B62, B67, B69. Te testen in de eigen omgeving.
- **Voorstel (kies één):** (a) de flow van D3.9 deactiveert alle onderliggende records en de flow van regel 15 activeert ze opnieuw; (b) één synchrone controle op wijzigen en verwijderen van die vijf tabellen: "het dossier is niet Afgerond". (b) dekt ook flows en de Web API (B62) en is één regel in plaats van vijf statusovergangen.

### 25. Risicoformule: een lege factor telt als 0 — `fout`
- **Wat:** in een formulekolom wordt een lege numerieke kolom in een berekening als 0 behandeld. De drie factoren zijn optioneel en in geen enkel voorbeeld ingevuld. `iok_risicoscore` wordt dan 0 en `iok_risicoklasse` "Licht" voor **elk** resultaat zonder score, ook in de overzichten van D4.3.
- **Waar:** `iok_resultaat.iok_risicoscore`, `iok_risicoklasse`.
- **Bron:** Microsoft Learn, *Work with formula columns* ("If there's a numeric column that's null then it's considered 0"); B45, B64.
- **Voorstel:** beide formules beginnen met een test op leeg, bv. `If(IsBlank(iok_impact) || IsBlank(iok_kans) || IsBlank(iok_blootstelling), Blank(), iok_impact * iok_kans * iok_blootstelling)`; de klasse geeft leeg terug als de score leeg is. Precisie van de score: 2 decimalen (0,5 × 0,5 × 1 = 0,25). Te testen.

### 26. De risicoklasse heeft een gat op 70 — `risico`
- **Wat:** de brontabel zegt 20 < R < 70 en 70 < R < 160: precies 70 valt nergens. Met de toegelaten waarden is 70 haalbaar (7 × 10 × 1). 160 en 320 zijn met deze waarden niet haalbaar. Het model noemt de vijf klassen zonder grenzen.
- **Waar:** `iok_risicoklasse`.
- **Bron:** `C_2026` (legende risicoanalyse, tabel "Risico"); B45.
- **Voorstel:** grenzen uitschrijven in het model (voorstel: bovengrens inbegrepen, dus 70 = Mogelijk) en als korte vraag aan IOK bij Q08.

### 27. Formulekolommen zijn niet sorteerbaar of doorzoekbaar — `verbetering`
- **Wat:** een formulekolom wordt bij het ophalen berekend en kan niet gesorteerd of doorzocht worden; er kan ook geen flow op starten. Een overzicht "hoogste risico eerst" kan dus niet op `iok_risicoscore`.
- **Waar:** §6.4; regel 16.
- **Bron:** Microsoft Learn, *Types of columns* ("Formulas … can't be sorted") en *Work with formula columns*.
- **Voorstel:** vermelden in §6.4. Is sorteren nodig, dan de score als gewone decimale kolom laten vullen door de app.

### 28. 162 terreincodes werken niet als sleutel in de Web API — `risico`
- **Wat:** 160 van de 604 terreincodes bevatten "/" (bv. `BA.G/0.01`, `BKO/G`) en 2 een "+". Met die tekens werkt ophalen of bijwerken via de alternatieve sleutel in de URL niet. Hetzelfde geldt voor 8 typenamen (`Schommel enkel/ dubbel`, `Doel + basketring`, …). Uniekheid blijft wel afgedwongen.
- **Waar:** §9 (`iok_speelterrein.iok_code`, `iok_toesteltype.iok_naam`).
- **Bron:** Microsoft Learn, *Define alternate keys* en *Retrieve a table row using the Web API*; `Overzicht bestaande speelterreinen.md`; `Overzicht soorten speeltoestellen.md`; vaste eis "later koppeling via de Web API".
- **Voorstel:** in §9 vermelden dat de sleutel voor uniekheid dient en dat de koppeling `$filter` gebruikt, of de tekens vervangen bij het hercoderen (Q20). Geen modelwijziging.

### 29. Ontbrekende sleutels — `verbetering`
- **Wat / voorstel:**
  - `iok_beoordeling`: sleutel `iok_inspectiedossierid` + `iok_speeltoestelid` dwingt "hoogstens één per toestel" af. Voor de terreinbeoordeling (toestel leeg) geldt de sleutel niet: bij lege sleutelkolommen wordt uniekheid niet afgedwongen. Regel 10 blijft dus nodig voor het terrein.
  - `iok_terreingroep`: sleutel `iok_bestuurid` + `iok_naam` (het argument van B56).
  - `iok_inspectiedossier.iok_dossiernummer`: sleutel, zodat de koppeling met besturen een dossier op nummer kan opvragen.
- **Waar:** §9.
- **Bron:** Microsoft Learn, *Define alternate keys* ("When NULL values are used … uniqueness will not be enforced"); B56; regel 10.

### 30. Parental op de sjablonen heeft geen functie en botst met "niemand verwijdert" — `risico` ⚑
- **Wat:** checklist → onderdeel → controlepunt is parental, maar §10 zegt dat niemand sjablonen verwijdert, en tabellen in organisatie-eigendom hebben geen eigenaar om door te geven. Gevolg: een fout aangemaakt controlepunt in een Concept-checklist kan niemand verwijderen. Zou verwijderen wel toegelaten worden, dan botst de cascade vermoedelijk op "beperken" van `iok_ouderid` en `iok_hoofdstukid` (te testen).
- **Waar:** §8, §10.
- **Bron:** datamodel §8 en §10; Microsoft Learn, *Table relationships* (Restrict).
- **Voorstel:** de beheerder mag onderdelen en controlepunten verwijderen zolang de checklist in Concept staat (zelfde controle als punt 23), van onder naar boven. Bij dossier → beoordeling in §8 vermelden dat parental daar dient voor het doorgeven van de eigenaar, niet voor verwijderen.

### 31. Eigenaar van records die een flow aanmaakt — `risico`
- **Wat:** D1.2–D1.4 zijn systeemtaken. Een record dat een flow aanmaakt, krijgt de eigenaar van de flowverbinding, niet de inspecteur, tenzij de flow de eigenaar zelf invult. "Eigenaar = inspecteur" (B63) en "verwijderen Eigen" (B67) kloppen dan niet voor overgenomen resultaten. Een overname door een collega moet via **Toewijzen** gebeuren, anders blijven de onderliggende records van de eerste inspecteur.
- **Waar:** §2, §10, §11.
- **Bron:** B63, B67; Microsoft Learn, *Configure table relationship cascading behavior* (assign cascadeert naar onderliggende records). Te testen.
- **Voorstel:** regel toevoegen: elke flow die dossierrecords aanmaakt, zet `ownerid` op de inspecteur; overnemen = toewijzen van het dossier.

### 32. Rollen: Append, Append To en Assign ontbreken — `verbetering`
- **Wat:** §10 noemt enkel maken, lezen, wijzigen, verwijderen. Een lookup invullen vraagt Append/Append To; een N:N-koppeling vraagt Append op **beide** tabellen, dus de inspecteur ook op `iok_checklistonderdeel`. Overnemen vraagt Assign.
- **Waar:** §10.
- **Bron:** Microsoft Learn, *Security roles and privileges*.
- **Voorstel:** in de specificatie van stap 6 per tabel alle acht rechten opnemen.

### 33. Dubbele paden: regels ontbreken en twee paden zijn niet vermeld — `verbetering`
- **Wat:** §8 zegt "elk met een consistentieregel", maar enkel pad 1 staat in §11 (regel 12). De regels van pad 3 (maatregel/foto: zelfde beoordeling als het resultaat), pad 4 (onderdelen horen bij de checklist van de beoordeling) en pad 5 (hoofdstuk = top van de ouderketen) staan verspreid in de tabelteksten. Niet vermeld:
  - `iok_beoordeling.iok_norm` naast beoordeling → checklist → `iok_norm`;
  - resultaat → controlepunt → onderdeel naast resultaat → beoordeling ↔ onderdeel (het controlepunt moet in een gekozen onderdeel zitten);
  - `iok_speeltoestel.iok_code` naast `iok_toestelcode.iok_ishoofdcode` (regel 11 bestaat, het pad staat niet in §8).
- **Waar:** §8, §11.
- **Bron:** skill `dataverse-modellering` §4; B21, B44, B51, B52.
- **Voorstel:** de lijst in §8 uitbreiden tot acht en elke regel een nummer in §11 geven. Pad 2 is in orde.

### 34. Onderdelen en controlepunten van een vervangen checklist deactiveren — `risico`
- **Wat:** de CRUD-matrix deactiveert in D4.2 ook onderdelen en controlepunten. Een dossier dat nog op die versie loopt, moet dan resultaten koppelen aan inactieve controlepunten; standaard-opzoekvensters tonen inactieve records niet.
- **Waar:** §5.1; CRUD D4.2 (C+X).
- **Bron:** B19, B69; **geen officiële bron gevonden voor het gedrag van opzoekvensters** — te testen in de eigen omgeving.
- **Voorstel:** enkel de checklist krijgt Vervangen; onderdelen en controlepunten blijven actief (ze zijn toch onveranderlijk, punt 23). De overige statusredenen van B69 kloppen; wijzigen van een inactieve rapportversie (Verzonden, verzonden op) kan enkel via een flow, zoals B69 al zegt.

### 35. Kleine typepunten voor de specificatie — `verbetering`
- `iok_controledatum`: gedrag **Alleen datum** vastleggen (niet Lokale tijd van gebruiker); de kolom zit in een sleutel en tijdzones mogen de datum niet verschuiven. Bron: Microsoft Learn, *Behavior and format of the date and time column*.
- `iok_dossiernummer`: de juiste notatie is `DOS-{DATETIMEUTC:yyyy}-{SEQNUM:5}`. Het jaar is het aanmaakjaar in UTC, niet het jaar van de controle, en de reeks begint niet opnieuw per jaar. Bron: Microsoft Learn, *Autonumber columns*.
- `iok_foto.iok_url` en `iok_document.iok_url` (400): SharePoint-links met mapnamen worden langer; een tekstkolom mag tot 4.000 tekens. Voorstel: 2.000.
- `iok_speelterrein.iok_postcode` tekst (4): past niet voor een uitbater buiten België (Q01); enkel relevant als punt 18 dezelfde lengte overneemt.

---

## E. CRUD-matrix (niet gewijzigd)

### 36. De matrix loopt achter op B57 en B69 — `verbetering`
- D1.2 vult bestuur-, contact- en uitbaternaam, maar heeft geen R op `account` en `contact`.
- D1.3 en D1.4 vullen de kopie van de toestelcode, maar hebben geen R op `iok_toestelcode`; D1.4 heeft ook geen R op `iok_toesteltype` en `iok_speelterrein`.
- D3.5 leest `account`, `contact`, `iok_speelterrein`, `iok_speeltoestel` en `iok_toestelcode`, terwijl de PDF volgens B57 enkel het dossier leest.
- D3.8 maakt een nieuw document, maar zet het vorige niet op Vervangen (geen U op `iok_document`).
- H3: zie punt 6.
- **Voorstel:** bijwerken in stap 6, samen met de punten die je aanvaardt.

---

## Bronnen Microsoft Learn

- Work with formula columns — https://learn.microsoft.com/en-us/power-apps/maker/data-platform/formula-columns
- Types of columns — https://learn.microsoft.com/en-us/power-apps/maker/data-platform/types-of-fields
- Define alternate keys to reference rows — https://learn.microsoft.com/en-us/power-apps/maker/data-platform/define-alternate-keys-reference-records
- Retrieve a table row using the Web API — https://learn.microsoft.com/en-us/power-apps/developer/data-platform/webapi/retrieve-entity-using-web-api
- Table relationships — https://learn.microsoft.com/en-us/power-apps/maker/data-platform/create-edit-entity-relationships
- Configure table relationship cascading behavior — https://learn.microsoft.com/en-us/power-apps/developer/data-platform/configure-entity-relationship-cascading-behavior
- Define custom state model transitions — https://learn.microsoft.com/en-us/power-apps/developer/data-platform/define-custom-state-model-transitions
- Types of tables (eigenaarschap) — https://learn.microsoft.com/en-us/power-apps/maker/data-platform/types-of-entities
- Security roles and privileges — https://learn.microsoft.com/en-us/power-platform/admin/security-roles-privileges
- Autonumber columns — https://learn.microsoft.com/en-us/power-apps/developer/data-platform/create-auto-number-attributes
- Behavior and format of the date and time column — https://learn.microsoft.com/en-us/power-apps/developer/data-platform/behavior-format-date-time-attribute
