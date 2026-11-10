"""Secure RAG demonstration with untrusted retrieval boundary."""
from pathlib import Path
import json
from datetime import datetime, timezone
from .detector import detect
from .retriever import load_documents, retrieve

class SafeRAG:
    def __init__(self, data_dir=None, audit_path=None, threshold=6):
        root=Path(__file__).resolve().parents[1]
        self.data_dir=Path(data_dir or root/"data")
        self.audit_path=Path(audit_path or root/"evidence"/"audit.jsonl")
        self.threshold=threshold
        self.documents=load_documents(self.data_dir)

    def answer(self, question):
        hits=retrieve(question,self.documents)
        inspected=[]
        accepted=[]
        for hit in hits:
            result=detect(hit["text"])
            item={"id":hit["id"],"source":hit["source"],"retrieval_score":hit["score"],
                  "detection":result.to_dict()}
            inspected.append(item)
            if result.risk_score >= self.threshold:
                item["action"]="quarantined"
            else:
                item["action"]="included_as_untrusted_evidence"
                accepted.append(hit)
        response=self._extract_answer(question,accepted)
        event={"timestamp":datetime.now(timezone.utc).isoformat(),"question":question,
               "inspected":inspected,"answer":response,
               "mitigation":"high-risk retrieved chunks quarantined; accepted text treated as untrusted evidence"}
        self.audit_path.parent.mkdir(parents=True,exist_ok=True)
        with self.audit_path.open("a",encoding="utf-8") as f: f.write(json.dumps(event)+"\n")
        return {"answer":response,"retrieved":inspected,"accepted_sources":[d["source"] for d in accepted],
                "quarantined":[x["source"] for x in inspected if x["action"]=="quarantined"],
                "mitigation":event["mitigation"]}

    @staticmethod
    def _extract_answer(question, docs):
        # Deterministic extractive answerer; never follows instructions in source text.
        q=question.lower()
        facts=[]
        for d in docs:
            for line in d["text"].splitlines():
                line=line.strip()
                if not line or line.startswith("#"): continue
                if any(term in line.lower() for term in ("refund","support","shipping","return","business days","days","policy")):
                    facts.append(line)
        if facts: return "Based on approved retrieved evidence: " + " ".join(dict.fromkeys(facts))
        return "I could not find a supported answer in the approved documents. Please consult the source owner."
