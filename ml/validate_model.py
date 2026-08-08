from pathlib import Path
import json
import warnings

import pandas as pd
import numpy as np

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

from xgboost import XGBClassifier

warnings.filterwarnings("ignore")


# ============================================================
# CARTGUARD AI
# XGBOOST MODEL VALIDATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "final_training_dataset.csv"

MODEL_DIR = BASE_DIR / "saved_models"

MODEL_PATH = MODEL_DIR / "xgboost.pkl"
FEATURE_LIST_PATH = MODEL_DIR / "xgboost_feature_list.json"
THRESHOLD_PATH = MODEL_DIR / "xgboost_threshold.json"

VALIDATION_METRICS_PATH = (
    MODEL_DIR / "xgboost_validation_metrics.json"
)


# ============================================================
# Header
# ============================================================

print("=" * 70)
print(" CARTGUARD AI - XGBOOST MODEL VALIDATION ")
print("=" * 70)


# ============================================================
# Check Files
# ============================================================

print("\nChecking Required Files...")

required_files = [

    DATASET_PATH,
    MODEL_PATH,
    FEATURE_LIST_PATH,
    THRESHOLD_PATH

]

for file_path in required_files:

    if not file_path.exists():

        raise FileNotFoundError(
            f"Required file not found:\n{file_path}"
        )

    print(f"Found : {file_path.name}")


# ============================================================
# Load Dataset
# ============================================================

print("\nLoading validation dataset...")

df = pd.read_csv(DATASET_PATH)

print(f"Dataset Shape : {df.shape}")


# ============================================================
# Load Feature List
# ============================================================

print("\nLoading feature list...")

with open(FEATURE_LIST_PATH, "r") as file:

    feature_data = json.load(file)


# Support both possible formats:
#
# 1. ["feature1", "feature2", ...]
#
# 2. {"features": ["feature1", "feature2", ...]}

if isinstance(feature_data, list):

    FEATURES = feature_data

elif isinstance(feature_data, dict):

    FEATURES = feature_data.get(
        "features",
        feature_data.get(
            "feature_list",
            []
        )
    )

else:

    FEATURES = []


if not FEATURES:

    raise ValueError(
        "Feature list is empty or invalid."
    )


print(f"Features Loaded : {len(FEATURES)}")


# ============================================================
# Validate Dataset Columns
# ============================================================

print("\nValidating Dataset Columns...")

missing_features = [

    feature
    for feature in FEATURES
    if feature not in df.columns

]

if missing_features:

    raise ValueError(
        f"Missing Features : {missing_features}"
    )


if "target" not in df.columns:

    raise ValueError(
        "Target column not found."
    )


print("All required features found.")


# ============================================================
# Prepare Validation Data
# ============================================================

print("\nPreparing Validation Data...")

X = df[FEATURES].copy()

y = df["target"].copy()


# ============================================================
# Numeric Validation
# ============================================================

print("\nValidating Feature Data Types...")

non_numeric = X.select_dtypes(
    exclude=[np.number]
).columns.tolist()


if non_numeric:

    raise ValueError(
        f"Non-numeric features found: {non_numeric}"
    )


print("All features are numeric.")


# ============================================================
# Missing Value Validation
# ============================================================

print("\nChecking Missing Values...")

missing_values = X.isnull().sum().sum()

print(
    f"Missing Feature Values : {missing_values:,}"
)


if missing_values > 0:

    raise ValueError(
        "Validation dataset contains missing values."
    )


# ============================================================
# Dataset Information
# ============================================================

print("\n")

print("=" * 70)
print("VALIDATION DATASET INFORMATION")
print("=" * 70)

print(
    f"\nSamples  : {len(X):,}"
)

print(
    f"Features : {X.shape[1]}"
)

print("\nTarget Distribution")

print(y.value_counts())

print("\nTarget Percentage")

print(
    (y.value_counts(normalize=True) * 100)
    .round(2)
)


# ============================================================
# Load XGBoost Model
# ============================================================

print("\nLoading XGBoost Model...")

model = XGBClassifier()

model.load_model(MODEL_PATH)

print("XGBoost Model Loaded Successfully.")


# ============================================================
# Model Feature Validation
# ============================================================

print("\nValidating Model Features...")

model_feature_count = model.get_booster().num_features()

dataset_feature_count = X.shape[1]


print(
    f"Model Features   : {model_feature_count}"
)

print(
    f"Dataset Features : {dataset_feature_count}"
)


if model_feature_count != dataset_feature_count:

    raise ValueError(
        "Model and dataset feature counts do not match."
    )


print("Feature Count Validation Passed.")


# ============================================================
# Load Classification Threshold
# ============================================================

print("\nLoading Classification Threshold...")

with open(THRESHOLD_PATH, "r") as file:

    threshold_data = json.load(file)


if isinstance(threshold_data, dict):

    THRESHOLD = threshold_data.get(
        "threshold",
        threshold_data.get(
            "classification_threshold",
            threshold_data.get(
                "best_threshold",
                0.50
            )
        )
    )

else:

    THRESHOLD = float(threshold_data)


THRESHOLD = float(THRESHOLD)


print(
    f"Classification Threshold : {THRESHOLD:.2f}"
)


# ============================================================
# Generate Probabilities
# ============================================================

print("\nGenerating Prediction Probabilities...")

y_probability = model.predict_proba(X)[:, 1]

print("Probability Prediction Completed.")


# ============================================================
# Apply Threshold
# ============================================================

print("\nApplying Classification Threshold...")

y_prediction = (
    y_probability >= THRESHOLD
).astype(int)

print("Final Predictions Generated.")


# ============================================================
# Calculate Metrics
# ============================================================

print("\nCalculating Validation Metrics...")


accuracy = accuracy_score(
    y,
    y_prediction
)

precision = precision_score(
    y,
    y_prediction,
    zero_division=0
)

recall = recall_score(
    y,
    y_prediction,
    zero_division=0
)

f1 = f1_score(
    y,
    y_prediction,
    zero_division=0
)

roc_auc = roc_auc_score(
    y,
    y_probability
)


# ============================================================
# Confusion Matrix
# ============================================================

cm = confusion_matrix(
    y,
    y_prediction
)


# ============================================================
# Classification Report
# ============================================================

report = classification_report(
    y,
    y_prediction,
    zero_division=0
)


# ============================================================
# Display Results
# ============================================================

print("\n")

print("=" * 70)
print("XGBOOST VALIDATION PERFORMANCE")
print("=" * 70)

print(
    f"\nAccuracy  : {accuracy:.4f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print(
    f"ROC AUC   : {roc_auc:.4f}"
)

print(
    f"Threshold : {THRESHOLD:.2f}"
)


# ============================================================
# Confusion Matrix
# ============================================================

print("\n")

print("=" * 70)
print("CONFUSION MATRIX")
print("=" * 70)

print(cm)


# ============================================================
# Classification Report
# ============================================================

print("\n")

print("=" * 70)
print("CLASSIFICATION REPORT")
print("=" * 70)

print(report)


# ============================================================
# Compare With Training Results
# ============================================================

print("\n")

print("=" * 70)
print("TRAINING VS VALIDATION")
print("=" * 70)


TRAINING_METRICS_PATH = (
    MODEL_DIR / "xgboost_metrics.json"
)


if TRAINING_METRICS_PATH.exists():

    with open(
        TRAINING_METRICS_PATH,
        "r"
    ) as file:

        training_metrics = json.load(file)

    def get_metric(data, *keys):

        for key in keys:

            if key in data:

                return float(data[key])

        return None


    training_accuracy = get_metric(
        training_metrics,
        "accuracy",
        "Accuracy"
    )

    training_precision = get_metric(
        training_metrics,
        "precision",
        "Precision"
    )

    training_recall = get_metric(
        training_metrics,
        "recall",
        "Recall"
    )

    training_f1 = get_metric(
        training_metrics,
        "f1_score",
        "F1 Score"
    )

    training_auc = get_metric(
        training_metrics,
        "roc_auc",
        "ROC AUC"
    )


    print()

    print(
        f"{'Metric':<15}"
        f"{'Training':<15}"
        f"{'Validation':<15}"
        f"{'Difference':<15}"
    )

    print("-" * 60)


    comparisons = [

        (
            "Accuracy",
            training_accuracy,
            accuracy
        ),

        (
            "Precision",
            training_precision,
            precision
        ),

        (
            "Recall",
            training_recall,
            recall
        ),

        (
            "F1 Score",
            training_f1,
            f1
        ),

        (
            "ROC AUC",
            training_auc,
            roc_auc
        )

    ]


    for name, train_value, validation_value in comparisons:

        if train_value is not None:

            difference = (
                validation_value - train_value
            )

            print(
                f"{name:<15}"
                f"{train_value:<15.4f}"
                f"{validation_value:<15.4f}"
                f"{difference:+.4f}"
            )


# ============================================================
# Validation Status
# ============================================================

print("\n")

print("=" * 70)
print("VALIDATION STATUS")
print("=" * 70)


validation_passed = True


# Basic sanity checks

if len(X) == 0:

    validation_passed = False


if X.shape[1] != len(FEATURES):

    validation_passed = False


if missing_values > 0:

    validation_passed = False


if not (0 <= accuracy <= 1):

    validation_passed = False


if not (0 <= precision <= 1):

    validation_passed = False


if not (0 <= recall <= 1):

    validation_passed = False


if not (0 <= f1 <= 1):

    validation_passed = False


if not (0 <= roc_auc <= 1):

    validation_passed = False


if validation_passed:

    print("\nMODEL VALIDATION : PASSED")

else:

    print("\nMODEL VALIDATION : FAILED")


# ============================================================
# Save Validation Metrics
# ============================================================

validation_metrics = {

    "model": "XGBoost",

    "validation_status": (
        "PASSED"
        if validation_passed
        else "FAILED"
    ),

    "dataset": DATASET_PATH.name,

    "samples": int(len(X)),

    "features": int(X.shape[1]),

    "accuracy": round(
        float(accuracy),
        4
    ),

    "precision": round(
        float(precision),
        4
    ),

    "recall": round(
        float(recall),
        4
    ),

    "f1_score": round(
        float(f1),
        4
    ),

    "roc_auc": round(
        float(roc_auc),
        4
    ),

    "classification_threshold": round(
        float(THRESHOLD),
        4
    ),

    "confusion_matrix": cm.tolist()

}


with open(
    VALIDATION_METRICS_PATH,
    "w"
) as file:

    json.dump(
        validation_metrics,
        file,
        indent=4
    )


print("\nValidation Metrics Saved.")

print(
    f"Saved To : {VALIDATION_METRICS_PATH}"
)


# ============================================================
# Final Summary
# ============================================================

print("\n")

print("=" * 70)
print("MODEL VALIDATION SUMMARY")
print("=" * 70)

print(
    f"\nModel              : XGBoost"
)

print(
    f"Validation Samples : {len(X):,}"
)

print(
    f"Features            : {X.shape[1]}"
)

print(
    f"Accuracy            : {accuracy:.4f}"
)

print(
    f"Precision           : {precision:.4f}"
)

print(
    f"Recall              : {recall:.4f}"
)

print(
    f"F1 Score            : {f1:.4f}"
)

print(
    f"ROC AUC             : {roc_auc:.4f}"
)

print(
    f"Threshold           : {THRESHOLD:.2f}"
)

print(
    f"Status              : "
    f"{'PASSED' if validation_passed else 'FAILED'}"
)


print("\n")

print("=" * 70)
print("XGBOOST MODEL VALIDATION COMPLETED")
print("=" * 70)