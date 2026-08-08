from pathlib import Path
import json
import pandas as pd

# ============================================================
# CARTGUARD AI
# MODEL COMPARISON
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "saved_models"

LOGISTIC_PATH = MODEL_DIR / "logistic_metrics.json"
RANDOM_FOREST_PATH = MODEL_DIR / "random_forest_metrics.json"
XGBOOST_PATH = MODEL_DIR / "xgboost_metrics.json"

OUTPUT_PATH = MODEL_DIR / "model_comparison.csv"


# ============================================================
# Header
# ============================================================

print("=" * 70)
print(" CARTGUARD AI - MODEL COMPARISON ")
print("=" * 70)


# ============================================================
# Load Metrics
# ============================================================

def load_metrics(path, model_name):

    try:

        with open(path, "r") as file:
            metrics = json.load(file)

        print(f"{model_name} metrics loaded.")

        return metrics

    except FileNotFoundError:

        print(f"{model_name} metrics file not found:")
        print(path)

        return None


print("\nLoading Model Metrics...")

logistic_metrics = load_metrics(
    LOGISTIC_PATH,
    "Logistic Regression"
)

random_forest_metrics = load_metrics(
    RANDOM_FOREST_PATH,
    "Random Forest"
)

xgboost_metrics = load_metrics(
    XGBOOST_PATH,
    "XGBoost"
)


# ============================================================
# Extract Metric
# ============================================================

def get_metric(metrics, *keys, default=0):

    for key in keys:

        if key in metrics:

            try:
                return float(metrics[key])

            except (ValueError, TypeError):
                return default

    return default


# ============================================================
# Build Comparison
# ============================================================

comparison = []


# ------------------------------------------------------------
# Logistic Regression
# ------------------------------------------------------------

if logistic_metrics:

    comparison.append({

        "Model": "Logistic Regression",

        "Accuracy": get_metric(
            logistic_metrics,
            "accuracy",
            "Accuracy"
        ),

        "Precision": get_metric(
            logistic_metrics,
            "precision",
            "Precision"
        ),

        "Recall": get_metric(
            logistic_metrics,
            "recall",
            "Recall"
        ),

        "F1 Score": get_metric(
            logistic_metrics,
            "f1_score",
            "F1 Score"
        ),

        "ROC AUC": get_metric(
            logistic_metrics,
            "roc_auc",
            "ROC AUC"
        ),

        "Threshold": get_metric(
            logistic_metrics,
            "classification_threshold",
            "Threshold",
            default=0.50
        ),

        "Features": int(
            get_metric(
                logistic_metrics,
                "number_of_features",
                "Features"
            )
        )

    })


# ------------------------------------------------------------
# Random Forest
# ------------------------------------------------------------

if random_forest_metrics:

    comparison.append({

        "Model": "Random Forest",

        "Accuracy": get_metric(
            random_forest_metrics,
            "accuracy",
            "Accuracy"
        ),

        "Precision": get_metric(
            random_forest_metrics,
            "precision",
            "Precision"
        ),

        "Recall": get_metric(
            random_forest_metrics,
            "recall",
            "Recall"
        ),

        "F1 Score": get_metric(
            random_forest_metrics,
            "f1_score",
            "F1 Score"
        ),

        "ROC AUC": get_metric(
            random_forest_metrics,
            "roc_auc",
            "ROC AUC"
        ),

        "Threshold": get_metric(
            random_forest_metrics,
            "classification_threshold",
            "Threshold",
            default=0.50
        ),

        "Features": int(
            get_metric(
                random_forest_metrics,
                "number_of_features",
                "Features"
            )
        )

    })


# ------------------------------------------------------------
# XGBoost
# ------------------------------------------------------------

if xgboost_metrics:

    comparison.append({

        "Model": "XGBoost",

        "Accuracy": get_metric(
            xgboost_metrics,
            "accuracy",
            "Accuracy"
        ),

        "Precision": get_metric(
            xgboost_metrics,
            "precision",
            "Precision"
        ),

        "Recall": get_metric(
            xgboost_metrics,
            "recall",
            "Recall"
        ),

        "F1 Score": get_metric(
            xgboost_metrics,
            "f1_score",
            "F1 Score"
        ),

        "ROC AUC": get_metric(
            xgboost_metrics,
            "roc_auc",
            "ROC AUC"
        ),

        "Threshold": get_metric(
            xgboost_metrics,
            "classification_threshold",
            "Threshold",
            default=0.50
        ),

        "Features": int(
            get_metric(
                xgboost_metrics,
                "number_of_features",
                "Features"
            )
        )

    })


# ============================================================
# Create DataFrame
# ============================================================

comparison_df = pd.DataFrame(comparison)


# ============================================================
# Display Comparison
# ============================================================

print("\n")

print("=" * 70)
print("MODEL PERFORMANCE COMPARISON")
print("=" * 70)

print()

print(
    comparison_df.to_string(
        index=False,
        float_format=lambda x: f"{x:.4f}"
    )
)


# ============================================================
# Best Model By Metric
# ============================================================

print("\n")

print("=" * 70)
print("BEST MODEL BY METRIC")
print("=" * 70)


metrics_to_compare = [

    "Accuracy",
    "Precision",
    "Recall",
    "F1 Score",
    "ROC AUC"

]


for metric in metrics_to_compare:

    best_index = comparison_df[metric].idxmax()

    best_model = comparison_df.loc[
        best_index,
        "Model"
    ]

    best_value = comparison_df.loc[
        best_index,
        metric
    ]

    print(
        f"{metric:<12} : "
        f"{best_model:<20} "
        f"({best_value:.4f})"
    )


# ============================================================
# Overall Model Score
# ============================================================

# CartGuard is an imbalanced classification problem.
#
# Therefore:
# F1 Score = 50%
# ROC AUC  = 50%
#
# Accuracy is not used for final model selection.

comparison_df["Overall_Score"] = (

    comparison_df["F1 Score"] * 0.50

    +

    comparison_df["ROC AUC"] * 0.50

)


best_index = comparison_df[
    "Overall_Score"
].idxmax()


best_model = comparison_df.loc[
    best_index,
    "Model"
]

best_f1 = comparison_df.loc[
    best_index,
    "F1 Score"
]

best_auc = comparison_df.loc[
    best_index,
    "ROC AUC"
]

best_score = comparison_df.loc[
    best_index,
    "Overall_Score"
]


# ============================================================
# Recommended Model
# ============================================================

print("\n")

print("=" * 70)
print("RECOMMENDED MODEL")
print("=" * 70)

print(
    f"\nBest Model     : {best_model}"
)

print(
    f"F1 Score       : {best_f1:.4f}"
)

print(
    f"ROC AUC        : {best_auc:.4f}"
)

print(
    f"Overall Score  : {best_score:.4f}"
)


# ============================================================
# Save Comparison
# ============================================================

comparison_df.to_csv(
    OUTPUT_PATH,
    index=False
)


print("\n")

print("=" * 70)
print("COMPARISON SAVED")
print("=" * 70)

print(
    f"\nSaved To : {OUTPUT_PATH}"
)


print("\n")

print("=" * 70)
print("MODEL COMPARISON COMPLETED SUCCESSFULLY")
print("=" * 70)