# import pandas as pd
# # df=pd.read_csv(r"D:\MY_PROJECTS\Hackathon1-1\ml\cleaned_data\ecommerce_clickstream_transactions_cleaned.csv")
# # print(df["sessionid"].nunique())
# # print(df["userid"].nunique())

# # print("\nSession IDs:")
# # print(df["sessionid"].value_counts())

# # print("\nOutcome Distribution:")
# # print(df["outcome"].value_counts(dropna=False))

# df = pd.read_csv(r"D:\MY_PROJECTS\Hackathon1-1\ml\datasets\yashwant\2019-Oct.csv", nrows=5)

# print(df.head())
# print("\nColumns:")
# print(df.columns.tolist())

# print("\nData Types:")
# print(df.dtypes)
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

df = pd.read_csv(
    BASE_DIR / "cleaned_data" / "2019-Oct_cleaned.csv",
    nrows=2_000_000
)

print("Event Type Distribution:")
print(df["event_type"].value_counts())

print("\nPurchase Sessions:")
print(df[df["event_type"] == "purchase"]["user_session"].nunique())

print("\nTotal Sessions:")
print(df["user_session"].nunique())
features = pd.read_csv(BASE_DIR / "final_training_dataset.csv")

print(features.head())

print("\nTarget Distribution:")
print(features["target"].value_counts())

print("\nFeature Correlation with Target:")
print(features.corr(numeric_only=True)["target"].sort_values(ascending=False))