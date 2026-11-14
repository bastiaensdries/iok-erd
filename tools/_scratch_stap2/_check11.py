import re, sys, collections
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

pats = {
    "alles": None,
    "geen trailing dot": r"^[A-Z]\.?\d+(\.\d+)*$",
    "min 2 niveau": r"^[A-Z]\.?\d+(\.\d+)+$",
    "kort (<=12)": None,
}
for name, body in sheets(r"01_context/docs/Indienststelling versie 2022.md"):
    if name != "Algemeen":
        continue
    rows = [parse(l) for l in body.split("\n") if l.startswith("- r")]
    both = [(r, d) for r, d in rows if d.get("A", "").strip() and d.get("B", "").strip()]
    lens = collections.Counter(len(d["A"].strip()) for r, d in both)
    print("lengtes A:", sorted(lens.items()))
    for r, d in both:
        a = d["A"].strip()
        if len(a) > 12:
            print("  lang:", r, repr(a))
