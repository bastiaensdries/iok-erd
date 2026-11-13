# IOK_02_ToBe_uitgeklapt_aangepast.bpmn

_Samenvatting zonder diagramcoördinaten. Volgorde volgt de sequence flows._

## Berichtenstromen

- Inspecteur verstuurt definitieve PDF(s) handmatig → Lokaal bestuur / uitbater [PDF-rapportpakket]


## Proces: IOK

Lanes: Inspecteur, Systeem

- **Start**: Inspectie aan de orde
- **Subproces**: D1 Dossier voorbereiden
- **Gebruikerstaak**: Terrein controleren en bevindingen registreren
- **Subproces**: D2 Toestel controleren
- **Subproces**: D3 Verslag en preventiesamenvatting afwerken en bewaren
- **Gebruikerstaak**: Inspecteur verstuurt definitieve PDF(s) handmatig
- **Beslissing (XOR)**: Door inspecteur verzonden?
  - → [Nee] Inspecteur lost verzendprobleem op en controleert status
  - → [Ja] Verzendstatus registreren
- **Gebruikerstaak**: Inspecteur lost verzendprobleem op en controleert status
- **Systeemtaak**: Verzendstatus registreren
- **Einde**: Rapport verzonden en bewaard

#### Subproces: D1 Dossier voorbereiden

- **Start**: Voorbereiden — _Inspecteur_
- **Gebruikerstaak**: Bestuur, terrein en inspectiescope kiezen — _Inspecteur_
- **Systeemtaak**: Nieuw inspectiedossier met controledatum en uniek ID maken — _Systeem_
- **Beslissing (XOR)**: Jaarlijkse controle? — _Systeem_
  - → [Jaarlijks] Bruikbare historiek of maatregelen?
  - → [Nieuwe controle] Lege toepasselijke checklists klaarzetten
- **Beslissing (XOR)**: Bruikbare historiek of maatregelen? — _Systeem_
  - → [Ja] Historiek als concept overnemen
  - → [Nee] Lege toepasselijke checklists klaarzetten
- **Systeemtaak**: Lege toepasselijke checklists klaarzetten — _Systeem_
- **Systeemtaak**: Historiek als concept overnemen — _Systeem_
- **Beslissing (XOR)**: (TOBE_D1_merge) — _Systeem_
  - → Inspectiedossier voorbereid
- **Einde**: Inspectiedossier voorbereid — _Inspecteur_

#### Subproces: D2 Toestel controleren

- **Start**: Volgend toestel — _Inspecteur_
- **Gebruikerstaak**: Toestel, norm en beoordelingsbasis vaststellen — _Inspecteur_
- **Beslissing (XOR)**: Eerste controle van dit toestel? — _Inspecteur_
  - → [Ja] Beoordeeld als conform?
  - → [Nee, jaarlijks] Jaarlijks alle toepasselijke controlepunten beoordelen
- **Beslissing (XOR)**: Beoordeeld als conform? — _Inspecteur_
  - → [Conform] Indienststelling en plaatsing beoordelen
  - → [Niet conform] Uitgebreide risicoanalyse uitvoeren
- **Gebruikerstaak**: Jaarlijks alle toepasselijke controlepunten beoordelen — _Inspecteur_
- **Gebruikerstaak**: Indienststelling en plaatsing beoordelen — _Inspecteur_
- **Gebruikerstaak**: Uitgebreide risicoanalyse uitvoeren — _Inspecteur_
- **Beslissing (XOR)**: (TOBE_D2_join) — _Inspecteur_
  - → Tekortkomingen vastgesteld?
- **Beslissing (XOR)**: Tekortkomingen vastgesteld? — _Inspecteur_
  - → [Ja] Norm, toelichting, foto’s en risicobeoordeling vastleggen
  - → [Nee] (TOBE_D2_merge)
- **Gebruikerstaak**: Norm, toelichting, foto’s en risicobeoordeling vastleggen — _Inspecteur_
- **Beslissing (XOR)**: (TOBE_D2_merge) — _Inspecteur_
  - → Besluit en benodigde preventiemaatregelen vastleggen
- **Gebruikerstaak**: Besluit en benodigde preventiemaatregelen vastleggen — _Inspecteur_
- **Einde**: Toestel beoordeeld — _Inspecteur_

#### Subproces: D3 Verslag en preventiesamenvatting afwerken en bewaren

- **Start**: Veldwerk afgerond — _Inspecteur_
- **Gebruikerstaak**: Dossier en controledatum nakijken en afwerken — _Inspecteur_
- **Systeemtaak**: Verplichte gegevens, risico’s en foto’s valideren — _Systeem_
- **Beslissing (XOR)**: Dossier volledig? — _Systeem_
  - → [Nee] Ontbrekende dossiergegevens aanvullen
  - → [Ja] Samenvatting preventiemaatregelen voor terrein en toestellen samenstellen
- **Gebruikerstaak**: Ontbrekende dossiergegevens aanvullen — _Inspecteur_
- **Systeemtaak**: Samenvatting preventiemaatregelen voor terrein en toestellen samenstellen — _Systeem_
- **Beslissing (XOR)**: (TOBE_D3_genmerge) — _Systeem_
  - → Rapport-PDF en preventiesamenvatting met controledatum genereren
- **Systeemtaak**: Rapport-PDF en preventiesamenvatting met controledatum genereren — _Systeem_
- **Beslissing (XOR)**: PDF-generatie geslaagd? — _Systeem_
  - → [Nee] Generatiefout oplossen
  - → [Ja] PDF en preventiesamenvatting inhoudelijk nakijken
- **Gebruikerstaak**: Generatiefout oplossen — _Inspecteur_
- **Gebruikerstaak**: PDF en preventiesamenvatting inhoudelijk nakijken — _Inspecteur_
- **Beslissing (XOR)**: PDF correct voor verzending? — _Inspecteur_
  - → [Nee] PDF corrigeren of na dossiercorrectie opnieuw maken
  - → [Ja] Definitieve PDF, controledatum en historische dossiergegevens bewaren
- **Gebruikerstaak**: PDF corrigeren of na dossiercorrectie opnieuw maken — _Inspecteur_
- **Systeemtaak**: Definitieve PDF, controledatum en historische dossiergegevens bewaren — _Systeem_
- **Beslissing (XOR)**: Definitieve versie veilig bewaard? — _Systeem_
  - → [Nee] Bewaarfout oplossen en definitieve versie behouden
  - → [Ja] Definitieve PDF bewaard; inspecteur kan verzenden
- **Gebruikerstaak**: Bewaarfout oplossen en definitieve versie behouden — _Inspecteur_
- **Einde**: Definitieve PDF bewaard; inspecteur kan verzenden — _Systeem_

## Proces: IOK

Lanes: Bevoegde beheerder, Inspecteur / bevoegde IOK-medewerker, Systeem

- **Start**: Stamgegevenswijziging nodig — _Bevoegde beheerder_
- **Start**: Maatregelenoverzicht gevraagd — _Inspecteur / bevoegde IOK-medewerker_
- **Start**: Inspecteur vraagt financieel overzicht — _Inspecteur / bevoegde IOK-medewerker_
- **Gebruikerstaak**: Stamgegevens en vaste teksten bijwerken — _Bevoegde beheerder_
- **Systeemtaak**: Preventiemaatregelen en tekortkomingen per bestuur samenvatten — _Systeem_
- **Gebruikerstaak**: Periode kiezen: laatste 3 maanden of van begin- tot einddatum — _Inspecteur / bevoegde IOK-medewerker_
- **Systeemtaak**: Nieuwe stamgegevensversie vastleggen; historische inspecties behouden — _Systeem_
- **Einde**: Maatregelenoverzicht beschikbaar — _Systeem_
- **Systeemtaak**: Uitgevoerde controles en historische eenheden binnen gekozen periode naar Excel exporteren — _Systeem_
- **Einde**: Wijziging geldt voor toekomstig gebruik — _Systeem_
- **Einde**: Financieel overzicht voor gekozen periode beschikbaar — _Systeem_