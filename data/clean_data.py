"""Clean the raw Customer Personality Analysis dataset and derive growth-analysis columns."""
import pandas as pd

df = pd.read_csv("data/marketing_campaign.csv", sep=";")
n_start = len(df)

df["Dt_Customer"] = pd.to_datetime(df["Dt_Customer"], format="%Y-%m-%d")
reference_date = df["Dt_Customer"].max()

df = df.drop(columns=["Z_CostContact", "Z_Revenue"])

df = df[df["Year_Birth"] >= 1940]
df = df[(df["Income"].isna()) | (df["Income"] <= 200000)]

df["Income"] = df["Income"].fillna(df["Income"].median())

df["Marital_Status"] = df["Marital_Status"].replace(
    {"Alone": "Single", "Absurd": "Other", "YOLO": "Other"}
)

df["Age"] = reference_date.year - df["Year_Birth"]

spend_cols = ["MntWines", "MntFruits", "MntMeatProducts", "MntFishProducts", "MntSweetProducts", "MntGoldProds"]
df["Total_Spend"] = df[spend_cols].sum(axis=1)

purchase_cols = ["NumDealsPurchases", "NumWebPurchases", "NumCatalogPurchases", "NumStorePurchases"]
df["Total_Purchases"] = df[purchase_cols].sum(axis=1)

campaign_cols = ["AcceptedCmp1", "AcceptedCmp2", "AcceptedCmp3", "AcceptedCmp4", "AcceptedCmp5", "Response"]
df["Total_Campaigns_Accepted"] = df[campaign_cols].sum(axis=1)

df["Customer_Tenure_Days"] = (reference_date - df["Dt_Customer"]).dt.days

df.to_csv("data/processed/marketing_campaign_clean.csv", index=False)

print(f"Rows: {n_start} -> {len(df)} ({n_start - len(df)} removed)")
print(f"Reference date used for Age / tenure: {reference_date.date()}")
print(f"Columns: {len(df.columns)}")
