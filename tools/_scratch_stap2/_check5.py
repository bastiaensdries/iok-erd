import re, sys, collections
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

print("=== B_risicoanalyse terrein")
for name, body in sheets(r"01_context/docs/B_risicoanalyse terrein.md"):
    rows = cells(body)
    st = [(r, d["G"]) for r, d in sorted(rows.items()) if d.get("G", "").strip() and r and d.get("G").strip() in ("OK", "NOK", "nvt")]
    print(name, len(st), collections.Counter(v for _, v in st))
    print([ (r, v) for r, v in st])

print()
print("=== Overzicht bestaande speelterreinen")
for name, body in sheets(r"01_context/docs/Overzicht bestaande speelterreinen.md"):
    rows = cells(body)
    print("blad", name, "rijen met data:", len(rows))
    hdr = rows[min(rows)]
    codes = [(r, d.get("B", "").strip()) for r, d in sorted(rows.items()) if d.get("B", "").strip() and r != min(rows)]
    c = collections.Counter(x for _, x in codes)
    dup = {k: v for k, v in c.items() if v > 1}
    print("codes:", len(codes), "uniek:", len(c), "dubbele codes:", len(dup), "rijen in dup:", sum(dup.values()))
    print("dup:", sorted(dup.items(), key=lambda x: -x[1]))
    ids = [(r, d.get("A", "").strip()) for r, d in rows.items() if d.get("A", "").strip() and r != min(rows)]
    print("unieke ID:", len(set(x for _, x in ids)), "van", len(ids))
    gem = set(d.get("D", "").strip() for r, d in rows.items() if d.get("D", "").strip() and r != min(rows))
    print("gemeenten:", len(gem))
    best = collections.Counter(d.get("E", "").strip() for r, d in rows.items() if d.get("E", "").strip() and r != min(rows))
    print("bestuur:", best)
    F = [int(float(d.get("F", "0") or 0)) for r, d in rows.items() if r != min(rows)]
    G = [int(float(d.get("G", "0") or 0)) for r, d in rows.items() if r != min(rows)]
    print("F som:", sum(F), "max:", max(F), "verdeling 0/1/>1:", sum(1 for x in F if x == 0), sum(1 for x in F if x == 1), sum(1 for x in F if x > 1))
    print("G som:", sum(G), "max:", max(G))
