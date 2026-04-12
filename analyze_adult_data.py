from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path

import pandas as pd

MPL_DIR = Path(tempfile.gettempdir()) / "dv_project_mpl"
MPL_DIR.mkdir(parents=True, exist_ok=True)
os.environ["MPLCONFIGDIR"] = str(MPL_DIR)

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import seaborn as sns
from pandas.plotting import parallel_coordinates
from statsmodels.graphics.mosaicplot import mosaic


BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
FIGURES_DIR = OUTPUT_DIR / "figures"
DATA_PATH = OUTPUT_DIR / "adult_cleaned_no_missing.csv"


def ensure_directories() -> None:
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)


def load_data() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["income_binary"] = (df["income"] == ">50K").astype(int)
    return df


def save_summary(df: pd.DataFrame) -> Path:
    summary = {
        "row_count": int(len(df)),
        "column_count": int(df.shape[1] - 1),  # exclude helper column
        "income_distribution": {
            key: int(value) for key, value in df["income"].value_counts().sort_index().items()
        },
        "numeric_summary": df[
            ["age", "education_num", "capital_gain", "capital_loss", "hours_per_week"]
        ]
        .describe()
        .round(2)
        .to_dict(),
        "top_categories": {
            column: {
                key: int(value)
                for key, value in df[column].value_counts().head(10).items()
            }
            for column in ["workclass", "education", "marital_status", "occupation", "race", "sex"]
        },
    }

    summary_path = OUTPUT_DIR / "eda_summary.json"
    with summary_path.open("w", encoding="utf-8") as file:
        json.dump(summary, file, indent=2)
    return summary_path


def style_plots() -> None:
    sns.set_theme(style="whitegrid", palette="deep")
    plt.rcParams["figure.figsize"] = (10, 6)
    plt.rcParams["axes.titlesize"] = 14
    plt.rcParams["axes.labelsize"] = 11


def save_education_chart(df: pd.DataFrame) -> Path:
    education_order = (
        df.groupby("education")["education_num"].mean().sort_values().index.tolist()
    )
    education_share = (
        df.groupby("education", observed=False)["income_binary"]
        .mean()
        .reindex(education_order)
        .mul(100)
    )

    fig, ax = plt.subplots()
    education_share.plot(kind="bar", color="#2a9d8f", ax=ax)
    ax.set_title("Share of Individuals Earning >50K by Education")
    ax.set_xlabel("Education")
    ax.set_ylabel("Percent earning >50K")
    ax.tick_params(axis="x", rotation=45, labelsize=9)
    fig.tight_layout()

    path = FIGURES_DIR / "education_vs_income.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def save_gender_chart(df: pd.DataFrame) -> Path:
    top_statuses = df["marital_status"].value_counts().head(5).index.tolist()
    subset = df[df["marital_status"].isin(top_statuses)].copy()

    fig, ax = plt.subplots(figsize=(11, 7))
    mosaic(
        subset,
        ["marital_status", "sex", "income"],
        ax=ax,
        title="Mosaic Plot of Marital Status, Gender, and Income",
        gap=0.02,
    )
    ax.set_xlabel("Marital Status / Gender / Income")
    fig.tight_layout()

    path = FIGURES_DIR / "gender_marital_status_income_mosaic.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def save_race_chart(df: pd.DataFrame) -> Path:
    race_order = df["race"].value_counts().index.tolist()

    fig, ax = plt.subplots(figsize=(10, 6.5))
    sns.boxplot(
        data=df,
        x="race",
        y="age",
        hue="income",
        order=race_order,
        ax=ax,
    )
    ax.set_title("Age Distribution by Race and Income")
    ax.set_xlabel("Race")
    ax.set_ylabel("Age")
    ax.tick_params(axis="x", rotation=20)
    fig.tight_layout()

    path = FIGURES_DIR / "race_age_income_boxplot.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def save_occupation_chart(df: pd.DataFrame) -> Path:
    top_occupations = df["occupation"].value_counts().head(10).index
    subset = df[df["occupation"].isin(top_occupations)].copy()
    occupation_hours = (
        subset.groupby(["occupation", "income"], observed=False)["hours_per_week"]
        .mean()
        .reset_index()
    )
    occupation_order = (
        subset.groupby("occupation", observed=False)["income_binary"]
        .mean()
        .sort_values(ascending=False)
        .index
        .tolist()
    )

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.violinplot(
        data=subset,
        x="hours_per_week",
        y="occupation",
        hue="income",
        order=occupation_order,
        cut=0,
        inner="quartile",
        ax=ax,
    )
    ax.set_title("Hours Worked by Occupation and Income")
    ax.set_xlabel("Hours per Week")
    ax.set_ylabel("Occupation")
    fig.tight_layout()

    path = FIGURES_DIR / "occupation_hours_income_violin.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def save_workclass_chart(df: pd.DataFrame) -> Path:
    top_workclasses = [
        value for value in df["workclass"].value_counts().index.tolist() if value != "Without-pay"
    ][:6]
    subset = df[df["workclass"].isin(top_workclasses)].copy()
    share = (
        subset.groupby(["occupation", "workclass"], observed=False)["income_binary"]
        .mean()
        .reset_index()
    )
    share = share.sort_values("income_binary", ascending=False).head(18).copy()
    share["income_share_pct"] = share["income_binary"] * 100
    share = share.sort_values("income_share_pct", ascending=True)

    fig, ax = plt.subplots(figsize=(10, 7))
    sns.scatterplot(
        data=share,
        x="income_share_pct",
        y="occupation",
        hue="workclass",
        s=110,
        ax=ax,
    )
    for _, row in share.iterrows():
        ax.hlines(
            y=row["occupation"],
            xmin=0,
            xmax=row["income_share_pct"],
            color="#cfd8dc",
            linewidth=1.5,
            zorder=0,
        )
    ax.set_title("Top Occupation-Workclass Combinations by Share Earning >50K")
    ax.set_xlabel("Percent earning >50K")
    ax.set_ylabel("Occupation")
    fig.tight_layout()

    path = FIGURES_DIR / "occupation_workclass_income_dotplot.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def save_multi_variable_chart(df: pd.DataFrame) -> Path:
    sample_parts = []
    for _, group in df.groupby("income", observed=False):
        sample_parts.append(group.sample(min(len(group), 400), random_state=42))
    sample = pd.concat(sample_parts, ignore_index=True).copy()

    features = ["age", "education_num", "hours_per_week", "capital_gain"]
    scaled = sample[features].copy()
    for column in features:
        col_min = scaled[column].min()
        col_max = scaled[column].max()
        if col_max == col_min:
            scaled[column] = 0
        else:
            scaled[column] = (scaled[column] - col_min) / (col_max - col_min)
    scaled["income"] = sample["income"].values

    fig, ax = plt.subplots(figsize=(11, 7))
    parallel_coordinates(
        scaled,
        class_column="income",
        cols=features,
        color=["#4c78a8", "#e45756"],
        alpha=0.15,
        ax=ax,
    )
    ax.set_title("Parallel Coordinates Plot for Income-Related Factors")
    ax.set_xlabel("Variables")
    ax.set_ylabel("Scaled Value")
    fig.tight_layout()

    path = FIGURES_DIR / "parallel_coordinates_income_factors.png"
    fig.savefig(path, dpi=200)
    plt.close(fig)
    return path


def print_key_findings(df: pd.DataFrame) -> None:
    print("\nEDA summary")
    print(f"Rows analyzed: {len(df)}")
    print("\nIncome distribution:")
    for label, count in df["income"].value_counts().sort_index().items():
        percentage = (count / len(df)) * 100
        print(f"  - {label}: {count} ({percentage:.2f}%)")

    print("\nAverage values by income:")
    grouped = (
        df.groupby("income", observed=False)[
            ["age", "education_num", "capital_gain", "capital_loss", "hours_per_week"]
        ]
        .mean()
        .round(2)
    )
    print(grouped.to_string())

    print("\nTop 5 occupations:")
    for occupation, count in df["occupation"].value_counts().head(5).items():
        print(f"  - {occupation}: {count}")


def main() -> None:
    ensure_directories()
    style_plots()
    df = load_data()

    summary_path = save_summary(df)
    figure_paths = [
        save_education_chart(df),
        save_gender_chart(df),
        save_race_chart(df),
        save_occupation_chart(df),
        save_workclass_chart(df),
        save_multi_variable_chart(df),
    ]

    print_key_findings(df)
    print(f"\nSaved EDA summary to: {summary_path}")
    print("Saved figures:")
    for path in figure_paths:
        print(f"  - {path}")


if __name__ == "__main__":
    main()
