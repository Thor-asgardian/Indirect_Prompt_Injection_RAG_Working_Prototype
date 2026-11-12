# Explainable and Adaptive Prompt Injection Detection Framework for LLM Applications

A research prototype that detects potentially malicious instructions in
prompts and retrieved text using a hybrid rule-based and
machine-learning approach. The project also provides feature-level
explanations, human-reviewed feedback, and controlled model retraining.

> **Research prototype notice:** This project is intended for academic
> experimentation and demonstration. Its current evaluation uses a
> curated synthetic dataset and does not establish production-grade
> security or generalization to all prompt-injection attacks.

## Table of Contents

-   [Overview](#overview)
-   [Key Features](#key-features)
-   [Architecture](#architecture)
-   [Technology Stack](#technology-stack)
-   [Experimental Dataset and
    Results](#experimental-dataset-and-results)
-   [Project Structure](#project-structure)
-   [Prerequisites](#prerequisites)
-   [Installation on Windows](#installation-on-windows)
-   [Run the Application](#run-the-application)
-   [API Endpoints](#api-endpoints)
-   [Testing](#testing)
-   [Model and Decision
    Configuration](#model-and-decision-configuration)
-   [Adaptive Learning Workflow](#adaptive-learning-workflow)
-   [Limitations](#limitations)
-   [Responsible Use](#responsible-use)
-   [Research Paper](#research-paper)

## Overview

Large Language Model (LLM) applications may process user prompts
together with external content such as webpages, documents, and
retrieved passages. Malicious instructions embedded in this content can
attempt to redirect the model away from the user's intended task. This
is commonly described as prompt injection; when the instructions are
embedded in external content, it is often called indirect prompt
injection.

This prototype analyzes submitted text using two complementary
components:

1.  **Rule-based detector:** checks configured suspicious patterns and
    calculates a rule risk score.
2.  **Machine-learning detector:** transforms text into TF-IDF features
    and applies a Logistic Regression classifier to estimate the
    malicious class probability.

The framework combines these signals using configured thresholds and
returns a decision with supporting information.

## Key Features

-   Hybrid rule-based and TF-IDF + Logistic Regression detection.
-   Direct prompt and retrieved-document text analysis.
-   Explainability using signed feature contributions from the linear
    classifier.
-   Rule evidence and detection-reason reporting.
-   FastAPI backend with interactive Swagger documentation.
-   HTML dashboard with prompt scanner, evaluation summary, and model
    information.
-   Feedback submission and human review workflow.
-   Candidate retraining using approved feedback.
-   Versioned model artifacts, active-model pointer, and retained
    baseline for comparison/rollback.
-   Audit logging for detection and adaptive-learning activity.

## Architecture

``` text
                  User / Retrieved Text
                           |
                           v
                    HTML Frontend
                           |
                           v
                     FastAPI API
                           |
               +-----------+-----------+
               |                       |
               v                       v
         Rule-based Engine        ML Detector
         - Pattern checks         - TF-IDF
         - Risk score             - Logistic Regression
               |                       |
               +-----------+-----------+
                           |
                           v
                    Hybrid Decision
                           |
              +------------+-------------+
              |            |             |
              v            v             v
          Decision     Rule Evidence  ML Feature
                                       Contributions
                           |
                           v
                    API JSON Response

       Human Feedback -> Review -> Approved Feedback
                                      |
                                      v
                              Candidate Retraining
                                      |
                                      v
                           Validation / Promotion
                                      |
                                      v
                             Model Version Registry
```

The feature contributions explain the Logistic Regression component.
They are not causal explanations and do not, by themselves, explain
every part of the hybrid decision.

## Technology Stack

  -----------------------------------------------------------------------
  Component                           Technology
  ----------------------------------- -----------------------------------
  Programming language                Python 3.12

  Backend API                         FastAPI

  API server                          Uvicorn

  Request validation                  Pydantic

  Machine learning                    scikit-learn

  Text representation                 TF-IDF

  Classifier                          Logistic Regression

  Model serialization                 joblib

  Feedback storage                    SQLite

  Frontend                            HTML, CSS, JavaScript

  Testing                             pytest

  Local LLM integration               Ollama (where enabled in the
                                      project configuration)
  -----------------------------------------------------------------------

## Experimental Dataset and Results

The template-aware experimental dataset contains **500 curated synthetic
samples** across these categories:

-   Benign
-   Direct injection
-   Indirect injection
-   Instruction override
-   Role manipulation
-   Context manipulation

The dataset split used in the reported experiment is:

  Partition               Samples
  --------------------- ---------
  Training                    366
  Validation                   69
  Independent testing          65
  **Total**               **500**

Template families were assigned to only one partition to reduce
repeated-template leakage. This does not guarantee semantic independence
or representativeness of real-world inputs.

### Independent-test results

At the application's configured ML probability threshold of **0.60**,
the promoted template-aware candidate produced:

  Metric              Result
  ----------------- --------
  Accuracy            92.31%
  Precision           98.11%
  Recall              92.86%
  F1-score            95.41%
  True negatives           8
  False positives          1
  False negatives          4
  True positives          52

The independent test set contains only 65 samples. In particular, the
context-manipulation category has only two test examples and neither was
detected. These results should be interpreted as prototype results on
this dataset, not as a guarantee of performance on unseen production
traffic.

## Project Structure

The following is a representative structure based on the implemented
modules. Some files may differ depending on the current local project
version.

``` text
Explainable_Adaptive_Prompt_Injection/
|
+-- app/
|   +-- main.py
|   +-- detector.py
|   +-- feedback_store.py
|   +-- adaptive_learning.py
|   +-- ml_detector.py
|   +-- evaluate_detectors.py
|   +-- analyze_errors.py
|   +-- analyze_thresholds.py
|   +-- explain_error_features.py
|
+-- frontend/
|   +-- index.html
|
+-- dataset/
|   +-- all_samples.csv
|
+-- dataset_template_aware/
|   +-- [dataset and evaluation CSV files]
|
+-- models/
|   +-- [versioned model artifacts]
|   +-- current_version.txt
|
+-- logs/
|   +-- adaptive_feedback.db
|   +-- hybrid_audit.jsonl
|
+-- tests/
|   +-- [pytest test modules]
|
+-- .venv/
+-- .gitignore
+-- README.md
```

The exact names of model files and supporting scripts may change as the
project evolves. Do not commit virtual environments, local databases,
secrets, or large generated artifacts unless your research repository
explicitly requires them.

## Prerequisites

-   Windows 10/11 or a compatible operating system.
-   Python 3.12.
-   Visual Studio Code or another Python IDE.
-   Internet access for initial package installation.
-   Git (optional).
-   Ollama only if the optional local LLM response-generation component
    is enabled.

## Installation on Windows

Open PowerShell in the project directory.

### 1. Create and activate a virtual environment

``` powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation for the current user, use the
appropriate execution-policy setting permitted on your computer, or
activate the environment using the VS Code Python interpreter selector.

### 2. Install dependencies

If the project contains a `requirements.txt` file:

``` powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If there is no requirements file, install the core packages used by the
API and ML prototype:

``` powershell
python -m pip install fastapi "uvicorn[standard]" pydantic scikit-learn joblib pandas pytest
```

Install any additional dependencies required by the modules in your
local project.

## Run the Application

Use two separate terminals.

### Terminal 1: Start the FastAPI backend

From the project root, with the virtual environment activated:

``` powershell
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Useful backend URLs:

-   Health check: http://127.0.0.1:8000/health
-   API documentation: http://127.0.0.1:8000/docs
-   API root: http://127.0.0.1:8000/

The health endpoint should return a JSON response indicating that the
application is healthy.

### Terminal 2: Start the HTML frontend

``` powershell
cd frontend
python -m http.server 5500
```

Open the dashboard:

http://127.0.0.1:5500

The frontend calls the local API at `http://127.0.0.1:8000`. The FastAPI
application must include CORS middleware permitting the frontend
origins:

-   `http://127.0.0.1:5500`
-   `http://localhost:5500`

If the browser reports `Failed to fetch`, check that both servers are
running, confirm the API URL in `frontend/index.html`, inspect the
browser Console, and check the backend terminal for exceptions.

## API Endpoints

  Method   Endpoint                           Purpose
  -------- ---------------------------------- --------------------------------------
  GET      `/`                                Application information
  GET      `/health`                          Health check
  POST     `/detect`                          Analyze prompt or document text
  POST     `/feedback`                        Submit a prediction for human review
  POST     `/feedback/review/{feedback_id}`   Record a reviewed label
  GET      `/feedback/summary`                Retrieve feedback statistics
  POST     `/adaptive/retrain`                Run candidate retraining workflow

### Example: Prompt detection

Request:

``` http
POST /detect
Content-Type: application/json
```

``` json
{
  "text": "Explain the basic concepts of cloud computing."
}
```

The response contains a decision and nested analysis objects. The
principal fields include:

-   `decision`
-   `reason`
-   `rule_analysis.rule_score`
-   `rule_analysis.detected_rules`
-   `rule_analysis.rule_flag`
-   `ml_analysis.ml_prediction`
-   `ml_analysis.ml_probability`
-   `explainability.summary`
-   `explainability.rule_summary`
-   `explainability.rule_evidence`
-   `explainability.ml_evidence.malicious_supporting_features`
-   `explainability.ml_evidence.benign_supporting_features`
-   `explainability.method`
-   `explainability.limitations`

Use `/docs` to inspect the exact request and response schemas exposed by
the running version.

### Feedback request

The current API request model accepts:

``` json
{
  "text": "Text that was analyzed",
  "predicted_label": 0
}
```

`predicted_label` must be `0` or `1`. Feedback remains pending until
reviewed.

### Review request

The review endpoint accepts:

``` json
{
  "reviewed_label": 1
}
```

Use the actual `feedback_id` returned by the feedback submission
endpoint.

## Testing

Run the automated test suite from the project root with the virtual
environment activated:

``` powershell
python -m pytest -v
```

The previously recorded run completed with **16 passed tests and 3
warnings**. Re-run tests after making code changes; the result from an
earlier run does not guarantee the current code still passes.

For a manual API test, open `/docs`, select `POST /detect`, choose **Try
it out**, submit a benign test prompt, and inspect the JSON response.

## Model and Decision Configuration

The reported application configuration uses:

  Setting                                   Value
  ------------------------------------ ----------
  Rule risk threshold                           6
  ML probability threshold                   0.60
  TF-IDF n-gram range                      (1, 2)
  Logistic Regression max iterations         1000
  Class weighting                        balanced
  Random state                                 42

The hybrid decision marks an input suspicious when the rule score
reaches the rule threshold, or when the ML classifier predicts the
malicious class and its probability meets the configured ML threshold.
Confirm the exact implementation in `app/detector.py` before changing or
documenting decision behavior.

## Adaptive Learning Workflow

1.  A prompt is analyzed by the active detector.
2.  Feedback can be submitted with the text and predicted label.
3.  Submitted feedback is stored as pending.
4.  An authorized reviewer records the reviewed label.
5.  Approved feedback can be used by the retraining workflow.
6.  A candidate model is trained and evaluated.
7.  Model promotion should occur only when the configured validation
    checks pass.
8.  The versioned registry retains model history and a baseline for
    comparison or rollback.

Do not treat unreviewed feedback as trusted ground truth. Keep access to
feedback review and retraining restricted to authorized operators.

## Limitations

-   The reported dataset is synthetic and relatively small.
-   The independent test partition contains only 65 examples.
-   Some categories have very few independent-test samples.
-   Template separation reduces repeated-template leakage but does not
    prove semantic independence.
-   TF-IDF and Logistic Regression may miss semantic, obfuscated,
    multilingual, or novel attacks.
-   Feature contributions explain the linear classifier's score, not the
    causal intent of text or every component of the hybrid decision.
-   The thresholds are prototype configuration values and require
    further validation for other deployments.
-   The current results do not establish resistance to adaptive
    attackers or production-level security.

## Responsible Use

Use this project for defensive research, controlled testing, and
educational demonstrations. Test with synthetic or otherwise authorized
prompts and documents. Do not use the framework to process confidential
information unless the deployment has been reviewed for privacy, access
control, logging, and data-retention requirements.

## Research Paper

The accompanying research paper draft is titled:

**"Explainable and Adaptive Prompt Injection Detection Framework for LLM
Applications."**

Before academic submission:

-   Add the institution, department, supervisor, and author details.
-   Verify bibliographic metadata and citation style.
-   Include genuine screenshots and the exact experiment configuration.
-   Re-run the experiments and update reported metrics if the
    implementation or data changes.
-   Follow institutional rules for originality, authorship, and
    AI-assisted writing.

------------------------------------------------------------------------

## Author

**Bhuvan R**\
M.Tech Programme\
Institution: `[Add institution name]`

## Acknowledgement

This repository documents an academic prototype. Dataset construction,
implementation details, evaluation results, and limitations should be
reviewed and validated before external publication or deployment.
