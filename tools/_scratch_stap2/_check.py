import re, sys, io
sys.stdout.reconfigure(encoding="utf-8")
p = r"01_context/docs/A_Verslaggeving Indienststelling Schommel.md"
txt = open(p, encoding="utf-8").read()
sheets = re.split(r"\n## Blad: ", txt)
total = 0
for s in sheets[1:]:
    name = s.split("\n")[0]
    rows = s.split("\n")
    st = [r.strip() for r in rows if re.search(r"\|\s*G:\s*\S", r)]
    total += len(st)
    print("=== ", name, "G-status:", len(st))
    for r in st:
        print("    ", r)
print("TOTAAL", total)
