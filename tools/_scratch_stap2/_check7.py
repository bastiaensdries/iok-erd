import re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
p = r"01_context/docs/Overzicht bestaande speelterreinen.md"
lines = [l for l in open(p, encoding="utf-8").read().split("\n") if l.startswith("- r")]

def parse(line):
    m = re.match(r"- r(\d+) \| (.*)$", line)
    row, rest = int(m.group(1)), m.group(2)
    d = {}
    for t in rest.split(" | "):
        mm = re.match(r"([A-Z]{1,3}): (.*)$", t)
        if mm:
            d[mm.group(1)] = mm.group(2)
    return row, d

data = [(r, d) for r, d in (parse(l) for l in lines) if r > 1]
bycode = collections.defaultdict(list)
for r, d in data:
    if d.get("B", "").strip():
        bycode[d["B"].strip().upper()].append((r, d))

dup = {k: v for k, v in bycode.items() if len(v) > 1}
print("case-insensitive dup codes:", len(dup), "rijen:", sum(len(v) for v in dup.values()))
for k in sorted(dup):
    print(k, [(r, d.get("A"), d.get("C"), d.get("D"), d.get("B")) for r, d in dup[k]])
print()
print("zonder code:", [(r, d.get("A"), d.get("C"), d.get("D")) for r, d in data if not d.get("B", "").strip()])
