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
print("=== OVT")
print("rijen:", len(data), "| zonder F:", [r for r, d in data if not d.get("F")], "| zonder G:", [r for r, d in data if not d.get("G")])
F = collections.Counter(int(float(d.get("F", "0") or 0)) for r, d in data)
G = collections.Counter(int(float(d.get("G", "0") or 0)) for r, d in data)
print("F-verdeling:", sorted(F.items()))
print("F som:", sum(k * v for k, v in F.items()), "max:", max(F))
print("G som:", sum(k * v for k, v in G.items()), "max:", max(G), "G=0:", G.get(0))
print("F=15:", [(r, d.get("C"), d.get("D"), d.get("G")) for r, d in data if d.get("F") == "15"])
print("F=0:", [(r, d.get("C"), d.get("D"), d.get("B")) for r, d in data if d.get("F") == "0"])
print("G>45:", [(r, d.get("C"), d.get("D"), d.get("G")) for r, d in data if int(float(d.get("G") or 0)) > 45])
print()

print("=== OST")
p2 = r"01_context/docs/Overzicht soorten speeltoestellen.md"
lines2 = [l for l in open(p2, encoding="utf-8").read().split("\n") if l.startswith("- r")]
data2 = [(r, d) for r, d in (parse(l) for l in lines2) if r > 1]
print("rijen:", len(data2))
cat = None
cats = []
types = 0
for r, d in data2:
    a = d.get("A", "").strip()
    b = d.get("B", "").strip()
    c = d.get("C", "").strip()
    if a:
        cat = a
        cats.append([a, 0, 0])
    if b:
        types += 1
        if cats:
            cats[-1][1] += 1
            try:
                cats[-1][2] += int(float(c))
            except Exception:
                pass
print("categorieen:", len(cats), "types:", types)
for x in cats:
    print("  ", x)
print("som eenheden:", sum(x[2] for x in cats))
