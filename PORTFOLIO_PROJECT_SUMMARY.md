# Retail Demand Forecasting

## Business Problem

Retail planning depends on reliable demand forecasts, but average forecast
accuracy does not show whether errors consistently occur in an operationally
important direction.
This project forecasts daily category demand and then examines how forecast
uncertainty changes service and inventory exposure under controlled assumptions.

## Approach

The analysis uses the M5 dataset for `FOODS`, `HOBBIES`, and `HOUSEHOLD`:

1. Prepare category-day demand data.
2. Explore trend, weekly seasonality, events, and outliers.
3. Compare baseline, statistical, and machine-learning forecasts.
4. Select models with 13 expanding validation windows.
5. Evaluate selected models once on an untouched test year.
6. Calibrate historical safety buffers from validation residuals.
7. Evaluate inventory sensitivity on test data and simulated demand paths.

## Key Findings

- Validation-selected test WAPE was 10.22% for `FOODS`, 8.78% for `HOBBIES`, and 8.31% for `HOUSEHOLD`.
- More complex models did not consistently provide more value; simpler alternatives remained competitive by category.
- Forecast-error direction differed across categories, so one buffer rule would not fit every category.
- At a hypothetical 14-day lead time, the validation-calibrated p95 buffer increased `FOODS` test fill rate from 94.30% to 99.07%, while average on-hand inventory increased from 12,256 to 38,622 units.
- Monte Carlo analysis showed that still larger buffers produced smaller average service gains, although tail-risk exposure continued to decline.

## Technical Skills

- Python, pandas, NumPy, matplotlib
- Time-aware validation and recursive forecasting
- Linear Regression, Prophet, XGBoost, and ETS
- Forecast-error analysis and controlled inventory simulation
- ACF, Ljung-Box, moving block bootstrap, Monte Carlo, and CVaR

## Limitations

The inventory extension uses hypothetical lead times, lost-sales behavior, and
order-up-to logic. M5 does not provide Walmart inventory positions, supplier
constraints, margin, carrying cost, or stockout cost. The results demonstrate
analytical tradeoffs rather than a production replenishment recommendation.

## Portfolio Story

The project moves from a clear forecasting question to a practical decision
question: after selecting a model honestly, what do its errors mean for risk?
The progression shows data preparation, validation discipline, model comparison,
and uncertainty analysis without presenting simulated inventory as observed
business performance.
