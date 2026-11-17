# Datamodel v3 – IOK veiligheidsinspecties speelterreinen

_Stap 4 (maken), 2026-11-14, uitgewerkt in Claude. Bronnen: `BESLISSINGEN.md` (B01–B84), `02_werk/crud_matrix.md`, `02_werk/velddekking.md`, `02_werk/ontwerpvragen.md`, `01_context/datamodel_v2/IOK_erd_v2.md`, `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md`._

_Stap 7 (2026-11-15): gebouwd in Dataverse; het model is ongewijzigd gebleven (B87 teruggedraaid door B88). Zie de opmerking over de naamkolom in §9._

_Stap 6 (2026-11-14): bijgewerkt met B70–B84 en de aanvaarde punten uit `02_werk/review_v3.md`. Wat in stap 6 nieuw of gewijzigd is, draagt een B-nummer vanaf B70 in de kolom Bron. Overzicht van de wijzigingen: `03_output/changelog_v2_v3.md`._

**Dit document beschrijft wat gebouwd moet worden; er is niets gebouwd.** ERD: `03_output/ERD_v3.md` (Mermaid) en `03_output/IOK_erd_v3.drawio`. Specificatie: `03_output/spec.yaml`, gegenereerd uit dit document (`python tools/stap6_genereer.py`).

## Leeswijzer

- **V** = verplicht, **O** = optioneel. **Sleutel** = alternatieve sleutel (uniek, ook bruikbaar via de Web API).
- Elke tabel heeft daarnaast de standaardkolommen van Dataverse (GUID-sleutel, `createdon`, `modifiedon`, `statecode`, `statuscode`, en bij gebruikerseigendom `ownerid`). Die staan niet in de kolomlijsten, behalve waar ze een rol spelen.
- **Kopie** = kopiekolom: bevroren waarde uit de stamgegevens, gevuld bij het aanmaken (B57).
- Schemanamen: eigen tabellen en kolommen `iok_…` (B01); lookups eindigen op `id`.
- **Achteraf niet te wijzigen** (skill `dataverse-modellering` §5): schemanamen, eigenaarschapstype, kolomtype. Die keuzes staan in §2 en in de kolomlijsten.

## 1. Overzicht

**23 tabellen**: 4 standaardtabellen, 17 eigen tabellen, 2 koppelingen (N:N).

| Groep | Tabel | Soort | Eigenaarschap | Herkomst |
|---|---|---|---|---|
| Stamgegevens | `account` (bestuur) | standaard | gebruiker/team | v2 BESTUUR, B16 |
| | `contact` | standaard | gebruiker/team | v2 BESTUUR.contact_…, B16 |
| | `iok_terreingroep` | eigen | gebruiker/team | nieuw, B47 |
| | `iok_speelterrein` | eigen | gebruiker/team | v2 SPEELTERREIN |
| | `iok_speeltoestel` | eigen | gebruiker/team | v2 SPEELTOESTEL |
| | `iok_toestelcode` | eigen | gebruiker/team | nieuw, B44 |
| | `iok_toesteltype` | eigen | organisatie | v2 TOESTELTYPE |
| Sjablonen | `iok_checklist` | eigen | organisatie | v2 CHECKLIST |
| | `iok_checklistonderdeel` | eigen | organisatie | nieuw, B51 |
| | `iok_controlepunt` | eigen | organisatie | v2 CONTROLEPUNT |
| | `iok_toesteltype_onderdeel` | N:N | – | v2 TOESTEL_CHECKLIST, B26/B51 (in de CRUD-matrix eerst `iok_type_onderdeel`) |
| | `iok_standaardtekst` | eigen | organisatie | nieuw, B35 |
| Inspectie | `iok_inspectiedossier` | eigen | gebruiker/team | v2 CONTROLE |
| | `iok_beoordeling` | eigen | gebruiker/team | v2 BEOORDELING |
| | `iok_beoordeling_onderdeel` | N:N | – | nieuw, B51 |
| | `iok_resultaat` | eigen | gebruiker/team | v2 RESULTAAT |
| | `iok_maatregel` | eigen | gebruiker/team | nieuw, B18 |
| | `iok_hicmeting` | eigen | gebruiker/team | nieuw, B20 |
| | `iok_foto` | eigen | gebruiker/team | v2 FOTO |
| Communicatie | `iok_rapportversie` | eigen | gebruiker/team | v2 CONTROLEVERSIE |
| | `iok_document` | eigen | gebruiker/team | nieuw, B11/B22 |
| Platform | `systemuser` | standaard | – | v2 INSPECTEUR, B13 |
| | `sharepointdocumentlocation` | standaard | – | B22/B30/B60 |

**Niet gebruikt** (CRUD-matrix, "Overbodig"): `email`, `task`, `annotation`, `team`. Geen van de eigen tabellen is een activiteitstabel; notities en activiteiten worden op geen enkele eigen tabel aangezet (eenmaal aan, blijft aan).

## 2. Eigenaarschap (B13, B63)

- **Organisatie-eigendom** voor de sjablonen en opzoektabellen (`iok_toesteltype`, `iok_checklist`, `iok_checklistonderdeel`, `iok_controlepunt`, `iok_standaardtekst`): iedereen leest ze, enkel de bevoegde beheerder schrijft (B08). Er is nooit een reden om ze per bestuur af te schermen.
- **Gebruiker/team-eigendom** voor alles wat bij een bestuur hoort (terreinen, toestellen, dossiers en hun onderliggende records): elk record houdt een eigenaar, zodat latere afscherming per bestuur mogelijk blijft zonder de tabellen te herbouwen (B13, Q07). Wie inspecteerde, staat in `iok_inspectiedossier.iok_inspecteurid` met een naamkopie (B73); de eigenaar dient voor rechten en latere afscherming. Elke flow die dossierrecords aanmaakt, zet `ownerid` op de inspecteur, en een dossier overnemen gebeurt met **Toewijzen**, zodat de onderliggende records meegaan (regel 20, B84).

## 3. Globale keuzelijsten

| Keuzelijst | Waarden | Gebruikt op | Bron |
|---|---|---|---|
| `iok_bestuursoort` | Gemeente · OCMW · Andere | `account.iok_soort` | B16, Q01 |
| `iok_doelgroep` | de 15 waarden uit de sjablonen, opgeschoond (geen opsommingsteken, geen eindpunt) | terrein, toestel, dossier, beoordeling | B32, Q14; velddekking §4 en §6.1–6.2 |
| `iok_toezicht` | Geen toezicht · Sociale controle · Regelmatige controle · Constant toezicht | terrein, dossier | B33 |
| `iok_categorie` | de 16 categorieën ("Zitelementen" gecorrigeerd) | `iok_toesteltype` | B26; velddekking §17.1 |
| `iok_norm` | EN 1176 · EN 14974 | toesteltype, checklist, beoordeling | B21 |
| `iok_checklistsoort` | Toestel · Terrein | checklist | B23, B52 |
| `iok_soortbeoordeling` | Terrein · Toestel | beoordeling | B23 |
| `iok_beoordelingsbasis` | Jaarlijkse controle · Indienststelling · Risicoanalyse | beoordeling | B21 |
| `iok_soortcontrole` | Jaarlijkse controle · Nieuwe controle | dossier | B78; BPMN D1 |
| `iok_besluit` | Conform · Niet conform · Niet beoordeeld | beoordeling | B18, B71 |
| `iok_antwoord` | OK · NOK · nvt | resultaat | B36 |
| `iok_standaardtekstsoort` | Opmerking bij controlepunt · Maatregel · Besluit beoordeling · Algemeen besluit | standaardtekst | B35, B81 |
| `iok_fotosoort` | Overzicht · Gebrek | foto | B15 |
| `iok_documenttype` | Rapport · Preventiesamenvatting | document | B11 |

## 4. Stamgegevens

### 4.1 `account` – bestuur (standaardtabel)

Hergebruikt: `name`, `address1_line1`, `address1_postalcode`, `address1_city`, `primarycontactid` (de primaire contactpersoon, B16), `emailaddress1`.

| Eigen kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_soort` | keuze `iok_bestuursoort` | V | Gemeente/OCMW/Andere | B16; velddekking §16.3 punt 2 |

Geen `iok_eenheden` op Account (B61).

### 4.2 `contact` – contactpersoon (standaardtabel)

Hergebruikt: `fullname`, `emailaddress1`, `telephone1`, `parentcustomerid` (→ `account`). Geen eigen kolommen. 1..N per bestuur; de primaire staat op `account.primarycontactid` (B16, B37).

### 4.3 `iok_terreingroep` (B47, B56)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (120), primaire kolom | V | bv. "Onthaalmoeders OCMW" | velddekking §16.2 |
| `iok_bestuurid` | lookup → `account` | V | regel: gelijk aan het bestuur van de terreinen in de groep | B56 |
| `iok_legacyid` | geheel getal | O | oude `ID_speelterrein` van een gesplitste bronrij | B49 |

Geen adres, geen code, geen dossier (B50). Blijft leeg tot IOK de locaties aanlevert (B56).

### 4.4 `iok_speelterrein`

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (120), primaire kolom | V | benaming speelterrein | TER r5 |
| `iok_code` | tekst (20), **sleutel** | V | uniek over alle besturen; hoofdletters bij het laden | B25, B48, B49 |
| `iok_bestuurid` | lookup → `account` | V | "Verantwoordelijke" | B16, B37 |
| `iok_uitbaterid` | lookup → `account` | O | leeg = het bestuur zelf | B37, Q01 |
| `iok_terreingroepid` | lookup → `iok_terreingroep` | O | | B47 |
| `iok_straat` | tekst (120) | O | | TER r8; v2 |
| `iok_postcode` | tekst (4) | O | | v2 |
| `iok_plaats` | tekst (80) | O | | v2 |
| `iok_doelgroep` | keuze `iok_doelgroep` | O | één waarde | B32, Q14 |
| `iok_toezicht` | keuze `iok_toezicht` | O | | B33 |
| `iok_eenheden` | geheel getal | O | enkel als het terrein zelf eenheden telt | v2; Q12, B61 |
| `iok_legacyid` | geheel getal | O | oude `ID_speelterrein` | B49 |

Status: Actief / Inactief (vervangt v2 `actief`).

### 4.5 `iok_speeltoestel`

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (120), primaire kolom | V | omschrijving toestel | IND r5 |
| `iok_code` | tekst (30) | V | hoofdcode, voor weergave en PDF; uniekheid zit in `iok_toestelcode` | B44 |
| `iok_codeweergave` | tekst (100) | O | weergave bij meerdere codes, bv. "BOA 1 + BOA 2"; leeg = de hoofdcode; ingevuld door de beheerder | B44, B84; `C_2026`, `B_IND` r15 |
| `iok_speelterreinid` | lookup → `iok_speelterrein` | V | | v2 |
| `iok_toesteltypeid` | lookup → `iok_toesteltype` | V | | B26, B34 |
| `iok_leverancier` | tekst (80) | O | | IND r20 |
| `iok_typefabrikant` | tekst (60) | O | fabrikantbenaming, niet het toesteltype | IND r21 |
| `iok_serienummer` | tekst (60) | O | gebruik te bevestigen (Q19) | B70; IND r22; projectopdracht §4.1 |
| `iok_bouwjaar` | geheel getal | O | | IND r23 |
| `iok_attest` | tekst (60) | O | het attestdocument; de norm staat op de beoordeling | IND r24; B21, Q08 |
| `iok_doelgroep` | keuze `iok_doelgroep` | O | | B32 |
| `iok_eenheden` | geheel getal | V | standaardwaarde uit het type, per toestel aanpasbaar | B58; velddekking §17.1 |

Statusredenen: **In gebruik** (actief) · **Buiten gebruik** (inactief) (B24). Geen kolom voor datum onderhoud (B41, Q19). Geen toezicht per toestel (B33).

### 4.6 `iok_toestelcode` (B44)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_code` | tekst (30), primaire kolom, **sleutel** | V | uniek over alle besturen | B25, B44 |
| `iok_speeltoestelid` | lookup → `iok_speeltoestel` | V | | B44 |
| `iok_ishoofdcode` | ja/nee | V | precies één ja per toestel; gelijk aan `iok_speeltoestel.iok_code` | B44 |

### 4.7 `iok_toesteltype` (B26, B34, B58)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (80), primaire kolom, **sleutel** | V | 128 types | velddekking §17.1; Q15 |
| `iok_categorie` | keuze `iok_categorie` | V | | B26 |
| `iok_eenheden` | geheel getal | V | standaardwaarde (1–9) | velddekking §17.1 |
| `iok_norm` | keuze `iok_norm` | V | standaardnorm voor de beoordeling | B21 |

Niet geversioneerd: wijzigen ter plaatse, deactiveren als het type vervalt (B58).

## 5. Sjablonen

### 5.1 `iok_checklist` – het geheel, met versie (B19, B51)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (80), primaire kolom | V | bv. "Speeltoestellen EN 1176" | v2 |
| `iok_versie` | tekst (10) | V | bv. "2022" | v2; B19 |
| `iok_soort` | keuze `iok_checklistsoort` | V | | B52 |
| `iok_norm` | keuze `iok_norm` | O | leeg bij een terreinchecklist | B21, B52 |
| `iok_vorigeversieid` | lookup → `iok_checklist` | O | de versie waarvan deze gekopieerd is | B19 |

**Sleutel:** `iok_naam` + `iok_versie`. Statusredenen: **Concept** (actief; enige toestand waarin checklist, onderdelen en controlepunten wijzigbaar zijn) · **Actief** (actief; in gebruik voor nieuwe dossiers) · **Vervangen** (inactief) (B57). Regel: per soort en norm hoogstens één versie Actief. Enkel de checklist krijgt Vervangen; onderdelen en controlepunten blijven actief, zodat een dossier op een oudere versie ze kan blijven opzoeken (B81). Een nieuwe versie wordt pas Actief als er geen dossier in Concept of In uitvoering op de vorige versie staat (regel 7, B81).

Drie checklists bij de start: speeltoestellen EN 1176 (indienststelling en risicoanalyse zijn dezelfde reeks, B38), skate EN 14974 (B39), terrein (B23).

### 5.2 `iok_checklistonderdeel` (B51, B52)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (120), primaire kolom | V | "Deel 1 Algemeen", "Schommels", "Curbs", "Terrein" | sjablonen, bladnamen |
| `iok_checklistid` | lookup → `iok_checklist` | V | | B51 |
| `iok_altijdvantoepassing` | ja/nee | V | ja voor Deel 1 en het terreinonderdeel | B52 |
| `iok_volgorde` | geheel getal | V | volgorde in app en PDF | volgorde van de bladen in de sjablonen; `B_SAM` |

**Sleutel:** `iok_checklistid` + `iok_naam`.

### 5.3 `iok_controlepunt` (B40, B43, B53, B55)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (200), primaire kolom | V | code + begin van de tekst | – |
| `iok_code` | tekst (20) | V | bv. "G.2.6.2"; genormaliseerd bij het laden | velddekking §14 |
| `iok_tekst` | meerregelige tekst (2000) | V | de vraag of de hoofdstuktitel | v2 |
| `iok_toelichting` | meerregelige tekst (2000) | O | normwaarden, bv. "min. 40 mm / max. 1000 mm" | B53 |
| `iok_onderdeelid` | lookup → `iok_checklistonderdeel` | V | | B51 |
| `iok_ouderid` | lookup → `iok_controlepunt` | O | leeg = hoofdstuk; diepte onbeperkt | B43 |
| `iok_hoofdstukid` | lookup → `iok_controlepunt` | O | het bovenste niveau; leeg bij het hoofdstuk zelf; onveranderlijk na aanmaak | B43 |
| `iok_volgorde` | geheel getal | V | de code is geen volgnummer | velddekking §6.9 |
| `iok_nokbepaalthoofdstuk` | ja/nee, standaard ja | V | enkel betekenisvol op een hoofdstuk | B55, Q18 |

**Sleutel:** `iok_onderdeelid` + `iok_code`. Enkel wijzigbaar zolang de checklist in Concept staat (afgedwongen, regel 17). In Concept mag de beheerder een controlepunt of onderdeel verwijderen, van onder naar boven (B75).

### 5.4 `iok_toesteltype_onderdeel` – N:N (B26, B51, B52)

Native N:N tussen `iok_toesteltype` en `iok_checklistonderdeel`, zonder eigen kolommen. 0..N: een type zonder Deel 2-onderdeel is geldig. Bij een nieuwe checklistversie worden de koppelingen naar de nieuwe onderdelen gekopieerd (CRUD D4.2). Inhoud: Q21.

### 5.5 `iok_standaardtekst` (B35, B59, B65)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (120), primaire kolom | V | korte titel om te kiezen | – |
| `iok_tekst` | meerregelige tekst (2000) | V | de zin, letterlijk | velddekking §5, §12 |
| `iok_soort` | keuze `iok_standaardtekstsoort` | V | ingedeeld naar gebruik; de lijst (Markeringen, AREI, …) volgt uit het controlepunt | B35, B81 |
| `iok_controlepuntid` | lookup → `iok_controlepunt` | O | leeg = algemene zin | B35 |

Niet geversioneerd: de gekozen tekst wordt gekopieerd (B59). Bij een nieuwe checklistversie verhuist `iok_controlepuntid` naar het overeenkomstige nieuwe controlepunt (B65).

## 6. Inspectie

### 6.1 `iok_inspectiedossier` (B11, B17, B19, B57)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_dossiernummer` | autonummer, primaire kolom, **sleutel** | V | notatie `DOS-{DATETIMEUTC:yyyy}-{SEQNUM:5}`; het jaar is het aanmaakjaar in UTC en de reeks begint niet opnieuw per jaar | B19, B78; BPMN D1.2 |
| `iok_speelterreinid` | lookup → `iok_speelterrein` | V | | B46, B50 |
| `iok_controledatum` | datum (alleen datum) | V | versiesleutel; gedrag **Alleen datum**, zodat tijdzones de datum niet verschuiven | B06, B78 |
| `iok_soortcontrole` | keuze `iok_soortcontrole` | V | gekozen in D1.1; bepaalt D1.3 of D1.4 en de titel van de PDF | B78; BPMN D1 |
| `iok_inspecteurid` | lookup → `systemuser` | V | wie de controle uitvoerde | B73 |
| `iok_inspecteurnaam` | tekst (160) | V | **kopie** ("RA uitgevoerd door") | B73; `A_` r13 |
| `iok_bestuurid` | lookup → `account` | V | **kopie**: het bestuur op het moment van de controle | B57; D4.3/D4.5 |
| `iok_bestuurnaam` | tekst (160) | V | **kopie** | B57 |
| `iok_contactnaam` | tekst (160) | O | **kopie**: primaire contactpersoon | B37, B57 |
| `iok_uitbaternaam` | tekst (160) | O | **kopie** | B57 |
| `iok_uitbaterstraat` | tekst (120) | O | **kopie**: adres van de uitbater; zonder uitbater het adres van het bestuur | B78; `A_` r11–13 |
| `iok_uitbaterpostcode` | tekst (10) | O | **kopie** | B78 |
| `iok_uitbaterplaats` | tekst (80) | O | **kopie** | B78 |
| `iok_terreinnaam` | tekst (120) | V | **kopie** | B57 |
| `iok_terreincode` | tekst (20) | V | **kopie** | B57 |
| `iok_straat` | tekst (120) | O | **kopie**: adres van het terrein | B57 |
| `iok_postcode` | tekst (4) | O | **kopie** | B57 |
| `iok_plaats` | tekst (80) | O | **kopie** | B57 |
| `iok_doelgroep` | keuze `iok_doelgroep` | O | **kopie** | B57 |
| `iok_toezicht` | keuze `iok_toezicht` | O | **kopie** | B33, B57 |
| `iok_algemeenbesluit` | meerregelige tekst (2000) | O | slottekst van het verslag, gekopieerd uit een standaardzin | B68; `C_2026` r165 |
| `iok_algemeenbesluitstandaardtekstid` | lookup → `iok_standaardtekst` | O | herkomst van het algemeen besluit | B59, B79 |

**Sleutels:** `iok_speelterreinid` + `iok_controledatum` (B19) en `iok_dossiernummer` (B78). Statusredenen: **Concept** · **In uitvoering** (actief) · **Afgerond** · **Geannuleerd** (inactief) (B17, B78). Geannuleerd dient enkel voor een dossier dat al een rapportversie heeft; een dossier zonder rapportversie verwijdert de beheerder, want een inactief dossier houdt de sleutel terrein + controledatum bezet (regel 25). Eigenaar = de inspecteur (regel 20). De kopiekolommen worden gevuld in D1.2 en zijn tot Afgerond te corrigeren in het dossier (B57).

### 6.2 `iok_beoordeling` (B21, B23, B42, B57)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (160), primaire kolom | V | dossiernummer + "Terrein" of toestelcode | – |
| `iok_inspectiedossierid` | lookup → `iok_inspectiedossier` | V | | B11 |
| `iok_soort` | keuze `iok_soortbeoordeling` | V | | B23 |
| `iok_speeltoestelid` | lookup → `iok_speeltoestel` | O | verplicht bij soort Toestel, leeg bij Terrein | v2 |
| `iok_checklistid` | lookup → `iok_checklist` | V | de gebruikte versie | B19, B51 |
| `iok_norm` | keuze `iok_norm` | O | standaard uit het type; leeg bij Terrein | B21 |
| `iok_beoordelingsbasis` | keuze `iok_beoordelingsbasis` | O | bepaalt de invulplicht; leeg bij het aanmaken (D1.3), vastgesteld in D2.1, verplicht bij afronden; standaard Jaarlijkse controle als het dossier jaarlijks is | B21, B40, B79 |
| `iok_besluit` | keuze `iok_besluit` | O | verplicht bij afronden; Niet beoordeeld = toestel verwijderd of onbruikbaar aangetroffen; wordt in D1.4 niet overgenomen | B18, B71, B79 |
| `iok_besluittekst` | meerregelige tekst (2000) | O | bv. "Het toestel is conform de norm.", gekopieerd uit een standaardzin; bij Niet beoordeeld de bevinding | B59, B68, B71 |
| `iok_besluitstandaardtekstid` | lookup → `iok_standaardtekst` | O | herkomst van de besluittekst | B59, B79 |
| `iok_volgorde` | geheel getal | O | volgorde in het verslag; terrein = 0 | B79; `C_2026` |
| `iok_opmerking` | meerregelige tekst (2000) | O | één per beoordeling | B42 |
| `iok_bronbeoordelingid` | lookup → `iok_beoordeling` | O | de beoordeling waaruit de historiek is overgenomen | B28, B66 |
| `iok_toestelcode` | tekst (100) | O | **kopie**: hoofdcode of codebereik ("SCB 01 -> SCB 04") | B44, B57 |
| `iok_toestelnaam` | tekst (120) | O | **kopie** | B57 |
| `iok_typenaam` | tekst (80) | O | **kopie** | B57, B58 |
| `iok_leverancier` | tekst (80) | O | **kopie** | B57 |
| `iok_typefabrikant` | tekst (60) | O | **kopie** | B57 |
| `iok_serienummer` | tekst (60) | O | **kopie** | B70 |
| `iok_attest` | tekst (60) | O | **kopie** | B57 |
| `iok_bouwjaar` | geheel getal | O | **kopie** | B57 |
| `iok_doelgroep` | keuze `iok_doelgroep` | O | **kopie** | B57 |
| `iok_eenheden` | geheel getal | O | **kopie**; bron van het financiële overzicht | B58, B61 |

**Sleutel:** `iok_inspectiedossierid` + `iok_speeltoestelid` (B79): hoogstens één beoordeling per toestel per dossier. Bij de terreinbeoordeling is het toestel leeg en dwingt de sleutel niets af; daarvoor blijft regel 10 nodig. Regels: precies één terreinbeoordeling per dossier (B23); de gekozen onderdelen horen bij `iok_checklistid` (regel 23). In D1.4 worden besluit, besluittekst en opmerking niet overgenomen (B79).

### 6.3 `iok_beoordeling_onderdeel` – N:N (B51)

Native N:N tussen `iok_beoordeling` en `iok_checklistonderdeel`. Gevuld in D1.3 (alle "altijd"-onderdelen + die van het type) of D1.4; de inspecteur past aan in D2.1, bv. welke skate-onderdelen aanwezig zijn.

### 6.4 `iok_resultaat` (B36, B40, B45, B64)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (100), primaire kolom | V | code van het controlepunt | – |
| `iok_beoordelingid` | lookup → `iok_beoordeling` | V | | v2 |
| `iok_controlepuntid` | lookup → `iok_controlepunt` | V | ook een hoofdstuk kan een resultaat hebben | B40 |
| `iok_antwoord` | keuze `iok_antwoord` | O | leeg kan, als er enkel een opmerking is | B36, B40 |
| `iok_opmerking` | meerregelige tekst (2000) | O | één per controlepunt | vaste eis |
| `iok_standaardtekstid` | lookup → `iok_standaardtekst` | O | herkomst van de opmerking | B59 |
| `iok_impact` | decimaal (1 decimaal) | O | toegelaten: 1 · 3 · 7 · 15 · 40 | B45, B64 |
| `iok_kans` | decimaal (1 decimaal) | O | toegelaten: 0,2 · 0,5 · 1 · 3 · 6 · 10 | B45, B64 |
| `iok_blootstelling` | decimaal (1 decimaal) | O | toegelaten: 0,5 · 1 · 2 · 3 · 6 · 10 | B45, B64 |
| `iok_risicoscore` | formulekolom (decimaal, 2 decimalen) | – | leeg als een factor leeg is, anders impact × kans × blootstelling | B45, B64, B82 |
| `iok_risicoklasse` | formulekolom (tekst) | – | leeg als de score leeg is; ≤ 20 Licht · ≤ 70 Mogelijk · ≤ 160 Substantieel · ≤ 320 Hoog · > 320 Zeer hoog (bovengrens inbegrepen; precies 70 = Q24) | B45, B64, B82 |
| `iok_isovergenomen` | ja/nee, standaard nee | V | ja = overgenomen uit de vorige beoordeling van dit toestel en nog niet bevestigd | vaste eis; B66, B80 |

**Sleutel:** `iok_beoordelingid` + `iok_controlepuntid`. Geen lege rijen vooraf (B40).

Formules (B82; te testen in de eigen omgeving):

- `iok_risicoscore` = `If(IsBlank(iok_impact) || IsBlank(iok_kans) || IsBlank(iok_blootstelling), Blank(), iok_impact * iok_kans * iok_blootstelling)`
- `iok_risicoklasse` = `If(IsBlank(iok_risicoscore), Blank(), iok_risicoscore <= 20, "Licht", iok_risicoscore <= 70, "Mogelijk", iok_risicoscore <= 160, "Substantieel", iok_risicoscore <= 320, "Hoog", "Zeer hoog")`

Zonder de test op leeg telt een lege factor als 0 en wordt elk resultaat zonder score "Licht". Een formulekolom is niet sorteerbaar of doorzoekbaar en kan geen flow starten: een overzicht "hoogste risico eerst" kan dus niet op `iok_risicoscore` sorteren (B82).

### 6.5 `iok_maatregel` (B18, B59)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (200), primaire kolom | V | begin van de tekst | – |
| `iok_beoordelingid` | lookup → `iok_beoordeling` | V | | B18 |
| `iok_resultaatid` | lookup → `iok_resultaat` | O | hoogstens één; zelfde beoordeling | B18 |
| `iok_tekst` | meerregelige tekst (2000) | V | gekopieerde standaardzin of vrije tekst | B18, B59 |
| `iok_standaardtekstid` | lookup → `iok_standaardtekst` | O | herkomst | B59 |
| `iok_volgorde` | geheel getal | O | volgorde in de preventiesamenvatting | volgorde van de maatregelen in `B_SAM` |
| `iok_isovergenomen` | ja/nee, standaard nee | V | | B66 |

Geen opvolgingsstatus (B18).

### 6.6 `iok_hicmeting` (B20, B45)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (100), primaire kolom | V | toestelcode + volgnummer | – |
| `iok_beoordelingid` | lookup → `iok_beoordeling` | V | enkel toestelbeoordelingen | B20 |
| `iok_volgnummer` | geheel getal | V | "No." | `C_2026` r8-17 |
| `iok_peak` | decimaal (1 decimaal) | V | G-waarde; drempel < 200 | B45 |
| `iok_hic` | decimaal (1 decimaal) | V | drempel < 1000 | B45 |
| `iok_valhoogte` | geheel getal (cm) | V | | B20 |
| `iok_meetmoment` | datum en tijd | V | | B20 |

**Sleutel:** `iok_beoordelingid` + `iok_volgnummer`. De drempels zijn geen validatie tot Q03 beantwoord is.

### 6.7 `iok_foto` (B15, B22)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (200), primaire kolom | V | bestandsnaam | – |
| `iok_beoordelingid` | lookup → `iok_beoordeling` | V | het toestel volgt uit de beoordeling | B15 |
| `iok_resultaatid` | lookup → `iok_resultaat` | O | bij een foto van een gebrek; meerdere per gebrek mogelijk | B15 |
| `iok_soort` | keuze `iok_fotosoort` | V | | CRUD "Ontbrekend 4" |
| `iok_url` | URL (2000) | V | link naar het bestand in SharePoint | B22, B83 |
| `iok_genomenop` | datum en tijd | O | nodig om de meest recente foto te vinden | B15 |
| `iok_inverslag` | ja/nee, standaard ja | V | een nieuwe overzichtsfoto zet enkel de **overgenomen** overzichtsfoto op nee; die blijft bestaan. Meerdere eigen overzichtsfoto's kunnen | vaste eis foto's; B80 |
| `iok_isovergenomen` | ja/nee, standaard nee | V | ja = hernomen uit een eerdere beoordeling van hetzelfde toestel (zelfde bestand); markering, blokkeert het afronden niet | B15, B80 |

Geen bestand- of afbeeldingskolom (B03, B22). D1.3 en D1.4 maken in de nieuwe beoordeling een `iok_foto` aan die naar het bestand van de meest recente overzichtsfoto van hetzelfde toestel wijst (`iok_isovergenomen` = ja). De PDF leest zo enkel het dossier en een latere foto verandert geen oud verslag (B15, B80, Q02).

## 7. Communicatie

### 7.1 `iok_rapportversie` (B06, B12, B17)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (100), primaire kolom | V | dossiernummer + "v" + versienummer | – |
| `iok_inspectiedossierid` | lookup → `iok_inspectiedossier` | V | | B11 |
| `iok_versienummer` | geheel getal | V | 1, 2, … | v2 |
| `iok_definitiefop` | datum en tijd | O | | B17 |
| `iok_verzondenop` | datum en tijd | O | | B05, B17 |
| `iok_verzondenaan` | tekst (254) | O | e-mailadres waarnaar verstuurd is | H2 |

**Sleutel:** `iok_inspectiedossierid` + `iok_versienummer`. Statusredenen: **Concept** (actief) · **Definitief** · **Verzonden** · **Vervangen** (inactief, dus alleen-lezen in de app) (B17, B69). De overgang Definitief → Verzonden gebeurt met een knop of flow (H4), niet door het formulier te bewerken. De controledatum komt van het dossier; "Versie d.d." in het verslag is `createdon` van het `iok_document` (B83). Geen kolommen voor verzendpogingen: verzenden gebeurt buiten Dataverse en geen stap schrijft ze (B05, B83). Een verzonden versie wordt nooit aangepast: een correctie geeft een nieuwe versie (B12, Q04).

### 7.2 `iok_document` (B11, B22)

| Kolom | Type | V/O | Toelichting | Bron |
|---|---|---|---|---|
| `iok_naam` | tekst (200), primaire kolom | V | bestandsnaam | – |
| `iok_rapportversieid` | lookup → `iok_rapportversie` | V | | B11 |
| `iok_documenttype` | keuze `iok_documenttype` | V | | B11 |
| `iok_url` | URL (2000) | O | leeg bij een mislukte generatie | B22, B83 |
| `iok_handmatigaangepast` | ja/nee, standaard nee | V | ja = de inspecteur paste de PDF zelf aan; ze kan dan afwijken van de dossiergegevens | B83; vaste eis |

Statusredenen: **Concept** (actief) · **Definitief** · **Mislukt** · **Vervangen** (inactief) (B69). Een mislukte of vervangen PDF blijft als spoor staan (CRUD D3.6, D3.8).

### 7.3 `sharepointdocumentlocation` (standaardtabel)

Eén locatie per dossier (`regardingobjectid` → `iok_inspectiedossier`), aangemaakt door een flow bij het aanmaken van het dossier; D3.5 is het vangnet (B60, B62). Documentbeheer moet daarvoor op `iok_inspectiedossier` aanstaan. Foto's en PDF's van het dossier staan in die map.

## 8. Relaties en verwijdergedrag

Uitgangspunt: **er wordt niets verwijderd dat in een verslag kan staan.** Stamgegevens en sjablonen worden gedeactiveerd; de relaties blokkeren het verwijderen (restrict). Enkel binnen een dossier in opbouw verwijdert een bovenliggend record zijn onderliggende records mee (parental). Elke tabel heeft hoogstens één parental-relatie.

| Van (1) | Naar (N) | Lookup | V/O | Gedrag bij verwijderen |
|---|---|---|---|---|
| `account` | `contact` | `parentcustomerid` | O | standaard |
| `account` | `iok_terreingroep` | `iok_bestuurid` | V | beperken |
| `account` | `iok_speelterrein` | `iok_bestuurid` | V | beperken |
| `account` | `iok_speelterrein` | `iok_uitbaterid` | O | koppeling verwijderen |
| `account` | `iok_inspectiedossier` | `iok_bestuurid` | V | beperken |
| `systemuser` | `iok_inspectiedossier` | `iok_inspecteurid` | V | beperken |
| `iok_terreingroep` | `iok_speelterrein` | `iok_terreingroepid` | O | koppeling verwijderen |
| `iok_speelterrein` | `iok_speeltoestel` | `iok_speelterreinid` | V | beperken |
| `iok_speelterrein` | `iok_inspectiedossier` | `iok_speelterreinid` | V | beperken |
| `iok_toesteltype` | `iok_speeltoestel` | `iok_toesteltypeid` | V | beperken |
| `iok_speeltoestel` | `iok_toestelcode` | `iok_speeltoestelid` | V | **parental** |
| `iok_speeltoestel` | `iok_beoordeling` | `iok_speeltoestelid` | O | beperken |
| `iok_checklist` | `iok_checklist` | `iok_vorigeversieid` | O | koppeling verwijderen |
| `iok_checklist` | `iok_checklistonderdeel` | `iok_checklistid` | V | **parental** |
| `iok_checklist` | `iok_beoordeling` | `iok_checklistid` | V | beperken |
| `iok_checklistonderdeel` | `iok_controlepunt` | `iok_onderdeelid` | V | **parental** |
| `iok_controlepunt` | `iok_controlepunt` | `iok_ouderid` | O | beperken |
| `iok_controlepunt` | `iok_controlepunt` | `iok_hoofdstukid` | O | beperken |
| `iok_controlepunt` | `iok_standaardtekst` | `iok_controlepuntid` | O | koppeling verwijderen |
| `iok_controlepunt` | `iok_resultaat` | `iok_controlepuntid` | V | beperken |
| `iok_inspectiedossier` | `iok_beoordeling` | `iok_inspectiedossierid` | V | **parental** |
| `iok_inspectiedossier` | `iok_rapportversie` | `iok_inspectiedossierid` | V | beperken |
| `iok_inspectiedossier` | `sharepointdocumentlocation` | `regardingobjectid` | – | standaard |
| `iok_beoordeling` | `iok_beoordeling` | `iok_bronbeoordelingid` | O | koppeling verwijderen |
| `iok_beoordeling` | `iok_resultaat` | `iok_beoordelingid` | V | **parental** |
| `iok_beoordeling` | `iok_maatregel` | `iok_beoordelingid` | V | **parental** |
| `iok_beoordeling` | `iok_hicmeting` | `iok_beoordelingid` | V | **parental** |
| `iok_beoordeling` | `iok_foto` | `iok_beoordelingid` | V | **parental** |
| `iok_resultaat` | `iok_maatregel` | `iok_resultaatid` | O | koppeling verwijderen |
| `iok_resultaat` | `iok_foto` | `iok_resultaatid` | O | koppeling verwijderen |
| `iok_standaardtekst` | `iok_resultaat` | `iok_standaardtekstid` | O | koppeling verwijderen |
| `iok_standaardtekst` | `iok_maatregel` | `iok_standaardtekstid` | O | koppeling verwijderen |
| `iok_standaardtekst` | `iok_beoordeling` | `iok_besluitstandaardtekstid` | O | koppeling verwijderen |
| `iok_standaardtekst` | `iok_inspectiedossier` | `iok_algemeenbesluitstandaardtekstid` | O | koppeling verwijderen |
| `iok_rapportversie` | `iok_document` | `iok_rapportversieid` | V | beperken |
| `iok_toesteltype` ↔ `iok_checklistonderdeel` | N:N | `iok_toesteltype_onderdeel` | – | – |
| `iok_beoordeling` ↔ `iok_checklistonderdeel` | N:N | `iok_beoordeling_onderdeel` | – | – |

**Bewuste dubbele paden** (skill §4), elk met een consistentieregel:

1. Terrein → bestuur en terrein → groep → bestuur (B56) → regel 12.
2. Dossier → bestuur naast dossier → terrein → bestuur: de eerste is de bevroren kopie (B57); geen regel nodig.
3. Maatregel → beoordeling naast maatregel → resultaat → beoordeling (B18). Idem voor foto → regel 22.
4. Beoordeling → checklist naast beoordeling ↔ onderdeel → checklist (B51) → regel 23.
5. Controlepunt → ouder en controlepunt → hoofdstuk (B43) → regel 24.
6. `iok_beoordeling.iok_norm` naast beoordeling → checklist → `iok_norm` (B21) → regel 23.
7. Resultaat → controlepunt → onderdeel naast resultaat → beoordeling ↔ onderdeel (B51) → regel 23.
8. `iok_speeltoestel.iok_code` naast `iok_toestelcode.iok_ishoofdcode` (B44) → regel 11.

Gevolg van "beperken": een dossier met een rapportversie kan niet meer verwijderd worden, en een controlepunt met resultaten ook niet. Een dossier **zonder** rapportversie kan de beheerder verwijderen; beoordelingen en wat eronder hangt gaan dan mee (B78).

Parental bij dossier → beoordeling en beoordeling → resultaat/maatregel/HIC/foto dient vooral om de eigenaar door te geven bij Toewijzen (regel 20). Bij de sjablonen (checklist → onderdeel → controlepunt) kan enkel verwijderd worden in Concept, van onder naar boven (B75); of een cascade van bovenaf botst op "beperken" van `iok_ouderid` en `iok_hoofdstukid` is te testen.

## 9. Alternatieve sleutels

| Tabel | Sleutel | Bron |
|---|---|---|
| `iok_speelterrein` | `iok_code` | B25, B48 |
| `iok_terreingroep` | `iok_bestuurid` + `iok_naam` | B56, B84 |
| `iok_toestelcode` | `iok_code` | B44 |
| `iok_toesteltype` | `iok_naam` | velddekking §17.1 (geen dubbele namen) |
| `iok_checklist` | `iok_naam` + `iok_versie` | B19 |
| `iok_checklistonderdeel` | `iok_checklistid` + `iok_naam` | B51 |
| `iok_controlepunt` | `iok_onderdeelid` + `iok_code` | B43 |
| `iok_inspectiedossier` | `iok_speelterreinid` + `iok_controledatum` | B19 |
| `iok_inspectiedossier` | `iok_dossiernummer` | B78 |
| `iok_beoordeling` | `iok_inspectiedossierid` + `iok_speeltoestelid` | B79 |
| `iok_resultaat` | `iok_beoordelingid` + `iok_controlepuntid` | vaste eis (één opmerking per controlepunt) |
| `iok_hicmeting` | `iok_beoordelingid` + `iok_volgnummer` | B20 |
| `iok_rapportversie` | `iok_inspectiedossierid` + `iok_versienummer` | B06 |

**Naamkolom en sleutels (B88, vastgesteld bij het bouwen op 15/11/2026):** Dataverse maakt de naamkolom (primaire kolom) van een nieuwe tabel via de Web API altijd aan met 850 tekens en niet-verplicht, ook als iets anders gevraagd is; `tools/dv_bouw.py` zet daarna de lengte en de verplichtstelling goed. In de databank blijft de kolom 850 tekens breed. De drie sleutels die de naamkolom met een tweede kolom combineren (`iok_terreingroep`, `iok_checklist`, `iok_checklistonderdeel`) bleven daardoor meer dan een uur op Pending voor ze actief werden. Bij een nieuwe bouw: wachten en opnieuw controleren.

Een sleutel is standaard hoofdletterongevoelig en telt ook inactieve records mee: de code van een toestel buiten gebruik blijft dus bezet (B62; te testen in de eigen omgeving). Is een sleutelkolom leeg, dan wordt de uniekheid niet afgedwongen (terreinbeoordeling, B79).

160 terreincodes bevatten "/" en 2 een "+", net als 8 typenamen. De sleutel dwingt de uniekheid wel af, maar ophalen of bijwerken via de sleutel in de URL van de Web API werkt met die tekens niet: de koppeling met besturen gebruikt daar `$filter`, of de tekens verdwijnen bij het hercoderen (Q20). Geen modelwijziging (B84).

## 10. Beveiligingsrollen (B08, B13, B67)

Niveaus: **Org** = alle records, **Eigen** = enkel eigen records, **–** = geen recht.

| Tabel(groep) | Inspecteur | Bevoegde beheerder |
|---|---|---|
| `account`, `contact` | lezen Org | maken, lezen, wijzigen Org |
| `iok_terreingroep`, `iok_speelterrein`, `iok_speeltoestel`, `iok_toestelcode` | lezen Org | maken, lezen, wijzigen Org |
| `iok_toesteltype`, `iok_checklist`, `iok_standaardtekst` | lezen Org | maken, lezen, wijzigen Org |
| `iok_checklistonderdeel`, `iok_controlepunt` | lezen Org | maken, lezen, wijzigen Org; **verwijderen Org** (enkel in Concept, B75) |
| `iok_inspectiedossier`, `iok_beoordeling` | maken, lezen, wijzigen, toewijzen Org | lezen Org; **verwijderen Org** (enkel een dossier zonder rapportversie, B78) |
| `iok_resultaat`, `iok_maatregel`, `iok_hicmeting`, `iok_foto` | maken, lezen, wijzigen, toewijzen Org; **verwijderen Eigen** | lezen Org; verwijderen Org (enkel via het dossier, B78) |
| `iok_rapportversie`, `iok_document` | maken, lezen, wijzigen Org | lezen Org |
| `sharepointdocumentlocation` | maken, lezen Org | lezen Org |

- **Niemand verwijdert stamgegevens, checklists, toesteltypes, standaardteksten of rapportversies**; deactiveren hoort bij het wijzigrecht. Uitzonderingen: onderdelen en controlepunten van een checklist in Concept (B75) en een dossier zonder rapportversie (B78), beide enkel door de beheerder.
- De inspecteur verwijdert enkel een verkeerd ingevoerd resultaat, maatregel, HIC-meting of foto in een dossier dat nog actief is (B67). Een rol kent enkel het niveau Eigen/Org en geen voorwaarde op het bovenliggende record: de voorwaarden "in Concept", "zonder rapportversie" en "dossier actief" worden afgedwongen door de synchrone controle van regel 4 en 17 en door de relatie dossier → rapportversie (beperken), niet door de rol (B74, B77).
- De inspecteur schrijft op Org-niveau op dossiers, zodat een collega een dossier kan overnemen met **Toewijzen**; er zijn geen business units (B13, regel 20).
- De tabel hierboven noemt enkel maken, lezen, wijzigen, verwijderen en toewijzen. `03_output/spec.yaml` bevat per tabel en per rol alle acht rechten (ook Toevoegen, Toevoegen aan en Delen): een lookup invullen vraagt Toevoegen/Toevoegen aan, en een N:N-koppeling vraagt Toevoegen op beide tabellen, dus de inspecteur ook op `iok_checklistonderdeel` (B84).
- Of het verwijderen van een dossier door de beheerder ook verwijderrecht op de onderliggende tabellen vraagt, is te testen in de eigen omgeving.
- Registratie van terreinen en toestellen ligt voorlopig bij de beheerder (CRUD D4.1). Een indienststelling kan daardoor niet starten zonder de beheerder: **Q06 heeft hoge prioriteit**. Het antwoord kan de rechten verruimen zonder modelwijziging (B84).
- Besturen hebben geen toegang (B13, Q07).

## 11. Regels buiten het datamodel

Deze regels zitten niet in kolommen of relaties en moeten als bedrijfsregel, flow of app-logica gebouwd worden.

| # | Regel | Waar | Bron |
|---|---|---|---|
| 1 | Invulplicht voor een toestel, per beoordelingsbasis: risicoanalyse = elk controlepunt zonder kinderen heeft een antwoord; indienststelling = elk hoofdstuk heeft een antwoord **of** alle punten eronder hebben er één, verder punten enkel bij afwijking; jaarlijkse controle = enkel het besluit, punten en hoofdstukken alleen bij een afwijking (te bevestigen, Q27). Besluit **Niet beoordeeld** = geen invulplicht | D3.2 | B40, B53, B69, B71, B72 |
| 2 | Terrein bij indienststelling en jaarlijks: enkel het besluit is verplicht | D3.2 | B54 |
| 3 | Is er een NOK onder een hoofdstuk met `iok_nokbepaalthoofdstuk` = ja en heeft dat hoofdstuk een resultaat, dan is dat resultaat NOK | D3.2 | B40, B43, B55 |
| 4 | **Slot**: beoordeling, resultaat, maatregel, HIC-meting en foto kunnen enkel gewijzigd of verwijderd worden zolang hun dossier actief is (Concept of In uitvoering). Eén synchrone controle (voorlopig een plug-in, B77), die ook voor flows en de Web API geldt. Een status gaat niet mee naar onderliggende records, dus de status van het dossier alleen volstaat niet. Rapportversie en document buiten Concept zijn alleen-lezen in de app | D3.1–D3.9 | B57, B62, B74, B77 |
| 5 | Kopiekolommen vullen bij het aanmaken van dossier en beoordeling; de PDF leest enkel het dossier | D1.2–D1.4, D3.5 | B57 |
| 6 | Gekozen standaardzin kopiëren naar het tekstveld en de herkomst invullen | H1, D2.x | B59 |
| 7 | Nieuwe checklistversie: onderdelen, controlepunten (met ouder en hoofdstuk), type-koppelingen kopiëren en standaardteksten omhangen; oude checklist → Vervangen (onderdelen en controlepunten blijven actief). Activeren kan pas als geen dossier in Concept of In uitvoering op de oude versie staat | D4.2 | B19, B51, B65, B81 |
| 8 | D1.3: onderdelen = alle "altijd"-onderdelen van de actieve checklist van de norm + die van het type | D1.3 | B52 |
| 9 | D1.4: per toestel in gebruik de **meest recente afgeronde beoordeling van dat toestel** overnemen (ongeacht het dossier), voor het terrein de meest recente terreinbeoordeling. Resultaten en maatregelen komen mee met `iok_isovergenomen` = ja; besluit, besluittekst en opmerking **niet**. Een toestel zonder historiek krijgt een lege beoordeling zoals in D1.3; de kopiekolommen komen altijd vers uit de stamgegevens. Bevestigen of wijzigen zet de vlag op nee; bij afronden mag op resultaat en maatregel geen ja meer overblijven | D1.4, D3.2 | vaste eis; B28, B66, B79, B80 |
| 10 | Eén terreinbeoordeling per dossier, hoogstens één per toestel (sleutel, B79); een toestel Buiten gebruik komt niet in een nieuw dossier. De gekozen toestellen (inspectiescope) zijn een parameter van D1.3/D1.4, geen kolom | D1.3, D1.4 | B12, B23, B24, B79 |
| 11 | Eén hoofdcode per toestel, gelijk aan `iok_speeltoestel.iok_code` | D4.1 | B44 |
| 12 | Bestuur van het terrein = bestuur van de groep | D4.1 | B56 |
| 13 | Risicofactoren: enkel de toegelaten waarden | D2.4 | B45, B64 |
| 14 | Flow bij een nieuw dossier: SharePoint-map en documentlocatie aanmaken | D1.2 | B60, B62 |
| 15 | Nieuwe versie na verzending: vorige versie → Vervangen, dossier heropenen (→ In uitvoering, waardoor het slot van regel 4 opengaat) | D3.8 | B12, B17, B74 |
| 16 | Overzichten D4.3 en D4.5 zijn views en exports; eenheden = som van `iok_beoordeling.iok_eenheden` in de periode. Of een beoordeling met besluit Niet beoordeeld meetelt, is Q26 | D4.3–D4.5 | B10, B61, B71 |
| 17 | **Sjablonen onveranderlijk**: checklist, onderdeel en controlepunt zijn enkel te wijzigen of te verwijderen zolang de checklist in Concept staat; zelfde soort synchrone controle als regel 4. De rol alleen kan dit niet afdwingen | D4.1, D4.2 | B57, B75, B77 |
| 18 | Opmerking (`iok_resultaat.iok_opmerking`) = wat er vastgesteld is; maatregel (`iok_maatregel.iok_tekst`) = wat het bestuur moet doen. Een NOK zonder maatregel geeft een waarschuwing (blokkeert niet). De PDF drukt beide onder het controlepunt; de preventiesamenvatting leest enkel maatregelen | D2.x, D3.2, D3.4 | B18, B84; `C_2026`, `B_SAM` |
| 19 | D2.1: een onderdeel waarop al resultaten staan, kan niet uit de beoordeling gehaald worden. D3.9 voert de validatie van D3.2 opnieuw uit vóór het dossier Afgerond wordt | D2.1, D3.9 | B51, B84; BPMN D3 |
| 20 | Elke flow die dossierrecords aanmaakt (D1.2–D1.4), zet `ownerid` op de inspecteur. Een dossier overnemen = **Toewijzen** van het dossier; de onderliggende records gaan mee (parental) | D1.2–D1.4 | B63, B67, B84 |
| 21 | Foto's: D1.3/D1.4 hernemen de meest recente overzichtsfoto van het toestel als nieuw `iok_foto` (`iok_isovergenomen` = ja, zelfde bestand). Een nieuwe overzichtsfoto zet de overgenomen foto op `iok_inverslag` = nee. De vlag blokkeert het afronden niet | D1.3, D1.4, D2.1 | B15, B80 |
| 22 | Een maatregel of foto met een resultaat hoort bij dezelfde beoordeling als dat resultaat | H1, D2.x | B18 |
| 23 | De onderdelen van een beoordeling horen bij haar checklist; een resultaat verwijst naar een controlepunt uit een gekozen onderdeel; `iok_beoordeling.iok_norm` = de norm van de checklist | D1.3, D2.1, D2.x | B21, B51, B52 |
| 24 | `iok_controlepunt.iok_hoofdstukid` = de top van de ouderketen, gevuld bij het aanmaken | D4.1, D4.2 | B43 |
| 25 | Fout dossier: zonder rapportversie → de beheerder verwijdert het (maakt de sleutel terrein + controledatum vrij); met rapportversie → Geannuleerd | – (geen BPMN-stap) | B78 |
| 26 | `iok_soortcontrole` wordt gekozen in D1.1 en ingevuld in D1.2; Jaarlijkse controle → D1.4 als er historiek is, anders D1.3 | D1.1, D1.2 | B78; BPMN D1 |

## 12. Nog te bevestigen

- **Bij IOK, zonder gevolg voor de structuur:** Q01 (private uitbaters), Q02 (foto's), Q03 (HIC verplicht), Q04, Q05, **Q06 (hoge prioriteit)**, Q07, Q08, Q12, Q14, Q15, Q17, Q18, Q19, Q20, Q21, Q22, Q23, Q24 (risicoklasse op precies 70), Q25 (punt 6.5 leeg in `B_SAM`), Q26 (verwijderd toestel: eenheden en wie zet het Buiten gebruik), Q27 (bevestiging B72).
- **In de eigen omgeving te testen:** hoofdlettergevoeligheid van de sleutels; gedrag van inactieve records; de flow voor de SharePoint-map (B62); het slot van regel 4 en 17 (B74, B77); `Blank()` in de risicoformules (B82); verwijderen van onder naar boven in een Concept-checklist en het verwijderen van een dossier zonder rapportversie (B75, B78); de eigenaar van records die een flow aanmaakt (regel 20).
- **Mechanisme van het slot (B77, na te lezen):** voorlopig een plug-in. Het alternatief zonder code (realtime workflow) leest maar één stap ver en vraagt dan een rechtstreekse lookup naar het dossier op resultaat, maatregel, HIC-meting en foto, en naar de checklist op het controlepunt.
- **Voor de lector (Q09):** les 4b is **niet getoetst**; `01_context/cursus/` was ook in stap 6 leeg.
