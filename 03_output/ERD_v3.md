# ERD datamodel v3 – IOK

_Gegenereerd uit `03_output/datamodel_v3.md` door `tools/stap6_genereer.py` (stap 6). Niet met de hand wijzigen._

21 tabellen (4 standaard, 17 eigen), 35 relaties 1:N en 2 native N:N. Volledige kolomlijsten staan in `datamodel_v3.md`; de diagrammen tonen de sleutel (PK), alternatieve sleutels (UK), lookups (FK) en de primaire kolom. Hetzelfde model met alle kolommen: `IOK_erd_v3.drawio`.

Notatie: `||--o{` = verplichte lookup (1 : 0..N), `|o--o{` = optionele lookup (0..1 : 0..N), `}o--o{` = native N:N. Bekijken: VS Code (Markdown Preview Mermaid Support) of mermaid.live.

## 1. Overzicht (alle tabellen en relaties)

```mermaid
erDiagram
    %% Stamgegevens
    account |o--o{ contact : "heeft contactpersoon"
    account ||--o{ iok_terreingroep : "heeft groep"
    account ||--o{ iok_speelterrein : "beheert"
    account |o--o{ iok_speelterrein : "baat uit"
    iok_terreingroep |o--o{ iok_speelterrein : "groepeert"
    iok_speelterrein ||--o{ iok_speeltoestel : "bevat"
    iok_toesteltype ||--o{ iok_speeltoestel : "typeert"
    iok_speeltoestel ||--o{ iok_toestelcode : "draagt"
    iok_toesteltype }o--o{ iok_checklistonderdeel : "vraagt"
    %% Sjablonen
    iok_checklist |o--o{ iok_checklist : "volgt op"
    iok_checklist ||--o{ iok_checklistonderdeel : "bestaat uit"
    iok_checklistonderdeel ||--o{ iok_controlepunt : "bevat"
    iok_controlepunt |o--o{ iok_controlepunt : "is ouder van"
    iok_controlepunt |o--o{ iok_controlepunt : "is hoofdstuk van"
    iok_controlepunt |o--o{ iok_standaardtekst : "heeft zinnen"
    %% Inspectie
    account ||--o{ iok_inspectiedossier : "is bestuur in (kopie)"
    systemuser ||--o{ iok_inspectiedossier : "inspecteert"
    iok_speelterrein ||--o{ iok_inspectiedossier : "wordt gecontroleerd in"
    iok_speeltoestel |o--o{ iok_beoordeling : "wordt beoordeeld in"
    iok_checklist ||--o{ iok_beoordeling : "wordt gebruikt in"
    iok_controlepunt ||--o{ iok_resultaat : "wordt beantwoord in"
    iok_inspectiedossier ||--o{ iok_beoordeling : "bevat"
    iok_beoordeling |o--o{ iok_beoordeling : "is bron van"
    iok_beoordeling ||--o{ iok_resultaat : "heeft resultaat"
    iok_beoordeling ||--o{ iok_maatregel : "leidt tot"
    iok_beoordeling ||--o{ iok_hicmeting : "heeft meting"
    iok_beoordeling ||--o{ iok_foto : "heeft foto"
    iok_resultaat |o--o{ iok_maatregel : "onderbouwt"
    iok_resultaat |o--o{ iok_foto : "toont gebrek van"
    iok_standaardtekst |o--o{ iok_resultaat : "is herkomst van opmerking"
    iok_standaardtekst |o--o{ iok_maatregel : "is herkomst van maatregel"
    iok_standaardtekst |o--o{ iok_beoordeling : "is herkomst van besluit"
    iok_standaardtekst |o--o{ iok_inspectiedossier : "is herkomst van algemeen besluit"
    iok_beoordeling }o--o{ iok_checklistonderdeel : "gebruikt"
    %% Communicatie
    iok_inspectiedossier ||--o{ iok_rapportversie : "heeft versie"
    iok_rapportversie ||--o{ iok_document : "omvat"
    %% Platform
    iok_inspectiedossier |o--o{ sharepointdocumentlocation : "heeft archiefmap"
```

## 2. Stamgegevens

Tabellen van deze groep met hun sleutels en lookups; tabellen uit andere groepen staan er enkel als naam bij.

```mermaid
erDiagram
    %% Stamgegevens
    account |o--o{ contact : "heeft contactpersoon"
    account ||--o{ iok_terreingroep : "heeft groep"
    account ||--o{ iok_speelterrein : "beheert"
    account |o--o{ iok_speelterrein : "baat uit"
    account ||--o{ iok_inspectiedossier : "is bestuur in (kopie)"
    iok_terreingroep |o--o{ iok_speelterrein : "groepeert"
    iok_speelterrein ||--o{ iok_speeltoestel : "bevat"
    iok_speelterrein ||--o{ iok_inspectiedossier : "wordt gecontroleerd in"
    iok_toesteltype ||--o{ iok_speeltoestel : "typeert"
    iok_speeltoestel ||--o{ iok_toestelcode : "draagt"
    iok_speeltoestel |o--o{ iok_beoordeling : "wordt beoordeeld in"
    iok_toesteltype }o--o{ iok_checklistonderdeel : "vraagt"
    account {
        guid accountid PK
        string name
        string address1_line1
        string address1_postalcode
        string address1_city
        string emailaddress1
        lookup primarycontactid
        choice iok_soort
    }
    contact {
        guid contactid PK
        string fullname
        string emailaddress1
        string telephone1
        lookup parentcustomerid FK
    }
    iok_terreingroep {
        guid iok_terreingroepid PK
        string iok_naam UK "primaire kolom"
        lookup iok_bestuurid FK, UK
    }
    iok_speelterrein {
        guid iok_speelterreinid PK
        string iok_naam "primaire kolom"
        string iok_code UK
        lookup iok_bestuurid FK
        lookup iok_uitbaterid FK
        lookup iok_terreingroepid FK
    }
    iok_speeltoestel {
        guid iok_speeltoestelid PK
        string iok_naam "primaire kolom"
        lookup iok_speelterreinid FK
        lookup iok_toesteltypeid FK
    }
    iok_toestelcode {
        guid iok_toestelcodeid PK
        string iok_code UK "primaire kolom"
        lookup iok_speeltoestelid FK
    }
    iok_toesteltype {
        guid iok_toesteltypeid PK
        string iok_naam UK "primaire kolom"
    }
```

## 3. Sjablonen

Tabellen van deze groep met hun sleutels en lookups; tabellen uit andere groepen staan er enkel als naam bij.

```mermaid
erDiagram
    %% Sjablonen
    iok_checklist |o--o{ iok_checklist : "volgt op"
    iok_checklist ||--o{ iok_checklistonderdeel : "bestaat uit"
    iok_checklist ||--o{ iok_beoordeling : "wordt gebruikt in"
    iok_checklistonderdeel ||--o{ iok_controlepunt : "bevat"
    iok_controlepunt |o--o{ iok_controlepunt : "is ouder van"
    iok_controlepunt |o--o{ iok_controlepunt : "is hoofdstuk van"
    iok_controlepunt |o--o{ iok_standaardtekst : "heeft zinnen"
    iok_controlepunt ||--o{ iok_resultaat : "wordt beantwoord in"
    iok_standaardtekst |o--o{ iok_resultaat : "is herkomst van opmerking"
    iok_standaardtekst |o--o{ iok_maatregel : "is herkomst van maatregel"
    iok_standaardtekst |o--o{ iok_beoordeling : "is herkomst van besluit"
    iok_standaardtekst |o--o{ iok_inspectiedossier : "is herkomst van algemeen besluit"
    iok_toesteltype }o--o{ iok_checklistonderdeel : "vraagt"
    iok_beoordeling }o--o{ iok_checklistonderdeel : "gebruikt"
    iok_checklist {
        guid iok_checklistid PK
        string iok_naam UK "primaire kolom"
        string iok_versie UK
        lookup iok_vorigeversieid FK
    }
    iok_checklistonderdeel {
        guid iok_checklistonderdeelid PK
        string iok_naam UK "primaire kolom"
        lookup iok_checklistid FK, UK
    }
    iok_controlepunt {
        guid iok_controlepuntid PK
        string iok_naam "primaire kolom"
        string iok_code UK
        lookup iok_onderdeelid FK, UK
        lookup iok_ouderid FK
        lookup iok_hoofdstukid FK
    }
    iok_standaardtekst {
        guid iok_standaardtekstid PK
        string iok_naam "primaire kolom"
        lookup iok_controlepuntid FK
    }
```

## 4. Inspectie

Tabellen van deze groep met hun sleutels en lookups; tabellen uit andere groepen staan er enkel als naam bij.

```mermaid
erDiagram
    %% Inspectie
    account ||--o{ iok_inspectiedossier : "is bestuur in (kopie)"
    systemuser ||--o{ iok_inspectiedossier : "inspecteert"
    iok_speelterrein ||--o{ iok_inspectiedossier : "wordt gecontroleerd in"
    iok_speeltoestel |o--o{ iok_beoordeling : "wordt beoordeeld in"
    iok_checklist ||--o{ iok_beoordeling : "wordt gebruikt in"
    iok_controlepunt ||--o{ iok_resultaat : "wordt beantwoord in"
    iok_inspectiedossier ||--o{ iok_beoordeling : "bevat"
    iok_inspectiedossier ||--o{ iok_rapportversie : "heeft versie"
    iok_inspectiedossier |o--o{ sharepointdocumentlocation : "heeft archiefmap"
    iok_beoordeling |o--o{ iok_beoordeling : "is bron van"
    iok_beoordeling ||--o{ iok_resultaat : "heeft resultaat"
    iok_beoordeling ||--o{ iok_maatregel : "leidt tot"
    iok_beoordeling ||--o{ iok_hicmeting : "heeft meting"
    iok_beoordeling ||--o{ iok_foto : "heeft foto"
    iok_resultaat |o--o{ iok_maatregel : "onderbouwt"
    iok_resultaat |o--o{ iok_foto : "toont gebrek van"
    iok_standaardtekst |o--o{ iok_resultaat : "is herkomst van opmerking"
    iok_standaardtekst |o--o{ iok_maatregel : "is herkomst van maatregel"
    iok_standaardtekst |o--o{ iok_beoordeling : "is herkomst van besluit"
    iok_standaardtekst |o--o{ iok_inspectiedossier : "is herkomst van algemeen besluit"
    iok_beoordeling }o--o{ iok_checklistonderdeel : "gebruikt"
    iok_inspectiedossier {
        guid iok_inspectiedossierid PK
        string iok_dossiernummer UK "primaire kolom"
        lookup iok_speelterreinid FK, UK
        date iok_controledatum UK
        lookup iok_inspecteurid FK
        lookup iok_bestuurid FK
        lookup iok_algemeenbesluitstandaardtekstid FK
    }
    iok_beoordeling {
        guid iok_beoordelingid PK
        string iok_naam "primaire kolom"
        lookup iok_inspectiedossierid FK, UK
        lookup iok_speeltoestelid FK, UK
        lookup iok_checklistid FK
        lookup iok_besluitstandaardtekstid FK
        lookup iok_bronbeoordelingid FK
    }
    iok_resultaat {
        guid iok_resultaatid PK
        string iok_naam "primaire kolom"
        lookup iok_beoordelingid FK, UK
        lookup iok_controlepuntid FK, UK
        lookup iok_standaardtekstid FK
    }
    iok_maatregel {
        guid iok_maatregelid PK
        string iok_naam "primaire kolom"
        lookup iok_beoordelingid FK
        lookup iok_resultaatid FK
        lookup iok_standaardtekstid FK
    }
    iok_hicmeting {
        guid iok_hicmetingid PK
        string iok_naam "primaire kolom"
        lookup iok_beoordelingid FK, UK
        int iok_volgnummer UK
    }
    iok_foto {
        guid iok_fotoid PK
        string iok_naam "primaire kolom"
        lookup iok_beoordelingid FK
        lookup iok_resultaatid FK
    }
```

## 5. Communicatie

Tabellen van deze groep met hun sleutels en lookups; tabellen uit andere groepen staan er enkel als naam bij.

```mermaid
erDiagram
    %% Communicatie
    iok_inspectiedossier ||--o{ iok_rapportversie : "heeft versie"
    iok_rapportversie ||--o{ iok_document : "omvat"
    iok_rapportversie {
        guid iok_rapportversieid PK
        string iok_naam "primaire kolom"
        lookup iok_inspectiedossierid FK, UK
        int iok_versienummer UK
    }
    iok_document {
        guid iok_documentid PK
        string iok_naam "primaire kolom"
        lookup iok_rapportversieid FK
    }
```

## 6. Platform

`systemuser` en `sharepointdocumentlocation` zijn standaardtabellen zonder eigen kolommen; ze staan in het overzicht en in de groepen Inspectie en Communicatie.
