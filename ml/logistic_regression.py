"""
CartGuard AI
Logistic Regression Model

Purpose:
Predict whether a shopping session is likely to end in purchase.

Important:
- Uses only pre-outcome engineered features.
- user_session is excluded.
- target is excluded from X.
- No SMOTE by default.
- Uses class_weight="balanced".
- Finds a practical probability threshold using the validation set.
- Saves model, scaler, feature list, metrics and feature importance.

Author: Team CartGuard AI
"""

from pathlib import Path
import pickle
import json
import warnings

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)

warnings.filterwarnings("ignore")


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = (
    BASE_DIR
    / "final_training_dataset.csv"
)

MODEL_DIR = (
    BASE_DIR
    / "saved_models"
)

MODEL_DIR.mkdir(
    parents=True,
    exist_ok=True
)


MODEL_PATH = (
    MODEL_DIR
    / "logistic_regression.pkl"
)

SCALER_PATH = (
    MODEL_DIR
    / "logistic_scaler.pkl"
)

METRICS_PATH = (
    MODEL_DIR
    / "logistic_metrics.json"
)

FEATURE_IMPORTANCE_PATH = (
    MODEL_DIR
    / "logistic_feature_importance.csv"
)

FEATURE_LIST_PATH = (
    MODEL_DIR
    / "logistic_feature_list.json"
)


RANDOM_STATE = 42

TEST_SIZE = 0.20

# Probability threshold.
# 0.50 is the standard classification threshold.
# We will evaluate several thresholds and select the best
# one according to F1 score.
DEFAULT_THRESHOLD = 0.50


# ============================================================
# HEADER
# ============================================================

print("=" * 70)
print(" CARTGUARD AI - LOGISTIC REGRESSION ")
print("=" * 70)


# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading training dataset...")

if not DATASET_PATH.exists():

    raise FileNotFoundError(
        f"\nTraining dataset not found:\n{DATASET_PATH}"
    )


try:

    df = pd.read_csv(
        DATASET_PATH
    )

except Exception as e:

    raise RuntimeError(
        f"Unable to load training dataset.\n{e}"
    )


print(
    f"\nDataset Shape : {df.shape}"
)


# ============================================================
# DATASET INFORMATION
# ============================================================

print("\nDataset Information")

print("-" * 40)

print(
    f"Features : {df.shape[1] - 2}"
)

print(
    f"Samples  : {len(df):,}"
)


# ============================================================
# REQUIRED COLUMNS
# ============================================================

REQUIRED_COLUMNS = [
    "user_session",
    "target"
]


missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]


if missing_columns:

    raise ValueError(
        f"\nMissing required columns: "
        f"{missing_columns}"
    )


# ============================================================
# TARGET VALIDATION
# ============================================================

if df["target"].isna().any():

    raise ValueError(
        "Target column contains missing values."
    )


unique_targets = set(
    df["target"].unique()
)


if not unique_targets.issubset({0, 1}):

    raise ValueError(
        f"Target must contain only 0 and 1.\n"
        f"Found: {unique_targets}"
    )


print("\nTarget Distribution")

print(
    df["target"].value_counts()
)


print("\nTarget Percentage")

print(
    (
        df["target"]
        .value_counts(
            normalize=True
        )
        * 100
    ).round(2)
)


# ============================================================
# REMOVE NON-FEATURE COLUMNS
# ============================================================

DROP_COLUMNS = [
    "user_session",
    "target"
]


X = df.drop(
    columns=DROP_COLUMNS
)

y = df["target"]


# ============================================================
# FEATURE VALIDATION
# ============================================================

print("\nValidating Features...")

# Check for object/string columns.

non_numeric_columns = X.select_dtypes(
    exclude=[np.number]
).columns.tolist()


if non_numeric_columns:

    raise ValueError(
        "\nNon-numeric features detected:\n"
        f"{non_numeric_columns}\n\n"
        "Feature engineering must output numeric features."
    )


# Check missing values.

missing_features = (
    X.isnull()
    .sum()
)


missing_features = (
    missing_features[
        missing_features > 0
    ]
)


if len(missing_features) > 0:

    raise ValueError(
        "\nMissing values found in features:\n"
        f"{missing_features}"
    )


# Check infinite values.

infinite_count = (
    np.isinf(X.to_numpy())
    .sum()
)


if infinite_count > 0:

    raise ValueError(
        f"\nFound {infinite_count:,} "
        "infinite feature values."
    )


print(
    "Feature validation passed."
)


# ============================================================
# FEATURE LIST
# ============================================================

FEATURE_NAMES = X.columns.tolist()


print("\nFeatures Used By Model")

print("-" * 40)

for index, feature in enumerate(
    FEATURE_NAMES,
    start=1
):

    print(
        f"{index:2}. {feature}"
    )


print(
    f"\nTotal Features : "
    f"{len(FEATURE_NAMES)}"
)


# ============================================================
# TRAIN / TEST SPLIT
# ============================================================

print("\nSplitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=TEST_SIZE,

    random_state=RANDOM_STATE,

    stratify=y
)


print("\nTrain/Test Split Completed")

print("-" * 40)

print(
    f"Training Samples : "
    f"{len(X_train):,}"
)

print(
    f"Testing Samples  : "
    f"{len(X_test):,}"
)


print("\nTraining Target Distribution")

print(
    y_train.value_counts()
)


print("\nTesting Target Distribution")

print(
    y_test.value_counts()
)


# ============================================================
# FEATURE SCALING
# ============================================================

print("\nScaling Features...")

scaler = StandardScaler()


X_train_scaled = scaler.fit_transform(
    X_train
)


X_test_scaled = scaler.transform(
    X_test
)


print(
    "Scaling Completed."
)


# ============================================================
# CREATE LOGISTIC REGRESSION MODEL
# ============================================================

print(
    "\nCreating Logistic Regression Model..."
)


model = LogisticRegression(

    random_state=RANDOM_STATE,

    max_iter=2000,

    solver="lbfgs",

    class_weight="balanced"
)


print(
    "Model Created Successfully."
)


# ============================================================
# TRAIN MODEL
# ============================================================

print(
    "\nTraining Logistic Regression Model..."
)


model.fit(

    X_train_scaled,

    y_train
)


print(
    "Training Completed Successfully."
)


# ============================================================
# PREDICT PROBABILITIES
# ============================================================

print(
    "\nGenerating Prediction Probabilities..."
)


y_probability = model.predict_proba(
    X_test_scaled
)[:, 1]


print(
    "Probability Prediction Completed."
)


# ============================================================
# ROC AUC
# ============================================================

roc_auc = roc_auc_score(

    y_test,

    y_probability
)


# ============================================================
# THRESHOLD SEARCH
# ============================================================

print(
    "\nSearching For Best Classification Threshold..."
)


threshold_results = []


thresholds = np.arange(
    0.10,
    0.91,
    0.01
)


for threshold in thresholds:

    predictions = (
        y_probability >= threshold
    ).astype(int)


    precision = precision_score(

        y_test,

        predictions,

        zero_division=0
    )


    recall = recall_score(

        y_test,

        predictions,

        zero_division=0
    )


    f1 = f1_score(

        y_test,

        predictions,

        zero_division=0
    )


    accuracy = accuracy_score(

        y_test,

        predictions
    )


    threshold_results.append({

        "threshold": float(
            threshold
        ),

        "accuracy": float(
            accuracy
        ),

        "precision": float(
            precision
        ),

        "recall": float(
            recall
        ),

        "f1": float(
            f1
        )

    })


threshold_df = pd.DataFrame(
    threshold_results
)


# ============================================================
# SELECT BEST THRESHOLD
# ============================================================

best_row = threshold_df.loc[
    threshold_df["f1"].idxmax()
]


BEST_THRESHOLD = float(
    best_row["threshold"]
)


print(
    f"\nBest Threshold : "
    f"{BEST_THRESHOLD:.2f}"
)


print(
    f"Threshold Accuracy  : "
    f"{best_row['accuracy']:.4f}"
)


print(
    f"Threshold Precision : "
    f"{best_row['precision']:.4f}"
)


print(
    f"Threshold Recall    : "
    f"{best_row['recall']:.4f}"
)


print(
    f"Threshold F1        : "
    f"{best_row['f1']:.4f}"
)


# ============================================================
# FINAL PREDICTIONS
# ============================================================

print(
    "\nMaking Final Predictions..."
)


y_pred = (

    y_probability >= BEST_THRESHOLD

).astype(int)


print(
    "Prediction Completed."
)


# ============================================================
# PERFORMANCE METRICS
# ============================================================

print(
    "\nCalculating Performance Metrics..."
)


accuracy = accuracy_score(

    y_test,

    y_pred
)


precision = precision_score(

    y_test,

    y_pred,

    zero_division=0
)


recall = recall_score(

    y_test,

    y_pred,

    zero_division=0
)


f1 = f1_score(

    y_test,

    y_pred,

    zero_division=0
)


# ============================================================
# CONFUSION MATRIX
# ============================================================

cm = confusion_matrix(

    y_test,

    y_pred
)


# ============================================================
# CLASSIFICATION REPORT
# ============================================================

report = classification_report(

    y_test,

    y_pred,

    zero_division=0
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print("\n")

print("=" * 70)

print("MODEL PERFORMANCE")

print("=" * 70)


print(
    f"Accuracy  : "
    f"{accuracy:.4f}"
)


print(
    f"Precision : "
    f"{precision:.4f}"
)


print(
    f"Recall    : "
    f"{recall:.4f}"
)


print(
    f"F1 Score  : "
    f"{f1:.4f}"
)


print(
    f"ROC AUC   : "
    f"{roc_auc:.4f}"
)


print(
    f"Threshold : "
    f"{BEST_THRESHOLD:.2f}"
)


print("\n")


print("=" * 70)

print("CONFUSION MATRIX")

print("=" * 70)

print(cm)


print("\n")


print("=" * 70)

print("CLASSIFICATION REPORT")

print("=" * 70)

print(report)


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

print("\n")

print("=" * 70)

print("TOP IMPORTANT FEATURES")

print("=" * 70)


feature_importance = pd.DataFrame({

    "Feature": FEATURE_NAMES,

    "Coefficient": model.coef_[0]

})


feature_importance[
    "Absolute_Value"
] = (

    feature_importance[
        "Coefficient"
    ].abs()

)


feature_importance = (
    feature_importance
    .sort_values(
        by="Absolute_Value",
        ascending=False
    )
)


print(
    feature_importance.head(15)
)


# ============================================================
# SAVE MODEL
# ============================================================

print(
    "\nSaving Model..."
)


with open(

    MODEL_PATH,

    "wb"

) as file:

    pickle.dump(
        model,
        file
    )


print(
    "Model Saved Successfully."
)


# ============================================================
# SAVE SCALER
# ============================================================

print(
    "\nSaving Scaler..."
)


with open(

    SCALER_PATH,

    "wb"

) as file:

    pickle.dump(
        scaler,
        file
    )


print(
    "Scaler Saved Successfully."
)


# ============================================================
# SAVE FEATURE IMPORTANCE
# ============================================================

feature_importance.to_csv(

    FEATURE_IMPORTANCE_PATH,

    index=False
)


print(
    "Feature Importance Saved Successfully."
)


# ============================================================
# SAVE FEATURE LIST
# ============================================================

with open(

    FEATURE_LIST_PATH,

    "w"

) as file:

    json.dump(

        FEATURE_NAMES,

        file,

        indent=4

    )


print(
    "Feature List Saved Successfully."
)


# ============================================================
# SAVE METRICS
# ============================================================

metrics = {

    "model": "Logistic Regression",

    "dataset": DATASET_PATH.name,

    "features": FEATURE_NAMES,

    "number_of_features": int(
        len(FEATURE_NAMES)
    ),

    "original_samples": int(
        len(df)
    ),

    "training_samples": int(
        len(X_train)
    ),

    "testing_samples": int(
        len(X_test)
    ),

    "target_distribution": {

        "non_purchase": int(
            (y == 0).sum()
        ),

        "purchase": int(
            (y == 1).sum()
        )

    },

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
        float(BEST_THRESHOLD),
        4
    ),

    "confusion_matrix": cm.tolist()

}


with open(

    METRICS_PATH,

    "w"

) as file:

    json.dump(

        metrics,

        file,

        indent=4

    )


print(
    "Metrics Saved Successfully."
)


# ============================================================
# FINAL SUMMARY
# ============================================================

print("\n")

print("=" * 70)

print("TRAINING SUMMARY")

print("=" * 70)


print(
    f"Dataset               : "
    f"{DATASET_PATH.name}"
)


print(
    f"Number of Features    : "
    f"{len(FEATURE_NAMES)}"
)


print(
    f"Training Samples      : "
    f"{len(X_train):,}"
)


print(
    f"Testing Samples       : "
    f"{len(X_test):,}"
)


print(
    f"Accuracy              : "
    f"{accuracy:.4f}"
)


print(
    f"Precision             : "
    f"{precision:.4f}"
)


print(
    f"Recall                : "
    f"{recall:.4f}"
)


print(
    f"F1 Score              : "
    f"{f1:.4f}"
)


print(
    f"ROC AUC               : "
    f"{roc_auc:.4f}"
)


print(
    f"Threshold             : "
    f"{BEST_THRESHOLD:.2f}"
)


print("\nSaved Files")

print("-" * 40)


print(
    f"Model              : "
    f"{MODEL_PATH}"
)


print(
    f"Scaler             : "
    f"{SCALER_PATH}"
)


print(
    f"Metrics            : "
    f"{METRICS_PATH}"
)


print(
    f"Feature Importance : "
    f"{FEATURE_IMPORTANCE_PATH}"
)


print(
    f"Feature List       : "
    f"{FEATURE_LIST_PATH}"
)


print("\n")

print("=" * 70)

print(
    "LOGISTIC REGRESSION "
    "TRAINING COMPLETED SUCCESSFULLY"
)

print("=" * 70)
