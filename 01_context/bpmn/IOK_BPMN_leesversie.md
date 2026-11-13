IOK veiligheidskeuringen speelterreinen
BPMN As-Is en To-Be - uitwerking voor de feedbacksessie van 13 november 2026
Leesroute
Er zijn twee bewerkbare modellen: de huidige werking met Excel en Word, en een voorstel met Power
Apps, Dataverse, SharePoint en Power Automate. De hoofdtekeningen volgen één inspectiedossier
voor één speelterrein. De detailbladen D1, D2 en D3 werken de voorbereiding, de beoordeling per
toestel en de rapportage uit. D4 van de To-Be bevat stamgegevensbeheer en de twee optionele
overzichten.
De opdracht vraagt eerst het door de klant beschreven proces te modelleren en vervolgens
verbeteringen te bespreken. Twee modellen is daarom de gekozen opdeling; er is geen afzonderlijke
opdrachtregel die exact twee bestanden voorschrijft. De oorspronkelijke AI-bestanden zijn
vergelijkingsmateriaal, niet de basis voor onbevestigde klantafspraken.
Wat inhoudelijk vastligt
• Eerst het terrein, daarna alle te controleren toestellen. Elk toestel krijgt de passende controle: jaarlijks,
indienststelling bij aantoonbare conformiteit, of een uitgebreide risicoanalyse bij nieuw niet-conform
materiaal.
• Vorige verslagen en preventiemaatregelen zijn een vertrekpunt. De jaarlijkse beoordeling moet
opnieuw gebeuren; een gekopieerd antwoord is nog geen nieuwe inspectie.
• Elke tekortkoming krijgt normbepaling, toelichting, foto en risicobeoordeling. Voor skate geldt EN
14974; voor de gewone speeltoestellen EN 1176. De precieze rekentabel wordt niet verzonnen.
• Rapporten gaan als PDF naar het bestuur. Bij een nieuwe uitgebreide risicoanalyse hoort een extra
preventiemaatregelen-document. Niet ieder jaarlijks gebrek vereist daarom een apart preventie-PDF.
• Planning en standaard herstelopvolging worden niet door de app overgenomen. Het bestuur blijft
verantwoordelijk voor maatregelen en herstel.
De veldregistratie kan op kantoor worden afgewerkt. De To-Be heeft één inhoudelijk controlemoment
door de inspecteur, naast automatische technische validatie. Een verplichte tweede goedkeurder is niet
bevestigd.

Ontwerpkeuzes en bespreekpunten
Keuze To-Be voorstel en praktische grens
O1 Offline Een geselecteerd pakket met terrein, checklists, historiek en nodige foto’s vooraf downloaden.
voorbereiding Omvang en implementatie testen; geen claim dat SharePoint-foto’s vanzelf offline synchroniseren.
O2 Synchronisatie Lokale data behouden bij fouten of conflicten; expliciete herstelroute. Pas verder als gegevens én
foto’s volledig zijn gekoppeld.
O3 Eén De inspecteur kijkt het verslag op laptop na en dient het in. De automatische volledigheidscontrole
controlemoment vervangt geen inhoudelijke beoordeling.
O4 Versie en Rapportversie met gebruikte data- en fotoreferenties vóór verzending bewaren. Verzendfout
verzending herstellen en bestaande verzendstatus controleren om dubbels te voorkomen.
O5 Stamgegevens Bevoegd beheer van categorieën, normen en standaardteksten. Probleemoverzicht en Excel voor
en overzichten financiering blijven nice to have; geen automatische facturatie.
O6 Onduidelijke Ontbrekende of onduidelijke bewijsstukken eerst inhoudelijk laten beoordelen; niet automatisch
conformiteit gelijkstellen aan niet-conformiteit. Af te spreken met IOK.
Prioritaire vragen aan IOK
• Welke conformiteitsdocumenten volstaan en wat gebeurt er als een attest ontbreekt of onduidelijk is?
• Welke risicofactoren, scoretabel en drempels gelden precies? Wanneer is een aanvullende meting,
zoals HIC, vereist?
• Wie mag een speelterrein registreren of wijzigen, wat is het derde profiel, en wie mag definitieve
rapporten corrigeren?
• Hoe lang en met hoeveel foto’s moet men offline kunnen werken? Hoe worden gelijktijdige wijzigingen
afgehandeld?
• Hoe worden acute gevaren gemeld, via welk kanaal en aan wie? Er is geen vaste alarmdrempel of
onmiddellijke verzendplicht uit de bron afgeleid.
• Hoe verwerkt men een verdwenen toestel, correcties op een al verstuurd verslag en de bewaartermijn?
Geen automatische deactivering of verwijdering zonder afspraak.

Bronnen en controle
Bronhiërarchie
S01 is de primaire schriftelijke projectopdracht. S11 is de automatische transcriptie van het klantgesprek
met tijdstempels; deze bevat herkenningsfouten en vereist bij twijfel bevestiging. S12 is de automatische
transcriptie van de technische les. S02/S03 zijn afgeleide samenvattingen. De oudere
prompt/AI-uitwerking S04/S08 en de vier BPMN’s van het teamlid zijn niet als zelfstandig bewijs van
klanteisen gebruikt.
• S01 - Projectopdracht IOK 2026-2027 (NL).pdf, p.3 (analyse), p.7-8 (controles), p.8-9 (huidige werking), p.9-10 (verwachtingen
en randvoorwaarden).
• S11 - Notities klantgesprek IOK, 2 oktober 2026: 00:07-00:08 en 00:52-00:53 (veld en kantoor); 00:21-00:31 en 00:36 (controle
per toestel); 00:34-00:39 (rollen); 00:41-00:44 (historiek en gebreken); 00:45-00:46 (geen herstelopvolging); 00:54-00:55 en
01:09-01:11 (offline en planning); 01:01-01:09 (rapporten).
• S12 - Notities les M365 en SharePoint, 2 oktober 2026: 00:26-00:28 (Dataverse), 00:36-00:42 (foto-opslag en automatische
metadata), 00:43 (goedkeuringsflow niet gevraagd), 00:44-00:47 (portaal). S02/S03 ondersteunen dit als secundaire analyses.
• Bijlage C - C_2026 Jaarlijkse controle De Bogaard (algemeen).pdf, p.2: HIC-meetlegende. Onderbouwt dat HIC kan
voorkomen, niet dat dit een verplichte handeling bij elk gebrek is.
• Bijlagen A/B - Voorbeelden indienststelling en samengesteld verslag nieuw terrein: identiteit, normhoofdstukken, terrein plus
toestellen en verslagstructuur.
Controle van de vier aangeleverde varianten
BPMN_Finaal_1_Hoofdproces bevat onvolledige dataInputAssociation en lege conditionalEventDefinition-elementen;
BPMN_ToBe_variant_B_een_controlemoment bevat eveneens een lege conditie en een dataObject op een ongeldige
XML-positie. De twee andere bestanden zijn XSD-geldig. XSD-geldigheid bewijst echter niet dat de proceskeuzes kloppen. De
herinnering na vijf werkdagen, vaste weektrigger, algemene automatische deactivering en derde goedkeurder zijn niet als
klanteis overgenomen.
Validatie van deze uitwerking
De twee nieuwe bestanden zijn gecontroleerd tegen de officiële OMG BPMN 2.0 XML-schema’s. Verder: unieke IDs,
verwijzingen, scope van sequence flows, lane-toewijzing, bereikbaarheid, paden naar einde, gatewaylabels, herhalingen,
DI-coördinaten en grafische overlap. Ze zijn niet als uitvoerbare workflow bedoeld. De leesversie is een vectorweergave van
dezelfde modelcoördinaten; import in jouw specifieke modeler blijft een afzonderlijke compatibiliteitscontrole.
Normatieve notatie: https://www.omg.org/spec/BPMN/2.0.2/ en de gekoppelde BPMN20, Semantic, BPMNDI, DC en DI
XML-schema’s. Sequence flows blijven binnen de proces- en poolgrenzen; de aflevering aan het bestuur is een message flow.
Herhaling per toestel is sequentiële multi-instance.
Open de .bpmn-bestanden in een BPMN 2.0-modeler. Detaildiagrammen horen bij de ingeklapte subprocessen D1-D3; gebruik
een modeler met subprocess-drilldown, of raadpleeg alle detailbladen in deze PDF. Exacte bronpaden en het machineleesbare
controleverslag staan bij de bestanden.

IOK | Veiligheidskeuringen speelterreinen
As-Is hoofdproces
|            | Terrein controleren |            | Definitieve PDF(s) |
| ---------- | ------------------- | ---------- | ------------------ |
| D1 Dossier |                     | D2 Toestel |                    |
D3 Verslag afwerken Verzonden versie in
| voorbereiden | en bevindingen | controleren | bezorgen aan |
| ------------ | -------------- | ----------- | ------------ |
backoffice bewaren
|     | registreren |     | bestuur |
| --- | ----------- | --- | ------- |
Rapport verzonden en
Inspectie aan de orde
bewaard
ruetcepsnI
KOI
PDF-rapportpakket
Lokaal bestuur / uitbater
Eén procesinstantie = één inspectiedossier voor één speelterrein. Een bezoek kan bestaande én nieuwe toestellen omvatten.
D1, D2 en D3 zijn uitklapbare subprocessen. Drie horizontale streepjes = herhaling na elkaar. Planning en herstelopvolging vallen buiten de app.

IOK | Veiligheidskeuringen speelterreinen
As-Is D1 Dossier voorbereiden
ruetcepsnI
Bruikbaar vorig verslag
of maatregelen?
Jaarlijks Ja Vorig verslag of
maatregelen
Jaarlijkse controle? kopiëren
Basisgegevens Benodigde titels en
Nee
terrein en toestellen standaardteksten
aanvullen overnemen
Dossier nodig Dossier voorbereid
Nieuw
Word-document
aanmaken
Nieuwe controle
Excel-sjabloon voor
nieuwe controle
openen
Jaarlijks: vorig verslag of preventiemaatregelen als basis. Geen bruikbare basis: nieuw Word-document. Nieuwe controle: Excel-sjabloon.
De kopie is een vertrekpunt voor een nieuwe controle; gegevens en uitkomsten worden opnieuw beoordeeld. [S01 p.8-9]

IOK | Veiligheidskeuringen speelterreinen
As-Is D2 Eén toestel beoordelen
ruetcepsnI
Beoordeeld als
conform?
Ja Conform
Indienststelling en
plaatsing beoordelen
Eerste controle van dit Tekortkomingen
toestel? vastgesteld?
Niet conform
Identiteit, type en Uitgebreide Nee Besluit en benodigde
toepasselijke norm risicoanalyse preventiemaatregelen
bepalen uitvoeren vastleggen
Volgend toestel
Ja
Nee, jaarlijks Jaarlijks alle Norm, toelichting, foto’s
toepasselijke en risicobeoordeling
controlepunten vastleggen
beoordelen
Toestel beoordeeld
Dit subproces wordt voor elk te controleren toestel herhaald. Samengestelde toestellen krijgen alle toepasselijke deelchecklists. [S11 00:21-00:24]
Aanvullende metingen, zoals HIC, horen bij de toepasselijke beoordeling. Een HIC-meting is niet automatisch nodig bij ieder gebrek. [Voorbeeld C p.2]

IOK | Veiligheidskeuringen speelterreinen
As-Is D3 Documenten handmatig afwerken
ruetcepsnI
Ja Extra document met
preventiemaatregelen
Nieuwe uitgebreide opstellen
risicoanalyse?
Foto’s van Notities en foto’s in Nee
Risico’s, besluiten Rapportdocumenten
smartphone naar pc Excel of Word
en verslag afwerken als PDF exporteren
overzetten verwerken
Veldgegevens
beschikbaar
PDF-pakket gereed
Een inspecteur kan de analyse of rapportage op kantoor afwerken. Er is geen onderbouwde tweede goedkeurder toegevoegd.
Nieuwe uitgebreide risicoanalyse: extra preventiemaatregelen-document. Jaarlijkse gebreken blijven in het jaarverslag. [S01 p.7-9]

IOK | Veiligheidskeuringen speelterreinen
To-Be hoofdproces
KOI
ruetcepsnI
meetsyS
D1 Dossier Terrein controleren D2 Toestel
voorbereiden en bevindingen controleren
registreren
Inspectie aan de orde
Verzendfout
oplossen en status
controleren
Opnieuw proberen
D3 Synchroniseren Definitieve PDF(s)
Verzendstatus
en verslag afwerken bezorgen aan
registreren
bestuur
Rapport verzonden en
bewaard
Herstellen
Verzendfout
PDF-rapportpakket
Lokaal bestuur / uitbater
Eén procesinstantie = één inspectiedossier voor één speelterrein. Een bezoek kan bestaande én nieuwe toestellen omvatten.
D1, D2 en D3 zijn uitklapbare subprocessen. Drie horizontale streepjes = herhaling na elkaar. Planning en herstelopvolging vallen buiten de app.

IOK | Veiligheidskeuringen speelterreinen
To-Be D1 Dossier en offlinepakket voorbereiden
ruetcepsnI
meetsyS
Nee
Offlinepakket
bruikbaar?
Bestuur, terrein en Offlinepakket
inspectiescope downloaden en op
kiezen tablet controleren
Voorbereiden
Ja
Ontbrekende data of
pakket aanvullen
Veldwerk voorbereid
Bruikbare historiek of
Jaarlijkse controle?
maatregelen?
Nieuw Jaarlijks Ja
Historiek als concept
inspectiedossier met
overnemen
datum en ID maken
Nee
Nieuwe controle Lege toepasselijke
checklists
klaarzetten
O1 ontwerp: vooraf een bruikbaar offlinepakket met geselecteerde terreinen, benodigde historiek en foto’s klaarzetten. Geen vaste weektermijn.
Technische uitwerking en omvang van offline foto-opslag nog valideren. Dit diagram belooft geen automatische SharePoint-offlinefunctie.

IOK | Veiligheidskeuringen speelterreinen
To-Be D2 Eén toestel beoordelen
ruetcepsnI
Beoordeeld als
conform?
Ja Conform
Indienststelling en
plaatsing beoordelen
Eerste controle van dit Tekortkomingen
toestel? vastgesteld?
Niet conform
Toestel, norm en Uitgebreide Nee Besluit en benodigde
beoordelingsbasis risicoanalyse preventiemaatregelen
vaststellen uitvoeren vastleggen
Volgend toestel
Ja
Nee, jaarlijks Jaarlijks alle Norm, toelichting, foto’s
toepasselijke en risicobeoordeling
controlepunten vastleggen
beoordelen
Toestel beoordeeld
Dit subproces wordt voor elk te controleren toestel herhaald. Samengestelde toestellen krijgen alle toepasselijke deelchecklists. [S11 00:21-00:24]
Aanvullende metingen, zoals HIC, horen bij de toepasselijke beoordeling. Een HIC-meting is niet automatisch nodig bij ieder gebrek. [Voorbeeld C p.2]
O6 voorstel: onduidelijke conformiteitsinformatie eerst binnen de eerste taak verduidelijken; ontbrekend attest is niet automatisch niet-conform.

IOK | Veiligheidskeuringen speelterreinen
To-Be D3 Synchroniseren en definitief rapport voorbereiden
ruetcepsnI
meetsyS
Netwerk beschikbaar?
Ja Verslag op laptop
nakijken, afwerken
en indienen
Veldwerk afgerond
Nee
Syncfout of conflict Generatiefout of
Ontbrekende
oplossen; lokale opmaakprobleem
gegevens aanvullen
data behouden oplossen
Ja
Wachten op verbinding
Data en foto’s volledig en Nee Nee Nieuwe uitgebreide Nee PDF-generatie
Dossier volledig?
conflictvrij? risicoanalyse? geslaagd?
Data en foto’s Verplichte gegevens, Ja Nee Rapport-PDF(s) met Ja Definitieve versie en
synchroniseren; risico’s en
versiedatum gebruikte data- en
metadata en fotokoppelingen
genereren fotoreferenties bewaren
koppelingen bijwerken valideren
Ja
Extra document met
preventiemaatregelen
genereren
Pakket klaar voor
verzending
O2/O3 ontwerp: lokale gegevens blijven behouden bij fouten; geen definitieve PDF zolang data en foto’s onvolledig of conflicterend zijn.
Eén inhoudelijk controlemoment door de inspecteur vóór genereren; technische validatie is geen tweede menselijke goedkeuring. Geen vaste retrytermijn.

IOK | Veiligheidskeuringen speelterreinen
To-Be D4 Stamgegevens en optionele overzichten
KOI
rekrewedem-KOI
/
redreeheB
meetsyS
Bevoegde beheerder
werkt stamgegevens
en teksten bij
Stamgegevenswijziging
nodig
Probleemoverzicht gevraagd
Wijzigingen
controleren en
versie vastleggen
Stamgegevens
bijgewerkt
Tekortkomingen per
bestuur
samenbrengen
Overzicht beschikbaar
Uitgevoerde controles
en wegingsnummers
naar Excel exporteren
Financieringsoverzicht
Overzicht klaar voor IOK
gevraagd
Stamgegevensbeheer beschermt categorieën, normen en vaste teksten. Exacte autorisaties en het derde gebruikersprofiel nog bevestigen. [S11 00:34-00:39]
De twee overzichten zijn nice to have. Een facturatieoverzicht bereidt de financiering voor; dit model maakt of verzendt geen factuur. [S01 p.10]