# Final Report — Retail Demand and POS Forecasting

## Executive summary

This project tested whether historical point-of-sale demand can forecast daily category-level unit sales for `FOODS`, `HOBBIES`, and `HOUSEHOLD`.

The answer is yes. Every advanced model improved on the Naive benchmark during the untouched 365-day test period. The best observed test WAPE by category was:

| Category | Best observed test model | Test WAPE | Improvement versus Naive |
|---|---|---:|---:|
| FOODS | XGBoost Faster | 10.22% | 5.88 percentage points |
| HOBBIES | XGBoost Shallow | 8.00% | 9.47 percentage points |
| HOUSEHOLD | Linear Regression (Full) | 7.05% | 12.83 percentage points |

The results also show that more complex models are not automatically more valuable. XGBoost produced the lowest observed error for `FOODS`, but ETS was close with less complexity. For `HOBBIES`, XGBoost, Prophet, and ETS were almost tied. For `HOUSEHOLD`, Linear Regression performed best on the test period.

## Business questions answered

### Can historical POS demand forecast future category demand accurately?

Yes. The Naive model produced test WAPE values of 16.10% for `FOODS`, 17.47% for `HOBBIES`, and 19.88% for `HOUSEHOLD`. Every advanced approach reduced those errors. Historical demand therefore provides a useful basis for daily category-level forecasting.

### What demand patterns matter?

- Weekly seasonality is clear across all categories, with stronger demand from Friday through Sunday.
- Christmas Day demand falls to zero or near zero, consistent with store closures. It was retained in the data and treated as a known calendar effect.
- `FOODS` is relatively stable, `HOBBIES` is more variable, and `HOUSEHOLD` shows the clearest upward movement over time.
- These patterns justify weekly seasonal baselines, calendar features, lag features, rolling averages, and holiday-aware models.

### Do more advanced models improve on simple baselines?

Yes, but the value depends on the category. ETS was the strongest baseline during rolling validation. Linear Regression, Prophet, and XGBoost were then tested using the same 13 expanding monthly validation windows before final test evaluation.

### Is the extra modelling effort worth it?

| Category | Practical assessment |
|---|---|
| FOODS | Conditionally. XGBoost had the lowest observed test WAPE, but ETS was only 0.47 WAPE points higher. Use XGBoost when that marginal accuracy gain justifies additional maintenance; otherwise ETS is a credible simpler option. |
| HOBBIES | Not clearly. XGBoost was lowest, but Prophet and ETS were within 0.12 WAPE points. The small gain alone does not justify a much more complex workflow. |
| HOUSEHOLD | No. Linear Regression outperformed both Prophet and XGBoost on the test period, so the more complex alternatives did not provide enough value. |

## Method

The M5 Forecasting dataset was aggregated to one daily observation per category:

```text
ds | cat_id | y
```

The chronological split was fixed before model comparison:

| Period | Dates |
|---|---|
| Train | 2011-01-29 to 2014-06-20 |
| Validation | 2014-06-21 to 2015-06-20 |
| Test | 2015-06-21 to 2016-06-19 |

Validation used 13 calendar-aligned, expanding windows. Every model was refitted using only the history available before a window. The test set was held out until the final notebook.

Model families evaluated:

- Baselines: Naive, Seasonal Naive, 7-Day SMA, and ETS.
- Linear Regression: lag, rolling, trend, calendar, and Christmas features; both full and reduced versions were tested using permutation importance.
- Prophet: weekly and yearly seasonality, Christmas as a holiday, and four understandable trend/seasonality settings.
- XGBoost: the shared lag, rolling, calendar, trend, and holiday feature set with four small parameter configurations.

WAPE is the primary business-facing metric because it expresses absolute error relative to total demand. Lower is better. MAE and RMSE were also calculated in the notebooks.

## Final test results

The table below includes every model evaluated in the final fixed test comparison. These scores are reported transparently, but they were not used to tune any settings after the test was opened.

| Category | Model | Test WAPE | Effort |
|---|---|---:|---|
| FOODS | XGBoost Faster | 10.22% | High |
| FOODS | ETS | 10.69% | Medium |
| FOODS | Linear Regression (Reduced) | 11.06% | Medium |
| FOODS | Prophet Additive | 13.16% | Medium |
| FOODS | 7-Day SMA | 14.17% | Low |
| FOODS | Seasonal Naive | 14.61% | Low |
| FOODS | Naive | 16.10% | Low |
| HOBBIES | XGBoost Shallow | 8.00% | High |
| HOBBIES | Prophet Flexible | 8.04% | Medium |
| HOBBIES | ETS | 8.12% | Medium |
| HOBBIES | Linear Regression (Full) | 8.78% | Medium |
| HOBBIES | Seasonal Naive | 9.38% | Low |
| HOBBIES | 7-Day SMA | 11.60% | Low |
| HOBBIES | Naive | 17.47% | Low |
| HOUSEHOLD | Linear Regression (Full) | 7.05% | Medium |
| HOUSEHOLD | XGBoost Shallow | 7.53% | High |
| HOUSEHOLD | Prophet Flexible | 8.31% | Medium |
| HOUSEHOLD | ETS | 8.44% | Medium |
| HOUSEHOLD | Seasonal Naive | 9.17% | Low |
| HOUSEHOLD | 7-Day SMA | 14.45% | Low |
| HOUSEHOLD | Naive | 19.88% | Low |

## Validation selection versus test performance

The validation winners were frozen before test evaluation. Their test errors were higher than validation errors, which is normal for a new out-of-sample period and reinforces why validation and test data must remain separate.

| Category | Validation-selected model | Validation WAPE | Test WAPE |
|---|---|---:|---:|
| FOODS | XGBoost Faster | 6.99% | 10.22% |
| HOBBIES | Linear Regression (Full) | 6.50% | 8.78% |
| HOUSEHOLD | Prophet Flexible | 6.88% | 8.31% |

The lowest observed test model differs from the validation-selected model for `HOBBIES` and `HOUSEHOLD`. This is an important finding, not a reason to tune again on the test period. Before changing the validated choice for a live use case, these alternatives should be assessed on a new future holdout period.

## What each model contributed

| Model | What it added | Main limitation |
|---|---|---|
| Naive | A simple minimum benchmark. | Ignores weekly patterns, trend, and calendar effects. |
| Seasonal Naive | Repeats the previous week's day-of-week pattern. | Repeats unusual weeks directly. |
| 7-Day SMA | A smooth, easy-to-explain demand estimate. | Smooths away important day-of-week variation. |
| ETS | Level, damped trend, and weekly seasonality with moderate effort. | Does not use explicit calendar or lag features. |
| Linear Regression | Clear feature effects and an interpretable reduced-feature option. | Assumes linear relationships; recursive forecasts can compound error. |
| Prophet | Trend, weekly/yearly seasonality, holidays, and uncertainty intervals. | Its additional structure did not consistently improve category-level accuracy. |
| XGBoost | Non-linear relationships among lag, rolling, and calendar features. | Higher complexity and lower interpretability; marginal gains were category-specific. |

## Limitations

- Forecasts are at the daily category level, not at SKU-store level.
- The analysis does not model price, promotions, product substitutions, stockouts, or inventory availability as predictive inputs.
- Recursive multi-day forecasts use earlier predictions to construct later lag and rolling features, so errors can accumulate.
- The test period is one historical year. Demand changes should be monitored and models should be re-evaluated on future data.
- This project forecasts demand only. Allocation, replenishment, safety stock, and order recommendations are intentionally out of scope.

## Assumptions

- Daily sales can be summed across all items and stores within each category to create a meaningful category-level demand target.
- Future calendar dates, day of week, month, and Christmas are known when a forecast is made.
- The 13 expanding validation windows are representative enough to choose model configurations before the final test period.
- Demand cannot be negative, so negative model predictions were clipped to zero.
- The four small Prophet and XGBoost configuration sets are sufficient for a portfolio comparison; this is not an exhaustive hyperparameter search.
- Final test scores are a fixed report of the pre-specified models. They are not used to tune model settings or retroactively change the validation selection rule.

## Recommended next step

Use these forecasts as an input to a separate, smaller allocation or replenishment project. That follow-on work should define its own service-level targets, lead times, inventory constraints, and decision rules rather than adding allocation logic to this forecasting project.

## Notebook map

| Notebook | Contribution |
|---|---|
| `00_data_preparation.ipynb` | Joined and validated the M5 analytical data. |
| `01_data_exploration.ipynb` | Identified category behavior, weekly patterns, and calendar effects. |
| `02_baseline_forecasting.ipynb` | Established initial benchmark performance. |
| `03_forecast_validation.ipynb` | Performed expanding-window baseline validation. |
| `04_linear_regression.ipynb` | Tested interpretable feature-based forecasting and feature reduction. |
| `05_prophet_model.ipynb` | Tested holiday-aware trend and seasonality forecasting. |
| `06_xgboost_model.ipynb` | Tested non-linear feature-based forecasting. |
| `07_model_comparison.ipynb` | Performed the final untouched test evaluation. |
