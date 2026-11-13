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

- **Ingebouwde Dataverse-tabellen hergebruiken** waar ze passen (Account, Contact, Gebruiker, Team, E-mail, Taak, SharePoint-documentlocatie, …). Alle **eigen tabellen, kolommen en keuzelijsten krijgen het prefix `iok_`**, ook eigen kolommen op standaardtabellen (B01, B02).
- Alle gegevens in **Dataverse-tabellen**, geen SharePoint-lijsten (uitdrukkelijke eis van de klant). SharePoint alleen als archief voor PDF's en foto's.
- De app werkt op een **tablet (Samsung Galaxy 5G, Android)** en op een laptop. **Offline is volgens IOK niet meer nodig** (feedback 13/11); het is voor mij een mogelijke uitbreiding, maar **niet bepalend voor het ERD** (B04).
- **Eén verslag per terrein = één PDF**, automatisch gegenereerd, samen met een **samenvatting van de preventiemaatregelen** (volgens IOK zeer belangrijk). De inspecteur kan de PDF nakijken en aanpassen vóór verzending, en **verstuurt ze zelf** (geen automatische verzending, B05). De verzendstatus wordt geregistreerd.
- **Versiebeheer op basis van de controledatum** (B06): de definitieve PDF, de controledatum en de historische dossiergegevens worden bewaard.
- **Stamgegevens** (moederdata) wijzigen **zonder terugwerkende kracht**: een wijziging maakt een nieuwe versie en historische inspecties blijven ongewijzigd (B07). Maar **één bevoegde beheerder** mag stamgegevens wijzigen (B08).
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

Bron: `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md` (finaal, verwerkt de feedback van 13 november; zie `01_context/feedback/`). `IOK_02_ToBe` is een **oudere** versie met offline/synchronisatie en geldt niet meer. Rollen (lanes): **Inspecteur, Systeem, Bevoegde beheerder**, met het **lokaal bestuur/uitbater** als externe partij.

**Hoofdproces (één inspectiedossier voor één terrein)**
- **D1 Dossier voorbereiden:** bestuur, terrein en inspectiescope kiezen; nieuw inspectiedossier met controledatum en uniek ID; bij een jaarlijkse controle bruikbare historiek of maatregelen als concept overnemen, anders lege toepasselijke checklists klaarzetten.
- **Terrein controleren** en bevindingen registreren.
- **D2 Toestel controleren (per toestel):** toestel, norm en beoordelingsbasis vaststellen; eerste controle? → conform: indienststelling en plaatsing beoordelen / niet conform: uitgebreide risicoanalyse; anders jaarlijks alle toepasselijke controlepunten; bij tekortkomingen norm, toelichting, foto's en risicobeoordeling vastleggen; **besluit en benodigde preventiemaatregelen** vastleggen.
- **D3 Verslag en preventiesamenvatting afwerken en bewaren:** dossier en controledatum nakijken; systeem valideert verplichte gegevens, risico's en foto's; **samenvatting preventiemaatregelen** voor terrein en toestellen; rapport-PDF en preventiesamenvatting **met controledatum** genereren (met foutpad); inhoudelijk nakijken en zo nodig **PDF corrigeren** of na dossiercorrectie opnieuw maken; definitieve PDF, controledatum en historische dossiergegevens bewaren (met foutpad).
- **Afsluiting:** inspecteur verstuurt de definitieve PDF(s) **handmatig** naar het bestuur; verzendstatus registreren (met herstelpad).

**D4 Ondersteunende processen**
- Stamgegevens en vaste teksten bijwerken (bevoegde beheerder) → nieuwe stamgegevensversie, historische inspecties behouden, wijziging geldt voor toekomstig gebruik.
- Maatregelenoverzicht: preventiemaatregelen en tekortkomingen per bestuur samenvatten.
- Financieel overzicht: **periode kiezen** (laatste 3 maanden of begin- tot einddatum) → uitgevoerde controles en historische eenheden naar Excel.

**Vragen uit een vorige BPMN-versie (V1–V11)** zitten niet meer als aparte stappen in het finale BPMN (o.a. intake via sjabloon, acuut gevaar, verdwenen toestel, risicofactoren/scoretabel/HIC). Waar ze het datamodel raken, modelleren we ze als **optioneel of uitbreidbaar**, en we nemen ze op in `02_werk/open_vragen.md`. Offline (V11) valt weg (B04).

---

## Het datamodel v2 (vertrekpunt)

Bron: `01_context/datamodel_v2/IOK_erd_v2.md` (omgezet uit `00_bronnen/datamodel_v2/IOK_erd_v2.drawio`). Het is een **relationeel, logisch model** met 13 tabellen en 15 relaties, nog zonder Dataverse-namen of -types en zonder prefix:

| Groep | Tabellen |
| --- | --- |
| Stamgegevens | BESTUUR, SPEELTERREIN, SPEELTOESTEL, TOESTELTYPE, INSPECTEUR |
| Sjablonen | CHECKLIST, CONTROLEPUNT (hiërarchisch via ouder_id), TOESTEL_CHECKLIST (N:N) |
| Inspectie | CONTROLE, BEOORDELING (terrein of toestel), RESULTAAT (OK/NOK/nvt + kans/blootstelling/impact), FOTO, CONTROLEVERSIE (PDF, versie, verzonden_op) |

**Te bekijken bij de herziening (vaststellingen, geen beslissingen):**
- BESTUUR en INSPECTEUR zijn eigen tabellen; mogelijk passen de standaardtabellen Account en Gebruiker (B02).
- Adresvelden staan los op BESTUUR en SPEELTERREIN.
- Er is nog geen plek voor: besluiten en standaardzinnen, (samenvatting van) preventiemaatregelen, HIC-meting, versies van stamgegevens, verzendstatus naast `verzonden_op`, en de foto-historiek per toestel.
- Doelgroep en toezicht zijn vrije tekst op zowel terrein als toestel; `code` is niet verplicht en niet uniek.
- CONTROLE → CONTROLEVERSIE: label (1 : 0..M) en pijlpunt (1..N) spreken elkaar tegen.
- De beschrijving van v2 in een eerdere versie van deze prompt (17 `iok_`-tabellen) hoort niet bij dit diagram en vervalt.

---

## Werkwijze die ik voorstel

1. **Proces naast data.** Maak per BPMN-stap een overzicht van welke gegevens hij leest, aanmaakt of wijzigt (een CRUD-matrix: proces × tabel). Zo zien we wat ontbreekt en wat overbodig is.
2. **Velddekking uit de bronbestanden.** Inventariseer de velden in de Excel-checklists, de ingevulde voorbeelden, het Word-verslag en de Excel-overzichten. Wijs elk veld toe aan een kolom, of markeer het als ontbrekend of bewust weggelaten.
3. **Ontwerpvragen beslissen,** met per vraag de opties, voor- en nadelen en een voorstel. Denk aan adres, versies, HIC, de V-afhankelijke tabellen, statussen en historiek van foto's.
4. **Tabel per tabel herzien,** daarna relaties en verwijdergedrag, eigenaarschap, beveiligingsrollen (inspecteur, beheerder). (Een mobile offline profile is niet nodig, B04.)
5. **Toetsen aan de cursus (les 4b Dataverse)** en aan wat de lector op het examen vraagt: een helder en verdedigbaar Dataverse-model.
6. **Pas daarna de technische specificatie:** schemanamen, types, lengtes, verplicht of niet, standaardwaarden, keuzelijsten, statusredenen, alternatieve sleutels en N:N-namen. Onderscheid wat achteraf niet meer te wijzigen is: prefix, schemanaam, eigenaarschap, kolomtype.

**Gewenst resultaat op het einde**
- Datamodel v3 als document, met een ERD-diagram en een changelog ten opzichte van v2.
- De CRUD-matrix en de velddekking als bijlage.
- Een lijst van nog openstaande vragen voor IOK.
- Een machineleesbare specificatie (JSON of YAML), als basis voor een bouwscript via de Dataverse Web API in een volgende stap.

---

## Bijlagen

Lees de markdownversies in `01_context/`, niet de originelen in `00_bronnen/` (zie de bestandskaart in AGENTS.md).

- Projectopdracht: `01_context/Projectopdracht_IOK.md`
- Procesmodel: `01_context/bpmn/IOK_02_ToBe_uitgeklapt_aangepast.md` (finaal); AsIs en leesversies als achtergrond; `IOK_02_ToBe` is verouderd
- Datamodel v2: `01_context/datamodel_v2/IOK_erd_v2.md`
- Feedback IOK 13 november: `01_context/feedback/feedback_IOK_2026-11-13.md` (kick-off: _nog toe te voegen_)
- Lege sjablonen: `01_context/docs/` → Indienststelling versie 2022, Risicoanalyse toestellen versie 2022, risicoanalyse skate toestellen versie 2022, risicoanalyse terrein versie 2022
- Ingevulde voorbeelden: `01_context/docs/` → A_Verslaggeving Indienststelling Schommel, B_Indienststelling Evenwichtsparcours, B_risicoanalyse terrein, B_Samengesteld verslag nieuw speelterrein, C_2026 - Jaarlijkse controle De Bogaard
- Overzichten: `01_context/docs/` → Overzicht bestaande speelterreinen, Overzicht soorten speeltoestellen
- Keuzelijsten uit de Excel-sjablonen: `01_context/keuzelijsten/`
- Cursus les 4b/4c/4d: `01_context/cursus/` — _nog toe te voegen_

We beginnen met **stap 0: de intake** (zie het commando /intake): vragen in rondes tot de bedoeling duidelijk is, afgesloten met een teach-back. Nog niets schrijven.
