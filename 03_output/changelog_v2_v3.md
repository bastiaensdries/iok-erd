# Changelog datamodel v2 → v3

_Stap 6, 2026-11-14. Vertrekpunt: `01_context/datamodel_v2/IOK_erd_v2.md` (13 tabellen, 15 relaties, relationele notatie). Resultaat: `03_output/datamodel_v3.md` (21 tabellen + 2 native N:N, 35 relaties 1:N), `03_output/spec.yaml`, `03_output/ERD_v3.md`, `03_output/IOK_erd_v3.drawio`. Elke wijziging verwijst naar een beslissing in `BESLISSINGEN.md`. Er is niets gebouwd in Dataverse._

## 1. In het kort

| | v2 | v3 |
|---|---|---|
| Notatie | relationeel (INT-sleutels, VARCHAR) | Dataverse: schemanamen met `iok_`, kolomtypes, lookups (B01) |
| Tabellen | 13 eigen | 4 standaard + 17 eigen + 2 native N:N (B02) |
| Relaties | 15 | 35 × 1:N met verwijdergedrag, 2 × N:N |
| Uniekheid | enkel `INSPECTEUR.email` | 13 alternatieve sleutels |
| Status | tekstkolommen `status`, `actief` | statusredenen van Dataverse (B17, B24, B57, B69) |
| Historiek | niet voorzien | kopiekolommen + onveranderlijke checklistversies + slot na Afgerond (B57, B74) |
| Verslag | één `pdf_url` per versie | rapportversie + twee documenten per versie, PDF's in SharePoint (B11, B22) |
| Maatregelen, standaardzinnen, HIC | geen tabel | `iok_maatregel`, `iok_standaardtekst`, `iok_hicmeting` (B18, B20, B35) |
| Eigenaarschap en rollen | `INSPECTEUR.is_admin` | twee beveiligingsrollen, eigenaarschap per tabel (B13, B63) |

## 2. Tabel per tabel

| v2 | v3 | Wat verandert | Beslissing |
|---|---|---|---|
| BESTUUR | `account` + `contact` | standaardtabellen; eigen kolom `iok_soort` (Gemeente/OCMW/Andere); contactvelden worden Contact-records (1..N, één primair); `gemeente` is geen aparte kolom meer | B02, B16, B37 |
| INSPECTEUR | `systemuser` | geen eigen tabel; `is_admin` wordt de rol Bevoegde beheerder; het dossier krijgt `iok_inspecteurid` + naamkopie | B13, B73 |
| SPEELTERREIN | `iok_speelterrein` | `code` verplicht en uniek (sleutel); nieuw: uitbater (lookup naar Account), terreingroep, `iok_legacyid`; `actief` wordt de status; `eenheden` optioneel | B25, B46–B49, B37, B61 |
| – | `iok_terreingroep` | nieuw: optionele groepering boven het terrein, zonder adres of dossier | B47, B50, B56 |
| SPEELTOESTEL | `iok_speeltoestel` | `toezicht` vervalt (staat op het terrein); `status` wordt statusreden In gebruik / Buiten gebruik; `serienummer` blijft; nieuw: `iok_codeweergave`; uniekheid van de code verhuist naar `iok_toestelcode` | B24, B33, B44, B70, B84 |
| – | `iok_toestelcode` | nieuw: alle codes van een toestel (ook de hoofdcode), elk uniek over alle besturen | B44, B48 |
| TOESTELTYPE | `iok_toesteltype` | `categorie` wordt een keuzelijst (16 waarden); nieuw: standaardnorm; naam is sleutel; niet geversioneerd | B26, B34, B58 |
| CHECKLIST | `iok_checklist` + `iok_checklistonderdeel` | de checklist is het geheel met versie en statusreden Concept / Actief / Vervangen; `deel` wordt de tabel onderdeel (Deel 1, Schommels, Curbs, …) met "altijd van toepassing"; `voor` wordt `iok_soort` | B19, B51, B52, B57 |
| CONTROLEPUNT | `iok_controlepunt` | hangt aan een onderdeel in plaats van aan de checklist; nieuw: `iok_hoofdstukid`, toelichting (normwaarden), "NOK bepaalt hoofdstuk"; tekst 500 → 2000 | B43, B51, B53, B55 |
| TOESTEL_CHECKLIST | `iok_toesteltype_onderdeel` (N:N) | de koppeling staat op het **type** en wijst naar een **onderdeel**, niet meer toestel ↔ checklist; 0..N | B26, B51, B52 |
| – | `iok_beoordeling_onderdeel` (N:N) | nieuw: welke onderdelen in deze beoordeling gebruikt zijn (bevriezing per dossier) | B51 |
| – | `iok_standaardtekst` | nieuw: standaardzinnen voor opmerkingen, maatregelen en besluiten; de gekozen zin wordt gekopieerd | B35, B59, B65, B81 |
| CONTROLE | `iok_inspectiedossier` | automatisch dossiernummer; uniek per terrein + controledatum; statusredenen Concept / In uitvoering / Afgerond / Geannuleerd; soort controle; kopiekolommen van bestuur, contact, uitbater, terrein; algemeen besluit | B11, B17, B19, B57, B68, B78 |
| BEOORDELING | `iok_beoordeling` | nieuw: checklistversie, norm, beoordelingsbasis, besluit (met Niet beoordeeld) en besluittekst, opmerking, volgorde, bronbeoordeling, kopiekolommen van het toestel (o.a. eenheden); `overzichtsfoto_url` vervalt (wordt een `iok_foto`) | B21, B23, B42, B57, B66, B68, B71, B79 |
| RESULTAAT | `iok_resultaat` | `status` wordt keuzelijst OK / NOK / nvt en is optioneel; geen lege rijen vooraf; risicoscore en -klasse als formulekolom; herkomst standaardzin; `iok_isovergenomen`; sleutel beoordeling + controlepunt | B36, B40, B45, B59, B64, B66, B82 |
| – | `iok_maatregel` | nieuw: preventiemaatregel aan de beoordeling, optioneel aan één resultaat; geen opvolgingsstatus | B18, B59 |
| – | `iok_hicmeting` | nieuw: HIC-metingen per toestelbeoordeling | B20, B45 |
| FOTO | `iok_foto` | hangt aan de beoordeling, optioneel aan een resultaat (v2: verplicht aan een resultaat); soort Overzicht / Gebrek; "in verslag"; hernomen foto herkenbaar; bestand in SharePoint | B15, B22, B80 |
| CONTROLEVERSIE | `iok_rapportversie` + `iok_document` | statusredenen Concept / Definitief / Verzonden / Vervangen; `pdf_url` wordt één `iok_document` per PDF (rapport en preventiesamenvatting) | B06, B11, B12, B17, B22, B69, B83 |
| – | `sharepointdocumentlocation` | standaardtabel: één archiefmap per dossier | B22, B30, B60, B62 |

Onderzocht en niet gebruikt: `email`, `task`, `annotation`, `team` (CRUD-matrix, "Overbodig").

## 3. Nieuwe principes in v3

- **Bevriezen zonder snapshot-tabellen** (B14, B57): onveranderlijke checklistversies, kopiekolommen op dossier en beoordeling, en de PDF leest enkel het dossier.
- **Slot na Afgerond** (B74, B77): één synchrone controle op beoordeling, resultaat, maatregel, HIC-meting en foto, omdat een status niet meegaat naar onderliggende records.
- **Invulplicht per beoordelingsbasis** (B40, B53, B54, B69, B72): risicoanalyse = alle punten; indienststelling = hoofdstukresultaat of alle punten eronder; jaarlijks = enkel het besluit.
- **Historiek overnemen** (B28, B66, B79, B80): per toestel de meest recente afgeronde beoordeling, herkenbaar met `iok_isovergenomen`; het besluit wordt nooit overgenomen.
- **Verwijdergedrag** per relatie: wat in een verslag kan staan, wordt niet verwijderd (beperken); binnen een dossier in opbouw parental.
- **Eigenaarschap** (B63): organisatie voor sjablonen en opzoektabellen, gebruiker/team voor alles wat bij een bestuur hoort.
- **Overzichten zijn views en exports**, geen tabellen (B10, B61).

## 4. Wijzigingen in stap 6 (na de review van stap 5)

Het datamodel van stap 4 is bijgewerkt met B70–B84. Van de 36 reviewpunten zijn er 35 verwerkt en is punt 16 deels uitgesteld; geen enkel punt is afgewezen.

| Wijziging | Reviewpunt | Beslissing |
|---|---|---|
| `iok_speeltoestel.iok_serienummer` + kopie op de beoordeling | 1 | B70 |
| Besluit krijgt de waarde Niet beoordeeld | 8 | B71 |
| Jaarlijkse controle: voor een toestel enkel het besluit verplicht | 12 | B72 |
| `iok_inspecteurid` (→ `systemuser`) en `iok_inspecteurnaam` op het dossier | 19 | B73 |
| Slot na Afgerond met een synchrone controle; mechanisme voorlopig een plug-in | 24, 23 | B74, B77 |
| Beheerder mag onderdelen en controlepunten verwijderen in Concept | 30 | B75 |
| Dossier: `iok_soortcontrole`, statusreden Geannuleerd, uitbateradres (3 kopiekolommen), dossiernummer als sleutel en juiste autonummernotatie, controledatum Alleen datum | 9, 14, 18, 29, 35 | B78 |
| Beoordeling: basis optioneel bij aanmaak, `iok_volgorde`, herkomst van de besluitteksten (2 lookups), sleutel dossier + toestel, besluit niet overnemen | 2, 3, 10, 13, 29 | B79 |
| Historiek per toestel; hernomen foto als eigen record met `iok_foto.iok_isovergenomen` | 7, 17, 20 | B80 |
| `iok_standaardtekstsoort` heringedeeld; activeerregel voor een nieuwe checklistversie; enkel de checklist krijgt Vervangen | 4, 5, 34 | B81 |
| Risicoformules met test op leeg, 2 decimalen, grenzen uitgeschreven | 25, 26, 27 | B82 |
| `iok_verzendpogingen` en `iok_laatstepogingop` geschrapt; `iok_document.iok_handmatigaangepast`; URL-kolommen 2000 | 6, 22, 35 | B83 |
| `iok_codeweergave`; sleutel op `iok_terreingroep`; regels 17–26; acht rechten per rol in `spec.yaml`; opmerking over "/" en "+" in sleutels | 11, 15, 21, 28, 29, 31, 32, 33 | B84 |
| CRUD-matrix bijgewerkt | 36 | – |
| Q06 hoge prioriteit; rechten van de inspecteur op stamgegevens pas na het antwoord van IOK | 16 | B84 |

Saldo tegenover stap 4: +3 relaties (32 → 35), +3 alternatieve sleutels (10 → 13), +1 keuzelijst (13 → 14), 2 kolommen geschrapt, 14 kolommen toegevoegd (135 → 147 kolommen in de kolomtabellen); het aantal tabellen blijft 23.

## 5. Nog open

- **Niet getoetst aan les 4b**: `01_context/cursus/` is leeg (Q09).
- **Na te lezen door Dries**: B77 (plug-in in plaats van een workflow) en B70–B75 (aanvaard zonder afzonderlijke opmerkingen, B76).
- **Vragen voor IOK**: Q01–Q08, Q12, Q14, Q15, Q17–Q27; Q06 en Q20 met hoge prioriteit. Geen van die vragen wijzigt de structuur.
- **Te testen in de eigen omgeving**: zie `datamodel_v3.md` §12.
