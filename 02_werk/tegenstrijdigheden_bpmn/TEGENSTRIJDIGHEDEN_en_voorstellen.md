# IOK Speelterreinen — tegenstrijdigheden tussen BPMN, IOK-feedback en datamodel v3

Datum: 16 november 2026
Gebaseerd op: `IOK Speelterreinen — datamodel v3, volledig overzicht 1.pdf`, `IOK_02_ToBe_uitgeklapt_aangepast.bpmn` en de feedback van het gesprek met IOK.

**Uitgangspunt:** de BPMN is correct en leidend. Waar het model afwijkt, past het model aan.
**Niet opgenomen (bewust, tot er meer duidelijkheid is):** de opmerking van IOK "moederdata kan maar 1 persoon veranderen". Wat er precies onder valt, is nog onduidelijk.

Per punt staat een voorstel. Elk aangenomen voorstel krijgt een B-nummer (vanaf B89) in `BESLISSINGEN.md`, en de wijziging gaat via `datamodel_v3.md` en niet rechtstreeks in spec of Dataverse.

---

## A. Echte tegenstrijdigheden

### 1. Jaarlijkse controle: alle punten beoordelen of alleen het besluit?
- **BPMN (`D2_annual`):** "Jaarlijks opnieuw alle toepasselijke punten beoordelen, ook bij overgenomen gegevens."
- **Model (regel 1):** bij een jaarlijkse controle is alleen het besluit verplicht en zijn punten enkel nodig bij afwijking.
- **Raakt:** regel 1, Q27, regel 9 (historiek overnemen).
- **Voorstel:** vraag IOK wat "beoordelen" betekent: bekijken of ook vastleggen? Als het vastleggen is, wordt regel 1 voor jaarlijks gelijk aan indienststelling: elk punt of hoofdstuk heeft een antwoord. Overgenomen resultaten (`iok_isovergenomen = ja`) moeten dan bevestigd worden, en dat gebeurt al via regel 9. Dit is een bedrijfsregel en geen structuurwijziging.

### 2. Moment waarop het dossier op slot gaat
- **BPMN (D3):** correcties van brongegevens en rechtstreekse PDF-correcties zijn toegestaan tot de verzending. Bij een gewijzigd brongegeven wordt de PDF opnieuw gemaakt (`D3_correct`). Pas daarna wordt de definitieve PDF bewaard (`D3_archive`).
- **Model (regel 4 en 15):** afronden zet het dossier op slot. Heropenen kan pas na verzending.
- **Probleem:** als het slot al bij "afgerond" valt, kan de inspecteur tijdens het nakijken van de PDF geen brongegevens meer corrigeren.
- **Voorstel:** laat het slot vallen bij *definitief maken en bewaren* van de rapportversie (`D3_archive`), niet bij het genereren van de PDF. Tot dan blijft het dossier op "In uitvoering". Regel 15 (heropenen na verzending) blijft als aanvulling. Zie ook punt 12.

### 3. Rechten van de inspecteur op stamgegevens
- **BPMN (`D2_identify`):** de inspecteur kan zo nodig een nieuw toestel registreren. Beschermde norm- en standaardteksten blijven bij bevoegd beheer.
- **Model (rechtenmatrix):** de inspecteur heeft alleen *lezen* op terreingroep, terrein, toestel en toestelcode.
- **Raakt:** Q06.
- **Voorstel:** geef de inspecteur *maken* en *wijzigen* (Org) op `iok_speeltoestel` en `iok_toestelcode`. Voor terrein en terreingroep: zie punt 9. Toesteltype, checklist, onderdeel, controlepunt en standaardtekst blijven alleen-lezen. Dit is een wijziging in `spec.yaml` onder `rollen`. De structuur verandert niet.

### 4. Preventiesamenvatting: apart bestand of onderdeel van het rapport?
- **BPMN (`D3_prev`):** "De precieze presentatie als onderdeel van hetzelfde rapport of apart document is nog niet bevestigd. De taak legt geen verplicht apart PDF-bestand op."
- **Model:** `iok_documenttype` = Rapport of Preventiesamenvatting, en het PDF spreekt van "een aparte preventiesamenvatting".
- **Voorstel:** het model blijft geschikt, want het is een documenttype. Pas wel de formulering in het PDF aan naar "preventiesamenvatting (apart document of onderdeel van het rapport, nog te bevestigen met IOK)". IOK noemt de samenvatting "zeer belangrijk", dus de generatie moet altijd gebeuren, ook zonder maatregelen. In dat geval vermeldt het overzicht dat expliciet.

---

## B. Kleinere afwijkingen en gaten

### 5. Foto's valideren
- **BPMN (`D3_validate`):** valideert "verplichte gegevens, risico's en foto's".
- **Model:** Q02 gaat ervan uit dat foto's niet verplicht zijn.
- **Voorstel:** bevestig bij IOK wanneer een foto verplicht is. Waarschijnlijk is dat bij een tekortkoming met risicoanalyse, en bij een overzichtsfoto per terrein of toestel.

### 6. Tekortkoming zonder controlepunt kan geen risicoscore krijgen
- **BPMN (`D2_record`):** een lus over vastgestelde tekortkomingen, met kans, blootstelling en impact per tekortkoming.
- **Model:** de risicokolommen staan op `iok_resultaat`, dat een controlepunt verplicht (`iok_controlepuntid` is verplicht).
- **Voorstel:** bevestig dat elke tekortkoming aan een controlepunt hangt. Is dat niet zo, dan moeten de risicokolommen ook op `iok_maatregel` komen, of moet `iok_controlepuntid` optioneel worden. Dat is een migratie, dus eerst bevestigen.

### 7. Risicodrempels zijn nog niet bevestigd
- **BPMN (`D2_record`):** "Rekentabel, labels en drempels met IOK bevestigen. Geen verzonnen formule."
- **Model:** de drempels 20, 70, 160 en 320 staan vast in `iok_risicoklasse`. Zie ook Q24 (grenswaarde 70).
- **Voorstel:** laat IOK de rekentabel en de grenzen bevestigen en noteer de bron bij B82.

### 8. Conformiteit van het attest heeft geen status
- **BPMN (`D2_identify`, `D2_conform`, O6):** bij onduidelijkheid worden eerst bewijsstukken opgevraagd en beoordeeld. Een ontbrekend attest betekent niet automatisch niet-conform. Daarna volgt de poort "Beoordeeld als conform?", die kiest tussen indienststelling en risicoanalyse.
- **Model:** alleen een tekstveld `iok_attest`.
- **Probleem:** er is geen plek voor de uitkomst "conform, niet conform of onduidelijk". Het besluit "Conform / Niet conform" op de beoordeling heeft een andere betekenis, wat verwarrend is.
- **Voorstel:** overweeg een keuzekolom op `iok_beoordeling`, bijvoorbeeld `iok_attestbeoordeling` (Conform, Niet conform, Onduidelijk). Beslis eerst met IOK welke bewijsstukken geaccepteerd worden. Hernoem eventueel het besluit om verwarring te voorkomen.

### 9. Mag de inspecteur ook een terrein of terreingroep aanmaken?
- **BPMN:** noemt alleen een nieuw toestel.
- **Model:** zie punt 3.
- **Voorstel:** vraag dit aan IOK. Tot dan blijft terrein en terreingroep voor de inspecteur alleen-lezen.

### 10. Code van een nieuw toestel invoeren
- **Model:** codes worden bij het laden genormaliseerd (hoofdletters). De sleutel is hoofdletterongevoelig. Regel 11 eist precies één hoofdcode per toestel, gelijk aan `iok_speeltoestel.iok_code`.
- **Probleem:** door de inspecteur ingevoerde codes worden niet automatisch genormaliseerd.
- **Voorstel:** voeg een flow of plug-in toe die bij het aanmaken de code naar hoofdletters zet, de `iok_toestelcode` met `iok_ishoofdcode = ja` aanmaakt en de uniekheid controleert.

### 11. Verzendproblemen laten geen spoor na
- **BPMN (`TOBE_00_retry`):** de inspecteur lost een verzendprobleem op en controleert de status om dubbel verzenden te voorkomen.
- **Model:** er zijn bewust geen kolommen voor verzendpogingen.
- **Voorstel:** laat dit zo, want de BPMN legt geen pogingenteller op. Noteer het wel als bewuste keuze. Het volstaat dat de inspecteur `iok_verzondenop` en `iok_verzondenaan` invult na een geslaagde verzending.

### 12. Correctie na verzending
- **Model (regel 15):** nieuwe rapportversie, vorige wordt "Vervangen", dossier wordt heropend.
- **BPMN:** beschrijft alleen correcties vóór verzending.
- **Voorstel:** laat regel 15 staan als uitbreiding, maar vermeld in het PDF dat de BPMN dit niet beschrijft.

### 13. Controleomvang kiezen heeft geen eigen veld
- **BPMN (`D1_select`):** "Bestuur, terrein en inspectiescope kiezen".
- **Model:** de scope volgt impliciet uit welke beoordelingen aangemaakt worden (regel 8 en 10).
- **Voorstel:** geen wijziging. Noteer in het PDF dat de scope impliciet is, met als uitzondering dat toestellen "Buiten gebruik" niet meekomen.

### 14. "Nieuwe stamgegevensversie vastleggen" (D4)
- **BPMN (`D4_version`):** suggereert versiebeheer van stamgegevens.
- **Model (B57, B58):** alleen checklists zijn geversioneerd. De rest werkt met bevroren kopieën in dossier en beoordeling.
- **Voorstel:** dit voldoet aan de eis "geen terugwerkende kracht, historisch blijven resolven". Leg in het PDF uit dat bevriezen via kopieën de versie van stamgegevens vervangt.

### 15. Financieel overzicht: wat telt als "uitgevoerde controle"?
- **BPMN (`D4_finance`):** "Alleen uitgevoerde controles tellen, met de eenheden die toen golden."
- **Model:** niet gedefinieerd.
- **Voorstel:** leg vast dat alleen dossiers met status Afgerond tellen, gefilterd op `iok_controledatum`. Beslis ook of toestellen met besluit "Niet beoordeeld" meetellen voor de eenheden. Gebruik `iok_beoordeling.iok_eenheden` als bron, zoals regel 16.

---

## C. Interne fouten of onduidelijkheden in het PDF

| # | Wat | Voorstel |
|---|---|---|
| 16 | De rechtenmatrix geeft de inspecteur alleen *lezen* op `iok_checklistonderdeel`. De tekst eronder zegt dat *Toevoegen* op beide tabellen nodig is voor de N:N. | Corrigeer de matrix: Toevoegen (Org) op `iok_checklistonderdeel` voor de inspecteur, zonder wijzigings- of verwijderrechten. |
| 17 | De ERD-tekening zegt "18 tabellen", de tekst zegt 23. | Vermeld bij de tekening dat ze vereenvoudigd is, of pas het getal aan. |
| 18 | De tekst zegt dat `iok_beoordeling` 24 kolommen heeft. In de tabel tel ik er 23. | Tel opnieuw na en corrigeer. |
| 19 | `iok_hicmeting` is "alleen bij toestelbeoordelingen", maar er is geen regel die dat afdwingt. | Voeg een bedrijfsregel toe. |
| 20 | Q06 staat als "hoge prioriteit, proces staat stil". | Update zodra punt 3 en 9 beslist zijn. |
| 21 | Het PDF verwijst naar "sectie 2 tot en met 5", "11 tot en met 17" en "sectie 12", maar heeft geen genummerde secties. | Nummer de secties of pas de verwijzingen aan. |
| 22 | Het PDF zegt dat teamgenoten in dezelfde tenant "ThomasMoreStudent" zitten. | Controleer per teamlid of het schoolaccount in die tenant zit. |

---

## D. Nieuw uit de feedback van IOK
23. **Tablet: Samsung Galaxy 5G (Android).** Het PDF noemt dit niet. Het is relevant voor de keuze canvas of model-driven (voorlopig advies: canvas-app met tabletlayout voor het invulscherm), voor de camera en voor de licentie. Het exacte tabletmodel en de Android-versie moeten nog bevestigd worden. Zonder offline werken heeft de tablet altijd verbinding nodig, wat op een speelterrein een praktisch risico is.

---

## E. Vragen aan IOK (bundel)
1. Jaarlijkse controle: moeten alle punten vastgelegd worden of alleen afwijkingen? (punt 1)
2. Apart PDF-bestand voor de preventiesamenvatting of onderdeel van het rapport? (punt 4)
3. Wanneer is een foto verplicht? (punt 5)
4. Hangt elke tekortkoming aan een controlepunt? (punt 6)
5. Bevestiging van de rekentabel en drempels van het risico, inclusief grens 70. (punt 7)
6. Welke bewijsstukken gelden als conform en wie beslist erover? (punt 8)
7. Mag de inspecteur ook een terrein of terreingroep aanmaken? (punt 9)
8. Tellen toestellen met "Niet beoordeeld" mee in het financiële overzicht? (punt 15)
9. Tabletmodel en Android-versie. (punt 23)

---

## F. Prioriteit
1. **Eerst beslissen** (veranderen de werking): punt 1, 2 en 3.
2. **Daarna** (bevestiging of kleine aanpassing): punt 4, 6, 8 en 10.
3. **Daarna** (tekst en documentatie): de rest.
