"""
Reusable forecast evaluation metrics.

This module provides helpers for calculating MAE, RMSE, and WAPE
for baseline and validation forecasts.
"""

import numpy as np
import pandas as pd


def calculate_validation_metrics(actual, forecast):
    """
    Calculate forecast metrics from actual and forecast arrays.

    Parameters
    ----------
    actual : array-like
        Observed demand values.

    forecast : array-like
        Forecasted demand values.

    Returns
    -------
    dict
        MAE, RMSE, and WAPE percentage.
    """
    actual = np.asarray(actual, dtype=float)
    forecast = np.asarray(forecast, dtype=float)

    if actual.shape != forecast.shape:
        raise ValueError(
            "Actual and forecast values must have the same shape."
        )

    valid = np.isfinite(actual) & np.isfinite(forecast)
    actual = actual[valid]
    forecast = forecast[valid]

    if len(actual) == 0:
        return {
            "MAE": np.nan,
            "RMSE": np.nan,
            "WAPE (%)": np.nan
        }

    errors = actual - forecast

    mae = np.mean(np.abs(errors))
    rmse = np.sqrt(np.mean(errors ** 2))

    total_actual = np.abs(actual).sum()

    wape = (
        np.abs(errors).sum() / total_actual * 100
        if total_actual != 0
        else np.nan
    )

    return {
        "MAE": mae,
        "RMSE": rmse,
        "WAPE (%)": wape
    }


def calculate_forecast_metrics(
    group,
    forecast_col,
    actual_col="y"
):
    """
    Calculate forecast metrics from columns in a DataFrame group.

    This helper is useful with pandas groupby operations.

    Parameters
    ----------
    group : pandas DataFrame
        Data containing actual and forecast values.

    forecast_col : str
        Name of the forecast column.

    actual_col : str, default="y"
        Name of the actual-value column.

    Returns
    -------
    pandas Series
        MAE, RMSE, and WAPE percentage.
    """
    if actual_col not in group.columns:
        raise KeyError(
            f"Actual column '{actual_col}' was not found."
        )

    if forecast_col not in group.columns:
        raise KeyError(
            f"Forecast column '{forecast_col}' was not found."
        )

    metrics = calculate_validation_metrics(
        actual=group[actual_col],
        forecast=group[forecast_col]
    )

    return pd.Series(metrics)