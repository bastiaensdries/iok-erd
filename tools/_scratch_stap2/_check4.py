import re, sys
sys.stdout.reconfigure(encoding="utf-8")

def sheets(path):
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"\n## Blad: ", txt)
    return [(p.split("\n")[0].strip(), p) for p in parts[1:]]

def cells(body):
    rows = {}
    for line in body.split("\n"):
        if not line.startswith("- r"):
            continue
        m = re.match(r"- r(\d+) \| (.*)$", line)
        if not m:
            continue
        row, rest = int(m.group(1)), m.group(2)
        d = rows.setdefault(row, {})
        for part in re.split(r"\s\|\s(?=[A-Z]{1,3}:)", rest):
            mm = re.match(r"([A-Z]{1,3}):\s?(.*)$", part)
            if mm:
                d[mm.group(1)] = mm.group(2)
    return rows

for name, body in sheets(r"01_context/docs/Indienststelling versie 2022.md"):
    if name != "Draaitoestel":
        continue
    rows = cells(body)
    for r in sorted(rows):
        d = rows[r]
        if d.get("A", "").strip() and d.get("B", "").strip():
            print(r, "|A:", d["A"][:70], "|B:", d["B"][:60])
