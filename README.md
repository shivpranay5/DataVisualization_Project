# DV Project

This project uses the Adult Census Income dataset for the CSE 578 data visualization project - ASU

## Current setup

- `adult.data.txt`: raw dataset
- `adult.names.txt`: dataset description
- `process_adult_data.py`: cleaning pipeline for the raw dataset
- `outputs/`: generated cleaned data and cleaning summaries

## How to run

```bash
python3 process_adult_data.py
python3 analyze_adult_data.py
```

## What the script does

- assigns column names to the raw Adult dataset
- trims whitespace from categorical values
- converts `?` to missing values
- normalizes the `income` labels
- drops `fnlwgt` based on the course guidance
- writes a cleaned CSV and a JSON summary

## Analysis outputs

`analyze_adult_data.py` reads the cleaned no-missing dataset and creates:

- `outputs/eda_summary.json`
- `outputs/figures/education_vs_income.png`
- `outputs/figures/gender_marital_status_income_mosaic.png`
- `outputs/figures/race_age_income_boxplot.png`
- `outputs/figures/occupation_hours_income_violin.png`
- `outputs/figures/occupation_workclass_income_dotplot.png`
- `outputs/figures/parallel_coordinates_income_factors.png`
