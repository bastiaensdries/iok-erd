import re, sys, collections
sys.stdout.reconfigure(encoding="utf-8")
p = r"01_context/docs/Overzicht bestaande speelterreinen.md"
lines = [l for l in open(p, encoding="utf-8").read().split("\n") if l.startswith("- r")]

def parse(line):
    m = re.match(r"- r(\d+) \| (.*)$", line)
    row, rest = int(m.group(1)), m.group(2)
    toks = rest.split(" | ")
    d = {}
    for t in toks:
        mm = re.match(r"([A-Z]{1,3}): (.*)$", t)
        if mm:
            d[mm.group(1)] = mm.group(2)
        else:
            print("PARSE-FOUT rij", row, repr(t))
    return row, d

for want in (395, 410, 300, 296, 13):
    for l in lines:
        if l.startswith(f"- r{want} |"):
            row, d = parse(l)
            print("RIJ", row, d)
print()
rows = [parse(l) for l in lines]
print("aantal regels:", len(rows))
data = [(r, d) for r, d in rows if r > 1]
print("data-rijen:", len(data))
withcode = [(r, d) for r, d in data if d.get("B", "").strip()]
print("met code:", len(withcode))
c = collections.Counter(d["B"].strip() for r, d in withcode)
print("uniek:", len(c))
dup = {k: v for k, v in c.items() if v > 1}
print("dup codes:", len(dup), "rijen:", sum(dup.values()))
print(sorted(dup.items(), key=lambda x: -x[1]))
gem = set(d.get("D", "").strip() for r, d in data if d.get("D", "").strip())
print("gemeenten:", len(gem), sorted(gem))
print("bestuur:", collections.Counter(d.get("E", "").strip() for r, d in data))
print("zonder A:", [(r, d) for r, d in data if not d.get("A", "").strip()])
F = [int(float(d.get("F", "0") or 0)) for r, d in data]
G = [int(float(d.get("G", "0") or 0)) for r, d in data]
print("F:", sum(F), max(F), sum(1 for x in F if x == 0), sum(1 for x in F if x == 1), sum(1 for x in F if x > 1))
print("G:", sum(G), max(G), sum(1 for x in G if x == 0), sum(1 for x in G if x > 1))
print("F>1 rijen:", [(r, d.get("C"), d.get("F")) for r, d in data if int(float(d.get("F", "0") or 0)) > 1][:10])
print("G>50 rijen:", [(r, d.get("C"), d.get("G")) for r, d in data if int(float(d.get("G", "0") or 0)) > 50])
