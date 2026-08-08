"""
============================================================
CARTGUARD AI
Feature Engineering
============================================================

Purpose:
    Convert cleaned e-commerce clickstream events into
    session-level features for ML model training.

Important:
    Purchase events are NOT included in the observation
    features.

    This prevents target leakage.

Target:
    1 -> Session eventually resulted in purchase
    0 -> Session did not result in purchase

Input:
    cleaned_data/2019-Oct_cleaned.csv

Output:
    final_training_dataset.csv

Author:
    Team CartGuard AI
============================================================
"""

from pathlib import Path
import time

import numpy as np
import pandas as pd


# ============================================================
# START TIMER
# ============================================================

START_TIME = time.time()


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR
    / "cleaned_data"
    / "2019-Oct_cleaned.csv"
)

OUTPUT_FILE = (
    BASE_DIR
    / "final_training_dataset.csv"
)


# ============================================================
# CONFIGURATION
# ============================================================

REQUIRED_COLUMNS = [
    "event_time",
    "event_type",
    "product_id",
    "category_id",
    "category_code",
    "brand",
    "price",
    "user_id",
    "user_session",
]


# ============================================================
# HEADER
# ============================================================

print()
print("=" * 70)
print(" CARTGUARD AI - FEATURE ENGINEERING ")
print("=" * 70)


# ============================================================
# LOAD DATASET
# ============================================================

print("\nLoading cleaned dataset...")

load_start = time.time()

df = pd.read_csv(INPUT_FILE)

load_time = time.time() - load_start

print(f"Loaded Rows    : {len(df):,}")
print(f"Loaded Columns : {len(df.columns)}")
print(f"Loading Time   : {load_time:.2f} seconds")


# ============================================================
# VALIDATE REQUIRED COLUMNS
# ============================================================

print("\nValidating dataset...")

missing_columns = [
    column
    for column in REQUIRED_COLUMNS
    if column not in df.columns
]

if missing_columns:

    print("\nERROR: Missing required columns:")

    for column in missing_columns:
        print(f"- {column}")

    raise ValueError(
        "Dataset validation failed."
    )

print("All required columns found.")


# ============================================================
# KEEP ONLY REQUIRED COLUMNS
# ============================================================

df = df[REQUIRED_COLUMNS].copy()


# ============================================================
# CLEAN DATA
# ============================================================

print("\nCleaning dataset...")

before_cleaning = len(df)


# Remove rows without session ID
df = df.dropna(
    subset=["user_session"]
)


# Remove invalid event types
valid_event_types = [
    "view",
    "cart",
    "purchase",
]

df = df[
    df["event_type"].isin(valid_event_types)
]


# Remove invalid prices
df["price"] = pd.to_numeric(
    df["price"],
    errors="coerce"
)

df = df[
    df["price"].notna()
]

df = df[
    df["price"] >= 0
]


# Remove invalid product/category IDs
df = df.dropna(
    subset=[
        "product_id",
        "category_id",
    ]
)


removed_rows = (
    before_cleaning - len(df)
)

print(
    f"Removed Invalid Rows : {removed_rows:,}"
)

print("Dataset cleaned successfully.")


# ============================================================
# CONVERT TIMESTAMP
# ============================================================

print("\nConverting timestamps...")

df["event_time"] = pd.to_datetime(
    df["event_time"],
    errors="coerce"
)

invalid_timestamps = (
    df["event_time"].isna().sum()
)

if invalid_timestamps > 0:

    print(
        f"Removing Invalid Timestamps : "
        f"{invalid_timestamps:,}"
    )

    df = df.dropna(
        subset=["event_time"]
    )

else:

    print(
        "Invalid Timestamp Rows : 0"
    )


# ============================================================
# SORT EVENTS
# ============================================================

print("\nSorting events...")

df = df.sort_values(
    [
        "user_session",
        "event_time"
    ]
).reset_index(drop=True)

print("Events sorted successfully.")


# ============================================================
# CREATE TARGET
# ============================================================

print("\nCreating session targets...")


# Sessions that contain at least one purchase
purchase_sessions = set(
    df.loc[
        df["event_type"] == "purchase",
        "user_session"
    ].unique()
)


print(
    f"Purchase Sessions : "
    f"{len(purchase_sessions):,}"
)


# ============================================================
# TARGET LEAKAGE PROTECTION
# ============================================================

print(
    "\nCreating pre-outcome observation data..."
)

print(
    "Target leakage protection : ENABLED"
)


# ------------------------------------------------------------
# IMPORTANT
#
# For purchase sessions:
#   Only events BEFORE the FIRST purchase are used.
#
# For non-purchase sessions:
#   All events are used.
#
# This prevents:
#
# purchase_count
# purchase_event
# purchase_price
#
# etc. from directly revealing the target.
# ------------------------------------------------------------


# Find first purchase timestamp for every purchasing session

first_purchase_time = (
    df[
        df["event_type"] == "purchase"
    ]
    .groupby("user_session")["event_time"]
    .min()
    .rename("first_purchase_time")
)


# Attach first purchase time

df = df.merge(
    first_purchase_time,
    on="user_session",
    how="left"
)


# ------------------------------------------------------------
# Keep only observation events
#
# Purchase session:
#     event_time < first purchase
#
# Non-purchase session:
#     first_purchase_time is NaN
# ------------------------------------------------------------

observation_mask = (
    df["first_purchase_time"].isna()
    |
    (
        df["event_time"]
        <
        df["first_purchase_time"]
    )
)


observation_df = df[
    observation_mask
].copy()


# Remove helper column

observation_df.drop(
    columns=["first_purchase_time"],
    inplace=True
)


print(
    f"Observation Events : "
    f"{len(observation_df):,}"
)


# ============================================================
# SESSION TARGETS
# ============================================================

target_df = (
    df.groupby("user_session")
    .agg(
        target=(
            "event_type",
            lambda x:
            int("purchase" in set(x))
        )
    )
)


# ============================================================
# GENERATE SESSION FEATURES
# ============================================================

print("\nGenerating session features...")


# ============================================================
# BASIC SESSION FEATURES
# ============================================================

session_features = (
    observation_df
    .groupby("user_session")
    .agg(
        session_start=(
            "event_time",
            "min"
        ),

        session_end=(
            "event_time",
            "max"
        ),

        total_events=(
            "event_type",
            "count"
        ),

        unique_products=(
            "product_id",
            "nunique"
        ),

        unique_categories=(
            "category_id",
            "nunique"
        ),

        unique_brands=(
            "brand",
            "nunique"
        ),
    )
)


# ============================================================
# SESSION DURATION
# ============================================================

session_features[
    "session_duration"
] = (
    session_features["session_end"]
    -
    session_features["session_start"]
).dt.total_seconds()


# ============================================================
# PRICE FEATURES
# ============================================================

price_features = (
    observation_df
    .groupby("user_session")["price"]
    .agg(
        total_price="sum",

        average_price="mean",

        minimum_price="min",

        maximum_price="max",

        price_std="std",
    )
)


# ============================================================
# PRICE RANGE
# ============================================================

price_features[
    "price_range"
] = (
    price_features["maximum_price"]
    -
    price_features["minimum_price"]
)


# ============================================================
# EVENT COUNTS
# ============================================================

event_counts = pd.crosstab(
    observation_df["user_session"],
    observation_df["event_type"]
)


# Make sure every expected event column exists

for event_type in [
    "view",
    "cart",
]:

    if event_type not in event_counts.columns:

        event_counts[event_type] = 0


# Rename columns

event_counts = event_counts.rename(
    columns={
        "view": "view_count",
        "cart": "cart_count",
    }
)


# Keep only required event features

event_counts = event_counts[
    [
        "view_count",
        "cart_count",
    ]
]


# ============================================================
# MERGE FEATURES
# ============================================================

features = pd.concat(
    [
        session_features,
        price_features,
        event_counts,
    ],
    axis=1
)


# ============================================================
# REMOVE DATETIME COLUMNS
# ============================================================

features.drop(
    columns=[
        "session_start",
        "session_end",
    ],
    inplace=True
)


# ============================================================
# MISSING VALUES
# ============================================================

features["price_std"] = (
    features["price_std"]
    .fillna(0)
)


features = features.fillna(0)


# ============================================================
# CART BEHAVIOR FEATURES
# ============================================================

features["has_cart"] = (
    features["cart_count"] > 0
).astype(int)


# ============================================================
# CART TO EVENT RATIO
# ============================================================

features[
    "cart_to_event_ratio"
] = np.where(
    features["total_events"] > 0,

    features["cart_count"]
    /
    features["total_events"],

    0
)


# ============================================================
# VIEW TO EVENT RATIO
# ============================================================

features[
    "views_to_event_ratio"
] = np.where(
    features["total_events"] > 0,

    features["view_count"]
    /
    features["total_events"],

    0
)


# ============================================================
# CART TO VIEW RATIO
# ============================================================

features[
    "cart_to_view_ratio"
] = np.where(
    features["view_count"] > 0,

    features["cart_count"]
    /
    features["view_count"],

    0
)


# ============================================================
# EVENTS PER SECOND
# ============================================================

features[
    "events_per_second"
] = np.where(
    features["session_duration"] > 0,

    features["total_events"]
    /
    features["session_duration"],

    0
)


# ============================================================
# PRODUCTS PER CATEGORY
# ============================================================

features[
    "products_per_category"
] = np.where(
    features["unique_categories"] > 0,

    features["unique_products"]
    /
    features["unique_categories"],

    0
)


# ============================================================
# PRODUCTS PER BRAND
# ============================================================

features[
    "products_per_brand"
] = np.where(
    features["unique_brands"] > 0,

    features["unique_products"]
    /
    features["unique_brands"],

    0
)


# ============================================================
# CATEGORY PER EVENT RATIO
# ============================================================

features[
    "category_per_event_ratio"
] = np.where(
    features["total_events"] > 0,

    features["unique_categories"]
    /
    features["total_events"],

    0
)


# ============================================================
# BRAND PER EVENT RATIO
# ============================================================

features[
    "brand_per_event_ratio"
] = np.where(
    features["total_events"] > 0,

    features["unique_brands"]
    /
    features["total_events"],

    0
)


# ============================================================
# ATTACH TARGET
# ============================================================

print("\nAttaching target labels...")


features = features.join(
    target_df,
    how="inner"
)


# ============================================================
# RESET INDEX
# ============================================================

features.reset_index(
    inplace=True
)


# ============================================================
# FINAL COLUMN ORDER
# ============================================================

FEATURE_COLUMNS = [

    "user_session",

    "session_duration",

    "total_events",

    "unique_products",

    "unique_categories",

    "unique_brands",

    "total_price",

    "average_price",

    "minimum_price",

    "maximum_price",

    "price_range",

    "price_std",

    "view_count",

    "cart_count",

    "has_cart",

    "cart_to_event_ratio",

    "views_to_event_ratio",

    "cart_to_view_ratio",

    "events_per_second",

    "products_per_category",

    "products_per_brand",

    "category_per_event_ratio",

    "brand_per_event_ratio",

    "target",
]


features = features[
    FEATURE_COLUMNS
]


# ============================================================
# NUMERIC CONVERSION
# ============================================================

numeric_columns = [
    column
    for column in FEATURE_COLUMNS
    if column not in [
        "user_session"
    ]
]


for column in numeric_columns:

    features[column] = pd.to_numeric(
        features[column],
        errors="coerce"
    )


# ============================================================
# FINAL MISSING VALUE CHECK
# ============================================================

features[numeric_columns] = (
    features[numeric_columns]
    .replace(
        [
            np.inf,
            -np.inf
        ],
        0
    )
    .fillna(0)
)


# ============================================================
# TARGET INTEGER
# ============================================================

features["target"] = (
    features["target"]
    .astype(int)
)


# ============================================================
# VALIDATION
# ============================================================

print("\nFinalizing training dataset...")

print(
    "\nSessions : "
    f"{features['user_session'].nunique():,}"
)

print(
    "Columns  : "
    f"{len(features.columns)}"
)

print(
    "Missing Values : "
    f"{features.isnull().sum().sum():,}"
)

print(
    "Duplicate Sessions : "
    f"{features['user_session'].duplicated().sum():,}"
)


# ============================================================
# TARGET DISTRIBUTION
# ============================================================

print("\nTarget Distribution:")

print(
    features["target"]
    .value_counts()
    .sort_index()
)


# ============================================================
# TARGET PERCENTAGE
# ============================================================

print("\nTarget Percentage:")

print(
    (
        features["target"]
        .value_counts(
            normalize=True
        )
        .sort_index()
        * 100
    ).round(2)
)


# ============================================================
# FEATURE LIST
# ============================================================

print("\nFeature Columns:")

ml_features = [
    column
    for column in FEATURE_COLUMNS
    if column not in [
        "user_session",
        "target"
    ]
]

for index, feature in enumerate(
    ml_features,
    start=1
):

    print(
        f"{index}. {feature}"
    )


# ============================================================
# TARGET LEAKAGE CHECK
# ============================================================

print(
    "\nTarget Leakage Check : ",
    end=""
)


LEAKAGE_COLUMNS = [
    "purchase_count",
    "purchase_price",
    "purchase_event",
    "first_purchase_time",
]


leakage_found = [
    column
    for column in features.columns
    if column in LEAKAGE_COLUMNS
]


if leakage_found:

    print("FAILED")

    print(
        "Leakage columns found:",
        leakage_found
    )

    raise ValueError(
        "Target leakage detected."
    )

else:

    print("PASSED")


# ============================================================
# NUMERIC FEATURE CHECK
# ============================================================

print(
    "Numeric Feature Check : ",
    end=""
)


non_numeric_features = []

for column in ml_features:

    if not pd.api.types.is_numeric_dtype(
        features[column]
    ):

        non_numeric_features.append(
            column
        )


if non_numeric_features:

    print("FAILED")

    print(
        "Non-numeric features:",
        non_numeric_features
    )

    raise ValueError(
        "Non-numeric ML features detected."
    )

else:

    print("PASSED")


# ============================================================
# DUPLICATE CHECK
# ============================================================

if features["user_session"].duplicated().any():

    raise ValueError(
        "Duplicate sessions detected."
    )


# ============================================================
# TARGET VALIDATION
# ============================================================

if not set(
    features["target"].unique()
).issubset({0, 1}):

    raise ValueError(
        "Target must contain only 0 and 1."
    )


# ============================================================
# FINAL VALIDATION
# ============================================================

print("\nValidation Status : PASSED")


# ============================================================
# SAVE DATASET
# ============================================================

print("\nSaving training dataset...")

features.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# FINAL SUMMARY
# ============================================================

processing_time = (
    time.time() - START_TIME
)


print(
    f"\nSaved To : {OUTPUT_FILE}"
)

print(
    "\n" + "=" * 70
)

print(
    f"Sessions           : "
    f"{len(features):,}"
)

print(
    f"Features           : "
    f"{len(ml_features)}"
)

print(
    f"Total Columns      : "
    f"{len(features.columns)}"
)

print(
    f"Purchase Sessions  : "
    f"{(features['target'] == 1).sum():,}"
)

print(
    f"Non-Purchase Sessions : "
    f"{(features['target'] == 0).sum():,}"
)

print(
    f"\nProcessing Time : "
    f"{processing_time:.2f} seconds"
)

print(
    f"\nOutput File : "
    f"{OUTPUT_FILE}"
)

print(
    "\n" + "=" * 70
)