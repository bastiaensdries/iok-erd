# App: formulieren en views (stap 9)

_2026-11-17. **Status: aanvaard als vertrekpunt (B92).** Aanpassingen tijdens het bouwen eerst hier doorvoeren._

Dit document is de bron voor de formulieren en views van de model-driven app (B89, B91). Gebouwd wordt met de hand in de maker-portal, **binnen de solution `IOK Speelterreinen`**. Wijkt het gebouwde af, pas dan eerst dit document aan.

**Niet in dit document:** het invulscherm van een beoordeling (custom page, B89), flows, beveiligingsrollen.

## Uitgangspunten (B91)

- Per tabel wordt het **standaard hoofdformulier** ("Informatie" / "Information") aangepast. Geen extra hoofdformulieren, dus de gebruiker hoeft nooit van formulier te wisselen.
- **Geen wijzigingen aan tabellen of kolommen.** Ontbreekt er een kolom, dan stoppen we en gaat het via `datamodel_v3.md` (startprompt, harde regels).
- **Een formulier dwingt het slot niet af.** Dat doet de plug-in (regel 4 en 17, B77). Een kolom alleen-lezen zetten op het formulier is enkel gemak, geen beveiliging.
- **Kopiekolommen** (B57) staan op het formulier in een eigen tab "Bevroren gegevens" en blijven bewerkbaar: de inspecteur mag ze corrigeren tot Afgerond.
- **Formulekolommen** (`iok_risicoscore`, `iok_risicoklasse`) zijn vanzelf alleen-lezen.
- **Technische namen** op formulieren: `tab_…`, `sectie_…`, `subraster_…`, in kleine letters zonder spaties. Veldlabels worden niet overschreven: ze volgen de weergavenaam van de kolom (B93).
- `iok_legacyid` staat op geen enkel formulier (enkel voor het laden, B49).
- Resultaten worden in deze app **getoond, niet ingevuld**. Het invullen gebeurt in de custom page (B89).

## Bouwvolgorde

Doel: het dossier van De Bogaard openen en doorlopen.

0. App-schil (zie "Navigatie"), zodat elk formulier meteen te testen is
1. `iok_inspectiedossier`
2. `iok_beoordeling`
3. `iok_resultaat`, `iok_maatregel`
4. `iok_speelterrein`
5. `iok_speeltoestel`
6. `iok_hicmeting`, `iok_foto`
7. Later, in een volgende ronde: stamgegevens (`account`, `contact`, `iok_terreingroep`, `iok_toestelcode`, `iok_toesteltype`), sjablonen (`iok_checklist`, `iok_checklistonderdeel`, `iok_controlepunt`, `iok_standaardtekst`), communicatie (`iok_rapportversie`, `iok_document`)

## Navigatie (app-schil)

App: **IOK Speelterreinen**, model-driven, in de solution.

| Groep | Pagina's |
|---|---|
| Inspectie | Dossiers · Speelterreinen · Speeltoestellen |
| Stamgegevens | later (stap 7 van de bouwvolgorde) |
| Sjablonen | later |

Beoordelingen, resultaten, maatregelen, HIC-metingen en foto's krijgen **geen eigen pagina**: je bereikt ze via het dossier.

---

## 1. `iok_inspectiedossier`

**Koptekst:** `iok_dossiernummer` · statusreden · `iok_controledatum` · `iok_inspecteurid`

| Tab | Sectie | Kolommen / onderdeel |
|---|---|---|
| Algemeen | Dossier | `iok_dossiernummer` (autonummer, alleen-lezen) · `iok_speelterreinid` · `iok_controledatum` · `iok_soortcontrole` · `iok_inspecteurid` · eigenaar |
| Bevroren gegevens | Bestuur | `iok_bestuurid` · `iok_bestuurnaam` · `iok_contactnaam` |
| | Uitbater | `iok_uitbaternaam` · `iok_uitbaterstraat` · `iok_uitbaterpostcode` · `iok_uitbaterplaats` |
| | Terrein | `iok_terreinnaam` · `iok_terreincode` · `iok_straat` · `iok_postcode` · `iok_plaats` · `iok_doelgroep` · `iok_toezicht` |
| | Inspecteur | `iok_inspecteurnaam` |
| Beoordelingen | – | subraster `iok_beoordeling`, view **Beoordelingen van dossier** |
| Verslag | Algemeen besluit | `iok_algemeenbesluitstandaardtekstid` · `iok_algemeenbesluit` |
| | Rapportversies | subraster `iok_rapportversie`, view **Rapportversies van dossier** |

Documenten (SharePoint) komen er pas bij als documentbeheer op de tabel aanstaat (HANDOVER, nog te doen).

**Views**

| View | Filter | Kolommen | Sortering |
|---|---|---|---|
| Actieve dossiers (standaard) | status actief (Concept, In uitvoering) | dossiernummer · terreincode · terreinnaam · controledatum · soort controle · inspecteurnaam · statusreden | controledatum aflopend |
| Mijn actieve dossiers | idem + `iok_inspecteurid` = huidige gebruiker | idem | idem |
| Afgeronde dossiers | statusreden Afgerond | idem | controledatum aflopend |
| Snel zoeken | – | zoekt op dossiernummer, terreincode, terreinnaam | – |

## 2. `iok_beoordeling`

**Koptekst:** `iok_soort` · `iok_beoordelingsbasis` · `iok_besluit`

| Tab | Sectie | Kolommen / onderdeel |
|---|---|---|
| Algemeen | Beoordeling | `iok_naam` · `iok_inspectiedossierid` · `iok_soort` · `iok_speeltoestelid` · `iok_checklistid` · `iok_norm` · `iok_beoordelingsbasis` · `iok_volgorde` · `iok_bronbeoordelingid` |
| | Besluit | `iok_besluitstandaardtekstid` · `iok_besluit` · `iok_besluittekst` · `iok_opmerking` |
| Bevindingen | Resultaten | subraster `iok_resultaat`, view **Resultaten van beoordeling** |
| | Maatregelen | subraster `iok_maatregel`, view **Maatregelen van beoordeling** |
| Toestelgegevens | Bevroren gegevens | `iok_toestelcode` · `iok_toestelnaam` · `iok_typenaam` · `iok_leverancier` · `iok_typefabrikant` · `iok_serienummer` · `iok_attest` · `iok_bouwjaar` · `iok_doelgroep` · `iok_eenheden` |
| Metingen en foto's | HIC-metingen | subraster `iok_hicmeting` |
| | Foto's | subraster `iok_foto` |
| Onderdelen | – | subraster `iok_checklistonderdeel` via de N:N `iok_beoordeling_onderdeel` |

De tabs Toestelgegevens en HIC-metingen zijn leeg bij een terreinbeoordeling. Ze verbergen bij soort = Terrein is een bedrijfsregel; niet in deze eerste ronde.

**Views**

| View | Filter | Kolommen | Sortering |
|---|---|---|---|
| Beoordelingen van dossier (subraster) | actief | volgorde · naam · soort · toestelcode · toestelnaam · beoordelingsbasis · besluit | volgorde oplopend |
| Actieve beoordelingen (standaard) | actief | naam · dossier · soort · toestelcode · besluit | naam |

## 3. `iok_resultaat` en `iok_maatregel`

**`iok_resultaat`**

| Tab | Sectie | Kolommen / onderdeel |
|---|---|---|
| Algemeen | Resultaat | `iok_naam` · `iok_beoordelingid` · `iok_controlepuntid` · `iok_antwoord` · `iok_isovergenomen` |
| | Opmerking | `iok_standaardtekstid` · `iok_opmerking` |
| | Risico | `iok_impact` · `iok_kans` · `iok_blootstelling` · `iok_risicoscore` · `iok_risicoklasse` |
| | Maatregelen | subraster `iok_maatregel` (via `iok_resultaatid`) |
| | Foto's | subraster `iok_foto` (via `iok_resultaatid`) |

**View "Resultaten van beoordeling"** (subraster): controlepunt · antwoord · opmerking · risicoscore · risicoklasse · overgenomen. Sortering: zie open punt T1.

**`iok_maatregel`**: één sectie met `iok_naam` · `iok_beoordelingid` · `iok_resultaatid` · `iok_standaardtekstid` · `iok_tekst` · `iok_volgorde` · `iok_isovergenomen`.

**View "Maatregelen van beoordeling"** (subraster): volgorde · tekst · resultaat · overgenomen; sortering volgorde oplopend.

## 4. `iok_speelterrein`

| Tab | Sectie | Kolommen / onderdeel |
|---|---|---|
| Algemeen | Terrein | `iok_naam` · `iok_code` · `iok_bestuurid` · `iok_uitbaterid` · `iok_terreingroepid` |
| | Adres | `iok_straat` · `iok_postcode` · `iok_plaats` |
| | Kenmerken | `iok_doelgroep` · `iok_toezicht` · `iok_eenheden` |
| Toestellen | – | subraster `iok_speeltoestel`, view **Toestellen van terrein** |
| Dossiers | – | subraster `iok_inspectiedossier`, controledatum aflopend |

**Views:** Actieve speelterreinen (standaard): code · naam · bestuur · plaats · doelgroep; sortering code. Snel zoeken op code en naam.

## 5. `iok_speeltoestel`

| Tab | Sectie | Kolommen / onderdeel |
|---|---|---|
| Algemeen | Toestel | `iok_code` · `iok_codeweergave` · `iok_naam` · `iok_speelterreinid` · `iok_toesteltypeid` · `iok_eenheden` · `iok_doelgroep` |
| | Fabrikant | `iok_leverancier` · `iok_typefabrikant` · `iok_serienummer` · `iok_bouwjaar` · `iok_attest` |
| Codes | – | subraster `iok_toestelcode` |
| Historiek | – | subraster `iok_beoordeling` (via `iok_speeltoestelid`): dossier · beoordelingsbasis · besluit |

**Views:** Toestellen in gebruik (standaard) en Toestellen van terrein (subraster): code · naam · terrein · type · eenheden; sortering code (zie T2). Snel zoeken op code en naam.

## 6. `iok_hicmeting` en `iok_foto`

Eén sectie met alle kolommen uit `datamodel_v3.md` §6.6 en §6.7. Subrasterviews:

- HIC-metingen: volgnummer · peak · HIC · valhoogte · meetmoment; sortering volgnummer.
- Foto's: naam · soort · genomen op · in verslag · overgenomen; sortering genomen op aflopend.

## Open punten en tests

- **T1 – Resultaten op de volgorde van de checklist.** De volgorde staat op `iok_controlepunt.iok_volgorde`, niet op het resultaat. Microsoft Learn ("Choose and configure columns in model-driven app views") zegt dat een view kolommen uit een gerelateerde tabel kan **tonen**, maar zegt niets over **sorteren** erop. Te testen in de viewdesigner. Lukt het niet, dan kan het zonder modelwijziging enkel op `iok_naam` (de code), en die sorteert als tekst: G.10 komt dan vóór G.2. Een betere oplossing vraagt een kolom op het resultaat, dus een modelwijziging: dan **stoppen en beslissen**.
- **T2 – Toestelcodes sorteren als tekst**: "BOA 10" komt vóór "BOA 2". Zelfde soort probleem; voorlopig aanvaard.
- **T3 – "Mijn actieve dossiers"**: te testen of het filter "is gelijk aan huidige gebruiker" werkt op `iok_inspecteurid` (een lookup naar `systemuser`). Lukt het niet, dan valt deze view weg.
