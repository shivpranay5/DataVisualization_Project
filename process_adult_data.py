from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path


COLUMN_NAMES = [
    "age",
    "workclass",
    "fnlwgt",
    "education",
    "education_num",
    "marital_status",
    "occupation",
    "relationship",
    "race",
    "sex",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
    "native_country",
    "income",
]

NUMERIC_COLUMNS = {
    "age",
    "education_num",
    "capital_gain",
    "capital_loss",
    "hours_per_week",
}

DROP_COLUMNS = {"fnlwgt"}


def clean_value(column: str, value: str) -> str | int | None:
    trimmed = value.strip()

    if trimmed == "?":
        return None

    if column == "income":
        return trimmed.replace(".", "")

    if column in NUMERIC_COLUMNS:
        return int(trimmed)

    return trimmed


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    raw_path = base_dir / "adult.data.txt"
    output_dir = base_dir / "outputs"
    output_dir.mkdir(exist_ok=True)

    cleaned_path = output_dir / "adult_cleaned.csv"
    filtered_path = output_dir / "adult_cleaned_no_missing.csv"
    summary_path = output_dir / "cleaning_summary.json"

    kept_columns = [column for column in COLUMN_NAMES if column not in DROP_COLUMNS]

    row_count = 0
    rows_with_missing = 0
    missing_by_column = Counter()
    income_distribution = Counter()

    complete_row_count = 0

    with raw_path.open("r", encoding="utf-8", newline="") as infile, cleaned_path.open(
        "w", encoding="utf-8", newline=""
    ) as outfile, filtered_path.open("w", encoding="utf-8", newline="") as filtered_file:
        reader = csv.reader(infile, skipinitialspace=False)
        writer = csv.DictWriter(outfile, fieldnames=kept_columns)
        filtered_writer = csv.DictWriter(filtered_file, fieldnames=kept_columns)
        writer.writeheader()
        filtered_writer.writeheader()

        for raw_row in reader:
            if not raw_row or all(not value.strip() for value in raw_row):
                continue

            row_count += 1
            parsed_row = {
                column: clean_value(column, value)
                for column, value in zip(COLUMN_NAMES, raw_row)
            }

            row_has_missing = False
            for column, value in parsed_row.items():
                if value is None:
                    missing_by_column[column] += 1
                    row_has_missing = True

            if row_has_missing:
                rows_with_missing += 1

            income_distribution[str(parsed_row["income"])] += 1

            cleaned_row = {
                column: parsed_row[column] for column in kept_columns
            }
            writer.writerow(cleaned_row)

            if not row_has_missing:
                filtered_writer.writerow(cleaned_row)
                complete_row_count += 1

    summary = {
        "source_file": str(raw_path),
        "cleaned_file": str(cleaned_path),
        "cleaned_no_missing_file": str(filtered_path),
        "rows_processed": row_count,
        "columns_kept": kept_columns,
        "dropped_columns": sorted(DROP_COLUMNS),
        "rows_with_missing_values": rows_with_missing,
        "rows_without_missing_values": complete_row_count,
        "missing_by_column": dict(sorted(missing_by_column.items())),
        "income_distribution": dict(sorted(income_distribution.items())),
    }

    with summary_path.open("w", encoding="utf-8") as summary_file:
        json.dump(summary, summary_file, indent=2)

    print(f"Processed rows: {row_count}")
    print(f"Cleaned dataset written to: {cleaned_path}")
    print(f"Analysis-ready dataset written to: {filtered_path}")
    print(f"Cleaning summary written to: {summary_path}")
    print(f"Rows with missing values: {rows_with_missing}")
    print(f"Rows without missing values: {complete_row_count}")
    print("Missing values by column:")
    for column, count in sorted(missing_by_column.items()):
        print(f"  - {column}: {count}")


if __name__ == "__main__":
    main()
