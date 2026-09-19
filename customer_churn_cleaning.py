import pandas as pd

INPUT_FILE = "customer_churn_sample(1).csv"
OUTPUT_FILE = "customer_churn_cleaned.csv"

df = pd.read_csv(INPUT_FILE)

# 1. Standardize column headers
column_map = {
    "CustomerID": "customer_id",
    "Gender": "gender",
    "Age": "age",
    "TenureMonths": "tenure_months",
    "SubscriptionType": "subscription_type",
    "MonthlyCharges": "monthly_charges",
    "TotalCharges": "total_charges",
    "ContractType": "contract_type",
    "SupportTickets": "support_tickets",
    "PaymentMethod": "payment_method",
    "Churn": "churn",
}
df = df.rename(columns=column_map)

# 2. Standardize text/categorical values
text_cols = df.select_dtypes(include="object").columns
for col in text_cols:
    df[col] = (
        df[col].astype("string")
        .str.strip()
        .str.replace(r"\\s+", " ", regex=True)
    )

# 3. Validate/convert numeric fields
numeric_cols = [
    "age", "tenure_months", "monthly_charges",
    "total_charges", "support_tickets"
]
for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 4. Check missing values and duplicates
print("Missing values before handling:")
print(df.isna().sum())
print("\nDuplicate rows before removal:", df.duplicated().sum())

# The supplied sample has no missing values, so no imputation/drop is required.
df = df.drop_duplicates().reset_index(drop=True)

# 5. Business-rule validation
charge_diff = (
    df["monthly_charges"] * df["tenure_months"] - df["total_charges"]
).abs()

print("\nMissing values after cleaning:", df.isna().sum().sum())
print("Duplicate rows after cleaning:", df.duplicated().sum())
print("Total-charge mismatches (> 0.01):", (charge_diff > 0.01).sum())

# 6. Export
df.to_csv(OUTPUT_FILE, index=False)
print(f"\nCleaned file saved to {OUTPUT_FILE}")
