"""Small transparent keyword retriever for reproducible local experiments."""
from pathlib import Path
import re
def tokenize(s):
    return set(re.findall(r"[a-z0-9]+", s.lower()))
def load_documents(folder):
    docs=[]
    for path in sorted(Path(folder).glob("*.txt")):
        docs.append({"id":path.stem,"source":path.name,"text":path.read_text(encoding="utf-8")})
    return docs
def retrieve(question, documents, top_k=4):
    q=tokenize(question)
    scored=[]
    for d in documents:
        terms=tokenize(d["text"])
        score=len(q & terms) / max(1,len(q))
        if score > 0:
            scored.append((score,d))
    scored.sort(key=lambda x:(x[0],x[1]["id"]), reverse=True)
    return [{"score":round(s,3),**d} for s,d in scored[:top_k]]
