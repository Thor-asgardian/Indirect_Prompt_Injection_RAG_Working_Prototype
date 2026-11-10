# Indirect Prompt Injection Detection for RAG Systems

A local, educational M.Tech prototype that demonstrates a defensive RAG pipeline:
document ingestion → retrieval → untrusted-content inspection → safe context assembly → answer generation → audit logging.

## Features
- Local document corpus (Markdown/text); no API key required.
- Rule-based risk scoring for indirect prompt injection indicators.
- Quarantine mode: high-risk retrieved passages are excluded from model context.
- Safe-context mode: retrieved text is explicitly marked as untrusted evidence, never as instructions.
- Three built-in test cases plus a structured evaluation set.
- JSONL audit events and a simple CLI.

## Requirements
- Python 3.10+
- No third-party dependencies for the core prototype.
- Optional: `pytest` to run tests with `python -m pytest`.

## Windows / VS Code setup
1. Extract the project ZIP.
2. Open the `rag_indirect_injection_prototype` folder in VS Code.
3. Open Terminal → New Terminal.
4. Create and activate a virtual environment:
   ```powershell
   py -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
5. Install optional test runner:
   ```powershell
   py -m pip install pytest
   ```
6. Run the demo:
   ```powershell
   py -m app.cli --question "What is the refund period?"
   ```
7. Run the full test suite:
   ```powershell
   py -m pytest -q
   ```
   Or without pytest:
   ```powershell
   py -m app.evaluate
   ```

## Example
```powershell
py -m app.cli --question "What is the refund period?"
py -m app.cli --question "Summarize the support policy."
```

## Project structure
- `app/detector.py`: explainable indicator scoring.
- `app/retriever.py`: simple local keyword retrieval.
- `app/pipeline.py`: end-to-end secure RAG workflow.
- `app/cli.py`: command-line interface.
- `app/evaluate.py`: structured evaluation runner.
- `data/`: benign and adversarial sample documents.
- `tests/`: unit and integration tests.
- `evidence/`: sample run outputs and evaluation results.

## Security design
1. Retrieved documents are data, not instructions.
2. The detector flags suspicious phrases and instruction-like patterns.
3. High-risk chunks are quarantined by default.
4. Lower-risk chunks are wrapped in explicit untrusted-evidence delimiters.
5. The answer stage only extracts relevant facts from approved evidence; it does not execute document instructions.

## Limitations
- The detector is heuristic and can miss novel or obfuscated attacks.
- Keyword overlap retrieval is not a production vector database.
- The included answerer is extractive and deterministic, not a hosted LLM.
- Scores are triage signals, not proof that a document is malicious.
- Production deployment requires adversarial testing, human review, access controls, provenance, model-specific prompt hardening, and monitoring.

## Safe extension
An LLM can be added behind `AnswerGenerator` in `app/pipeline.py`. Keep the trust boundary: never concatenate retrieved text into privileged system instructions; use structured evidence fields and validate outputs.
