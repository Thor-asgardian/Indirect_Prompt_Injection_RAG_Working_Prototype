
from pathlib import Path

import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from app.detector import detect
from app.ml_detector import detect_ml


# ---------------------------------------------
# CONFIGURATION
# ---------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "evaluation_dataset.csv"

OUTPUT_PATH = BASE_DIR / "evaluation_results.csv"

RULE_THRESHOLD = 6


# ---------------------------------------------
# LOAD EVALUATION DATASET
# ---------------------------------------------

def load_evaluation_data():

    if not DATASET_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATASET_PATH}"
        )

    df = pd.read_csv(DATASET_PATH)

    if not {"text", "label"}.issubset(df.columns):
        raise ValueError(
            "Dataset must contain text and label columns."
        )

    df = df.dropna(subset=["text", "label"]).copy()

    df["text"] = df["text"].astype(str)
    df["label"] = df["label"].astype(int)

    if not set(df["label"].unique()).issubset({0, 1}):
        raise ValueError("Labels must be 0 or 1.")

    if df["label"].nunique() != 2:
        raise ValueError(
            "Evaluation dataset must contain both classes."
        )

    print("\nEvaluation dataset loaded.")
    print("Total samples:", len(df))
    print("Benign samples:", (df["label"] == 0).sum())
    print("Malicious samples:", (df["label"] == 1).sum())

    return df


# ---------------------------------------------
# RUN ALL THREE DETECTORS
# ---------------------------------------------

def evaluate_all_detectors(df):

    results = []

    for index, row in df.iterrows():

        text = row["text"]
        actual = int(row["label"])

        # Rule-based detection
        rule_result = detect(text)

        rule_prediction = int(
            rule_result.risk_score >= RULE_THRESHOLD
        )

        # ML-based detection
        ml_result = detect_ml(text)

        ml_prediction = int(
            ml_result["prediction"]
        )

        ml_probability = ml_result[
            "malicious_probability"
        ]

        # Hybrid detection:
        # Flag if either detector predicts malicious
        hybrid_prediction = int(
            rule_prediction == 1 or ml_prediction == 1
        )

        results.append({
            "text": text,
            "actual": actual,
            "rule_prediction": rule_prediction,
            "rule_score": rule_result.risk_score,
            "ml_prediction": ml_prediction,
            "ml_probability": ml_probability,
            "hybrid_prediction": hybrid_prediction
        })

    return pd.DataFrame(results)


# ---------------------------------------------
# CALCULATE PERFORMANCE METRICS
# ---------------------------------------------

def calculate_metrics(y_true, y_pred):

    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1]
    ).ravel()

    fpr = fp / (fp + tn) if (fp + tn) else 0
    fnr = fn / (fn + tp) if (fn + tp) else 0

    return {
        "Accuracy": accuracy_score(y_true, y_pred),
        "Precision": precision_score(
            y_true, y_pred, zero_division=0
        ),
        "Recall": recall_score(
            y_true, y_pred, zero_division=0
        ),
        "F1 Score": f1_score(
            y_true, y_pred, zero_division=0
        ),
        "False Positive Rate": fpr,
        "False Negative Rate": fnr,
        "TN": tn,
        "FP": fp,
        "FN": fn,
        "TP": tp
    }


# ---------------------------------------------
# COMPARATIVE EVALUATION
# ---------------------------------------------

def main():

    df = load_evaluation_data()

    results = evaluate_all_detectors(df)

    y_true = results["actual"]

    detector_columns = {
        "Rule-Based": "rule_prediction",
        "ML-Based": "ml_prediction",
        "Hybrid": "hybrid_prediction"
    }

    summary = {}

    print("\n========================================")
    print("COMPARATIVE DETECTOR EVALUATION")
    print("========================================")

    for detector_name, column in detector_columns.items():

        y_pred = results[column]

        metrics = calculate_metrics(y_true, y_pred)

        summary[detector_name] = metrics

        print(f"\n========== {detector_name} ==========")

        print(
            classification_report(
                y_true,
                y_pred,
                labels=[0, 1],
                target_names=["Benign", "Malicious"],
                zero_division=0
            )
        )

        print("Confusion Matrix:")

        print(
            confusion_matrix(
                y_true,
                y_pred,
                labels=[0, 1]
            )
        )

        print("\nPerformance Metrics:")

        for metric, value in metrics.items():

            if isinstance(value, float):
                print(f"{metric}: {value:.4f}")
            else:
                print(f"{metric}: {value}")

    # Save detailed predictions
    results.to_csv(OUTPUT_PATH, index=False)

    # Display comparison table
    comparison = pd.DataFrame(summary).T

    print("\n========================================")
    print("FINAL COMPARISON TABLE")
    print("========================================")

    print(comparison.round(4).to_string())

    print("\nDetailed results saved to:")
    print(OUTPUT_PATH)


if __name__ == "__main__":
    main()
