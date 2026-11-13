# Beslissingenlog

Formaat: **Bnn** – datum – beslissing – waarom / bron. Nieuwe beslissingen onderaan. Een herziening krijgt een nieuw nummer en verwijst naar het oude ("vervangt B03").

- **B01** – 2026-11-13 – Alle eigen tabellen, kolommen, keuzelijsten en relaties krijgen het publisherprefix **`iok_`**, ook eigen kolommen op standaardtabellen. – Keuze Dries. Het prefix ligt vast in de solution publisher en is achteraf niet te wijzigen.
- **B02** – 2026-11-13 – **Ingebouwde Dataverse-tabellen hergebruiken** waar ze passen; pas een eigen `iok_`-tabel als geen standaardtabel past (motiveren). – Keuze Dries.
- **B03** – (vaste eis klant) – Alle gegevens in Dataverse, geen SharePoint-lijsten; SharePoint enkel als archief voor PDF's en foto's. – Startprompt, "Vaste eisen".
- **B04** – 2026-11-13 – **Offline werken is geen eis** en stuurt het ERD niet; geen mobile offline profile in het ontwerp. Offline blijft een mogelijke uitbreiding. – Feedback IOK 13/11 ("offline hoeft niet meer"); keuze Dries.
- **B05** – 2026-11-13 – **PDF wordt niet automatisch verzonden**: de inspecteur kijkt na, kan aanpassen en verstuurt zelf; het systeem registreert de verzendstatus. – Feedback IOK 13/11; BPMN hoofdproces + D3.
- **B06** – 2026-11-13 – **Versiebeheer van verslagen op basis van de controledatum.** – Feedback IOK 13/11 (D3); BPMN D3.
- **B07** – 2026-11-13 – **Stamgegevens wijzigen zonder terugwerkende kracht**: nieuwe versie, historische inspecties blijven ongewijzigd. – Feedback IOK 13/11 (D4); BPMN D4.
- **B08** – 2026-11-13 – **Enkel één bevoegde beheerder** mag stamgegevens (moederdata) en vaste teksten wijzigen. – Feedback IOK 13/11 (D4); BPMN D4 lane "Bevoegde beheerder".
- **B09** – 2026-11-13 – Finaal procesmodel = `IOK_02_ToBe_uitgeklapt_aangepast`; datamodel v2 = `IOK_erd_v2.drawio` (13 tabellen). – Dries.
