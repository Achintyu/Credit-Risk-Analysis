from pathlib import Path

import numpy as np
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLEAN_DATASET_PATH = (
    PROJECT_ROOT / "data" / "cleaned" / "credit_risk_dataset_cleaned.csv"
)
FEATURED_DATASET_PATH = (
    PROJECT_ROOT / "data" / "featured" / "credit_risk_dataset_featured.csv"
)


def assign_risk_level(row: pd.Series) -> str:
    """Build a simple rule-based risk score and convert it into a label."""
    score = 0

    if row["cb_person_default_on_file"] == "Y":
        score += 2
    if row["loan_to_income_ratio"] > 0.35:
        score += 2
    if row["loan_int_rate"] > 15:
        score += 1
    if row["person_emp_length"] < 2:
        score += 1
    if row["cb_person_cred_hist_length"] < 3:
        score += 1
    if row["loan_grade"] in {"E", "F", "G"}:
        score += 1

    if score >= 4:
        return "HIGH"
    if score >= 2:
        return "MEDIUM"
    return "LOW"


def main() -> None:
    df = pd.read_csv(CLEAN_DATASET_PATH)

    # Keep the ratio explicit even though loan_percent_income already exists.
    df["loan_to_income_ratio"] = (df["loan_amnt"] / df["person_income"]).round(4)

    # A simple affordability view: money left after taking the loan amount.
    df["residual_income_after_loan"] = df["person_income"] - df["loan_amnt"]

    # Normalize employment length into coarse experience bands for easier grouping.
    df["employment_tenure_band"] = pd.cut(
        df["person_emp_length"],
        bins=[-np.inf, 2, 5, 10, np.inf],
        labels=["NEW", "EARLY", "MID", "LONG"],
        right=False,
    ).astype("string")

    df["risk_level"] = df.apply(assign_risk_level, axis=1)

    df.to_csv(FEATURED_DATASET_PATH, index=False)

    print(f"Input shape: {df.shape}")
    print("\nNew columns added:")
    print("loan_to_income_ratio")
    print("residual_income_after_loan")
    print("employment_tenure_band")
    print("risk_level")
    print("\nRisk level distribution:")
    print(df["risk_level"].value_counts().to_string())
    print(f"\nFeatured dataset saved to: {FEATURED_DATASET_PATH}")


if __name__ == "__main__":
    main()
