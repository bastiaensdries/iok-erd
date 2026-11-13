# IOK_01_AsIs_uitgeklapt.bpmn

_Samenvatting zonder diagramcoördinaten. Volgorde volgt de sequence flows._

## Berichtenstromen

- Definitieve PDF(s) bezorgen aan bestuur → Lokaal bestuur / uitbater [PDF-rapportpakket]


## Proces: IOK

Lanes: Inspecteur

- **Start**: Inspectie aan de orde
- **Subproces**: D1 Dossier voorbereiden
- **Taak**: Terrein controleren en bevindingen registreren
- **Subproces**: D2 Toestel controleren
- **Subproces**: D3 Verslag afwerken
- **Verzendtaak**: Definitieve PDF(s) bezorgen aan bestuur
- **Taak**: Verzonden versie in backoffice bewaren
- **Einde**: Rapport verzonden en bewaard

#### Subproces: D1 Dossier voorbereiden

- **Start**: Dossier nodig — _Inspecteur_
- **Beslissing (XOR)**: Jaarlijkse controle? — _Inspecteur_
  - → [Jaarlijks] Bruikbaar vorig verslag of maatregelen?
  - → [Nieuwe controle] Excel-sjabloon voor nieuwe controle openen
- **Beslissing (XOR)**: Bruikbaar vorig verslag of maatregelen? — _Inspecteur_
  - → [Ja] Vorig verslag of maatregelen kopiëren
  - → [Nee] Nieuw Word-document aanmaken
- **Taak**: Excel-sjabloon voor nieuwe controle openen — _Inspecteur_
- **Taak**: Vorig verslag of maatregelen kopiëren — _Inspecteur_
- **Taak**: Nieuw Word-document aanmaken — _Inspecteur_
- **Beslissing (XOR)**: (ASIS_D1_merge) — _Inspecteur_
  - → Basisgegevens terrein en toestellen aanvullen
- **Taak**: Basisgegevens terrein en toestellen aanvullen — _Inspecteur_
- **Taak**: Benodigde titels en standaardteksten overnemen — _Inspecteur_
- **Einde**: Dossier voorbereid — _Inspecteur_

#### Subproces: D2 Toestel controleren

- **Start**: Volgend toestel — _Inspecteur_
- **Taak**: Identiteit, type en toepasselijke norm bepalen — _Inspecteur_
- **Beslissing (XOR)**: Eerste controle van dit toestel? — _Inspecteur_
  - → [Ja] Beoordeeld als conform?
  - → [Nee, jaarlijks] Jaarlijks alle toepasselijke controlepunten beoordelen
- **Beslissing (XOR)**: Beoordeeld als conform? — _Inspecteur_
  - → [Conform] Indienststelling en plaatsing beoordelen
  - → [Niet conform] Uitgebreide risicoanalyse uitvoeren
- **Taak**: Jaarlijks alle toepasselijke controlepunten beoordelen — _Inspecteur_
- **Taak**: Indienststelling en plaatsing beoordelen — _Inspecteur_
- **Taak**: Uitgebreide risicoanalyse uitvoeren — _Inspecteur_
- **Beslissing (XOR)**: (ASIS_D2_join) — _Inspecteur_
  - → Tekortkomingen vastgesteld?
- **Beslissing (XOR)**: Tekortkomingen vastgesteld? — _Inspecteur_
  - → [Ja] Norm, toelichting, foto’s en risicobeoordeling vastleggen
  - → [Nee] (ASIS_D2_merge)
- **Taak**: Norm, toelichting, foto’s en risicobeoordeling vastleggen — _Inspecteur_
- **Beslissing (XOR)**: (ASIS_D2_merge) — _Inspecteur_
  - → Besluit en benodigde preventiemaatregelen vastleggen
- **Taak**: Besluit en benodigde preventiemaatregelen vastleggen — _Inspecteur_
- **Einde**: Toestel beoordeeld — _Inspecteur_

#### Subproces: D3 Verslag afwerken

- **Start**: Veldgegevens beschikbaar — _Inspecteur_
- **Taak**: Foto’s van smartphone naar pc overzetten — _Inspecteur_
- **Taak**: Notities en foto’s in Excel of Word verwerken — _Inspecteur_
- **Taak**: Risico’s, besluiten en verslag afwerken — _Inspecteur_
- **Beslissing (XOR)**: Nieuwe uitgebreide risicoanalyse? — _Inspecteur_
  - → [Ja] Extra document met preventiemaatregelen opstellen
  - → [Nee] (ASIS_D3_merge)
- **Taak**: Extra document met preventiemaatregelen opstellen — _Inspecteur_
- **Beslissing (XOR)**: (ASIS_D3_merge) — _Inspecteur_
  - → Rapportdocumenten als PDF exporteren
- **Taak**: Rapportdocumenten als PDF exporteren — _Inspecteur_
- **Einde**: PDF-pakket gereed — _Inspecteur_