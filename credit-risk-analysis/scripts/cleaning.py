from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RAW_PATH = PROJECT_ROOT / "data" / "raw" / "credit_risk_dataset.csv"
CLEAN_PATH = PROJECT_ROOT / "data" / "cleaned" / "credit_risk_dataset_cleaned.csv"


def standardize_column_name(name: str) -> str:
    """Normalize names to lowercase snake_case."""
    return (
        name.strip()
        .lower()
        .replace("%", "percent")
        .replace("/", "_")
        .replace(" ", "_")
    )


def clean_credit_risk_dataset() -> None:
    df = pd.read_csv(RAW_PATH)

    original_rows = len(df)
    duplicate_rows = int(df.duplicated().sum())

    # Standardize column names even though the source file already uses snake_case.
    df.columns = [standardize_column_name(col) for col in df.columns]

    # Normalize text columns to a consistent uppercase format with trimmed whitespace.
    text_columns = df.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        df[column] = df[column].astype("string").str.strip().str.upper()

    # Remove exact duplicate rows.
    df = df.drop_duplicates().copy()

    missing_before = df.isna().sum()

    # Impute missing numeric values with the median to preserve row count and reduce
    # sensitivity to skew/outliers in financial variables.
    numeric_columns = df.select_dtypes(include=["number"]).columns
    for column in numeric_columns:
        if df[column].isna().any():
            df[column] = df[column].fillna(df[column].median())

    missing_after = df.isna().sum()

    df.to_csv(CLEAN_PATH, index=False)

    print(f"Raw shape: ({original_rows}, {len(df.columns)})")
    print(f"Removed duplicate rows: {duplicate_rows}")
    print(f"Cleaned shape: {df.shape}")
    print("\nMissing values before cleaning:")
    print(missing_before[missing_before > 0].to_string())
    print("\nMissing values after cleaning:")
    remaining_missing = missing_after[missing_after > 0]
    if remaining_missing.empty:
        print("None")
    else:
        print(remaining_missing.to_string())
    print(f"\nCleaned file saved to: {CLEAN_PATH}")


if __name__ == "__main__":
    clean_credit_risk_dataset()
