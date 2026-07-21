# Retail Demand and POS Forecasting

A portfolio project that forecasts daily point-of-sale demand from the M5
Forecasting dataset. The work is intentionally focused on clear, reproducible,
category-level forecasting—not inventory optimization.

## Scope

The project models daily unit sales (`y`) by calendar date (`ds`) for:

- `FOODS`
- `HOBBIES`
- `HOUSEHOLD`

It covers data preparation, exploratory analysis, baseline and feature-based
forecasting, rolling validation, model comparison, and one final evaluation on
an untouched test period.

Inventory allocation, replenishment recommendations, safety-stock decisions,
and distribution optimization are outside this repository. A future, separate
allocation template may consume these forecasts, but it is not part of this
project.

## Business question

> How accurately can historical point-of-sale demand forecast future daily
> category-level unit sales?

The analysis examines trend, weekly seasonality, holidays, events, and the
relative accuracy and stability of several forecasting approaches.

## Dataset

The project uses the M5 Forecasting dataset, which provides Walmart daily sales
history, product and store hierarchy, calendar events, SNAP indicators, and
selling prices. Modeling data is aggregated to one row per category and date:

```text
ds | cat_id | y
```

## Workflow

| Notebook | Purpose |
| --- | --- |
| `00_data_preparation.ipynb` | Load and validate the joined M5 source data. |
| `01_data_exploration.ipynb` | Create category-day views and examine distributions, seasonality, and events. |
| `02_baseline_forecasting.ipynb` | Compare Naive, Seasonal Naive, 7-Day SMA, and ETS on an initial holdout. |
| `03_forecast_validation.ipynb` | Compare baselines with expanding-window, calendar-month validation. |
| `04_linear_regression.ipynb` | Evaluate recursive Linear Regression with time-series and calendar features. |
| `05_prophet.ipynb` | Evaluate Prophet with seasonality, holidays, and limited tuning. |
| `06_xgboost.ipynb` | Evaluate recursive XGBoost with the shared feature structure. |
| `07_model_comparison.ipynb` | Select the best validated model per category, refit it on train plus validation data, and evaluate it once on the untouched test set. |

## Validation approach

The data uses a strict chronological split:

```text
Train:      2011-01-29 through 2014-06-20
Validation: 2014-06-21 through 2015-06-20
Test:       2015-06-21 through 2016-06-19
```

Validation uses 13 calendar-aligned, expanding windows across 365 days. Each
model is refitted using only data available before a window and forecasts that
window without using future actuals. Models are selected by validation results,
then evaluated once on the untouched test period.

## Evaluation metrics

- MAE
- RMSE
- WAPE (%)

Models are compared on mean error and stability across validation windows.

## Current status

Data preparation, exploration, baseline forecasting, and baseline rolling
validation are complete. ETS is the leading baseline candidate across the
current category-level validation results. Linear Regression, Prophet, XGBoost,
and final model comparison remain.

## Reproducibility

Run the notebooks in numerical order. The M5 source data is stored under
`data/m5/datasets/`, and derived files are written under `data/processed/`.
Those data files are local and intentionally excluded from Git.

## Limitations

- Results are at the category level, not the SKU-store level.
- Forecasting demand does not prescribe inventory or allocation actions.
