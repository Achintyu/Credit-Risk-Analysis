from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = (
    PROJECT_ROOT / "data" / "featured" / "credit_risk_dataset_featured.csv"
)
PLOTS_DIR = PROJECT_ROOT / "outputs" / "plots"


def plot_default_distribution(df: pd.DataFrame) -> Path:
    output_path = PLOTS_DIR / "default_vs_non_default.png"

    plt.figure(figsize=(8, 5))
    ax = sns.countplot(data=df, x="loan_status", hue="loan_status", palette="Set2", legend=False)
    ax.set_title("Default vs Non-Default Distribution")
    ax.set_xlabel("Loan Status")
    ax.set_ylabel("Customer Count")
    ax.set_xticks([0, 1], ["Non-Default", "Default"])

    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    return output_path


def plot_income_vs_loan(df: pd.DataFrame) -> Path:
    output_path = PLOTS_DIR / "income_vs_loan.png"

    sample_df = df.sample(min(len(df), 5000), random_state=42)

    plt.figure(figsize=(9, 6))
    sns.scatterplot(
        data=sample_df,
        x="person_income",
        y="loan_amnt",
        hue="loan_status",
        palette={0: "#4C72B0", 1: "#DD8452"},
        alpha=0.65,
        s=45,
    )
    plt.title("Income vs Loan Amount")
    plt.xlabel("Person Income")
    plt.ylabel("Loan Amount")
    plt.legend(title="Loan Status", labels=["Non-Default", "Default"])
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    return output_path


def plot_risk_segmentation(df: pd.DataFrame) -> Path:
    output_path = PLOTS_DIR / "risk_segmentation.png"

    risk_order = ["LOW", "MEDIUM", "HIGH"]
    plt.figure(figsize=(8, 5))
    ax = sns.countplot(
        data=df,
        x="risk_level",
        order=risk_order,
        hue="risk_level",
        palette=["#55A868", "#E5C07B", "#C44E52"],
        legend=False,
    )
    ax.set_title("Customer Risk Segmentation")
    ax.set_xlabel("Risk Level")
    ax.set_ylabel("Customer Count")

    for container in ax.containers:
        ax.bar_label(container, fmt="%d", padding=3)

    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    plt.close()
    return output_path


def main() -> None:
    PLOTS_DIR.mkdir(exist_ok=True)
    sns.set_theme(style="whitegrid")

    df = pd.read_csv(DATASET_PATH)

    plot_paths = [
        plot_default_distribution(df),
        plot_income_vs_loan(df),
        plot_risk_segmentation(df),
    ]

    print("Generated plots:")
    for path in plot_paths:
        print(path)


if __name__ == "__main__":
    main()
