# CRUD-matrix – IOK-datamodel v3

_Datum: 2026-11-13, bijgewerkt 2026-11-14 na stap 2 (velddekking), stap 3 (ontwerpvragen) en stap 6 (review). Stap 1 (maken). Bronnen: `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md` (finaal, incl. D4), `01_context/datamodel_v2/IOK_erd_v2.md` (13 tabellen), `01_context/bpmn/IOK_BPMN_leesversie.md`, `01_context/feedback/feedback_IOK_2026-11-13.md`, `BESLISSINGEN.md` (B01–B84), `02_werk/velddekking.md`, `02_werk/opdrachtbegrip.md`._

Doel: per BPMN-stap aantonen welke gegevens gelezen, aangemaakt, gewijzigd of gedeactiveerd worden, en zo de ontbrekende en overbodige tabellen vinden. **Nog geen Dataverse-ontwerp**: kolomnamen zijn werknamen (B01), geen definitieve types.

## Leeswijzer

- **C** = Create, **R** = Read, **U** = Update, **D** = Delete, **X** = deactiveren (status/state, geen delete), **·** = geen toegang in deze stap. **+** = twee bewerkingen in dezelfde stap (bv. `R+U`).
- **BPMN-taak** = de taaknaam letterlijk uit het finale BPMN. De ID's (`H1`, `D2.3`, …) zijn door ons toegekend in BPMN-volgorde; het BPMN-bestand zelf bevat geen taak-ID's.
- **Lane/Wie**: lane uit het BPMN en of een gebruiker dan wel het systeem (flow) de bewerking doet.
- **Kolomvolgorde**: stamgegevens → sjablonen → inspectie → communicatie → standaardtabellen.
- **Nieuw t.o.v. v2** (geen v2-tabel): `contact` (B16), `iok_standaardtekst` (vaste eis, B08/B18), `iok_maatregel` (B18), `iok_hicmeting` (B20), `iok_document (nieuw?)` (B11/B22), `iok_toestelcode` (B44), `iok_terreingroep` (B47), `iok_checklistonderdeel` en `iok_beoordeling_onderdeel` (B51). De overige kolommen komen uit v2 of zijn standaardtabellen (B02).

## Matrix

| ID | BPMN-taak | Lane | Wie | account | contact | iok_speelterrein | iok_terreingroep | iok_speeltoestel | iok_toestelcode | iok_toesteltype | iok_checklist | iok_checklistonderdeel | iok_controlepunt | iok_toesteltype_onderdeel | iok_standaardtekst | iok_inspectiedossier | iok_beoordeling | iok_beoordeling_onderdeel | iok_resultaat | iok_maatregel | iok_hicmeting | iok_foto | iok_rapportversie | iok_document (nieuw?) | systemuser | sharepointdocumentlocation | email | task | annotation | team | Opmerking |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| D1.1 | Bestuur, terrein en inspectiescope kiezen | Inspecteur | gebruiker | R | · | R | R | R | R | R | R | R | · | R | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | Scope = terrein + te controleren toestellen. Registratie van een nieuw terrein/toestel heeft geen eigen BPMN-stap → Ontbrekend 10, Q06. Toestellen terugvinden via elke code op een element (B44). Contact niet nodig om bestuur/terrein te kiezen (B37) → ·. Terrein eventueel zoeken via de terreingroep (B47). De inspecteur kiest hier ook de soort controle (jaarlijks / nieuw, B78). |
| D1.2 | Nieuw inspectiedossier met controledatum en uniek ID maken | Systeem | systeem | R | R | R | · | · | · | · | · | · | · | · | · | C | · | · | · | · | · | · | · | · | R | C | · | · | · | · | Dossiernummer + controledatum + status Concept (B17/B19); eigenaar = inspecteur (B13); archieflocatie in SharePoint wordt hier aangemaakt (B22). De kopiekolommen van bestuur en terrein worden hier gevuld (B57); de archieflocatie hangt aan het aanmaken van het record, via een flow (B60/B62). Leest `account` en `contact` voor de kopiekolommen (naam, contactpersoon, uitbateradres, B57/B78); vult `iok_soortcontrole`, `iok_inspecteurid` en de naamkopie (B73, B78); de flow zet `ownerid` op de inspecteur (B84). |
| D1.3 | Lege toepasselijke checklists klaarzetten | Systeem | systeem | · | · | R | · | R | R | R | R | R | R | R | · | R | R+C | C | · | · | · | R+C | · | · | · | · | · | · | · | · | Eén beoordeling voor het terrein + één per toestel, elk met de toepasselijke checklistversie (B21/B23/B26). Geen lege resultaatrijen vooraf (B40). Onderdelen: alle "altijd van toepassing" + die van het type (B51/B52); kopiekolommen van het toestel op de beoordeling gevuld (B57). Leest de codes voor de kopie van de toestelcode (B57). Herneemt de meest recente overzichtsfoto van elk toestel als nieuw `iok_foto` (B80): R op eerdere beoordelingen en foto's. Beoordelingsbasis blijft leeg tot D2.1 (B79). |
| D1.4 | Historiek als concept overnemen | Systeem | systeem | · | · | R | · | R | R | R | R | R | · | · | · | R | R+C | R+C | R+C | R+C | · | R+C | R | R | · | · | · | · | · | · | Alternatief voor D1.3: neemt de beoordelingen van het vorige dossier over als concept, inclusief resultaten en maatregelen. Een overgenomen antwoord is nog geen nieuwe inspectie (vaste eis); enkel bij "bruikbare historiek" (XOR in D1). Neemt ook de gebruikte onderdelen over (B51). **Herzien (B79/B80):** per toestel de meest recente afgeronde beoordeling van dat toestel, niet "het vorige dossier"; besluit, besluittekst en opmerking worden niet overgenomen; toestel zonder historiek = lege beoordeling zoals D1.3; kopiekolommen vers uit de stamgegevens (R op terrein, toestelcode, toesteltype); hernomen foto als nieuw `iok_foto`. |
| H1 | Terrein controleren en bevindingen registreren | Inspecteur | gebruiker | · | · | R | · | R | · | R | R | R | R | · | R | R+U | R+U | R | C+U | C+U | · | C | · | · | · | R | · | · | · | · | De terreinbeoordeling wordt in D1.3 of D1.4 klaargezet en hier ingevuld (B23); HIC enkel bij een toestel (B20). Status dossier → In uitvoering (B17). Resultaten/maatregelen: C bij een nieuwe vaststelling, U op een concept uit D1.4 (B28/B40). |
| D2.1 | Toestel, norm en beoordelingsbasis vaststellen | Inspecteur | gebruiker | · | · | · | · | R | R | R | R | R | · | R | · | R | R+U | R+C+D | · | · | · | C+U | · | · | · | R | · | · | · | · | × per toestel. Leest de archieflocatie van het dossier (D1.2). Norm/basis per beoordeling (B21); toestelfoto ook bij een conform toestel (B15, Q02). Inspecteur identificeert het toestel via de code op het element (B44). Inspecteur past de gekozen onderdelen aan, bv. welke skate-onderdelen aanwezig zijn (B51): C+D op de koppeling. Een onderdeel met resultaten kan niet weg (B84, regel 19). Hier wordt de beoordelingsbasis vastgesteld (B79). |
| D2.2 | Jaarlijks alle toepasselijke controlepunten beoordelen | Inspecteur | gebruiker | · | · | · | · | · | · | · | R | R | R | · | R | · | R | R | C+U | · | · | · | · | · | · | · | · | · | · | · | Eén opmerking per controlepunt; 1 NOK maakt het hoofdstuk NOK (vaste eis). Hoofdstukresultaat = resultaat op het hoofdstukcontrolepunt + enkel afwijkende punten (B40). **Herzien (B72):** bij de jaarlijkse controle is voor een toestel enkel het besluit verplicht; punten en hoofdstukken alleen bij een afwijking. |
| D2.3 | Indienststelling en plaatsing beoordelen | Inspecteur | gebruiker | · | · | · | · | · | · | · | R | R | R | · | R | · | R | R | C+U | · | · | · | · | · | · | · | · | · | · | · | Deel 2-checklists; combinatietoestel = meerdere checklists (vaste eis/B26). Hoofdstukresultaat = resultaat op het hoofdstukcontrolepunt + enkel afwijkende punten (B40). |
| D2.4 | Uitgebreide risicoanalyse uitvoeren | Inspecteur | gebruiker | · | · | · | · | · | · | · | R | R | R | · | R | · | R | R | C+U | · | · | · | · | · | · | · | · | · | · | · | Impact × kans × blootstelling vastleggen (legende C-verslag); de scoretabel zelf is Q08. Alle controlepunten verplicht (B40). |
| D2.5 | Norm, toelichting, foto's en risicobeoordeling vastleggen | Inspecteur | gebruiker | · | · | · | · | · | · | · | R | · | · | · | R | · | R | · | U | · | C | C | · | · | · | R | · | · | · | · | Meerdere foto's per gebrek (B15); HIC enkel bij niet-conforme valondergrond (B20, Q03). |
| D2.6 | Besluit en benodigde preventiemaatregelen vastleggen | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | R | · | U | · | R | C | · | · | · | · | · | · | · | · | · | · | Besluit = Conform/Niet conform (B18); maatregel hangt aan de beoordeling en optioneel aan één resultaat. Algemene opmerking per beoordeling in `iok_opmerking` (B42). Besluit kent ook **Niet beoordeeld** voor een verwijderd of onbruikbaar toestel (B71). Opmerking = vaststelling, maatregel = wat het bestuur moet doen (B84, regel 18). |
| D3.1 | Dossier en controledatum nakijken en afwerken | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | R+U | R+U | · | R+U+D | R+U+D | R+D | R+D | · | · | · | · | · | · | · | · | Laatste inhoudelijke correctie vóór generatie; controledatum is de versiesleutel (B06). Verwijderen van een verkeerde invoer kan zolang het dossier niet Afgerond is (B67). De D en de U kunnen enkel zolang het dossier actief is: synchrone controle (B74, B77). |
| D3.2 | Verplichte gegevens, risico's en foto's valideren | Systeem | systeem | R | R | R | · | R | · | · | R | R | R | · | · | R | R | R | R | R | R | R | · | · | · | · | · | · | · | · | Technische volledigheidscontrole; geen tweede menselijke goedkeuring (B05). Validatie "1 NOK = hoofdstuk NOK" via `iok_hoofdstuk` (B40/B43) en invulplicht per beoordelingsbasis: risicoanalyse = alle punten, indienststelling/jaarlijks = hoofdstukresultaat + afwijkende punten (B40). Contact: primaire contactpersoon aanwezig voor PDF en verzending (B37). **Herzien (B71/B72):** jaarlijks = enkel het besluit voor een toestel; Niet beoordeeld = geen invulplicht; NOK zonder maatregel = waarschuwing (B84). |
| D3.3 | Ontbrekende dossiergegevens aanvullen | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | U | U | · | U | U | U | C | · | · | · | · | · | · | · | · | Lus terug naar D3.2; fotogebrek wordt hier aangevuld (B15). |
| D3.4 | Samenvatting preventiemaatregelen voor terrein en toestellen samenstellen | Systeem | systeem | · | · | R | · | R | · | · | · | · | · | · | · | · | R | · | R | R | · | · | · | · | · | · | · | · | · | · | Enkel samenstellen; de PDF volgt in D3.5 (apart document, B11). |
| D3.5 | Rapport-PDF en preventiesamenvatting met controledatum genereren | Systeem | systeem | · | · | · | · | · | · | · | R | R | R | · | · | R | R | R | R | R | R | R | C | C | · | R+C | · | · | · | · | Twee documenten per versie (B11); versie start als Concept (B17); link naar SharePoint (B22). PDF: verantwoordelijke = bestuur (Account), primaire contactpersoon ernaast (B37; velddekking r.423); hoofdcode of codebereik uit `iok_toestelcode` (B44). PDF uit de kopiekolommen van het dossier, niet uit de stamgegevens (B57). Archieflocatie: C enkel als ze ontbreekt (B60). **Herzien (review punt 36):** geen R meer op `account`, `contact`, `iok_speelterrein`, `iok_speeltoestel` en `iok_toestelcode`: de PDF leest enkel het dossier (B57). Wel R op `iok_controlepunt`: de checklistteksten komen uit de versie (B19); die R ontbrak. |
| D3.6 | Generatiefout oplossen | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | R | R | · | R | · | · | · | · | Geen delete: een mislukte PDF blijft als spoor staan (B22/B06). |
| D3.7 | PDF en preventiesamenvatting inhoudelijk nakijken | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | · | R | · | R | R | · | · | R | R | · | R | · | · | · | · | Vergelijkt de PDF met de dossiergegevens vóór verzending (B05). |
| D3.8 | PDF corrigeren of na dossiercorrectie opnieuw maken | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | U | U | · | U | U | · | · | R | C+U | · | · | · | · | · | · | Binnen dezelfde versie zolang niet verzonden; na verzending nieuwe versie (B12/V6, Q04). Het vorige document van dezelfde versie → Vervangen (U); `iok_handmatigaangepast` = ja als de inspecteur de PDF zelf aanpaste (B83). |
| D3.9 | Definitieve PDF, controledatum en historische dossiergegevens bewaren | Systeem | systeem | · | · | · | · | · | · | · | R | R | R | · | · | U | R | R | R | R | R | R | U | U | · | R | · | · | · | · | Status Definitief + bewaren in de archieflocatie die D1.2 heeft aangemaakt (B17/B22). Bevriezen van de dossiergegevens = Q10. Geen C: bevriezen gebeurt met kopiekolommen bij aanmaak; hier wordt alles alleen-lezen (B57). Voert de validatie van D3.2 opnieuw uit vóór het dossier Afgerond wordt (B84, regel 19): R op de beoordelingsgegevens. Daarna gaat het slot dicht (B74). |
| D3.10 | Bewaarfout oplossen en definitieve versie behouden | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | R | R | · | R | · | · | · | · | Opnieuw bewaren, nooit overschrijven of verwijderen (B06). |
| H2 | Inspecteur verstuurt definitieve PDF(s) handmatig | Inspecteur | gebruiker | R | R | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | R | R | · | R | · | · | · | · | Versturen gebeurt buiten Dataverse (eigen mailclient, B05). Geen schrijfactie: de status volgt in H4. Contact = e-mailadres van de primaire contactpersoon van het bestuur; verantwoordelijke zelf = Account (B37). |
| H3 | Inspecteur lost verzendprobleem op en controleert status | Inspecteur | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | R | R | · | · | · | · | · | · | Leest de bestaande verzendstatus om dubbels te vermijden (B05). Log van verzendpogingen ontbreekt → Ontbrekend 6. `iok_verzendpogingen` en `iok_laatstepogingop` zijn geschrapt (B83): H3 blijft enkel R. |
| H4 | Verzendstatus registreren | Systeem | systeem | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | R+U | · | · | · | · | · | · | · | Verzendstatus hoort bij de versie, niet bij het dossier (B17); enkel na bevestiging "verzonden" (XOR in hoofdproces). |
| D4.1 | Stamgegevens en vaste teksten bijwerken | Bevoegde beheerder | gebruiker | C+U | C+U | C+U | C+U | C+U+X | C+U | C+U | C+U | C+U+D | C+U+D | C+U | C+U | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | Enige rol die schrijft (B08); wijziging zonder terugwerkende kracht → D4.2 (B07). X = toestel buiten gebruik (B24). Wie terreinen/toestellen registreert = Q06. Codes van een toestel (ook de hoofdcode) in `iok_toestelcode`, uniek over alle besturen (B44/B25). `iok_hoofdstuk` op het controlepunt wordt bij het aanmaken van de checklistversie gevuld (B43). D op onderdelen en controlepunten enkel zolang de checklist in Concept staat, van onder naar boven (B75). |
| D4.2 | Nieuwe stamgegevensversie vastleggen; historische inspecties behouden | Systeem | systeem | · | · | · | · | · | · | · | C+X | C | C | C+U | U | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | Oude versie blijft bestaan (B19); bestaande dossiers blijven naar hun versie verwijzen (B14). N:N type→checklist volgt de nieuwe checklistversie. Enkel checklist, onderdelen en controlepunten krijgen versies; toesteltype en standaardtekst wijzigen ter plaatse in D4.1 (B58/B59). Standaardteksten verhuizen mee naar de nieuwe controlepunten (B65). **Herzien (B81):** enkel de checklist krijgt Vervangen (X); onderdelen en controlepunten blijven actief. Activeren kan pas als geen open dossier op de oude versie staat. |
| D4.3 | Preventiemaatregelen en tekortkomingen per bestuur samenvatten | Systeem | systeem | R | · | R | R | R | · | · | · | · | · | · | · | R | R | · | R | R | · | · | · | · | · | · | · | · | · | · | View/export, geen eigen overzichtstabel (B10). |
| D4.4 | Periode kiezen: laatste 3 maanden of van begin- tot einddatum | Inspecteur / bevoegde IOK-medewerker | gebruiker | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | · | Filterparameter, geen tabel (zie Ontbrekend 12). |
| D4.5 | Uitgevoerde controles en historische eenheden binnen gekozen periode naar Excel exporteren | Systeem | systeem | R | · | R | R | R | · | · | · | · | · | · | · | R | R | · | · | · | · | · | · | · | R | · | · | · | · | · | Export, geen tabel (B10). Eenheden komen bevroren uit het dossier (B14), niet uit de actuele stamgegevens (B07). Eenheden = som van de bevroren eenheden op de beoordelingen (B61). Of een beoordeling met besluit Niet beoordeeld meetelt in de eenheden: Q26. |

## Samenvatting per tabel

| Tabel | C | U | X | R | Oordeel |
|---|---|---|---|---|---|
| account | D4.1 | D4.1 | – | D1.1, D1.2, D3.2, H2, D4.3, D4.5 | Nodig (B16). Enige schrijfmoment in D4.1, want besturen aanmaken is geen BPMN-stap (Q01/Q06). |
| contact | D4.1 | D4.1 | – | D1.2, D3.2, H2 | Nodig (B16). Zelfde opmerking: contactbeheer valt buiten het proces. Gelezen voor de PDF (primaire contactpersoon naast het bestuur) en de verzending (e-mailadres), niet als verantwoordelijke (B37). |
| iok_speelterrein | D4.1 | D4.1 | – | D1.1, D1.2, D1.3, D1.4, H1, D3.2, D3.4, D4.3, D4.5 | Nodig. "Actief" wordt state (X), geen eigen kolom. |
| iok_terreingroep | D4.1 | D4.1 | – | D1.1, D4.3, D4.5 | Nieuw (B47). Optionele groepering boven het terrein; geen adres, geen dossier (B50). |
| iok_speeltoestel | D4.1 | D4.1 | D4.1 | D1.1, D1.3, D1.4, H1, D2.1, D3.2, D3.4, D4.3, D4.5 | Nodig. X = buiten gebruik stellen (B24), geen delete (B12/V4). |
| iok_toestelcode | D4.1 | D4.1 | – | D1.1, D1.3, D1.4, D2.1 | Nieuw (B44). Alle codes van een toestel, ook de hoofdcode; alternatieve sleutel op de code (uniek over alle besturen, B25). Enkel de bevoegde beheerder schrijft (B08). |
| iok_toesteltype | D4.1 | D4.1 | – | D1.1, D1.3, D1.4, H1, D2.1 | Nodig; **niet geversioneerd** (B58, herziet B26): typenaam en eenheden worden per beoordeling gekopieerd. |
| iok_checklist | D4.1, D4.2 | D4.1 | D4.2 | D1.1, D1.3, D1.4, H1, D2.1, D2.2, D2.3, D2.4, D2.5, D3.2, D3.5, D3.9 | Nodig; versie is de bevriezingssleutel (B19). |
| iok_checklistonderdeel | D4.1, D4.2 | D4.1 | – | D1.1, D1.3, D1.4, H1, D2.1, D2.2, D2.3, D2.4, D3.2, D3.5, D3.9 | Nieuw (B51). Deel 1, Deel 2-bladen, skate-onderdelen, terrein; versie volgt de checklist (B19). |
| iok_controlepunt | D4.1, D4.2 | D4.1 | – | D1.3, H1, D2.2, D2.3, D2.4, D3.2, D3.5, D3.9 | Nodig. Hiërarchie hoofdstuk → controlepunt (v2 `ouder_id`, vaste eis "1 NOK = hoofdstuk NOK"). |
| iok_toesteltype_onderdeel | D4.1, D4.2 | D4.1, D4.2 | – | D1.1, D1.3, D2.1 | Nodig. N:N type ↔ onderdeel, 0..N (B26, B51, B52); vroeger `iok_type_checklist`. |
| iok_standaardtekst | D4.1 | D4.1, D4.2 | – | H1, D2.2, D2.3, D2.4, D2.5, D2.6 | Nieuw. Vaste eis "besluiten en standaardzinnen komen uit een tabel" + B08/B18. Niet geversioneerd: de gekozen zin wordt als tekst gekopieerd (B59). |
| iok_inspectiedossier | D1.2 | H1, D3.1, D3.3, D3.8, D3.9 | – | D1.3, D1.4, H1, D2.1, D3.1, D3.2, D3.5, D4.3, D4.5 | Nodig. Vervangt v2 CONTROLE; uniek per terrein + controledatum (B19). |
| iok_beoordeling | D1.3, D1.4 | H1, D2.1, D2.6, D3.1, D3.3, D3.8 | – | D1.3, D1.4, H1, D2.1, D2.2, D2.3, D2.4, D2.5, D3.1, D3.2, D3.4, D3.5, D3.7, D3.9, D4.3, D4.5 | Nodig. Draagt norm, beoordelingsbasis en besluit (B21/B18); terrein en toestel delen de structuur (B23). |
| iok_beoordeling_onderdeel | D1.3, D1.4, D2.1 | – | – | D1.4, H1, D2.1, D2.2, D2.3, D2.4, D3.2, D3.5, D3.9 | Nieuw (B51). Welke onderdelen in deze beoordeling gebruikt zijn; D in D2.1 als de inspecteur een onderdeel weghaalt. |
| iok_resultaat | D1.4, H1, D2.2, D2.3, D2.4 | H1, D2.2, D2.3, D2.4, D2.5, D3.1, D3.3, D3.8 | – | D1.4, D2.6, D3.1, D3.2, D3.4, D3.5, D3.7, D3.9, D4.3 | Nodig. Antwoord per controlepunt + risicoscore; de scoretabel zelf is Q08. |
| iok_maatregel | D1.4, H1, D2.6 | H1, D3.1, D3.3, D3.8 | – | D1.4, D3.1, D3.2, D3.4, D3.5, D3.7, D3.9, D4.3 | Nieuw (B18). Zonder opvolgingsstatus; het bestuur beslist zelf. |
| iok_hicmeting | D2.5 | D3.3 | – | D3.1, D3.2, D3.5, D3.9 | Nieuw (B20). Optioneel, enkel bij niet-conforme valondergrond (Q03). |
| iok_foto | D1.3, D1.4, H1, D2.1, D2.5, D3.3 | D2.1 | – | D1.3, D1.4, D3.1, D3.2, D3.5, D3.9 | Nodig, maar niet meer alleen aan een resultaat (zie Ontbrekend 4). Bestand staat in SharePoint (B22). |
| iok_rapportversie | D3.5 | D3.9, H4 | – | D1.4, D3.6, D3.7, D3.8, D3.10, H2, H3, H4 | Nodig. Statusmodel Concept → Definitief → Verzonden → Vervangen (B17). |
| iok_document (nieuw?) | D3.5, D3.8 | D3.8, D3.9 | – | D1.4, D3.6, D3.7, D3.10, H2, H3 | Nieuw: vervangt v2 `CONTROLEVERSIE.pdf_url` door 1 record per PDF (B11/B22). |
| systemuser | – | – | – | D1.2, D4.5 | Standaardtabel; gebruikers worden in het platform beheerd, niet in dit proces (B02/B13). |
| sharepointdocumentlocation | D1.2, D3.5 | – | – | H1, D2.1, D2.5, D3.5, D3.6, D3.7, D3.9, D3.10, H2 | Standaardtabel; één archieflocatie per dossier, aangemaakt samen met het dossier (B03/B22). Aangemaakt door een flow bij het aanmaken van het dossier; D3.5 is het vangnet (B60/B62). |
| email | – | – | – | – | **Niet gebruikt**: de inspecteur mailt zelf (B05) en de verzendstatus is een veld op de versie. |
| task | – | – | – | – | **Niet gebruikt**: geen planning of herstelopvolging in scope (B18, projectopdracht). |
| annotation | – | – | – | – | **Niet gebruikt**: vrije tekst zit in resultaat, maatregel of standaardtekst. |
| team | – | – | – | – | **Niet gebruikt**: geen business units in v3 (B13). |

## Ontbrekend

Per bevinding: wat ontbreekt, in welke stap het nodig is en waarop het steunt.

1. **Maatregelentabel** – D2.6 en D3.4/D4.3 lezen maatregelen, maar v2 heeft geen tabel die een preventiemaatregel opslaat (v2 kent enkel vrije tekst in RESULTAAT). Nodig: `iok_maatregel` (beoordeling, optioneel één resultaat, tekst, bron standaardtekst of vrij). Bron: B18; vaste eis "preventiemaatregelen per bestuur"; BPMN D2 "Besluit en benodigde preventiemaatregelen vastleggen".
2. **Standaardtekstentabel** – D2.5/D2.6 lezen vaste zinnen; v2 heeft geen STANDaardTEKST-tabel (de startprompt noemde ze, het diagram niet). Nodig: `iok_standaardtekst`, versieerbaar en enkel door de bevoegde beheerder te wijzigen. Bron: vaste eis; B08; B18; v2-opmerking in `IOK_erd_v2.md` r.154.
3. **HIC-meting** – D2.5 registreert een meting; v2 heeft geen tabel. Nodig: `iok_hicmeting` (volgnummer, Peak/G, HIC, valhoogte, datum/tijd) aan de toestelbeoordeling. Bron: B20; legende in `01_context/docs/C_2026 - Jaarlijkse controle De Bogaard (algemeen).md` r.8-17; vaste eis HIC.
4. **Foto's breder dan één resultaat** – v2 `FOTO` hangt verplicht aan `RESULTAAT` (1 resultaat), en `BEOORDELING.overzichtsfoto_url` is één URL. D2.1 heeft een toestelfoto nodig ook als het toestel conform is, en D2.5 meerdere foto's per gebrek. Nodig: `iok_foto` met koppeling naar beoordeling (overzichtsfoto) én optioneel naar resultaat, meerdere per gebrek. Bron: B15; vaste eis foto's; `C_2026` (foto bij elk conform toestel).
5. **Dossiernummer** – v2 `CONTROLE` heeft enkel een technische sleutel; D1.2 maakt een "uniek ID" en D4/D3 verwijzen ernaar in het verslag. Nodig: automatisch dossiernummer op `iok_inspectiedossier`. Bron: B19; BPMN D1 "Nieuw inspectiedossier met controledatum en uniek ID maken".
6. **Twee PDF's per versie en de verzendpoging** – v2 `CONTROLEVERSIE` heeft één `pdf_url`; B11 vraagt een rapport-PDF én een aparte preventiesamenvatting, en H3 moet de laatste poging kunnen controleren. Nodig: `iok_document` (documenttype, versie, controledatum, link). De aanduiding van verzendpogingen is in stap 6 geschrapt: verzenden gebeurt buiten Dataverse en geen stap schrijft ze (B83). Bron: B11; B22; B05; BPMN H3.
7. **Norm en beoordelingsbasis per beoordeling** – v2 `BEOORDELING` heeft enkel `soort` en `overzichtsfoto_url`: geen norm, geen basis, geen verwijzing naar de gebruikte checklistversie. Nodig: norm (EN 1176/EN 14974), basis (jaarlijks/indienststelling/risicoanalyse) en FK naar `iok_checklist`. Bron: B21; B14; BPMN D2 "Toestel, norm en beoordelingsbasis vaststellen"; D1.3 "Lege toepasselijke checklists klaarzetten".
8. **Checklistversie per dossier/beoordeling** – v2 legt de checklist alleen via het toestel vast (`TOESTEL_CHECKLIST`) en niet per controle; D1.3 zet de versie klaar en D3.9 bewaart ze historisch. Nodig: FK van beoordeling naar checklistversie, plus de N:N op type in plaats van op toestel. Bron: B19; B26; B14.
9. **Bevroren dossiergegevens** – D3.9 "historische dossiergegevens bewaren" kan vandaag geen C in de matrix krijgen: v2 heeft geen kopie- of snapshotstructuur. Dit is de vraag of bevriezen door kopiëren dan wel door onveranderlijke versies gebeurt → **Q10**. Bron: B14; B19; B06.
10. **Registratie van bestuur, contact, terrein en toestel** – geen enkele BPMN-stap maakt deze records aan; D1.1 vooronderstelt dat ze bestaan. In de matrix staan ze daarom enkel bij D4.1 (stamgegevens). Te bevestigen: mag de bevoegde beheerder dat, of de inspecteur? → Q06 (en Q01 voor private uitbaters). Bron: B08; B13; B16; BPMN D1.1/D4.1.
11. **Risicoscore** – v2 heeft `impact`, `kans` en `blootstelling` op RESULTAAT. Die zijn **niet overbodig** (D2.4 "Uitgebreide risicoanalyse uitvoeren" en D2.5 "risicobeoordeling vastleggen"), maar de scoretabel en de drempels zelf zijn nog niet bevestigd. → Q08. Bron: BPMN D2; legende in `C_2026` r.18-41.
12. **Periodekeuze financieel overzicht** – D4.4 kiest een periode, maar er is geen tabel of veld waar die keuze wordt bewaard. Voor v3 is dat aanvaardbaar (parameter van de export); enkel bij een audit trail is een log nodig. Bron: B10; BPMN D4.4; feedback IOK 13/11 ("Periode selecteren").
13. **Conformiteitsdocument / attest** – v2 `SPEELTOESTEL.attest` is één tekstveld; D2.1 moet onduidelijke conformiteitsinformatie kunnen beoordelen (O6) en V8 vraagt conformiteitsdocumenten. Nu buiten scope, maar mogelijk een ontbrekende tabel. → Q08. Bron: `01_context/bpmn/IOK_BPMN_leesversie.md` r.42 (O6), r.44.
14. **Fout dossier annuleren of verwijderen** – geen BPMN-stap. Een dossier met het verkeerde terrein of de verkeerde datum houdt de sleutel terrein + controledatum bezet. Nodig: statusreden Geannuleerd (dossier met rapportversie) en verwijderen door de beheerder (dossier zonder rapportversie); dat is de enige D op `iok_inspectiedossier` en staat niet in de matrix omdat er geen stap voor bestaat. Bron: B78; review punt 14.

## Overbodig

1. **`email`** – geen enkele stap gebruikt ze: de inspecteur verstuurt zelf met zijn eigen mailclient en het systeem registreert enkel de status (B05, H2/H4). De standaardtabel blijft bestaan in Dataverse, maar hoort niet in het model.
2. **`task`** – geen planning of herstelopvolging in scope (B18; projectopdracht §5). De BPMN bevat geen taak- of herinneringsstap (B04 heeft offline/planning geschrapt).
3. **`annotation`** – vrije tekst zit in `iok_resultaat.opmerking`, `iok_maatregel.tekst` of `iok_standaardtekst`; een aparte notitie heeft geen processtap.
4. **`team`** – geen business units in v3 (B13); scoping gebeurt via de eigenaar per record.
5. **v2 `INSPECTEUR`** – vervalt als eigen tabel: `systemuser` + de twee beveiligingsrollen (B13). `is_admin` is een rol, geen kolom (B08).
6. **v2 `BESTUUR`** – vervalt: Account + `iok_soort` (B16). De adresvelden en contactvelden gaan naar Account/Contact.
7. **v2 `CONTROLEVERSIE.pdf_url`** – vervalt zodra `iok_document` bestaat (twee PDF's per versie, B11/B22).
8. **v2 `BEOORDELING.overzichtsfoto_url`** – vervalt: wordt een `iok_foto`-record met fotoType "overzicht" (B15).
9. **v2 `SPEELTERREIN.actief`** – wordt de state van het record (X), geen eigen kolom.
10. **v2 `TOESTEL_CHECKLIST` op toestel** – vervalt in die vorm: N:N staat op het toesteltype (B26) en de gebruikte versie wordt per dossier bevroren (B14).

## Wees

- **`contact`** wordt gelezen (D3.2, D3.5, H2: primaire contactpersoon voor PDF en verzending, B37) en enkel in D4.1 aangemaakt. Zonder die aanname is het een leestabel zonder bron → bevestigen in Q06.
- **`account`** idem: C+U in D4.1, daarbuiten enkel R. Bewust, want besturen worden buiten het inspectieproces beheerd (B02/B16).
- **`iok_speelterrein`** en **`iok_speeltoestel`** zijn alleen "wees" als D4.1 ze niet mag aanmaken; in deze matrix krijgen ze daar C+U (en X voor buiten gebruik).
- Geen enkele tabel is uitsluitend C of uitsluitend R: elke gebruikte tabel wordt minstens één keer gelezen én geschreven, behalve de vier standaardtabellen onder "Overbodig" en `systemuser` (platformtabel, B02/B13).

## Open

| # | Open punt | Waarvan afhankelijk | Status |
|---|---|---|---|
| 1 | Bevriezen van dossiergegevens: kopiëren of onveranderlijke versies? (bepaalt of D3.9 een C op snapshot-tabellen krijgt) | **Q10** | nieuw |
| 2 | Worden lege `iok_resultaat`-rijen al in D1.3 aangemaakt of pas bij het beantwoorden in D2.x? | **Q11** | Dries – stap 3 |
| 3 | Eenheden per bestuur: **berekend in de export** uit terreinen/toestellen, of een **afgesproken getal per bestuur** (bv. `account.iok_eenheden`)? | **Q12** | nieuw |
| 4 | Risicofactoren, scoretabel en drempels (impact/kans/blootstelling) wel of niet in het model? | Q08 | open |
| 5 | Conformiteitsdocumenten en het omgaan met een ontbrekend attest (O6, V8) | Q08 | open |
| 6 | Wie registreert een nieuw terrein, toestel, bestuur of contact? | Q06 (+ Q01) | open |
| 7 | Private uitbaters naast gemeente/OCMW: volstaat `iok_soort` = "Andere"? | Q01 | open |
| 8 | HIC verplicht of optioneel, en welke drempels? (bepaalt of D2.5 een validatie krijgt) | Q03 | open |
| 9 | Correctie na verzending = altijd nieuwe versie met nieuwe verzending? (D3.8/H4) | Q04 | open |
| 10 | Bewaartermijn van verslagen, PDF's en foto's (D3.9/D3.10) | Q05 | open |
| 11 | Eisen van de lector aan het Dataverse-model (stap 5) | Q09 | wacht op `01_context/cursus/` |

## Wijzigingen na stap 2 (2026-11-14)

Bijgewerkt in één keer na de velddekking (HANDOVER-taak "einde stap 2"); samenvatting per tabel opnieuw afgeleid en gecontroleerd: 24 tabellen, 0 verschillen.

| # | Wijziging | Stap(pen) | Grond |
|---|---|---|---|
| 1 | Nieuwe kolom `iok_toestelcode`: C+U in D4.1, R in D1.1, D2.1, D3.5 | D1.1, D2.1, D3.5, D4.1 | B44 |
| 2 | `contact` niet meer gelezen in D1.1; in D3.2, D3.5, H2 blijft R, met als reden de primaire contactpersoon (PDF, e-mailadres), niet de verantwoordelijke | D1.1, D3.2, D3.5, H2 | B37; velddekking r.423 |
| 3 | D3.2 leest `iok_controlepunt` (R) voor de validatie "1 NOK = hoofdstuk NOK" via `iok_hoofdstuk` en de invulplicht per beoordelingsbasis | D3.2 | B40, B43 |
| 4 | H1: `iok_resultaat` en `iok_maatregel` C → C+U (concept uit D1.4 aanpassen) | H1 | B28, B40 |
| 5 | Opmerkingen aangevuld: geen lege resultaatrijen (D1.3), hoofdstukresultaat + afwijkende punten (D2.2/D2.3), alle punten verplicht (D2.4), `iok_opmerking` op de beoordeling (D2.6), `iok_hoofdstuk` gevuld bij aanmaak checklistversie (D4.1) | D1.3, D2.2–D2.4, D2.6, D4.1 | B40, B42, B43 |

Niet in de matrix (geen CRUD-effect): B41 (datum onderhoud vervalt), B45 (risicoscore/HIC-drempels).

## Wijzigingen na stap 3 (2026-11-14)

Samenvatting per tabel opnieuw afgeleid uit de matrix: 27 tabellen.

| # | Wijziging | Stap(pen) | Grond |
|---|---|---|---|
| 1 | Nieuwe kolom `iok_terreingroep`: C+U in D4.1, R in D1.1, D4.3, D4.5 | D1.1, D4.1, D4.3, D4.5 | B47, B50 |
| 2 | Nieuwe kolom `iok_checklistonderdeel`: C+U in D4.1, C+X in D4.2, R waar controlepunten of onderdelen gelezen worden | D1.1–D2.4, D3.2, D3.5, D4.1, D4.2 | B51, B52 |
| 3 | `iok_type_checklist` heet nu `iok_toesteltype_onderdeel` | – | B51 |
| 4 | Nieuwe kolom `iok_beoordeling_onderdeel`: C in D1.3/D1.4, C+D in D2.1, R in de beoordelingsstappen | D1.3, D1.4, H1, D2.1–D2.4, D3.2, D3.5 | B51 |
| 5 | D4.2: geen C+X meer op `iok_toesteltype` en `iok_standaardtekst` | D4.2 | B58, B59 |
| 6 | D3.5: `sharepointdocumentlocation` R → R+C (enkel als de locatie ontbreekt) | D3.5 | B60, B62 |
| 7 | D3.9 blijft zonder C: bevriezen via kopiekolommen bij aanmaak | D1.2–D1.4, D3.5, D3.9 | B57 |

"Ontbrekend 9" (bevroren dossiergegevens) en "Open 1–3" (Q10, Q11, Q12) zijn hiermee afgehandeld: zie B57, B40 en B61.

## Wijzigingen tijdens stap 4 (2026-11-14)

| # | Wijziging | Stap | Grond |
|---|---|---|---|
| 1 | `iok_type_onderdeel` heet definitief `iok_toesteltype_onderdeel` | – | B63 |
| 2 | D3.1: D op `iok_resultaat`, `iok_maatregel`, `iok_hicmeting`, `iok_foto` (eerste en enige D in de matrix, naast de koppeling in D2.1) | D3.1 | B67 |
| 3 | D4.2: U op `iok_standaardtekst` (omhangen naar de nieuwe controlepunten) | D4.2 | B65 |

De samenvatting per tabel heeft geen D-kolom; de D's staan enkel in de matrix en hierboven.

## Wijzigingen in stap 6 (2026-11-14)

Review punt 36 en de gevolgen van B70–B84. De samenvatting per tabel is opnieuw afgeleid uit de matrix (met een script; vóór de wijzigingen kwam ze exact overeen met de matrix).

| # | Wijziging | Stap(pen) | Grond |
|---|---|---|---|
| 1 | D1.2 leest `account` en `contact` (kopiekolommen, uitbateradres) en vult soort controle en inspecteur | D1.2 | punt 36; B57, B73, B78 |
| 2 | D1.3 en D1.4 lezen `iok_toestelcode`; D1.4 leest ook `iok_toesteltype` en `iok_speelterrein` | D1.3, D1.4 | punt 36; B57 |
| 3 | D1.3 en D1.4 maken een `iok_foto` aan voor de hernomen overzichtsfoto (· → R+C, R → R+C); D1.3 leest daarvoor eerdere beoordelingen (C → R+C) ; D2.1 zet bij een nieuwe overzichtsfoto de overgenomen foto op `iok_inverslag` = nee (C → C+U) | D1.3, D1.4, D2.1 | B80 |
| 4 | D1.4 neemt per toestel de meest recente afgeronde beoordeling over; besluit, besluittekst en opmerking niet | D1.4 | B79, B80 |
| 5 | D3.5 leest geen stamgegevens meer (`account`, `contact`, `iok_speelterrein`, `iok_speeltoestel`, `iok_toestelcode`: R → ·) | D3.5 | punt 36; B57 |
| 6 | D3.5 leest `iok_controlepunt` (· → R): de checklistteksten in de PDF. **Stond niet in de review**; zonder die R kan de PDF de vragen niet drukken | D3.5 | B19 |
| 7 | D3.8 zet het vorige document op Vervangen (C → C+U) | D3.8 | punt 36; B83 |
| 8 | D3.9 voert de validatie opnieuw uit: R op checklist, onderdeel, controlepunt, beoordeling, koppeling, resultaat, maatregel en HIC-meting | D3.9 | B84 (punt 15) |
| 9 | D4.1: D op `iok_checklistonderdeel` en `iok_controlepunt` (enkel in Concept) | D4.1 | B75 |
| 10 | D4.2: onderdelen en controlepunten worden niet meer gedeactiveerd (C+X → C) | D4.2 | B81 (punt 34) |
| 11 | H3 blijft R; de kolommen voor verzendpogingen zijn geschrapt | H3 | B83 (punt 6) |
| 12 | Nieuw "Ontbrekend 14": annuleren of verwijderen van een fout dossier heeft geen BPMN-stap | – | B78 (punt 14) |
| 13 | Opmerkingen aangevuld bij D1.1, D2.1, D2.2, D2.6, D3.1, D3.2, D4.5 (soort controle, beoordelingsbasis, invulplicht jaarlijks, Niet beoordeeld, slot, Q26) | – | B71, B72, B74, B78, B79 |

De D's staan enkel in de matrix: D2.1 (koppeling), D3.1 (resultaat, maatregel, HIC-meting, foto) en D4.1 (onderdeel, controlepunt). Geen nieuwe tabellen: de matrix telt nog altijd 23 modeltabellen + de vier ongebruikte standaardtabellen.
