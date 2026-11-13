# Startprompt: herziening Dataverse-datamodel (ERD) IOK

Ik werk aan een studentenproject (bachelor, vak *Enterprise solutions: Microsoft 365 & Power Platform*, Thomas More) voor de klant **IOK**: de veiligheidsinspecties van speelterreinen en speeltoestellen digitaliseren in Microsoft 365 / Power Platform. We zijn een team van vier en bouwen een proof of concept voor een IOK-jury.

Het procesmodel (BPMN) is afgesloten. Er bestaat een **eerste versie van het datamodel (v2)**, maar die is gebaseerd op een oudere procesvariant. Voordat we iets in Dataverse bouwen, wil ik het datamodel **volledig herbekijken en verbeteren tot een v3** die klaar is om te bouwen.

**In deze chat bouwen we nog niets in Dataverse. We starten met overleggen; tekenen of uitwerken doen we pas als ik dat zeg.**

---

## Hoe ik wil werken

- Antwoord in het **Nederlands**.
- Stel bij elke stap eerst de vragen die belangrijk zijn, en wacht op mijn antwoord als een keuze echt van mij is.
- Als ik zeg "enkel overleggen" of "nog niet tekenen", dan bespreken we alleen.
- Baseer je op de bijlagen. Wat er niet in staat, is een vraag voor mij of voor IOK, geen aanname.
- Vermeld bij een voorstel waarop het steunt: BPMN-stap, bronbestand, cursusdia of beslissing hieronder.

---

## Vaste eisen en beslissingen

- Alle gegevens in **Dataverse-tabellen**, geen SharePoint-lijsten (uitdrukkelijke eis van de klant). SharePoint alleen als archief voor PDF's en foto's.
- De app werkt **offline** op een tablet (mobile offline profile) en ook op een laptop. Flows draaien niet offline: wat nodig is, wordt vooraf klaargezet en na synchronisatie verwerkt.
- **Eén verslag per terrein = één PDF**, automatisch gegenereerd en gemaild naar het bestuur. Na verzending is een versie vergrendeld; een correctie maakt een nieuwe versie en de oude blijft bewaard.
- **Indienststelling** als conformiteit aantoonbaar is; **risicoanalyse** zonder aantoonbare conformiteit of bij een herplaatst toestel. Skate volgt EN 14974. Een combinatietoestel krijgt meerdere Deel 2-checklists; twee schommels zijn één onderdeel.
- **Eén opmerking per controlepunt**; 1 NOK maakt het hoofdstuk NOK.
- **Foto's:**
  - elk toestel heeft een foto in het verslag, ook als het conform is;
  - een nieuwe foto vervangt de oude in het verslag;
  - de oude foto blijft bewaard bij het toestel.
- **Jaarlijkse controle:** de gegevens van vorig jaar worden als concept overgenomen. Een overgenomen antwoord is nog geen nieuwe inspectie.
- **HIC-meting** alleen bij een niet-conforme valondergrond.
- **Besluiten en standaardzinnen** komen uit een tabel.
- **Codes** van terreinen en toestellen zijn vanaf nu uniek. In de oude Excel kwamen 31 codes dubbel voor.
- **Kosten:** premium connectors mogen, maar de kost moet minimaal blijven. Financiering via eenheden valt buiten het proces; er is wel een overzicht van eenheden per bestuur.
- **Integratie:** later moet een koppeling met besturen mogelijk zijn via de Dataverse Web API.

---

## Het finale procesmodel

De details staan in de bijgevoegde BPMN-bestanden en in `IOK_BPMN_uitleg.pdf`. Rollen: **Inspecteur, Systeem, Beheerder**, met het **lokaal bestuur/uitbater** als externe partij.

**Hoofdproces (één inspectiedossier voor één terrein)**
- **D1 Dossier voorbereiden:**
  - bestuur, terrein en inspectiescope kiezen;
  - bruikbare historiek als concept overnemen of lege checklists aanmaken;
  - offlinepakket klaarzetten en controleren.
- **Terrein controleren.**
- **D2 Toestel controleren (herhaald per toestel):**
  - toestel, norm en beoordelingsbasis vaststellen;
  - *Toestel nog aanwezig?* (V4);
  - *Eerste controle?* en *Conformiteit aantoonbaar?*: indienststelling of uitgebreide risicoanalyse; anders de jaarlijkse controle van alle punten;
  - per tekortkoming norm, toelichting, foto's en risicobeoordeling vastleggen;
  - melding bij **acuut gevaar** (V3).
- **D3 Synchroniseren en verslag afwerken:**
  - synchroniseren, met een herstelpad bij een conflict;
  - volledigheidscontrole, en het enige inhoudelijke controlemoment: de inspecteur kijkt na en dient in;
  - PDF genereren, met een foutpad;
  - preventiedocument bij een nieuwe uitgebreide risicoanalyse (V5);
  - definitieve versie **vergrendelen** met data- en fotoreferenties.
- **Afsluiting:**
  - PDF-rapportpakket verzenden, met een herstelpad bij een verzendfout;
  - verzendstatus registreren;
  - verwijderde toestellen deactiveren (V4).

**D4 Ondersteunende processen**
- Intake van nieuwe terreinen en toestellen via een sjabloonbijlage, met herinneringen (V1, V2).
- Correcties na verzending met een nieuwe versie (V6).
- Stamgegevens wijzigen, met de versie vastgelegd.
- Probleemoverzicht en financieringsoverzicht (nice to have).

**Open vragen aan IOK (V1–V11)**
- V1 intake via sjabloon;
- V2 herinneringen;
- V3 acuut gevaar;
- V4 verdwenen toestel;
- V5 preventiedocument bij indienststelling met gebreken;
- V6 correcties en versies;
- V7 indienststelling per normhoofdstuk;
- V8 conformiteitsdocumenten;
- V9 risicofactoren, scoretabel en HIC;
- V10 rollen en wie terreinen registreert;
- V11 offline werken en gelijktijdige wijzigingen.

De antwoorden uit de feedbacksessie van 13 november zitten in bijlage, voor zover ik ze heb. Wat nog niet beantwoord is, moet als optioneel of uitbreidbaar in het model staan.

---

## Het datamodel v2 (vertrekpunt)

Zie bijlage. Het bevat 17 eigen tabellen met prefix `iok_` plus Account, Contact en E-mail:

| Groep | Tabellen |
| --- | --- |
| Stamgegevens | doelgroep, toestelcategorie, toestelsoort, speelterrein, speeltoestel |
| Sjablonen | checklist, hoofdstuk, controlepunt, standaardtekst |
| Inspectie | verslag, analyse, beoordeling, opmerking, foto, hicmeting |
| Communicatie | aanvraag, correctievraag |

**Al bekende zwakke plekken:**
- Het is een logisch model. Tekstlengtes, decimalen, statusredenen, een volledige lijst van sleutels en de namen van de N:N-tabellen ontbreken.
- Het gaat uit van een **weekplanning** die niet meer in het finale proces zit.
- Het mist gegevens voor nieuwe stappen in het finale proces:
  - status van het offlinepakket;
  - synchronisatieconflicten;
  - PDF-fout en verzendstatus of verzendfout;
  - versies van stamgegevens;
  - het probleemoverzicht.
- Verslag en correctievraag verwijzen in beide richtingen naar elkaar; één richting volstaat waarschijnlijk.
- De HIC-meting hangt zowel aan het verslag als aan de opmerking.
- De unieke terreincode botst met de dubbele codes in de oude Excel.
- Open ontwerpvragen:
  - Wordt adres een eigen tabel?
  - Hoe gebeurt het versiebeheer van verslagen precies?
  - Wat gaat er offline mee?

---

## Werkwijze die ik voorstel

1. **Proces naast data.** Maak per BPMN-stap een overzicht van welke gegevens hij leest, aanmaakt of wijzigt (een CRUD-matrix: proces × tabel). Zo zien we wat ontbreekt en wat overbodig is.
2. **Velddekking uit de bronbestanden.** Inventariseer de velden in de Excel-checklists, de ingevulde voorbeelden, het Word-verslag en de Excel-overzichten. Wijs elk veld toe aan een kolom, of markeer het als ontbrekend of bewust weggelaten.
3. **Ontwerpvragen beslissen,** met per vraag de opties, voor- en nadelen en een voorstel. Denk aan adres, versies, HIC, de V-afhankelijke tabellen, statussen en historiek van foto's.
4. **Tabel per tabel herzien,** daarna relaties en verwijdergedrag, eigenaarschap, beveiligingsrollen (inspecteur, beheerder) en het mobile offline profile.
5. **Toetsen aan de cursus (les 4b Dataverse)** en aan wat de lector op het examen vraagt: een helder en verdedigbaar Dataverse-model.
6. **Pas daarna de technische specificatie:** schemanamen, types, lengtes, verplicht of niet, standaardwaarden, keuzelijsten, statusredenen, alternatieve sleutels en N:N-namen. Onderscheid wat achteraf niet meer te wijzigen is: prefix, schemanaam, eigenaarschap, kolomtype.

**Gewenst resultaat op het einde**
- Datamodel v3 als document, met een ERD-diagram en een changelog ten opzichte van v2.
- De CRUD-matrix en de velddekking als bijlage.
- Een lijst van nog openstaande vragen voor IOK.
- Een machineleesbare specificatie (JSON of YAML), als basis voor een bouwscript via de Dataverse Web API in een volgende stap.

---

## Bijlagen

- Finaal procesmodel: `IOK_BPMN_uitleg.pdf`, `IOK_02_ToBe_samengevoegd.bpmn`, `IOK_03_ToBe_ondersteunende_processen.bpmn`, `IOK_01_AsIs.bpmn`
- Datamodel v2: `Dataverse_datamodel_IOK_v2.md` (of `.docx`) en `Dataverse_datamodel_IOK_v2_ERD.png`
- Feedback van IOK van 13 november (notities of transcriptie) en de transcriptie van de kick-off
- Projectopdracht: `Microsoft_365__Power_Platform_Project_IOK_2026-2027_NL_1.pdf`
- Lege sjablonen: indienststelling, risicoanalyse toestellen, skate en terrein (versie 2022)
- Ingevulde voorbeelden: verslaggeving indienststelling schommel, indienststelling evenwichtsparcours, risicoanalyse terrein, samengesteld verslag nieuw speelterrein, jaarlijkse controle De Bogaard
- Overzichten: bestaande speelterreinen en soorten speeltoestellen
- Cursus: les 4b Dataverse (en 4c model-driven apps, 4d co-ownership)

Begin met stap 1, en stel eerst de vragen die je nodig hebt.
