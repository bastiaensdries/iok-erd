---
name: dataverse-modellering
description: Conventies en checklist voor het ontwerpen van Dataverse-tabellen, kolommen, keuzelijsten en relaties voor het IOK-datamodel. Laden vóór je een tabel, kolom of relatie voorstelt of herziet.
---

# Dataverse-modellering (IOK)

## 1. Eerst een standaardtabel, dan pas `iok_` (B01, B02)
Controleer voor elk gegeven of een ingebouwde tabel past. Kandidaten om te **evalueren** (geen beslissing, wel bespreken):

| Standaardtabel (logische naam) | Mogelijke rol bij IOK | Aandachtspunt |
|---|---|---|
| Account (`account`) | lokaal bestuur / uitbater | heeft al adresvelden (address1_…); hiërarchie via `parentaccountid` |
| Contact (`contact`) | contactpersoon bij bestuur | |
| Gebruiker (`systemuser`) | inspecteur, beheerder | geen eigen inspecteurtabel nodig |
| Team / Business unit | eigenaarschap, beveiliging | |
| E-mail (`email`) | verzending PDF naar bestuur, verzendstatus | activiteit; regarding = verslag |
| Taak (`task`) | herinneringen bij intake (V2) | activiteit |
| Notitie (`annotation`) | bijlagen/notities | eis: bestanden horen in SharePoint |
| SharePoint-documentlocatie (`sharepointdocumentlocation`) | koppeling record ↔ SharePoint-map (archief PDF/foto's) | standaardintegratie |
| Klantadres (`customeraddress`) | extra adressen | alternatief voor een eigen adrestabel |

Eigen tabel nodig? Schemanaam `iok_<enkelvoud_kleine_letters>` (bv. `iok_speelterrein`). Eigen kolom op standaardtabel: ook `iok_` (bv. `account.iok_eenheden`).

## 2. Per tabel vastleggen
- Type: standaard of **activiteit**; eigenaarschap: **gebruiker/team** of **organisatie**
- Primaire naamkolom (wat de gebruiker ziet, bv. code + naam)
- Status (`statecode` Actief/Inactief) en **statusredenen** (`statuscode`) i.p.v. een eigen statuskolom waar mogelijk
- Alternatieve sleutel(s) voor unieke codes (eis: unieke terrein- en toestelcodes) en voor integratie via de Web API
- Bron: BPMN-stap + bronbestand

## 3. Kolommen
Kies het type bewust: tekst (lengte!), meerregelige tekst, geheel getal, decimaal (aantal decimalen), datum (alleen datum vs. datum+tijd, gedrag), keuze (lokaal of **globale keuzelijst** als ze herbruikbaar is), meerdere keuzes, ja/nee, lookup, bestand, afbeelding, autonummer, formule.
Keuzelijsten uit de Excel-sjablonen staan in `01_context/keuzelijsten/`: gebruik ze als bron. Lange standaardzinnen zijn **geen** keuzelijst maar rijen in een tabel (eis: besluiten en standaardzinnen uit een tabel).

## 4. Relaties
- 1:N met expliciet **verwijdergedrag**: koppeling verwijderen (referential), verwijderen beperken (restrict), alles trapsgewijs (parental) of aangepast. Een tabel kan maar één parental-relatie hebben.
- N:N: native (verborgen koppeltabel, géén extra kolommen) of manueel via een `iok_`-koppeltabel (wél extra kolommen). Kies manueel zodra de koppeling eigen gegevens heeft.
- Vermijd relaties in twee richtingen voor hetzelfde verband en dubbele paden (bv. HIC-meting aan verslag én opmerking).

## 5. Achteraf niet (of moeilijk) te wijzigen → expliciet melden
Publisherprefix, schemanaam van tabel/kolom, eigenaarschapstype, activiteitstabel ja/nee, kolomtype, en het aanzetten van notities/activiteiten/connecties op een tabel (eenmaal aan, blijft aan).

## 6. Verifiëren
Staat de MCP-server **dataverse** aan? Gebruik ze **alleen om te lezen**, bv. om na te gaan welke kolommen en relaties een standaardtabel (account, contact, systemuser, email) al heeft, zodat we geen dubbele `iok_`-kolommen maken. Nooit iets aanmaken of wijzigen.

Twijfel over een limiet of mogelijkheid (bestand- vs. afbeeldingskolommen voor foto's, aantal alternatieve sleutels, verwijdergedrag, …)? Zoek het op via de **mslearn**-MCP en vermeld de bron. Niet gokken.
