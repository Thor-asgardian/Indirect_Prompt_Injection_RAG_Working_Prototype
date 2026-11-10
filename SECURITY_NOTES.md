# Security outcome and response recommendations

## Demonstrated preventive control
High-risk retrieved chunks with score >= 6 are quarantined before answer construction. Lower-risk chunks remain explicitly untrusted evidence. The answerer extracts factual policy lines and does not interpret source text as instructions.

## Response recommendations
- Preserve source identity and provenance for every retrieved chunk.
- Keep system/developer instructions structurally separate from retrieved content.
- Quarantine or require human review for high-risk content.
- Apply least-privilege tool permissions; retrieval text must never authorize tool calls.
- Log detector labels, score, source, decision, and timestamp without logging secrets.
- Red-team with paraphrases, multilingual attacks, encoded text, indirect image/PDF content, and benign lookalikes.
- Validate the final answer against retrieved evidence and abstain when evidence is insufficient.

## Ethics and privacy
Use synthetic sample documents only. Do not upload confidential documents or real credentials. The evaluation set is small and educational; it is not a benchmark of real-world attack prevalence.
