from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = (
    PROJECT_ROOT / "data" / "featured" / "credit_risk_dataset_featured.csv"
)
REPORT_PATH = PROJECT_ROOT / "outputs" / "reports" / "loan_default_eda_report.txt"


def format_rate_table(df: pd.DataFrame, column: str) -> str:
    summary = (
        df.groupby(column)["loan_status"]
        .agg(customer_count="count", default_rate="mean")
        .sort_values("default_rate", ascending=False)
    )
    summary["default_rate"] = (summary["default_rate"] * 100).round(2)
    return summary.to_string()


def format_binned_rate_table(df: pd.DataFrame, source_col: str, label: str) -> str:
    bins = pd.qcut(df[source_col], q=4, duplicates="drop")
    summary = (
        df.assign(bin=bins)
        .groupby("bin", observed=False)["loan_status"]
        .agg(customer_count="count", default_rate="mean")
    )
    summary["default_rate"] = (summary["default_rate"] * 100).round(2)
    return f"{label}\n{summary.to_string()}"


def main() -> None:
    df = pd.read_csv(DATASET_PATH)

    overall_default_rate = round(df["loan_status"].mean() * 100, 2)
    numeric_cols = [
        "person_age",
        "person_income",
        "person_emp_length",
        "loan_amnt",
        "loan_int_rate",
        "loan_percent_income",
        "cb_person_cred_hist_length",
        "loan_to_income_ratio",
        "residual_income_after_loan",
    ]
    numeric_corr = (
        df[numeric_cols + ["loan_status"]]
        .corr(numeric_only=True)["loan_status"]
        .drop("loan_status")
        .sort_values(key=lambda s: s.abs(), ascending=False)
        .round(3)
    )

    means_by_status = (
        df.groupby("loan_status")[numeric_cols]
        .mean()
        .round(2)
        .rename(index={0: "non_default", 1: "default"})
    )

    report_sections = [
        "LOAN DEFAULT EXPLORATORY DATA ANALYSIS",
        f"Dataset: {DATASET_PATH}",
        f"Shape: {df.shape}",
        f"Overall default rate: {overall_default_rate}%",
        "",
        "CORRELATION WITH LOAN DEFAULT (NUMERIC FEATURES)",
        numeric_corr.to_string(),
        "",
        "NUMERIC FEATURE MEANS BY LOAN STATUS",
        means_by_status.to_string(),
        "",
        "DEFAULT RATE BY RISK LEVEL",
        format_rate_table(df, "risk_level"),
        "",
        "DEFAULT RATE BY PRIOR DEFAULT FLAG",
        format_rate_table(df, "cb_person_default_on_file"),
        "",
        "DEFAULT RATE BY LOAN GRADE",
        format_rate_table(df, "loan_grade"),
        "",
        "DEFAULT RATE BY LOAN INTENT",
        format_rate_table(df, "loan_intent"),
        "",
        "DEFAULT RATE BY HOME OWNERSHIP",
        format_rate_table(df, "person_home_ownership"),
        "",
        "DEFAULT RATE BY EMPLOYMENT TENURE BAND",
        format_rate_table(df, "employment_tenure_band"),
        "",
        "DEFAULT RATE ACROSS NUMERIC QUARTILES",
        format_binned_rate_table(df, "loan_to_income_ratio", "loan_to_income_ratio quartiles"),
        "",
        format_binned_rate_table(df, "loan_int_rate", "loan_int_rate quartiles"),
        "",
        format_binned_rate_table(df, "person_income", "person_income quartiles"),
        "",
        format_binned_rate_table(df, "person_emp_length", "person_emp_length quartiles"),
        "",
        format_binned_rate_table(
            df, "cb_person_cred_hist_length", "cb_person_cred_hist_length quartiles"
        ),
    ]

    report_text = "\n".join(report_sections)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(report_text)
    print(f"\n\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
