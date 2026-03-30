from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_PATH = (
    PROJECT_ROOT / "data" / "featured" / "credit_risk_dataset_featured.csv"
)
OUTPUT_PATH = PROJECT_ROOT / "outputs" / "plots" / "dashboard.png"


def main() -> None:
    sns.set_theme(style="whitegrid")
    df = pd.read_csv(DATASET_PATH)
    sample_df = df.sample(min(len(df), 5000), random_state=42)

    fig, axes = plt.subplots(1, 3, figsize=(20, 6))
    fig.suptitle("Credit Risk Dashboard", fontsize=18, fontweight="bold")

    ax1 = axes[0]
    sns.countplot(
        data=df,
        x="loan_status",
        hue="loan_status",
        palette="Set2",
        legend=False,
        ax=ax1,
    )
    ax1.set_title("Default vs Non-Default")
    ax1.set_xlabel("Loan Status")
    ax1.set_ylabel("Customer Count")
    ax1.set_xticks([0, 1], ["Non-Default", "Default"])
    for container in ax1.containers:
        ax1.bar_label(container, fmt="%d", padding=3)

    ax2 = axes[1]
    sns.scatterplot(
        data=sample_df,
        x="person_income",
        y="loan_amnt",
        hue="loan_status",
        palette={0: "#4C72B0", 1: "#DD8452"},
        alpha=0.65,
        s=40,
        ax=ax2,
    )
    ax2.set_title("Income vs Loan Amount")
    ax2.set_xlabel("Person Income")
    ax2.set_ylabel("Loan Amount")
    handles, _ = ax2.get_legend_handles_labels()
    ax2.legend(handles, ["Non-Default", "Default"], title="Loan Status")

    ax3 = axes[2]
    sns.countplot(
        data=df,
        x="risk_level",
        order=["LOW", "MEDIUM", "HIGH"],
        hue="risk_level",
        palette=["#55A868", "#E5C07B", "#C44E52"],
        legend=False,
        ax=ax3,
    )
    ax3.set_title("Risk Segmentation")
    ax3.set_xlabel("Risk Level")
    ax3.set_ylabel("Customer Count")
    for container in ax3.containers:
        ax3.bar_label(container, fmt="%d", padding=3)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_PATH, dpi=300, bbox_inches="tight")
    plt.close()

    print(f"Dashboard saved to: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
