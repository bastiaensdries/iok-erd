import re, sys
sys.stdout.reconfigure(encoding="utf-8")

def sheets(path):
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"\n## Blad: ", txt)
    out = []
    for p in parts[1:]:
        name = p.split("\n")[0].strip()
        out.append((name, p))
    return out

for path in [r"01_context/docs/Indienststelling versie 2022.md"]:
    tot = 0
    for name, body in sheets(path):
        codes = []
        for m in re.finditer(r"^- r(\d+) \| A: (.*)$", body, re.M):
            rowno, aval = int(m.group(1)), m.group(2)
            if "|" in aval:
                aval = aval.split("|")[0].strip()
            codes.append((rowno, aval))
        # rows with text in B
        b_rows = {}
        for m in re.finditer(r"^- r(\d+) \| B: (.*)$", body, re.M):
            b_rows[int(m.group(1))] = m.group(2)
        assessed = [(r, a) for (r, a) in codes if r in b_rows]
        inl = [(r, a) for (r, a) in assessed if b_rows[r].strip().endswith(":")]
        print(f"{name:45s} A-codes={len(codes):4d} met B-tekst={len(assessed):4d} inleidend={len(inl):3d} punten={len(assessed)-len(inl):4d}")
        tot += len(assessed) - len(inl)
    print("TOTAAL punten:", tot)
