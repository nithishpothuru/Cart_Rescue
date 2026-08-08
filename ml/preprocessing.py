# from pathlib import Path
# import pandas as pd
# import os

# # --------------------------------------------------
# # Paths
# # --------------------------------------------------

# BASE_DIR = Path(__file__).resolve().parent

# DATASET_PATHS = {
#     "waqi": BASE_DIR / "datasets" / "waqi",
#     "wafaa": BASE_DIR / "datasets" / "wafaa",
#     "yashwant": BASE_DIR / "datasets" / "yashwant",
#     "arashnic": BASE_DIR / "datasets" / "arashnic",
# }

# OUTPUT_DIR = BASE_DIR / "cleaned_data"
# OUTPUT_DIR.mkdir(exist_ok=True)


# # --------------------------------------------------
# # Read Dataset
# # --------------------------------------------------

# def read_file(file_path):
#     """
#     Read CSV or Excel files.
#     """

#     extension = file_path.suffix.lower()

#     if extension == ".csv":
#         return pd.read_csv(file_path)

#     elif extension in [".xlsx", ".xls"]:
#         return pd.read_excel(file_path)

#     else:
#         return None


# # --------------------------------------------------
# # Clean Column Names
# # --------------------------------------------------

# def clean_column_names(df):

#     df.columns = (
#         df.columns
#         .str.strip()
#         .str.lower()
#         .str.replace(" ", "_")
#         .str.replace("-", "_")
#         .str.replace("/", "_")
#     )

#     return df


# # --------------------------------------------------
# # Remove Duplicate Rows
# # --------------------------------------------------

# def remove_duplicates(df):

#     before = len(df)

#     df = df.drop_duplicates()

#     after = len(df)

#     print(f"Removed {before-after} duplicate rows.")

#     return df


# # --------------------------------------------------
# # Handle Missing Values
# # --------------------------------------------------

# def handle_missing_values(df):

#     for column in df.columns:

#         if df[column].dtype == "object":

#             df[column] = df[column].fillna("Unknown")

#         else:

#             median = df[column].median()

#             df[column] = df[column].fillna(median)

#     return df


# # --------------------------------------------------
# # Dataset Summary
# # --------------------------------------------------

# def dataset_summary(df):

#     print()

#     print("Rows :", len(df))
#     print("Columns :", len(df.columns))

#     print()

#     print(df.dtypes)

#     print()

#     print(df.isnull().sum())

#     print("-" * 60)


# # --------------------------------------------------
# # Process One Dataset
# # --------------------------------------------------

# def process_dataset(dataset_name, dataset_folder):

#     print("=" * 70)
#     print(dataset_name.upper())
#     print("=" * 70)

#     files = []

#     for root, _, filenames in os.walk(dataset_folder):

#         for file in filenames:

#             if file.endswith((".csv", ".xlsx", ".xls")):

#                 files.append(Path(root) / file)

#     if len(files) == 0:

#         print("No files found.")

#         return

#     for file in files:

#         print(f"\nProcessing : {file.name}")

#         df = read_file(file)

#         if df is None:
#             continue

#         df = clean_column_names(df)

#         df = remove_duplicates(df)

#         df = handle_missing_values(df)

#         dataset_summary(df)

#         output_file = OUTPUT_DIR / f"{file.stem}_cleaned.csv"

#         df.to_csv(output_file, index=False)

#         print(f"Saved : {output_file.name}")


# # --------------------------------------------------
# # Main
# # --------------------------------------------------

# def main():

#     print("\nCartGuard AI - Data Preprocessing\n")

#     for dataset_name, folder in DATASET_PATHS.items():

#         process_dataset(dataset_name, folder)

# if __name__ == "__main__":

#     main()





"""
==============================================================
CartGuard AI
Data Preprocessing Pipeline

Dataset:
    Yashwant Ecommerce Clickstream Dataset

Purpose:
    Clean raw clickstream data before feature engineering.

Author:
    Team CartGuard AI
==============================================================
"""

from pathlib import Path
import pandas as pd
import numpy as np
import time
# ============================================================
# Project Paths
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_FILE = (
    BASE_DIR / "datasets" / "yashwant" / "2019-Oct.csv"
)

OUTPUT_DIR = (
    BASE_DIR
    / "cleaned_data"
)

OUTPUT_DIR.mkdir(exist_ok=True)

OUTPUT_FILE = (
    OUTPUT_DIR
    / "2019-Oct_cleaned.csv"
)

# ============================================================
# Required Columns
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

    "user_session"

]

VALID_EVENTS = [

    "view",

    "cart",

    "purchase"

]

# ============================================================
# Load Dataset
# ============================================================

def load_dataset():

    print("=" * 70)
    print(" CARTGUARD AI - DATA PREPROCESSING ")
    print("=" * 70)

    print("\nLoading Dataset...")


    if not INPUT_FILE.exists():

        raise FileNotFoundError(
            f"""
            Dataset not found.

            Download:
            https://www.kaggle.com/datasets/yashwant020/ecommerce-clickstream-dataset-5-27-gb

            Place it here:

            {INPUT_FILE}

            """
        )

    df = pd.read_csv(
        INPUT_FILE,
        nrows=2_000_000,
        low_memory=False
    )   

    print(f"\nLoaded Rows : {len(df):,}")

    print(f"Loaded Columns : {len(df.columns)}")

    return df

# ============================================================
# Clean Column Names
# ============================================================

def clean_column_names(df):

    print("\nCleaning Column Names...")

    df.columns = (

        df.columns

        .str.strip()

        .str.lower()

        .str.replace(" ", "_")

        .str.replace("-", "_")

        .str.replace("/", "_")

    )

    print("Column Names Cleaned.")

    return df

# ============================================================
# Validate Required Columns
# ============================================================

def validate_columns(df):

    print("\nValidating Columns...")

    missing = [

        column

        for column in REQUIRED_COLUMNS

        if column not in df.columns

    ]

    if len(missing) > 0:

        raise Exception(

            f"Missing Columns : {missing}"

        )

    print("All Required Columns Found.")

# ============================================================
# Keep Only Required Columns
# ============================================================

def keep_required_columns(df):

    print("\nKeeping Required Columns...")

    df = df[REQUIRED_COLUMNS]

    print(f"Columns Retained : {len(df.columns)}")

    return df

# ============================================================
# Remove Invalid Records
# ============================================================

def remove_invalid_rows(df):

    print("\nRemoving Invalid Records...")

    before = len(df)

    # Required columns cannot be null
    df = df.dropna(

        subset=[

            "user_session",

            "event_time",

            "event_type",

            "product_id",

            "category_id",

            "price"

        ]

    )

    # Remove invalid prices
    df = df[df["price"] > 0]

    # Keep only supported event types
    df = df[

        df["event_type"].isin(

            VALID_EVENTS

        )

    ]

    after = len(df)

    print(f"Removed Rows : {before-after:,}")

    return df


# ============================================================
# Handle Missing Values
# ============================================================

def handle_missing_values(df):

    print("\nHandling Missing Values...")

    if "brand" in df.columns:

        df["brand"] = (

            df["brand"]

            .fillna("Unknown")

        )

    if "category_code" in df.columns:

        df["category_code"] = (

            df["category_code"]

            .fillna("Unknown")

        )

    print("Missing Values Handled.")

    return df


# ============================================================
# Convert Data Types
# ============================================================

def convert_dtypes(df):

    print("\nConverting Data Types...")

    df["event_time"] = pd.to_datetime(

        df["event_time"],

        errors="coerce"

    )

    df["price"] = (

        pd.to_numeric(

            df["price"],

            errors="coerce"

        )

        .astype("float32")

    )

    df["product_id"] = df["product_id"].astype("int64")

    df["category_id"] = df["category_id"].astype("int64")

    df["event_type"] = df["event_type"].astype("category")

    df["brand"] = df["brand"].astype("category")

    df["category_code"] = df["category_code"].astype("category")

    print("Data Types Converted.")

    return df


# ============================================================
# Remove Duplicate Events
# ============================================================

def remove_duplicate_events(df):

    print("\nRemoving Duplicate Events...")

    before = len(df)

    df = df.drop_duplicates(

        subset=[

            "user_session",

            "event_time",

            "event_type",

            "product_id"

        ]

    )

    after = len(df)

    print(f"Duplicate Events Removed : {before-after:,}")

    return df


# ============================================================
# Remove Invalid Datetime
# ============================================================

def remove_invalid_datetime(df):

    print("\nRemoving Invalid Timestamps...")

    before = len(df)

    df = df[

        df["event_time"].notna()

    ]

    after = len(df)

    print(f"Invalid Timestamp Rows : {before-after:,}")

    return df


# ============================================================
# Memory Optimization
# ============================================================

def optimize_memory(df):

    print("\nOptimizing Memory...")

    df["user_id"] = df["user_id"].astype("int32")
    df["product_id"] = df["product_id"].astype("int32")
    df["category_id"] = df["category_id"].astype("int64")
    df["price"] = df["price"].astype("float32")

    print("Memory Optimization Completed.")

    return df
# ============================================================
# Sort Dataset
# ============================================================

def sort_dataset(df):

    print("\nSorting Dataset...")

    df = df.sort_values(

        by=[

            "user_session",

            "event_time"

        ]

    ).reset_index(

        drop=True

    )

    print("Dataset Sorted Successfully.")

    return df

def remove_small_sessions(df):

    print("\nRemoving Very Small Sessions...")

    session_sizes = df.groupby("user_session").size()

    valid_sessions = session_sizes[
        session_sizes >= 2
    ].index

    before = len(df)

    df = df[
        df["user_session"].isin(valid_sessions)
    ]

    after = len(df)

    print(f"Removed Rows : {before-after:,}")

    return df
# ============================================================
# Validate Dataset
# ============================================================

def validate_dataset(df):

    print("\nRunning Validation Checks...")

    print("-" * 50)

    print(f"Rows              : {len(df):,}")

    print(f"Columns           : {len(df.columns)}")

    print(f"Unique Sessions   : {df['user_session'].nunique():,}")

    print(f"Unique Users      : {df['user_id'].nunique():,}")

    print()

    print("Event Distribution:")

    print(df["event_type"].value_counts())

    print()

    print("Missing Values:")

    print(df.isnull().sum())

    print()

    print("Data Types:")

    print(df.dtypes)

    print("-" * 50)


# ============================================================
# Save Dataset
# ============================================================

def save_dataset(df):

    print("\nSaving Clean Dataset...")

    df.to_csv(
    OUTPUT_FILE,
    index=False,
    compression="infer"
    )

    print(f"Saved To : {OUTPUT_FILE}")


# ============================================================
# Preprocessing Pipeline
# ============================================================

def preprocess():

    df = load_dataset()

    df = clean_column_names(df)

    validate_columns(df)

    df = keep_required_columns(df)

    df = remove_invalid_rows(df)

    df = handle_missing_values(df)

    df = convert_dtypes(df)

    df = remove_invalid_datetime(df)

    df = remove_duplicate_events(df)

    df = optimize_memory(df)

    df = sort_dataset(df)

    validate_dataset(df)

    save_dataset(df)

    return df
# ============================================================
# Final Summary
# ============================================================

def print_summary(df):

    print("\n")
    print("=" * 70)
    print("PREPROCESSING SUMMARY")
    print("=" * 70)

    print(f"Total Rows            : {len(df):,}")
    print(f"Total Columns         : {len(df.columns)}")
    print(f"Unique Sessions       : {df['user_session'].nunique():,}")
    print(f"Unique Users          : {df['user_id'].nunique():,}")
    print(f"Unique Products       : {df['product_id'].nunique():,}")
    print(f"Unique Categories     : {df['category_id'].nunique():,}")

    print("\nEvent Distribution")
    print("-" * 40)
    print(df["event_type"].value_counts())

    print("\nMemory Usage")
    print("-" * 40)

    memory = (
        df.memory_usage(deep=True).sum()
        / 1024
        / 1024
    )

    print(f"{memory:.2f} MB")

    print("\nOutput File")
    print("-" * 40)
    print(OUTPUT_FILE)

    print("\n")
    print("=" * 70)
    print("DATA PREPROCESSING COMPLETED SUCCESSFULLY")
    print("=" * 70)


# ============================================================
# Main
# ============================================================

def main():

    try:
        start = time.time()

        df = preprocess()

        print_summary(df)
        end = time.time()

        print(f"\nProcessing Time : {(end-start):.2f} seconds")

    except Exception as error:

        print("\n")
        print("=" * 70)
        print("PREPROCESSING FAILED")
        print("=" * 70)
        print(error)


# ============================================================
# Run
# ============================================================

if __name__ == "__main__":

    main()