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
        # split on " | X: " patterns
        for part in re.split(r"\s\|\s(?=[A-Z]{1,3}:)", rest):
            mm = re.match(r"([A-Z]{1,3}):\s?(.*)$", part)
            if mm:
                d[mm.group(1)] = mm.group(2)
    return rows

for path in [r"01_context/docs/Indienststelling versie 2022.md",
             r"01_context/docs/risicoanalyse skate toestellen versie 2022.md",
             r"01_context/docs/risicoanalyse terrein versie 2022.md"]:
    print("#####", path)
    tot = 0
    for name, body in sheets(path):
        rows = cells(body)
        assessed = [(r, d) for r, d in rows.items() if d.get("A", "").strip() and d.get("B", "").strip()]
        inl = [(r, d) for r, d in assessed if d["B"].strip().endswith(":")]
        print(f"{name:42s} A-codes={sum(1 for d in rows.values() if d.get('A','').strip()):4d} met B={len(assessed):4d} inleidend={len(inl):3d} punten={len(assessed)-len(inl):4d}")
        if path.endswith("Indienststelling versie 2022.md"):
            tot += len(assessed) - len(inl)
    if path.endswith("Indienststelling versie 2022.md"):
        print("TOTAAL punten (incl Standaardlijsten):", tot)
