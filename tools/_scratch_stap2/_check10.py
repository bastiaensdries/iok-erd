import re, sys
sys.stdout.reconfigure(encoding="utf-8")

def sheets(path):
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"\n## Blad: ", txt)
    return [(p.split("\n")[0].strip(), p) for p in parts[1:]]

def parse(line):
    m = re.match(r"- r(\d+) \| (.*)$", line)
    row, rest = int(m.group(1)), m.group(2)
    d = {}
    for t in rest.split(" | "):
        mm = re.match(r"([A-Z]{1,3}): (.*)$", t)
        if mm:
            d[mm.group(1)] = mm.group(2)
    return row, d

for name, body in sheets(r"01_context/docs/Indienststelling versie 2022.md"):
    if name != "Algemeen":
        continue
    rows = [parse(l) for l in body.split("\n") if l.startswith("- r")]
    both = [(r, d) for r, d in rows if d.get("A", "").strip() and d.get("B", "").strip()]
    print("totaal A+B:", len(both))
    # categorise A
    code = re.compile(r"^[A-Z]\.?\d+(\.\d+)*\.?$")
    nietcode = [(r, d) for r, d in both if not code.match(d["A"].strip())]
    print("A niet-code:", len(nietcode))
    for r, d in nietcode:
        print("   ", r, repr(d["A"][:60]), "|B:", d["B"][:50])
    inl = [(r, d) for r, d in both if d["B"].strip().endswith(":")]
    print("inleidend (B eindigt op :):", len(inl), [(r, d["A"], d["B"][:40]) for r, d in inl])
