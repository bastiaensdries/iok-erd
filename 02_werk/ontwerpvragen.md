# Ontwerpvragen – stap 3

_Denksessie, gestart 2026-11-14 (in Claude). Per vraag: opties, keuze, waarom, bron. De beslissingen zelf staan in `BESLISSINGEN.md`._

## Ronde 1 – basiseenheid speelterrein (Q20)

| # | Vraag | Opties | Keuze | Waarom | Beslissing |
|---|---|---|---|---|---|
| 1.1 | Wat is één `iok_speelterrein`? | A. fysieke locatie (±879) · B. bronrij (635) met locaties als kindtabel · C. bronrij zonder locatieniveau | **A** | Adres, doelgroep, toezicht en terreinbeoordeling horen bij één plek; "één verslag per terrein" en B19 blijven kloppen. B legt een extra niveau in elk dossier voor 68 gevallen; C geeft 15 plekken één adres. | B46 |
| 1.2 | Hoe de groepering boven het terrein modelleren? | A. geen · B. zelfverwijzende lookup · C. eigen tabel `iok_terreingroep`, optionele lookup · D. tekstkolom | **C** | Een groep heeft naam en bestuur, geen adres of dossier. Werkt met en zonder groepen, dus niet afhankelijk van het antwoord van IOK. B maakt van de groep een terrein zonder dossier. | B47 |
| 1.3 | Blijft de terreincode uniek over alle besturen? | A. B25 behouden · B. uniek per bestuur · C. geen sleutel, enkel waarschuwing | **A** | Eén eenvoudige sleutel, ook voor de Web API; `iok_toestelcode` (B44) blijft ongewijzigd. Een alternatieve sleutel is later aanpasbaar, dus streng beginnen kost weinig. B raakt B44; C schendt de vaste eis. | B48 |
| 1.4 | Terreinen zonder code en de oude `ID_speelterrein`? | A. code verplicht + `iok_legacyid` · B. code optioneel · C. code verplicht, geen legacy-ID | **A** | B25 blijft hard en elke migratierij blijft traceerbaar, ook na splitsen (1.1) en hercoderen (1.3). | B49 |
| 1.5 | Op welk niveau hangt het dossier? | A. altijd op het terrein · B. ook op groepsniveau | **A** | B11, B19 en B23 blijven ongewijzigd. B geeft meerdere terreinbeoordelingen per dossier en raakt bijna de hele CRUD-matrix. | B50 |

**Bronnen:** velddekking §16.2–16.3; B10, B11, B19, B23, B25, B37, B44; vaste eisen "codes zijn uniek" en "één verslag per terrein = één PDF".

**Blijft voor IOK (blokkeert niets):** betekent F "aantal locaties"? · hercoderen van de dubbele codes, en de code van een locatie binnen een groep · één gebundeld verslag per groep?

**Gevolg voor stap 4:** nieuwe tabel `iok_terreingroep`; `iok_speelterrein` krijgt een optionele lookup naar de groep en `iok_legacyid`; de CRUD-matrix krijgt een kolom `iok_terreingroep` (C+U in D4.1, R in D1.1, D4.3, D4.5).

## Ronde 2 – checklists en antwoorden

**Nieuw uit de bron:** in het skate-sjabloon hebben *Afmetingen* en *Veiligheidszone* een eigen Status-cel; de mm-waarden zijn normwaarden, geen invulvelden (`risicoanalyse skate toestellen versie 2022`, o.a. blad Curbs r12–r21).

| # | Vraag | Opties | Keuze | Waarom | Beslissing |
|---|---|---|---|---|---|
| 2.1 | Wat is één `iok_checklist`, en waar zit Deel 1 / Deel 2 / skate-onderdeel? | A. checklist = geheel + nieuwe tabel `iok_checklistonderdeel` · B. elk blad een eigen checklist · C. onderdeel = bovenste controlepuntniveau | **A** | Eén versie per geheel (B19); skate (B39) en combinatietoestel (B26) werken identiek. B geeft 12 versies per reeks; C breekt `iok_hoofdstuk` (B43). | B51 |
| 2.2 | Q21: kardinaliteit type → onderdeel, en Deel 1? | A. 0..N + kolom "altijd van toepassing" · B. 1..N met Deel 1 aan elk type · C. 1..N op Deel 2 | **A** | Evenwichtsparcours zonder Deel 2 is geldig (`B_IND`); geen 128 koppelrijen die hetzelfde zeggen. | B52 |
| 2.3 | Q16 + HIC: één meetwaarde-patroon? | A. geen generieke meting, HIC blijft B20 · B. meetwaarde + eenheid op resultaat · C. één `iok_meting` met soort | **A** | Volgt de bron; geen bron vult een gemeten waarde in; een HIC-meting heeft twee waarden en past niet in "waarde + eenheid". | B53 |
| 2.4 | Q22: het terrein bij een jaarlijkse controle? | A. altijd terreinbeoordeling met checklist, enkel besluit verplicht · B. geen checklist, enkel besluitveld | **A** | Model blijft gelijk, wat IOK ook antwoordt; een terreingebrek heeft altijd een controlepunt om aan te hangen. | B54 |
| 2.5 | Q18: tellen M en N mee voor "1 NOK = hoofdstuk NOK"? | A. geen uitzondering · B. ja/nee-kolom op het hoofdstuk, standaard ja · C. enkel waarschuwen | **B** | Standaard streng (vaste eis), maar instelbaar zonder modelwijziging. | B55 |

## Herlezing van ronde 1 en 2

Wat bij het nalezen niet klopte of ontbrak, en hoe het is opgelost:

1. **B46 veronderstelde locaties die de bron niet bevat.** Opgelost met een laadregel: 635 rijen → 635 terreinen, splitsen pas na IOK (B56).
2. **B47 gaf de groep een bestuur terwijl het terrein er ook één heeft** (dubbel pad). Bewust behouden, met een consistentieregel (B56).
3. **B40 zei "alle punten verplicht" bij risicoanalyse**, maar skate-hoofdstukken hebben geen punten. Nu: alle controlepunten zonder kinderen (B53).
4. **De invulplicht van B40 gold stilzwijgend ook voor het terrein**, terwijl de hoofdstukken van het terreinblad geen status hebben. Nu apart geregeld (B54).
5. **Telling in velddekking §16.2**: F heeft 4× nul, niet 6× (nageteld tegen de bron).

## Ronde 3 – bevriezen, archief, eenheden

_Door Dries gedelegeerd: de keuzes zijn voorstellen van Claude en kunnen herzien worden._

| # | Vraag | Opties | Keuze | Waarom | Beslissing |
|---|---|---|---|---|---|
| 3.1 | Q10: hoe bevriezen we wat in het verslag staat? | A. alles kopiëren naar snapshot-tabellen · B. enkel onveranderlijke versies · C. hybride: versies voor sjablonen, kopiekolommen voor stamgegevens · D. enkel de PDF als bevroren bron | **C** | B werkt niet voor bestuur/terrein/toestel (geen versies) en D maakt het financiële overzicht (historische eenheden) onmogelijk. A verdubbelt het model. | B57 |
| 3.2 | Wanneer wordt gekopieerd, en waaruit komt de PDF? | A. bij aanmaak, PDF uit het dossier · B. bij Definitief (D3.9), PDF uit de stamgegevens | **A** | PDF en bevroren gegevens zijn dan per definitie gelijk; de inspecteur corrigeert in het dossier zonder stamgegevens aan te raken (B08). | B57 |
| 3.3 | Blijft `iok_toesteltype` geversioneerd (B26)? | A. ja · B. nee, kopie op de beoordeling volstaat | **B** | Elke typeversie zou ±5.250 toestellen moeten omhangen; de kopie dekt de historiek al. | B58 (herziet B26) |
| 3.4 | Standaardzinnen: verwijzen of kopiëren? | A. lookup naar een geversioneerde zin · B. tekst kopiëren + optionele herkomst | **B** | De inspecteur mag de tekst aanpassen (B18); versies van zinnen worden overbodig. | B59 |
| 3.5 | Q13: archieflocatie voor een dossier dat niet via D1.2 ontstaat? | A. enkel in D1.2 · B. bij het aanmaken van het record + vangnet in D3.5 | **B** | Elk dossier krijgt een locatie, hoe het ook ontstaat. | B60 |
| 3.6 | Q12: eenheden per bestuur berekend of een afgesproken getal? | A. berekend uit bevroren eenheden · B. kolom `account.iok_eenheden` | **A** | D4.5 leest al de bevroren eenheden; een kolom kan later nog zonder andere wijzigingen. | B61 |

## Gevolgen voor stap 4

- **Nieuwe tabellen:** `iok_terreingroep` (B47), `iok_checklistonderdeel` (B51), koppeling beoordeling ↔ onderdeel (B51). `iok_type_checklist` wordt type ↔ onderdeel.
- **Nieuwe kolommen:** `iok_legacyid` (B49); "altijd van toepassing" op het onderdeel (B52); norm en soort op de checklist (B52); toelichtingstekst op het controlepunt (B53); "NOK bepaalt hoofdstukresultaat" (B55); kopiekolommen op dossier en beoordeling (B57); eenheden op toestel en beoordeling (B58); status Concept/Actief/Vervangen op de checklist (B57).
- **Vervalt:** versies van `iok_toesteltype` (B58) en `iok_standaardtekst` (B59); een aparte `iok_meting` (B53).
- **CRUD-matrix (gedaan):** kolommen `iok_terreingroep` en `iok_checklistonderdeel`; D4.2 zonder C+X op type en standaardtekst; D1.2–D1.4 vullen de kopiekolommen; D3.5 "C indien ontbreekt" op de archieflocatie.
- **Nagekeken (B62):** inactief record = alleen-lezen in de app, niet voor flows/API; alternatieve sleutel standaard hoofdletterongevoelig (testen in de eigen omgeving); SharePoint-map ontstaat standaard pas bij het openen van het tabblad Documenten → flow op "dossier aangemaakt".
- **CRUD-matrix is bijgewerkt** (sectie "Wijzigingen na stap 3").
