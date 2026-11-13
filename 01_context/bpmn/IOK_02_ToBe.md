# IOK_02_ToBe.bpmn

_Samenvatting zonder diagramcoördinaten. Volgorde volgt de sequence flows._

## Berichtenstromen

- Definitieve PDF(s) bezorgen aan bestuur → Lokaal bestuur / uitbater [PDF-rapportpakket]


## Proces: IOK

Lanes: Inspecteur, Systeem

- **Start**: Inspectie aan de orde — _Inspecteur_
- **Subproces**: D1 Dossier voorbereiden — _Inspecteur_
- **Gebruikerstaak**: Terrein controleren en bevindingen registreren — _Inspecteur_
- **Subproces**: D2 Toestel controleren — _Inspecteur_
- **Subproces**: D3 Synchroniseren en verslag afwerken — _Systeem_
- **Verzendtaak**: Definitieve PDF(s) bezorgen aan bestuur — _Systeem_
- **Systeemtaak**: Verzendstatus registreren — _Systeem_
- **Einde**: Rapport verzonden en bewaard — _Systeem_
- **Boundary-event error op 'Definitieve PDF(s) bezorgen aan bestuur'**: Verzendfout — _Systeem_
- **Gebruikerstaak**: Verzendfout oplossen en status controleren — _Inspecteur_

#### Subproces: D1 Dossier voorbereiden

- **Start**: Voorbereiden — _Inspecteur_
- **Gebruikerstaak**: Bestuur, terrein en inspectiescope kiezen — _Inspecteur_
- **Systeemtaak**: Nieuw inspectiedossier met datum en ID maken — _Systeem_
- **Beslissing (XOR)**: Jaarlijkse controle? — _Systeem_
  - → [Jaarlijks] Bruikbare historiek of maatregelen?
  - → [Nieuwe controle] Lege toepasselijke checklists klaarzetten
- **Beslissing (XOR)**: Bruikbare historiek of maatregelen? — _Systeem_
  - → [Ja] Historiek als concept overnemen
  - → [Nee] Lege toepasselijke checklists klaarzetten
- **Systeemtaak**: Lege toepasselijke checklists klaarzetten — _Systeem_
- **Systeemtaak**: Historiek als concept overnemen — _Systeem_
- **Beslissing (XOR)**: (TOBE_D1_merge) — _Systeem_
  - → Offlinepakket downloaden en op tablet controleren
- **Gebruikerstaak**: Offlinepakket downloaden en op tablet controleren — _Inspecteur_
- **Beslissing (XOR)**: Offlinepakket bruikbaar? — _Inspecteur_
  - → [Ja] Veldwerk voorbereid
  - → [Nee] Ontbrekende data of pakket aanvullen
- **Einde**: Veldwerk voorbereid — _Inspecteur_
- **Gebruikerstaak**: Ontbrekende data of pakket aanvullen — _Inspecteur_

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

#### Subproces: D3 Synchroniseren en verslag afwerken

- **Start**: Veldwerk afgerond — _Inspecteur_
- **Beslissing (XOR)**: Netwerk beschikbaar? — _Inspecteur_
  - → [Ja] (TOBE_D3_joinnet)
  - → [Nee] Wachten op verbinding
- **Beslissing (XOR)**: (TOBE_D3_joinnet) — _Inspecteur_
  - → Data en foto’s synchroniseren; metadata en koppelingen bijwerken
- **Tussen-event (vangt) conditional**: Wachten op verbinding — _Inspecteur_
- **Systeemtaak**: Data en foto’s synchroniseren; metadata en koppelingen bijwerken — _Systeem_
- **Beslissing (XOR)**: Data en foto’s volledig en conflictvrij? — _Systeem_
  - → [Nee] Syncfout of conflict oplossen; lokale data behouden
  - → [Ja] Verslag op laptop nakijken, afwerken en indienen
- **Gebruikerstaak**: Syncfout of conflict oplossen; lokale data behouden — _Inspecteur_
- **Gebruikerstaak**: Verslag op laptop nakijken, afwerken en indienen — _Inspecteur_
- **Systeemtaak**: Verplichte gegevens, risico’s en fotokoppelingen valideren — _Systeem_
- **Beslissing (XOR)**: Dossier volledig? — _Systeem_
  - → [Nee] Ontbrekende gegevens aanvullen
  - → [Ja] Nieuwe uitgebreide risicoanalyse?
- **Gebruikerstaak**: Ontbrekende gegevens aanvullen — _Inspecteur_
- **Beslissing (XOR)**: Nieuwe uitgebreide risicoanalyse? — _Systeem_
  - → [Ja] Extra document met preventiemaatregelen genereren
  - → [Nee] (TOBE_D3_joinprev)
- **Systeemtaak**: Extra document met preventiemaatregelen genereren — _Systeem_
- **Beslissing (XOR)**: (TOBE_D3_joinprev) — _Systeem_
  - → Rapport-PDF(s) met versiedatum genereren
- **Systeemtaak**: Rapport-PDF(s) met versiedatum genereren — _Systeem_
- **Beslissing (XOR)**: PDF-generatie geslaagd? — _Systeem_
  - → [Nee] Generatiefout of opmaakprobleem oplossen
  - → [Ja] Definitieve versie en gebruikte data- en fotoreferenties bewaren
- **Gebruikerstaak**: Generatiefout of opmaakprobleem oplossen — _Inspecteur_
- **Systeemtaak**: Definitieve versie en gebruikte data- en fotoreferenties bewaren — _Systeem_
- **Einde**: Pakket klaar voor verzending — _Systeem_

## Proces: IOK

Lanes: Beheerder / IOK-medewerker, Systeem

- **Start**: Stamgegevenswijziging nodig — _Beheerder / IOK-medewerker_
- **Start**: Probleemoverzicht gevraagd — _Beheerder / IOK-medewerker_
- **Start**: Financieringsoverzicht gevraagd — _Systeem_
- **Gebruikerstaak**: Bevoegde beheerder werkt stamgegevens en teksten bij — _Beheerder / IOK-medewerker_
- **Systeemtaak**: Tekortkomingen per bestuur samenbrengen — _Systeem_
- **Systeemtaak**: Uitgevoerde controles en wegingsnummers naar Excel exporteren — _Systeem_
- **Systeemtaak**: Wijzigingen controleren en versie vastleggen — _Systeem_
- **Einde**: Overzicht beschikbaar — _Systeem_
- **Einde**: Overzicht klaar voor IOK — _Systeem_
- **Einde**: Stamgegevens bijgewerkt — _Systeem_