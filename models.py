"""
Reusable baseline forecasting models.

Each function accepts:
    train: pandas Series containing historical demand
    horizon: number of future periods to forecast

Each function returns:
    NumPy array containing the forecasts
"""

import numpy as np
from statsmodels.tsa.holtwinters import ExponentialSmoothing


def naive_forecast(train, horizon):
    """
    Forecast every future period using the most recent observed value.
    """
    if len(train) == 0:
        raise ValueError("Training data cannot be empty.")

    last_value = float(train.iloc[-1])

    return np.repeat(last_value, horizon)


def seasonal_naive_forecast(train, horizon, season_length=7):
    """
    Forecast by repeating the most recent seasonal cycle.

    For daily data with weekly seasonality, season_length=7.
    """
    if len(train) < season_length:
        raise ValueError(
            "Training data is shorter than the seasonal period."
        )

    seasonal_pattern = (
        train
        .iloc[-season_length:]
        .astype(float)
        .to_numpy()
    )

    return np.resize(seasonal_pattern, horizon)


def sma_forecast(train, horizon, window=7):
    """
    Produce a recursive Simple Moving Average forecast.

    Each prediction is added to the history and used when calculating
    later predictions in the forecast horizon.
    """
    if len(train) < window:
        raise ValueError(
            "Training data is shorter than the moving-average window."
        )

    history = train.astype(float).tolist()
    forecasts = []

    for _ in range(horizon):
        prediction = np.mean(history[-window:])
        forecasts.append(prediction)
        history.append(prediction)

    return np.asarray(forecasts)


def ets_forecast(
    train,
    horizon,
    seasonal_periods=7,
    trend="add",
    damped_trend=True,
    seasonal="add"
):
    """
    Fit an ETS model and forecast future demand.

    Default specification:
        - Additive trend
        - Damped trend
        - Additive weekly seasonality
    """
    minimum_observations = seasonal_periods * 2

    if len(train) < minimum_observations:
        raise ValueError(
            "ETS requires at least two complete seasonal cycles."
        )

    model = ExponentialSmoothing(
        train.astype(float),
        trend=trend,
        damped_trend=damped_trend if trend is not None else False,
        seasonal=seasonal,
        seasonal_periods=(
            seasonal_periods if seasonal is not None else None
        ),
        initialization_method="estimated"
    )

    fitted_model = model.fit(optimized=True)

    forecasts = fitted_model.forecast(horizon)

    # Demand forecasts cannot be negative
    return np.clip(
        np.asarray(forecasts),
        a_min=0,
        a_max=None
    )


MODEL_FUNCTIONS = {
    "Naive": naive_forecast,
    "Seasonal Naive": seasonal_naive_forecast,
    "7-Day SMA": sma_forecast,
    "ETS": ets_forecast
}