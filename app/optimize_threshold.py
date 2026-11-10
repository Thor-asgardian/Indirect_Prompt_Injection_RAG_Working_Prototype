
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)

# Load the original training dataset.
# The independent test dataset is NOT used here.
df = pd.read_csv("data/prompt_injection_dataset.csv")

X = df["text"].astype(str)
y = df["label"].astype(int)

# Split into training and validation sets.
X_train, X_val, y_train, y_val = train_test_split(
    X,
    y,
    test_size=0.25,
    random_state=42,
    stratify=y
)

print("Training samples:", len(X_train))
print("Validation samples:", len(X_val))

# Train the model only on the training portion.
vectorizer = TfidfVectorizer(
    ngram_range=(1, 2),
    max_features=5000,
    sublinear_tf=True
)

X_train_vec = vectorizer.fit_transform(X_train)
X_val_vec = vectorizer.transform(X_val)

model = LogisticRegression(
    max_iter=1000,
    class_weight="balanced",
    random_state=42
)

model.fit(X_train_vec, y_train)

# Get malicious-class scores for validation samples.
probabilities = model.predict_proba(X_val_vec)[:, 1]

# Compare different decision thresholds.
thresholds = [0.40, 0.45, 0.50, 0.55, 0.60, 0.65]

results = []

for threshold in thresholds:
    predictions = (probabilities >= threshold).astype(int)

    results.append({
        "threshold": threshold,
        "accuracy": accuracy_score(y_val, predictions),
        "precision": precision_score(
            y_val, predictions, zero_division=0
        ),
        "recall": recall_score(
            y_val, predictions, zero_division=0
        ),
        "f1_score": f1_score(
            y_val, predictions, zero_division=0
        )
    })

results_df = pd.DataFrame(results)

print("\nVALIDATION THRESHOLD COMPARISON")
print(results_df.round(3).to_string(index=False))

# Save the validation comparison.
results_df.to_csv(
    "validation_threshold_results.csv",
    index=False
)

print("\nSaved: validation_threshold_results.csv")
print("\nConfusion matrix at the default threshold (0.50):")

default_predictions = (probabilities >= 0.50).astype(int)

print(confusion_matrix(y_val, default_predictions))
