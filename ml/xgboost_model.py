"""
CartGuard AI
XGBoost Classifier

Purpose:
Predict whether a customer session
will end in a purchase.
"""

from pathlib import Path
import json
import warnings

import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
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
# Project Configuration
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATASET_PATH = BASE_DIR / "final_training_dataset.csv"

MODEL_DIR = BASE_DIR / "saved_models"
MODEL_DIR.mkdir(exist_ok=True)

MODEL_PATH = MODEL_DIR / "xgboost.pkl"

METRICS_PATH = MODEL_DIR / "xgboost_metrics.json"

FEATURE_IMPORTANCE_PATH = (
    MODEL_DIR /
    "xgboost_feature_importance.csv"
)

FEATURE_LIST_PATH = (
    MODEL_DIR /
    "xgboost_feature_list.json"
)

THRESHOLD_PATH = (
    MODEL_DIR /
    "xgboost_threshold.json"
)

RANDOM_STATE = 42
TEST_SIZE = 0.20


# ============================================================
# Header
# ============================================================

print("=" * 70)
print(" CARTGUARD AI - XGBOOST ")
print("=" * 70)


# ============================================================
# Load Dataset
# ============================================================

print("\nLoading training dataset...")

try:

    df = pd.read_csv(DATASET_PATH)

except Exception as e:

    print("Unable to load dataset.")
    print(e)
    exit()

print(f"\nDataset Shape : {df.shape}")


# ============================================================
# Validate Dataset
# ============================================================

print("\nValidating Dataset...")

required_columns = [
    "user_session",
    "target"
]

missing = [
    column
    for column in required_columns
    if column not in df.columns
]

if missing:

    raise ValueError(
        f"Missing Required Columns : {missing}"
    )

print("Dataset validation passed.")


# ============================================================
# Prepare Features
# ============================================================

DROP_COLUMNS = [
    "user_session",
    "target"
]

X = df.drop(columns=DROP_COLUMNS)

y = df["target"]


# ============================================================
# Validate Features
# ============================================================

print("\nValidating Features...")

if X.isnull().sum().sum() > 0:

    raise ValueError(
        "Feature dataset contains missing values."
    )

if not all(
    pd.api.types.is_numeric_dtype(dtype)
    for dtype in X.dtypes
):

    raise ValueError(
        "All model features must be numeric."
    )

print("Feature validation passed.")

print("\n## Features Used By Model")

for index, column in enumerate(X.columns, start=1):

    print(f"{index}. {column}")

print(f"\nTotal Features : {X.shape[1]}")


# ============================================================
# Dataset Information
# ============================================================

print("\nDataset Information")
print("-" * 40)

print(f"Features : {X.shape[1]}")
print(f"Samples  : {len(df):,}")

print("\nTarget Distribution")

print(y.value_counts())

print("\nTarget Percentage")

print(
    (y.value_counts(normalize=True) * 100)
    .round(2)
)


# ============================================================
# Train Test Split
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

print(f"Training Samples : {len(X_train):,}")
print(f"Testing Samples  : {len(X_test):,}")


print("\nTraining Target Distribution")

print(y_train.value_counts())


print("\nTesting Target Distribution")

print(y_test.value_counts())


# ============================================================
# No SMOTE
# ============================================================

print("\nSMOTE : DISABLED")

print(
    "Using scale_pos_weight to handle class imbalance."
)


# ============================================================
# Calculate Class Weight
# ============================================================

negative_count = (y_train == 0).sum()
positive_count = (y_train == 1).sum()

scale_pos_weight = (
    negative_count /
    positive_count
)

print(
    f"\nScale Pos Weight : "
    f"{scale_pos_weight:.4f}"
)


# ============================================================
# Create XGBoost Model
# ============================================================

print("\nCreating XGBoost Model...")

model = XGBClassifier(

    objective="binary:logistic",

    eval_metric="auc",

    n_estimators=300,

    learning_rate=0.05,

    max_depth=6,

    min_child_weight=3,

    subsample=0.8,

    colsample_bytree=0.8,

    gamma=0.2,

    reg_alpha=0.1,

    reg_lambda=1.0,

    scale_pos_weight=scale_pos_weight,

    random_state=RANDOM_STATE,

    tree_method="hist",

    n_jobs=-1
)

print("Model Created Successfully.")


# ============================================================
# Train Model
# ============================================================

print("\nTraining XGBoost Model...")

model.fit(

    X_train,

    y_train,

    eval_set=[
        (X_test, y_test)
    ],

    verbose=False
)

print("Training Completed Successfully.")


# ============================================================
# Generate Prediction Probabilities
# ============================================================

print("\nGenerating Prediction Probabilities...")

y_prob = model.predict_proba(

    X_test

)[:, 1]

print("Probability Prediction Completed.")


# ============================================================
# Find Best Threshold
# ============================================================

print("\nSearching For Best Classification Threshold...")

threshold_results = []


for threshold in np.arange(
    0.20,
    0.91,
    0.01
):

    temp_pred = (
        y_prob >= threshold
    ).astype(int)

    temp_precision = precision_score(

        y_test,
        temp_pred,
        zero_division=0
    )

    temp_recall = recall_score(

        y_test,
        temp_pred,
        zero_division=0
    )

    temp_f1 = f1_score(

        y_test,
        temp_pred,
        zero_division=0
    )

    temp_accuracy = accuracy_score(

        y_test,
        temp_pred
    )

    threshold_results.append({

        "threshold": threshold,

        "accuracy": temp_accuracy,

        "precision": temp_precision,

        "recall": temp_recall,

        "f1": temp_f1
    })


threshold_df = pd.DataFrame(
    threshold_results
)


# ============================================================
# Select Best Threshold
# ============================================================

# For CartGuard, F1 is used to balance
# precision and recall for the purchase class.

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
# Final Predictions
# ============================================================

print("\nMaking Final Predictions...")

y_pred = (
    y_prob >= BEST_THRESHOLD
).astype(int)

print("Prediction Completed.")


# ============================================================
# Evaluation Metrics
# ============================================================

print("\nCalculating Performance Metrics...")

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

roc_auc = roc_auc_score(

    y_test,
    y_prob
)


# ============================================================
# Confusion Matrix
# ============================================================

cm = confusion_matrix(

    y_test,
    y_pred
)


# ============================================================
# Classification Report
# ============================================================

report = classification_report(

    y_test,
    y_pred,

    zero_division=0
)


# ============================================================
# Feature Importance
# ============================================================

feature_importance = pd.DataFrame({

    "Feature": X.columns,

    "Importance":
        model.feature_importances_

})


feature_importance = (
    feature_importance
    .sort_values(
        by="Importance",
        ascending=False
    )
    .reset_index(drop=True)
)


# ============================================================
# Display Results
# ============================================================

print("\n")

print("=" * 70)
print("MODEL PERFORMANCE")
print("=" * 70)

print(f"Accuracy  : {accuracy:.4f}")
print(f"Precision : {precision:.4f}")
print(f"Recall    : {recall:.4f}")
print(f"F1 Score  : {f1:.4f}")
print(f"ROC AUC   : {roc_auc:.4f}")
print(f"Threshold : {BEST_THRESHOLD:.2f}")


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


print("\n")

print("=" * 70)
print("TOP 15 IMPORTANT FEATURES")
print("=" * 70)

print(
    feature_importance.head(15)
)


# ============================================================
# Save Model
# ============================================================

print("\nSaving Model...")

model.save_model(

    MODEL_PATH

)

print("Model Saved Successfully.")


# ============================================================
# Save Feature Importance
# ============================================================

print("\nSaving Feature Importance...")

feature_importance.to_csv(

    FEATURE_IMPORTANCE_PATH,

    index=False

)

print("Feature Importance Saved Successfully.")


# ============================================================
# Save Feature List
# ============================================================

print("\nSaving Feature List...")

feature_list = list(X.columns)

with open(

    FEATURE_LIST_PATH,

    "w"

) as file:

    json.dump(

        feature_list,

        file,

        indent=4

    )

print("Feature List Saved Successfully.")


# ============================================================
# Save Classification Threshold
# ============================================================

print("\nSaving Classification Threshold...")

threshold_data = {

    "threshold": round(
        BEST_THRESHOLD,
        4
    )

}

with open(

    THRESHOLD_PATH,

    "w"

) as file:

    json.dump(

        threshold_data,

        file,

        indent=4

    )

print("Classification Threshold Saved Successfully.")


# ============================================================
# Save Metrics
# ============================================================

print("\nSaving Metrics...")

metrics = {

    "Model": "XGBoost",

    "Accuracy": round(
        float(accuracy),
        4
    ),

    "Precision": round(
        float(precision),
        4
    ),

    "Recall": round(
        float(recall),
        4
    ),

    "F1 Score": round(
        float(f1),
        4
    ),

    "ROC AUC": round(
        float(roc_auc),
        4
    ),

    "Threshold": round(
        float(BEST_THRESHOLD),
        4
    ),

    "Training Samples": int(
        len(X_train)
    ),

    "Testing Samples": int(
        len(X_test)
    ),

    "Features": int(
        X.shape[1]
    ),

    "Trees": int(
        model.n_estimators
    ),

    "Learning Rate": float(
        model.learning_rate
    ),

    "Max Depth": int(
        model.max_depth
    ),

    "Scale Pos Weight": round(
        float(scale_pos_weight),
        4
    )
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

print("Metrics Saved Successfully.")


# ============================================================
# Training Summary
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
    f"{X.shape[1]}"
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
    f"Model                : "
    f"{MODEL_PATH}"
)

print(
    f"Metrics              : "
    f"{METRICS_PATH}"
)

print(
    f"Feature Importance   : "
    f"{FEATURE_IMPORTANCE_PATH}"
)

print(
    f"Feature List         : "
    f"{FEATURE_LIST_PATH}"
)

print(
    f"Threshold            : "
    f"{THRESHOLD_PATH}"
)


print("\n")

print("=" * 70)
print("XGBOOST TRAINING COMPLETED SUCCESSFULLY")
print("=" * 70)