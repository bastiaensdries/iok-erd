import re, sys
sys.stdout.reconfigure(encoding="utf-8")

def count(path):
    txt = open(path, encoding="utf-8").read()
    parts = re.split(r"\n## Blad: ", txt)
    tot = 0
    out = []
    for p in parts[1:]:
        name = p.split("\n")[0].strip()
        rows = {}
        for l in p.split("\n"):
            if not l.startswith("- r"):
                continue
            m = re.match(r"- r(\d+) \| (.*)$", l)
            row, rest = int(m.group(1)), m.group(2)
            d = rows.setdefault(row, {})
            for t in rest.split(" | "):
                mm = re.match(r"([A-Z]{1,3}): (.*)$", t)
                if mm:
                    d[mm.group(1)] = mm.group(2)
        both = [(r, d) for r, d in rows.items() if d.get("A", "").strip() and d.get("B", "").strip()]
        code = [x for x in both if re.match(r"^[A-Z]?\.?\d", x[1]["A"].strip())]
        inl = [x for x in code if x[1]["B"].strip().endswith(":")]
        out.append((name, len(code), len(inl), len(code) - len(inl)))
        tot += len(code)
    return out, tot

for f in ["Indienststelling versie 2022.md", "Risicoanalyse toestellen versie 2022.md"]:
    out, tot = count(r"01_context/docs/" + f)
    print("###", f, "totaal code-rijen:", tot)
    for x in out:
        print("   ", x)
