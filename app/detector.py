"""Explainable heuristic detector for indirect prompt injection indicators."""
from dataclasses import dataclass, asdict
import re

PATTERNS = [
    ("override_instruction", r"\b(ignore|disregard|override)\b.{0,45}\b(previous|prior|above|system|developer|instructions?)\b", 4),
    ("secret_exfiltration", r"\b(reveal|print|send|expose|leak)\b.{0,40}\b(secret|password|api key|credential|token|system prompt)\b", 5),
    ("tool_misuse", r"\b(call|invoke|use|run)\b.{0,35}\b(tool|browser|shell|terminal|function|api)\b", 3),
    ("role_impersonation", r"\b(system message|developer message|new system prompt|assistant instruction)\b", 3),
    ("concealment", r"\b(do not tell|hide this|keep this secret|silently)\b", 2),
    ("instruction_claim", r"\b(this document|this page|the following text)\b.{0,50}\b(instructs|commands|orders)\b", 2),
]
@dataclass
class Detection:
    risk_score: int
    risk_level: str
    labels: list
    matched_phrases: list
    def to_dict(self): return asdict(self)

def detect(text: str) -> Detection:
    labels, matches, score = [], [], 0
    for label, pattern, weight in PATTERNS:
        found = re.findall(pattern, text or "", flags=re.I | re.S)
        if found:
            labels.append(label); score += weight
            # Save short matching context without dumping a whole document.
            m = re.search(pattern, text, flags=re.I | re.S)
            if m: matches.append(m.group(0)[:100])
    level = "low" if score < 3 else "medium" if score < 6 else "high"
    return Detection(score, level, labels, matches)
