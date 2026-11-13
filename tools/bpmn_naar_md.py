"""Vat BPMN-bestanden samen tot leesbare markdown (zonder diagramcoördinaten).

Gebruik:  python tools/bpmn_naar_md.py
Leest:    00_bronnen/BPMN/*.bpmn
Schrijft: 01_context/bpmn/<naam>.md  — per proces/subproces: lanes, stappen (in volgorde van
          sequence flows), beslissingen met uitgangen, data objects/stores en annotaties.
"""
import re
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC, OUT = ROOT / "00_bronnen/BPMN", ROOT / "01_context/bpmn"
B = "{http://www.omg.org/spec/BPMN/20100524/MODEL}"
NODE = {"task": "Taak", "userTask": "Gebruikerstaak", "serviceTask": "Systeemtaak", "manualTask": "Manuele taak",
        "sendTask": "Verzendtaak", "receiveTask": "Ontvangsttaak", "scriptTask": "Scripttaak",
        "businessRuleTask": "Regeltaak", "subProcess": "Subproces", "callActivity": "Call activity",
        "exclusiveGateway": "Beslissing (XOR)", "parallelGateway": "Parallel (AND)",
        "inclusiveGateway": "Inclusief (OR)", "eventBasedGateway": "Event-gateway",
        "startEvent": "Start", "endEvent": "Einde", "intermediateThrowEvent": "Tussen-event (gooit)",
        "intermediateCatchEvent": "Tussen-event (vangt)", "boundaryEvent": "Boundary-event"}


def nm(el):
    return re.sub(r"\s+", " ", (el.get("name") or "").strip()) or f"({el.get('id')})"


def event_kind(el):
    for c in el:
        t = c.tag.replace(B, "")
        if t.endswith("EventDefinition"):
            return " " + t.replace("EventDefinition", "")
    return ""


def walk(proc, depth, lanes, out):
    h = "#" * min(depth + 2, 6)
    nodes = {c.get("id"): c for c in proc if c.tag.replace(B, "") in NODE}
    flows = [c for c in proc if c.tag == B + "sequenceFlow"]
    succ = {}
    for f in flows:
        succ.setdefault(f.get("sourceRef"), []).append(f)
    # volgorde: breadth-first vanaf start-events
    order, seen = [], set()
    queue = [i for i, n in nodes.items() if n.tag == B + "startEvent"] or list(nodes)
    while queue:
        i = queue.pop(0)
        if i in seen or i not in nodes:
            continue
        seen.add(i); order.append(i)
        queue += [f.get("targetRef") for f in succ.get(i, [])]
    order += [i for i in nodes if i not in seen]
    for i in order:
        n = nodes[i]; t = n.tag.replace(B, "")
        lane = f" — _{lanes[i]}_" if i in lanes else ""
        extra = event_kind(n) if "Event" in t else ""
        if t == "boundaryEvent":
            extra += f" op '{nm(nodes.get(n.get('attachedToRef'), n))}'"
        out.append(f"- **{NODE[t]}{extra}**: {nm(n)}{lane}")
        outs = succ.get(i, [])
        if "Gateway" in t or len(outs) > 1:
            for f in outs:
                lab = f" [{nm(f)}]" if f.get("name") else ""
                out.append(f"  - →{lab} {nm(nodes[f.get('targetRef')]) if f.get('targetRef') in nodes else f.get('targetRef')}")
        for io in n.findall(f"{B}dataOutputAssociation") + n.findall(f"{B}dataInputAssociation"):
            pass
    for c in proc:
        t = c.tag.replace(B, "")
        if t in ("dataObjectReference", "dataStoreReference"):
            out.append(f"- _Data_: {nm(c)}")
        elif t == "textAnnotation":
            txt = re.sub(r"\s+", " ", "".join(c.itertext())).strip()
            if txt:
                out.append(f"- _Annotatie_: {txt}")
    for c in proc:
        if c.tag in (B + "subProcess", B + "transaction", B + "adHocSubProcess"):
            out.append(f"\n{h}# Subproces: {nm(c)}\n")
            walk(c, depth + 1, lanes, out)


def convert(path):
    root = ET.parse(path).getroot()
    out = [f"# {path.name}\n", "_Samenvatting zonder diagramcoördinaten. Volgorde volgt de sequence flows._\n"]
    names = {}
    for col in root.iter(B + "collaboration"):
        for p in col.findall(B + "participant"):
            names[p.get("processRef")] = nm(p)
        msgs = col.findall(B + "messageFlow")
        if msgs:
            idx = {e.get("id"): nm(e) for e in root.iter() if e.get("id")}
            out.append("## Berichtenstromen\n")
            for m in msgs:
                out.append(f"- {idx.get(m.get('sourceRef'))} → {idx.get(m.get('targetRef'))}" + (f" [{nm(m)}]" if m.get("name") else ""))
            out.append("")
    for proc in root.findall(B + "process"):
        lanes = {}
        for lane in proc.iter(B + "lane"):
            for ref in lane.findall(B + "flowNodeRef"):
                lanes[ref.text] = nm(lane)
        out.append(f"\n## Proces: {names.get(proc.get('id'), nm(proc))}\n")
        ln = sorted(set(lanes.values()))
        if ln:
            out.append("Lanes: " + ", ".join(ln) + "\n")
        walk(proc, 1, lanes, out)
    return "\n".join(out)


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for f in sorted(SRC.glob("*.bpmn")):
        md = convert(f)
        (OUT / f"{f.stem}.md").write_text(md, encoding="utf-8")
        print(f"OK   {f.name}  ({len(md)//1000} kB, origineel {f.stat().st_size//1000} kB)")
