# Datamodel v2 (uit `00_bronnen/datamodel_v2/IOK_erd_v2.drawio`)

_Automatisch omgezet uit draw.io. Kolommen per tabel in diagramvolgorde: sleutel | naam | (type/opmerking)._


## Diagram: Use case diagram IOK v2 — 13 tabellen


### BEOORDELING

- PK | beoordeling_id: INT {NNA}
- FK | controle_id: INT {NNA}
- FK | speeltoestel_id: INT (leeg = terrein)
- · | soort: VARCHAR(20) {NNA}
- · | overzichtsfoto_url: VARCHAR(400)

### BESTUUR

- PK | bestuur_id: INT {NNA}
- · | naam: VARCHAR(120) {NNA}
- · | soort: VARCHAR(10) {NNA} (Gemeente/OCMW)
- · | gemeente: VARCHAR(80) {NNA}
- · | straat_nr: VARCHAR(120)
- · | postcode: CHAR(4)
- · | plaats: VARCHAR(80)
- · | contact_naam: VARCHAR(120)
- · | contact_email: VARCHAR(254) {NNA}

### CHECKLIST

- PK | checklist_id: INT {NNA}
- · | naam: VARCHAR(80) {NNA}
- · | norm: VARCHAR(40) {NNA}
- · | versie: VARCHAR(10) {NNA}
- · | voor: VARCHAR(10) {NNA} (terrein/toestel)
- · | deel: SMALLINT {NNA} (1/2)

### CONTROLE

- PK | controle_id: INT {NNA}
- FK | speelterrein_id: INT {NNA}
- FK | inspecteur_id: INT {NNA}
- · | datum: DATE {NNA}
- · | status: VARCHAR(20) {NNA}

### CONTROLEPUNT

- PK | controlepunt_id: INT {NNA}
- FK | checklist_id: INT {NNA}
- FK | ouder_id: INT
- · | code: VARCHAR(10) {NNA}
- · | tekst: VARCHAR(500) {NNA}
- · | volgorde: SMALLINT {NNA}

### CONTROLEVERSIE

- PK | rapportversie_id: INT {NNA}
- FK | controle_id: INT {NNA}
- · | versienummer: SMALLINT {NNA}
- · | pdf_url: VARCHAR(400) {NNA}
- · | aangemaakt_op: DATETIME {NNA}
- · | verzonden_op: DATETIME
- · | status: VARCHAR(20) {NNA}

### FOTO

- PK | foto_id: INT {NNA}
- FK | resultaat_id: INT {NNA}
- · | bestand_url: VARCHAR(400) {NNA}

### INSPECTEUR

- PK | inspecteur_id: INT {NNA}
- · | naam: VARCHAR(120) {NNA}
- · | email: VARCHAR(254) {NNA} UQ
- · | is_admin: BOOLEAN {NNA}

### RESULTAAT

- PK | resultaat_id: INT {NNA}
- FK | beoordeling_id: INT {NNA}
- FK | controlepunt_id: INT {NNA}
- · | status: VARCHAR(3) {NNA} (OK/NOK/nvt)
- · | opmerking: VARCHAR(2000)
- · | impact: DECIMAL(4,1)
- · | kans: DECIMAL(4,1)
- · | blootstelling: DECIMAL(4,1)

### SPEELTERREIN

- PK | speelterrein_id: INT {NNA}
- FK | bestuur_id: INT {NNA}
- · | code: VARCHAR(20)
- · | naam: VARCHAR(120) {NNA}
- · | straat_nr: VARCHAR(120)
- · | postcode: CHAR(4)
- · | plaats: VARCHAR(80)
- · | doelgroep: VARCHAR(40) (keuze)
- · | toezicht: VARCHAR(40) (keuze)
- · | eenheden: SMALLINT {NNA} (std 1)
- · | actief: BOOLEAN {NNA}

### SPEELTOESTEL

- PK | speeltoestel_id: INT {NNA}
- FK | speelterrein_id: INT {NNA}
- FK | toesteltype_id: INT {NNA}
- · | code: VARCHAR(30)
- · | omschrijving: VARCHAR(120) {NNA}
- · | leverancier: VARCHAR(80)
- · | type_fabrikant: VARCHAR(60)
- · | serienummer: VARCHAR(60)
- · | bouwjaar: SMALLINT
- · | attest: VARCHAR(60)
- · | doelgroep: VARCHAR(40) (keuze)
- · | toezicht: VARCHAR(40) (keuze)
- · | eenheden: SMALLINT {NNA}
- · | status: VARCHAR(20) {NNA}

### TOESTELTYPE

- PK | toesteltype_id: INT {NNA}
- · | categorie: VARCHAR(60) {NNA}
- · | omschrijving: VARCHAR(80) {NNA}
- · | standaard_eenheden: SMALLINT {NNA}

### TOESTEL_CHECKLIST

- PK,FK | speeltoestel_id: INT {NNA}
- PK,FK | checklist_id: INT {NNA}

## Relaties (15)

Notatie: bron [kardinaliteit bij bron] — [kardinaliteit bij doel] doel : label

- BEOORDELING [1] — [0..N] RESULTAAT : 1 : 0..M
- BESTUUR [1] — [1..N] SPEELTERREIN : 1 : 1..M
- CHECKLIST [1] — [0..N] TOESTEL_CHECKLIST : 1 : 0..M
- CHECKLIST [1] — [1..N] CONTROLEPUNT : 1 : 1..M
- CONTROLE [1] — [1..N] BEOORDELING : 1 : 1..M
- CONTROLE [1] — [1..N] CONTROLEVERSIE : 1 : 0..M
- CONTROLEPUNT [0..1] — [0..N] CONTROLEPUNT : ouder 0..1 : 0..M
- CONTROLEPUNT [1] — [0..N] RESULTAAT : 1 : 0..M
- INSPECTEUR [1] — [0..N] CONTROLE : 1 : 0..M
- RESULTAAT [1] — [0..N] FOTO : 1 : 0..M
- SPEELTERREIN [1] — [0..N] CONTROLE : 1 : 0..M
- SPEELTERREIN [1] — [0..N] SPEELTOESTEL : 1 : 0..M
- SPEELTOESTEL [0..1] — [0..N] BEOORDELING : 0..1 : 0..M
- SPEELTOESTEL [1] — [0..N] TOESTEL_CHECKLIST : 1 : 0..M
- TOESTELTYPE [1] — [0..N] SPEELTOESTEL : 1 : 0..M
## Opmerkingen bij de omzetting
- Notatie in het diagram is relationeel (INT-sleutels, VARCHAR, `{NNA}` = verplicht, `UQ` = uniek). Nog geen Dataverse-namen of -types, geen `iok_`-prefix.
- Relatie CONTROLE → CONTROLEVERSIE: het label zegt `1 : 0..M`, de pijlpunt in het diagram `1..N`. Het label is waarschijnlijk juist (een controle heeft pas een versie na PDF-generatie).
- De beschrijving van v2 in de oorspronkelijke startprompt (17 tabellen met `iok_`, o.a. doelgroep, standaardtekst, hicmeting, aanvraag, correctievraag) komt **niet** overeen met dit diagram. Dit diagram is de bron.
