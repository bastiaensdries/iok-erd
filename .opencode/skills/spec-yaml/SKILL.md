---
name: spec-yaml
description: Schrijf de machineleesbare specificatie (spec.yaml) van het IOK-datamodel v3, als basis voor een later bouwscript via de Dataverse Web API.
---

# Specificatie (YAML)

**Uitvoer:** `03_output/spec.yaml`. Moet 1-op-1 overeenkomen met `03_output/datamodel_v3.md`.

## Schema
```yaml
publisher: { prefix: iok, naam: IOK }
solution: { naam: IOK_Speelterreinen, versie: 1.0.0 }
globale_keuzelijsten:
  - schema: iok_beoordeling
    opties: [ { label: OK, waarde: 100000000 }, { label: NOK, waarde: 100000001 }, { label: nvt, waarde: 100000002 } ]
tabellen:
  - schema: iok_speelterrein        # standaardtabel? → bestaand: true en enkel extra kolommen
    bestaand: false
    weergavenaam: { enkelvoud: Speelterrein, meervoud: Speelterreinen }
    eigenaarschap: user            # user | organization  (niet meer te wijzigen)
    primaire_kolom: { schema: iok_naam, lengte: 200 }
    notities: false                # niet meer uit te zetten
    statusredenen: { actief: [Actief], inactief: [Opgeheven] }
    kolommen:
      - { schema: iok_code, type: text, lengte: 20, verplicht: true }
    alternatieve_sleutels:
      - { schema: iok_ak_speelterrein_code, kolommen: [iok_code] }
relaties:
  - { schema: iok_account_speelterrein, type: 1N, van: account, naar: iok_speelterrein, lookup: iok_bestuurid, verwijderen: restrict }
  - { schema: iok_controlepunt_toestelsoort, type: NN, tabellen: [iok_controlepunt, iok_toestelsoort] }
```
## Regels
- Types: text, memo, int, decimal(precisie), float, money, date, datetime, choice, choices, bool, lookup, file, image, autonumber.
- Keuzewaarden starten bij `100000000` (standaard voor publisherprefixen).
- Markeer met `# ONZEKER:` wat nog afhangt van een open vraag (verwijs naar Qnn/Vn).
- Controleer na het schrijven: elke lookup heeft een relatie, elke relatie verwijst naar bestaande tabellen, geen dubbele schemanamen, alle eigen namen beginnen met `iok_`.
