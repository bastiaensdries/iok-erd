# 04_data – proefdata voor Dataverse (Geel)

_Gemaakt door `python tools/csv_maken.py` uit de bronnen in `01_context/docs/`. Niet met de hand wijzigen: pas het script aan en draai opnieuw. Beslissing: B85._

## Wat erin zit

| Bestand | Rijen | Bron | Opmerking |
|---|---|---|---|
| `account.csv` | 2 | Overzicht bestaande speelterreinen (kolom D en E) | Stad Geel en OCMW Geel; geen adres of contactpersoon in de bron |
| `iok_toesteltype.csv` | 128 | Overzicht soorten speeltoestellen | norm = EN 14974 voor de categorie Skate, anders EN 1176; "Zitelemeneten" → "Zitelementen" |
| `iok_checklist.csv` | 3 | de drie sjablonen 2022 | EN 1176, skate EN 14974, terrein; status Actief |
| `iok_checklistonderdeel.csv` | 25 | bladnamen van de sjablonen | Deel 1 + 11 bladen, skate Deel 1 + 11 onderdelen, terrein |
| `iok_controlepunt.csv` | 739 | Indienststelling 2022 (538), skate (138), terrein (63) | met ouder en hoofdstuk; kolom `_bron` = blad en rij |
| `iok_standaardtekst.csv` | 33 | bladen Standaardlijsten + besluitzinnen uit `C_2026` | de namenlijsten van inspecteurs zijn weggelaten (B37) |
| `iok_speelterrein.csv` | 55 | Overzicht bestaande speelterreinen, gemeente Geel | naam, code, bestuur, oud ID; **geen adres** in de bron |
| `iok_speeltoestel.csv` | 16 | `C_2026` (De Bogaard) | zie "Afleidingen" |
| `iok_toestelcode.csv` | 17 | `C_2026` | "Metalen doelen" draagt BOA 1 en BOA 2 |
| `iok_inspectiedossier.csv` | 1 | `C_2026` | jaarlijkse controle De Bogaard, 04/08/2026 |
| `iok_beoordeling.csv` | 17 | `C_2026` | terrein + 16 toestellen |
| `iok_resultaat.csv` | 7 | `C_2026` | de zeven bevindingen (NOK) met hun tekst |
| `iok_beoordeling_onderdeel.csv` | 18 | afgeleid | welke onderdelen bij welke beoordeling (N:N) |

`laadplan.json` = de laadvolgorde en de lookups. `_meldingen.txt` = wat het script onderweg genormaliseerd heeft.

## Hoe de bestanden werken

- `_sleutel` is de unieke naam van een rij. Een lookup-kolom (bv. `iok_speelterreinid`) bevat de `_sleutel` van de rij waarnaar ze verwijst. Geen GUID's.
- Kolommen die met `_` beginnen worden niet geladen (`_bron`, `_opmerking`, …).
- Keuzekolommen bevatten het label (bv. `EN 1176`), ja/nee-kolommen `ja` of `nee`, datums `jjjj-mm-dd`.
- `@ik` = de gebruiker die laadt (inspecteur van het voorbeelddossier).
- `statuscode` wordt als allerlaatste gezet.

## Afleidingen en gaten (nakijken)

1. **Toesteltype van 8 van de 16 toestellen is afgeleid uit de naam** (kolom `_opmerking` in `iok_speeltoestel.csv`): Galaxy → Klimtoestel, Evenwichtsbalken → Evenwichtstoestel, Zelf remmende veerwip → Veertoestel enkel, Draai wip → Draaitoestel, Klimtoren met netten → Klimnetten, Toren met glijbaan → Klimtoren met glijbaan, Dubbele veerwip paard → Veertoestel dubbel, Fitnesstoestellen → Fitnesstoestel. Het type is verplicht, dus er moest iets staan; de eenheden volgen het type. Te bevestigen (Q15).
2. **Er zijn geen andere toestellen.** Het overzicht geeft per terrein enkel een aantal (kolom `_toestellen_in_bron`). Alleen De Bogaard heeft toestellen, en daar 16 van de 30 die het overzicht telt.
3. **Besluit leeg bij BOA 11, 24, 30 en 35**: het verslag noemt bevindingen maar geen besluitzin. BOA 29, 32 en 38 kregen "Niet beoordeeld" (B71) met de zin uit het verslag.
4. **Bevinding en maatregel staan samen in `iok_resultaat.iok_opmerking`**, zoals in het verslag. Er zijn geen `iok_maatregel`-rijen: opsplitsen zou gissen zijn (review punt 11).
5. **BOA 11, Wip**: het verslag noemt code 1.5, in het sjabloon 2022 heeft dezelfde tekst code 1.1. Geladen op 1.1.
6. **Het dossier blijft op Concept.** Zet het na het laden zelf op Afgerond; dan kun je "historiek overnemen" (D1.4) tonen.
7. **Type → onderdeel (N:N) is niet geladen**: welke types bij welk Deel 2-blad horen, is Q21.
8. **Geen foto's, geen HIC-metingen, geen kopie van adres/contact in het dossier**: staan niet in de bron.
9. **Terreinen met een bijzonderheid** staan in `_opmerking` van `iok_speelterrein.csv`: rijen met meer dan één locatie (Q20) en de code `LSW / KSW` met een "/" (B84).
10. Subregels met een eigen code (bv. `G.2.6.2`) zijn een eigen controlepunt, zodat een bevinding erop kan hangen (velddekking §14). De dubbele subregel `E.5.1.1` onder `F.5.1` staat als toelichting bij `F.5.1`.

## Gaten tegenover het echte verslag (vastgesteld 2026-11-16)

Het bronverslag `C_2026 - Jaarlijkse controle De Bogaard algemeen.pdf` (13 pagina's) is regel voor regel naast de
proefdata gelegd. Het model draagt alles wat erin staat; de **proefdata** mist drie dingen. Alle drie op te lossen
in `csv_maken.py` en opnieuw te laden, zonder schemawijziging.

1. **BOA 5 ("Klimrots") ontbreekt.** Het verslag behandelt 17 toestellen (pagina 4 noemt Klimrots BOA 5, conform),
   `iok_speeltoestel.csv` bevat er 16 en `iok_beoordeling.csv` 17 rijen (terrein + 16). Er zouden er 18 moeten zijn.
2. **De risicocijfers zijn niet overgenomen.** Het verslag drukt bij elke bevinding impact, kans, blootstelling en
   resultaat af; `iok_resultaat.csv` heeft die kolommen niet. Uit het verslag: BOA 11 K.1 = 7 / 6,0 / 3,0 / 126,0 ·
   BOA 11 wip = 1 / 3,0 / 3,0 / 9,0 · BOA 24 K.1 = 3 / 6,0 / 3,0 / 54,0 · BOA 30 G.2.6.2 = 3 / 3,0 / 3,0 / 27,0 ·
   BOA 35 A.1.1 = 3 / 2,0 / 3,0 / 18,0 · BOA 35 E.1.3 = 3 / 3,0 / 3,0 / 27,0 · BOA 35 G.2.3 = 3 / 1,0 / ? / 3,0
   (in het verslag is daar een kolomkop weggevallen: "Impact Kans Resultaat" met drie getallen).
   Deze cijfers laden is meteen de test van de formulekolommen `iok_risicoscore` en `iok_risicoklasse`.
3. **Geen foto's.** Elk toestel heeft een foto in het verslag; `iok_foto` bestaat in het model maar er is niets geladen.

**Niet in het model, en terecht:** pagina 2 van het verslag (legende HIC-waarden en legende risicoanalyse) is in elk
verslag identiek en hoort in het PDF-sjabloon, niet in de databank.
