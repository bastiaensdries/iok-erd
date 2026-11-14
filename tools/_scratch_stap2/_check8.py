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
print("rijen:", len(data), "unieke A:", len(set(d.get("A") for r, d in data)))
per = collections.Counter(d.get("D", "").strip() for r, d in data)
print("per gemeente:", per)
print()
# dubbele (naam, gemeente)
cnt = collections.Counter((d.get("C", "").strip().upper(), d.get("D", "").strip()) for r, d in data)
dupn = {k: v for k, v in cnt.items() if v > 1}
print("dubbele (naam,gemeente):", len(dupn))
for k, v in sorted(dupn.items()):
    print("  ", k, v, [(r, d.get("A"), d.get("B"), d.get("F"), d.get("G")) for r, d in data if (d.get("C", "").strip().upper(), d.get("D", "").strip()) == k])
print()
print("Oud-Turnhout rijen:")
for r, d in data:
    if d.get("D", "").strip() == "Oud-Turnhout":
        print("  ", r, d.get("A"), d.get("B"), d.get("C"), d.get("F"), d.get("G"))
