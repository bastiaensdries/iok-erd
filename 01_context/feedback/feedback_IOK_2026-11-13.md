# Feedback IOK – feedbacksessie 13 november 2026

_Notities van Dries (letterlijk), daaronder hoe ze in het finale BPMN (`IOK_02_ToBe_uitgeklapt_aangepast`) verwerkt zijn._

## Notities
- Verzending pdf hoeft niet automatisch te gebeuren
- Offline hoeft niet meer
- Preventiemaatregelen samenvatting is zeer belangrijk
- D1: /  (geen opmerkingen)
- D2: /  (geen opmerkingen)
- D3: Versiebeheer: datum van controle · Pdf aanpassen voor verzending
- D4: Verandering van stamgegevens heeft geen terugwerkende kracht · Periode selecteren · Moederdata kan maar 1 persoon veranderen
- Tablet: Samsung Galaxy 5G

## Verwerking in het finale BPMN
| Feedback | BPMN-stap |
|---|---|
| Geen automatische verzending | Hoofdproces: "Inspecteur verstuurt definitieve PDF(s) handmatig" → "Verzendstatus registreren" |
| Offline niet meer nodig | Geen synchronisatie- of offlinestappen meer in het finale BPMN |
| Preventiesamenvatting zeer belangrijk | D3: "Samenvatting preventiemaatregelen voor terrein en toestellen samenstellen"; D4: "Preventiemaatregelen en tekortkomingen per bestuur samenvatten" |
| Versiebeheer = datum van controle | D3: "Rapport-PDF en preventiesamenvatting met controledatum genereren", "Definitieve PDF, controledatum en historische dossiergegevens bewaren" |
| PDF aanpassen voor verzending | D3: "PDF correct voor verzending?" → "PDF corrigeren of na dossiercorrectie opnieuw maken" |
| Stamgegevens zonder terugwerkende kracht | D4: "Nieuwe stamgegevensversie vastleggen; historische inspecties behouden" → "Wijziging geldt voor toekomstig gebruik" |
| Periode selecteren | D4: "Periode kiezen: laatste 3 maanden of van begin- tot einddatum" |
| Moederdata door 1 persoon | D4: lane "Bevoegde beheerder" |
| Tablet Samsung Galaxy 5G | Geen BPMN-stap; context voor app-ontwerp (Android-tablet) |
