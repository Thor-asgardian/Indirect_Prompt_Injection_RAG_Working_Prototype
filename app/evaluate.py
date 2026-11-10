"""Runs the included structured evaluation set and writes a reproducible result."""
import json
from pathlib import Path
from .detector import detect
from .pipeline import SafeRAG

def main():
    root=Path(__file__).resolve().parents[1]
    cases=json.loads((root/"data"/"evaluation_set.json").read_text(encoding="utf-8"))
    rows=[]
    for c in cases:
        d=detect(c["text"])
        predicted=d.risk_level in ("medium","high")
        rows.append({"id":c["id"],"expected_flag":c["expected_flag"],"predicted_flag":predicted,
                     "risk_score":d.risk_score,"risk_level":d.risk_level,
                     "pass":predicted==c["expected_flag"]})
    tp=sum(r["expected_flag"] and r["predicted_flag"] for r in rows)
    fp=sum((not r["expected_flag"]) and r["predicted_flag"] for r in rows)
    fn=sum(r["expected_flag"] and (not r["predicted_flag"]) for r in rows)
    tn=sum((not r["expected_flag"]) and (not r["predicted_flag"]) for r in rows)
    summary={"cases":len(rows),"passed":sum(r["pass"] for r in rows),"TP":tp,"FP":fp,"FN":fn,"TN":tn,
             "precision":round(tp/(tp+fp),3) if tp+fp else 0,
             "recall":round(tp/(tp+fn),3) if tp+fn else 0,"results":rows}
    out=root/"evidence"/"evaluation_results.json"
    out.parent.mkdir(exist_ok=True); out.write_text(json.dumps(summary,indent=2),encoding="utf-8")
    print(json.dumps(summary,indent=2))
if __name__=="__main__": main()
