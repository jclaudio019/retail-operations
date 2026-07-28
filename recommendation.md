# Website Recommendations — Retail Demand and POS Forecasting

This document gives Fable the evidence-based content and visual direction for the portfolio project page. It reflects the completed notebooks and saved outputs. The project is **demand/POS forecasting only**; it does not implement allocation, replenishment, safety-stock, or order-recommendation decisions.

## 1. Recommended portfolio project title

Options:

1. **Retail Demand Forecasting: Comparing Statistical and Machine-Learning Models**
2. **Daily POS Demand Forecasting Across Retail Categories**
3. **Retail Sales Forecasting with Rolling Validation and Model Comparison**
4. **Category-Level Retail Demand Forecasting: From Baselines to XGBoost**
5. **Forecasting Daily Retail Demand with Statistical and ML Models**

**Recommended title:** **Retail Demand Forecasting: Comparing Statistical and Machine-Learning Models**

It is clear to a hiring manager, accurately reflects the work, and does not imply inventory optimization was built.

## 2. One-sentence project summary

Forecasted daily POS unit sales for `FOODS`, `HOBBIES`, and `HOUSEHOLD` using leakage-safe rolling validation to compare baseline, statistical, and machine-learning models before a final untouched test-year evaluation.

## 3. Portfolio card description

Built a retail demand forecasting project using daily POS sales across three product categories. Compared Naive, ETS, Linear Regression, Prophet, and XGBoost with expanding monthly validation, then evaluated frozen model setups on an untouched 365-day test period. The project showed that the most complex model was not consistently the most useful across categories.

## 4. Full project overview

This project investigated how accurately daily point-of-sale demand could be forecast for the `FOODS`, `HOBBIES`, and `HOUSEHOLD` categories in the M5 retail dataset. The work progressed from data preparation and exploratory analysis to transparent forecasting baselines, expanding monthly validation, and feature-based and specialized time-series models.

The goal was not simply to find the most advanced algorithm. It was to identify the model that offered the best balance of accuracy, stability, interpretability, and practical effort for each category. Naive, Seasonal Naive, 7-Day SMA, and ETS established the baseline. Linear Regression added lag, rolling, trend, calendar, and Christmas features. Prophet tested trend, weekly/yearly seasonality, and holiday handling. XGBoost tested non-linear relationships in the same time-series features.

All model configuration choices were made with 13 expanding monthly validation windows. The final 365-day test period was held back until the final comparison.

## 5. Business context

Daily demand forecasting gives retail teams a more reliable signal than simply using recent averages. It can help teams understand expected sales patterns, anticipate weekly and annual seasonality, recognize calendar exceptions, and provide an input to labor, replenishment, or inventory-planning processes.

This project creates the **forecasting layer only**. It estimates future category demand; it does not prescribe how inventory should be allocated, replenished, or ordered. Those downstream decisions would require inventory, supply, assortment, capacity, and service-level information that is outside this repository.

## 6. Core business questions

- How accurately can daily category-level POS sales be forecast from historical sales?
- How important are weekly seasonal patterns and calendar effects?
- Does a more advanced model consistently outperform a well-specified baseline?
- Does the strongest approach differ across `FOODS`, `HOBBIES`, and `HOUSEHOLD`?
- How stable is performance across different monthly validation windows?
- How should the recurring December 25 sales disruption be treated?
- Do validation results remain useful on a fully untouched test year?
- Is any additional accuracy large enough to justify the added modelling effort?

## 7. Data and modelling scope

| Item | Scope |
|---|---|
| Frequency | Daily |
| Target | Category-level POS unit sales (`y`) |
| Categories | `FOODS`, `HOBBIES`, `HOUSEHOLD` |
| Train period | 2011-01-29 to 2014-06-20 |
| Validation period | 2014-06-21 to 2015-06-20 |
| Validation design | 13 calendar-aligned, expanding monthly windows across 365 days |
| Test period | 2015-06-21 to 2016-06-19, 365 untouched days |
| Metrics | MAE, RMSE, and WAPE; lower is better |

Chronological validation was essential because a forecasting model must only use information available at the time of prediction. A random train-test split would mix future and past observations and create an unrealistic experiment. Every model used the same category aggregation, validation dates, forecast horizons, actual values, and metric functions.

## 8. Models evaluated

| Family | Models | Business-friendly explanation |
|---|---|---|
| Baselines | Naive, Seasonal Naive, 7-Day SMA, ETS | Simple reference points: last value, last week's pattern, a rolling average, and a model of level/trend/weekly seasonality. |
| Interpretable regression | Linear Regression | Uses recent sales, rolling averages, trend, calendar, and Christmas features to make a transparent daily forecast. |
| Specialized time series | Prophet | Separates trend and seasonality, with weekly/yearly patterns and Christmas as a known holiday. |
| Machine learning | XGBoost | Learns non-linear relationships among lag, rolling, calendar, trend, and holiday features. |

Complexity was treated as a trade-off, not a goal. Linear Regression used permutation importance to test a reduced feature set. Prophet and XGBoost each used four small, understandable configurations rather than an exhaustive parameter search.

## 9. Main technical challenges

### A. Multiple seasonal patterns

The data contains a strong weekly sales cycle, category-specific changes across the year, and calendar effects. `FOODS`, `HOBBIES`, and `HOUSEHOLD` do not behave identically, so one seasonal profile could not be assumed to fit every category.

### B. Trend and changing demand levels

Sales levels changed through time, especially for `HOUSEHOLD`. A fixed historical average would not respond to recent demand or longer-term movement. The models therefore needed both recent lags and broader trend/seasonality information.

### C. December 25 anomaly

Christmas Day repeatedly showed zero or near-zero sales, consistent with store closures. The original data was retained for modelling. A December-25-excluded view was created only as an EDA diagnostic; Linear Regression and XGBoost used a Christmas indicator, while Prophet used Christmas as a holiday. This avoided treating the event as an ordinary low-sales day.

### D. Preventing time-series leakage

Lag and rolling features used only prior observations. Regression and XGBoost forecasts were recursive: each new forecast was added to the history used for the next day, rather than using actual values from the same future horizon. The test year remained untouched until notebook 07.

### E. Fair model comparison

Each model was evaluated against the same monthly windows. This required repeated refitting, category-specific forecasts, and consistent MAE/RMSE/WAPE calculations. The comparison therefore reflects a realistic forecasting process rather than a single convenient holdout.

### F. Advanced models did not automatically win

The strongest lesson is that more flexible models were not universally superior. ETS remained competitive, XGBoost led validation for `FOODS`, Linear Regression led validation for `HOBBIES`, and Prophet led validation for `HOUSEHOLD`. The observed test rankings differed in two categories, demonstrating real uncertainty rather than a single universal winner.

## 10. Model development journey

1. Prepared and validated the joined M5 sales, calendar, price, and item data.
2. Explored category demand, weekly patterns, trend, and the December 25 disruption.
3. Established transparent Naive, Seasonal Naive, SMA, and ETS benchmarks.
4. Used expanding monthly validation to select ETS as the strongest baseline.
5. Added Linear Regression with leakage-safe lag, rolling, calendar, trend, and Christmas features; then compared full and reduced versions.
6. Tested Prophet for trend, weekly/yearly seasonality, and holiday effects.
7. Tested XGBoost for non-linear relationships in the same feature structure.
8. Refit the selected configuration from each model family on all pre-test history.
9. Evaluated the frozen candidates once on the untouched test year.

The project intentionally moved from simple to complex. This made every additional layer of modelling justify itself against a credible baseline.

## 11. Final results

Validation selected one candidate per category before test evaluation. The final test comparison reported all pre-specified models; it did not retune settings or retroactively change the validation-selection rule.

| Category | Validation-selected model | Validation WAPE | Test WAPE | Test MAE | Test RMSE |
|---|---|---:|---:|---:|---:|
| FOODS | XGBoost Faster | 6.99% | 10.22% | 2,722.43 | 3,536.01 |
| HOBBIES | Linear Regression (Full) | 6.50% | 8.78% | 346.31 | 443.15 |
| HOUSEHOLD | Prophet Flexible | 6.88% | 8.31% | 812.54 | 984.08 |

Lowest observed test WAPE by category:

| Category | Model | Test WAPE | Naive test WAPE | Improvement versus Naive |
|---|---|---:|---:|---:|
| FOODS | XGBoost Faster | 10.22% | 16.10% | 5.88 WAPE points |
| HOBBIES | XGBoost Shallow | 8.00% | 17.47% | 9.47 WAPE points |
| HOUSEHOLD | Linear Regression (Full) | 7.05% | 19.88% | 12.83 WAPE points |

No single model won every category. `HOUSEHOLD` was easiest to forecast by best observed test WAPE; `FOODS` was hardest. Validation and test rankings were consistent for `FOODS`, but differed for `HOBBIES` and `HOUSEHOLD`. This is why the page should distinguish **validation selection** from the **final fixed test comparison**.

## 12. Key findings

1. Weekly demand patterns were strong enough to make seasonal baselines materially better than a simple last-value forecast.
2. December 25 was a recurring, operationally meaningful disruption and needed explicit treatment.
3. ETS was a strong and credible baseline across the categories.
4. Model performance depended on category behavior; there was no universal winner.
5. XGBoost delivered the lowest observed test WAPE for `FOODS`, but only narrowly beat ETS.
6. For `HOBBIES`, XGBoost, Prophet, and ETS were almost tied on test error; complexity offered little clear business value.
7. For `HOUSEHOLD`, Linear Regression had the lowest observed test WAPE, showing that an interpretable medium-effort model can outperform more complex alternatives.

## 13. Business interpretation

The results support using category-specific forecasting rather than assuming one model fits all demand patterns. Stable weekly patterns can support dependable short-horizon planning, while higher-error categories may need more review or larger planning buffers. Holiday exceptions should be represented explicitly instead of relying on a model to infer them as ordinary demand variation.

Forecast accuracy is not the only decision criterion. If a simpler model is nearly as accurate as a complex one, the simpler option may be preferable because it is easier to explain, maintain, and monitor. The project does not recommend inventory quantities or allocation actions; it provides a more reliable demand signal for a future planning layer.

## 14. What made the project difficult

The hardest part was not fitting individual models. It was designing a comparison that stayed realistic and fair. That meant building leakage-safe lag and rolling features, forecasting recursively when future demand was unknown, refitting models across 13 monthly windows, and holding the final test year aside until the end.

The December 25 pattern also required judgement: it was a repeatable operational disruption, not simply random low demand. The final lesson was equally important: increasing model complexity did not guarantee a better forecast. The work required translating model scores into a defensible business conclusion rather than presenting the most complex model as automatically best.

## 15. Limitations

- Category-level aggregation is useful for a strategic view but hides SKU-level intermittency, lifecycle changes, promotions, assortment changes, and store-level variation.
- The models do not use price, promotion depth, markdowns, stockouts, inventory availability, local weather, local events, store attributes, or competitor activity as predictive inputs.
- Observed POS sales may be lower than unconstrained demand when an item is unavailable. Without availability or lost-sales data, the project forecasts observed sales rather than true unconstrained demand.
- Recursive multi-day forecasts can accumulate error because later lags and rolling values depend on earlier predictions.
- There are few observations for any individual annual holiday, so holiday effects are inherently difficult to estimate with high certainty.
- The M5 data is a historical dataset; the findings should be re-evaluated before transfer to another retailer or time period.

## 16. What I would do with more time

1. **Move to SKU-level forecasting.** Address intermittent demand, lifecycle effects, cold starts, and much larger computational scale with methods such as Croston-style approaches, grouped/global models, and item clustering.
2. **Add store-category or store-SKU views.** Test regional and store-level demand differences.
3. **Add explanatory and operational features.** Include price, promotions, stockouts, availability, store attributes, weather, local events, and lifecycle data where available.
4. **Explore hierarchical forecasting.** Keep forecasts coherent across total, category, store, and item levels.
5. **Add uncertainty and monitoring.** Track prediction intervals, error by horizon, drift, holiday performance, and model degradation over time.

## 17. SKU-level forecasting and assortment limitations

Moving to SKU-store forecasting requires an assortment or ranging file. It would identify which items were authorized in each store, when an item entered or exited the assortment, and whether a zero sale means no demand, no stock, or that the item was not carried.

Without that information, item-store zeros are ambiguous. A model could mistake an unavailable or non-ranged product for a low-demand product. This distinction becomes critical at SKU and store-SKU granularity.

## 18. Downstream allocation context

A future downstream project could use these forecasts as an input to store-level inventory planning. That decision layer would need forecast demand, current inventory, incoming supply, assortment eligibility, store capacity, pack sizes, service-level targets, product priorities, and transfer constraints.

None of that allocation or replenishment logic is implemented here. It is deliberately outside the scope of this forecasting project.

## 19. Skills demonstrated

- Python and pandas
- Data preparation and validation
- Exploratory time-series analysis and visualization
- Statistical forecasting and Holt-Winters ETS
- Time-series feature engineering
- Linear Regression, Prophet, and XGBoost
- Recursive multi-step forecasting
- Expanding-window chronological validation
- Leakage prevention
- Hyperparameter comparison and feature importance
- MAE, RMSE, and WAPE evaluation
- Reproducible notebooks and saved modelling artifacts
- Business interpretation and technical communication

## 20. Recommended website sections

| Section | Purpose and approximate length | Best evidence | Placement |
|---|---|---|---|
| Hero | Title, one-sentence summary, tools; 30–50 words. | One key metric: 3 categories, 365-day test. | Above fold |
| Business problem | Explain why POS demand matters; 90–130 words. | No chart needed. | Above fold |
| Final outcome | State that winners differed by category; 80–120 words. | Compact best-test-results table. | Above fold |
| Demand patterns | Show weekly pattern and December 25 exception; 100–140 words. | Day-of-week chart plus small Christmas callout. | Middle |
| Method | Explain chronological split and rolling validation; 120–160 words. | Simple timeline/flow diagram. | Middle |
| Models compared | Explain model families; 100–150 words. | Small model/effort table. | Middle |
| Final test comparison | Show all final scores and complexity trade-off; 100–140 words. | Interactive WAPE chart. | Middle |
| Forecast examples | Make the work tangible. | Actual-versus-forecast chart with category selector. | Middle |
| Findings and limitations | Demonstrate judgement; 140–200 words. | Short bullets, no chart required. | Below fold |
| Future work and skills | Close with scope-aware next steps. | Skills chips and repository/notebook links. | Below fold |

## 21. Recommended visuals

Use **four core visuals**. Do not turn the page into a copy of the notebooks.

| Visual | Business question answered | Evidence source | Reuse guidance | Recommended caption |
|---|---|---|---|---|
| Final test WAPE by model and category | Which approach was most accurate, and how much did it improve on Naive? | `07_model_comparison.ipynb`; `data/processed/final_test_report.parquet` | Rebuild as a Plotly horizontal bar chart with a category filter. Keep only final test WAPE and effort labels. | “Forecast accuracy varied by category; no single model won everywhere.” |
| Actual versus forecast, test period | Did the selected model follow the demand pattern over the full unseen year? | `07_model_comparison.ipynb`; `data/processed/final_test_forecasts.parquet` | Rebuild as Plotly lines with a category selector. Show actual as solid and forecast as dashed. | “Validation-selected models remained useful on unseen demand, though test error increased.” |
| Weekly demand seasonality | Why were weekly baselines and seasonality features necessary? | `01_data_exploration.ipynb` weekday/seasonality charts | Simplify to one grouped weekday bar chart for all categories. | “Demand generally rises into the weekend across all three categories.” |
| Complexity versus value | Was added modelling effort justified? | `07_model_comparison.ipynb`; final test report | Build a simple slope or dumbbell chart: Naive → ETS → lowest observed test model. | “Additional complexity helped selectively, not universally.” |

Optional only if page length allows:

| Visual | Evidence source | Guidance |
|---|---|---|
| December 25 anomaly | `01_data_exploration.ipynb`, raw versus normalized diagnostic views | Use a small annotated trend callout, not a full second EDA section. State that the original data was retained. |
| Validation stability by month | `03_forecast_validation.ipynb`, WAPE across validation windows | Use only when explaining leakage-safe rolling validation. Simplify to selected candidates, not every configuration. |

Skip histograms, QQ plots, individual tuning charts, and all feature-importance charts on the main website page. They are useful notebook evidence but not the strongest portfolio narrative.

## 22. Suggested portfolio narrative

Retail demand is difficult to forecast because sales change by day of week, category, season, and holiday. I began by exploring daily POS patterns across `FOODS`, `HOBBIES`, and `HOUSEHOLD`, where weekly seasonality and the December 25 disruption were especially visible.

I then built a realistic forecasting experiment rather than jumping directly to a complex model. Transparent baselines established the value of weekly seasonality. ETS added level, trend, and weekly patterns; Linear Regression used lagged, rolling, calendar, and holiday features; Prophet tested trend and holiday structure; and XGBoost tested non-linear relationships.

All choices were made through expanding monthly validation windows that prevented future information from leaking into a forecast. The final test year showed that the best approach differed by category. XGBoost was strongest for `FOODS`, while simpler or medium-complexity approaches remained highly competitive elsewhere. The main lesson was not that one algorithm always wins, but that a defensible forecasting process makes model trade-offs visible.

## 23. Suggested interview talking points

1. I used chronological expanding-window validation because random splitting would leak future demand patterns into training.
2. I started with Naive, Seasonal Naive, SMA, and ETS so advanced models had to beat meaningful benchmarks.
3. Lag and rolling features were shifted to use only prior observations.
4. Linear Regression and XGBoost forecast recursively because future actual sales are unknown inside a multi-day horizon.
5. December 25 was retained in the original data but represented explicitly as a known calendar/holiday effect.
6. ETS was a strong baseline because weekly seasonality was so important at category level.
7. I used permutation importance to compare full and reduced Linear Regression features.
8. Model selection was based on validation; the final test year was held back until notebook 07.
9. The observed test ranking differed from validation in two categories, which demonstrates why a separate test period matters.
10. Category-level forecasting is more stable than SKU-store forecasting, but it cannot explain store, assortment, or item-level variation.
11. I would not build allocation decisions from these forecasts alone; a downstream project would need inventory, supply, assortment, and service-level constraints.

## 24. Ready-to-use copy

### A. Portfolio card

Forecasted daily retail POS demand across three product categories using expanding-window validation to compare baseline, statistical, and machine-learning models. Tested Naive, ETS, Linear Regression, Prophet, and XGBoost, then evaluated frozen candidates on an untouched 365-day test period. The project showed that forecasting accuracy and the value of model complexity varied by category.

### B. Project-page introduction

How accurately can historical POS sales forecast future daily retail demand? I explored this question using the M5 dataset across `FOODS`, `HOBBIES`, and `HOUSEHOLD`. The project moved from data preparation and exploratory analysis to transparent forecasting baselines, leakage-safe monthly rolling validation, and a comparison of Linear Regression, Prophet, and XGBoost. The goal was not simply to choose the most advanced model, but to identify which approach offered the best balance of accuracy, stability, interpretability, and practical effort for each category. Final results were evaluated once on an untouched 365-day test period.

### C. Business problem

Retail teams need a dependable view of expected demand before they can plan downstream activities such as labor, replenishment inputs, or inventory reviews. Recent averages alone can miss recurring weekly patterns, longer-term changes in demand, and calendar disruptions. This project focuses on the forecasting layer: estimating future daily category demand from historical POS sales. It does not prescribe allocation or replenishment actions, but it produces a more defensible demand signal that a future operational planning process could use.

### D. Technical challenge

The central challenge was building a fair forecasting experiment. Time-series models cannot use future information, so the validation design had to remain chronological. Lag and rolling features were shifted to use only past sales, and regression/tree forecasts were generated recursively because future actual demand is unavailable inside the forecast horizon. I also had to account for weekly seasonality, changing sales levels, category-specific behavior, and the recurring December 25 sales disruption. Every model was repeatedly refitted across the same 13 expanding monthly windows, allowing the comparison to measure both average error and stability rather than relying on one convenient holdout period.

### E. Key results

Every advanced model improved on the Naive benchmark during the untouched test year, but no single model won across all categories.

| Category | Best observed test model | Test WAPE |
|---|---|---:|
| FOODS | XGBoost Faster | 10.22% |
| HOBBIES | XGBoost Shallow | 8.00% |
| HOUSEHOLD | Linear Regression (Full) | 7.05% |

XGBoost was strongest for `FOODS`, but ETS was close with less complexity. For `HOBBIES`, XGBoost, Prophet, and ETS were nearly tied. For `HOUSEHOLD`, Linear Regression outperformed the more complex alternatives. The practical conclusion is that model complexity should earn its place category by category.

### F. Lessons learned

The most important lesson was that a realistic evaluation framework matters as much as the algorithm. Weekly seasonality made simple models materially stronger than a last-value forecast, while the December 25 disruption required explicit treatment. More complex models did not consistently deliver better forecasts: XGBoost added value for `FOODS`, but simpler or more interpretable approaches were competitive or better for the other categories. Holding back an untouched test year also showed that validation rankings can change when models face genuinely unseen demand.

### G. Limitations and next steps

This analysis forecasts daily demand at category level, which is useful for a strategic view but hides SKU, store, price, promotion, assortment, and availability effects. It forecasts observed POS sales rather than unconstrained consumer demand because stockout and lost-sales data are unavailable. The next analytical step would be to test whether these category-level patterns hold at SKU and store level, using assortment eligibility, inventory availability, prices, promotions, lifecycle information, and local context. A separate downstream inventory-planning project could then combine forecasts with supply, inventory, capacity, and service-level constraints.

### H. Resume bullet options

- Built a retail POS demand forecasting project across three product categories, comparing ETS, Linear Regression, Prophet, and XGBoost with expanding-window validation and a 365-day untouched test evaluation.
- Designed leakage-safe recursive forecasting workflows with lag, rolling, calendar, trend, and holiday features; evaluated models using MAE, RMSE, and WAPE.
- Demonstrated category-specific model trade-offs: XGBoost led observed test accuracy for `FOODS`, while Linear Regression was strongest for `HOUSEHOLD`.
- Developed an evidence-based model-comparison framework showing that added ML complexity did not consistently outperform simpler statistical or interpretable models.

### I. LinkedIn project description

Built a retail demand forecasting project using daily POS sales from the M5 dataset across `FOODS`, `HOBBIES`, and `HOUSEHOLD`. I started with Naive, Seasonal Naive, SMA, and ETS baselines, then compared Linear Regression, Prophet, and XGBoost using 13 expanding monthly validation windows. To avoid time-series leakage, lag and rolling features used only prior demand and multi-day regression/tree forecasts were recursive. Final candidates were evaluated once on an untouched 365-day test period. The project showed that no single model won across every category and that extra model complexity was only selectively worthwhile.

## Handoff to Fable

Use this file as the content source for the project detail page. Keep the page evidence-led and visual, not notebook-like. Lead with the business problem and final outcome, use the four core visuals above, and preserve the distinction between validation-selected candidates and the final fixed test comparison.
