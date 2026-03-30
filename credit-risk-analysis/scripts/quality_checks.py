from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = PROJECT_ROOT / "data" / "raw" / "credit_risk_dataset.csv"
REPORT_PATH = (
    PROJECT_ROOT / "outputs" / "reports" / "credit_risk_quality_report.txt"
)


def build_missing_value_report(df: pd.DataFrame) -> pd.DataFrame:
    total_rows = len(df)
    missing_counts = df.isna().sum()
    missing_percent = (missing_counts / total_rows * 100).round(2)
    report = pd.DataFrame(
        {
            "missing_count": missing_counts,
            "missing_percentage": missing_percent,
        }
    )
    return report.sort_values(["missing_percentage", "missing_count"], ascending=False)


def build_duplicate_report(df: pd.DataFrame) -> dict[str, int]:
    duplicate_rows = int(df.duplicated().sum())
    duplicate_percentage = round((duplicate_rows / len(df)) * 100, 2)
    return {
        "duplicate_rows": duplicate_rows,
        "duplicate_percentage": duplicate_percentage,
    }


def build_outlier_report(df: pd.DataFrame) -> pd.DataFrame:
    numeric_df = df.select_dtypes(include=["number"])
    rows = []

    for column in numeric_df.columns:
        series = numeric_df[column].dropna()

        if series.empty:
            rows.append(
                {
                    "column": column,
                    "lower_bound": None,
                    "upper_bound": None,
                    "outlier_count": 0,
                    "outlier_percentage": 0.0,
                }
            )
            continue

        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_mask = (series < lower_bound) | (series > upper_bound)
        outlier_count = int(outlier_mask.sum())
        outlier_percentage = round((outlier_count / len(series)) * 100, 2)

        rows.append(
            {
                "column": column,
                "lower_bound": round(float(lower_bound), 4),
                "upper_bound": round(float(upper_bound), 4),
                "outlier_count": outlier_count,
                "outlier_percentage": outlier_percentage,
            }
        )

    return pd.DataFrame(rows).sort_values(
        ["outlier_percentage", "outlier_count"], ascending=False
    )


def main() -> None:
    df = pd.read_csv(DATASET_PATH)

    missing_report = build_missing_value_report(df)
    duplicate_report = build_duplicate_report(df)
    outlier_report = build_outlier_report(df)

    report_lines = [
        "CREDIT RISK DATA QUALITY REPORT",
        f"Dataset: {DATASET_PATH}",
        f"Shape: {df.shape}",
        "",
        "MISSING VALUE REPORT",
        missing_report.to_string(),
        "",
        "DUPLICATE REPORT",
        f"duplicate_rows: {duplicate_report['duplicate_rows']}",
        f"duplicate_percentage: {duplicate_report['duplicate_percentage']}%",
        "",
        "OUTLIER REPORT (IQR METHOD)",
        outlier_report.to_string(index=False),
    ]

    report_text = "\n".join(report_lines)
    REPORT_PATH.write_text(report_text, encoding="utf-8")
    print(report_text)
    print(f"\nReport saved to: {REPORT_PATH}")


if __name__ == "__main__":
    main()
