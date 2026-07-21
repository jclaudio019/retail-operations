"""
Create shared train, validation, test, and validation-window files.

Split design
------------
Train:
    All earlier history.

Validation:
    The 365 days immediately before the test period.
    Used for monthly rolling validation and model selection.

Test:
    The final 365 days.
    Kept untouched until final model evaluation.
"""

from pathlib import Path

import pandas as pd


INPUT_PATH = Path(
    "data/processed/category_daily_raw.parquet"
)

OUTPUT_DIR = Path(
    "data/processed"
)

VALIDATION_DAYS = 365
TEST_DAYS = 365


def split_data(
    data,
    validation_days=365,
    test_days=365,
    date_col="ds"
):
    """
    Create chronological train, validation, and test datasets.
    """
    dates = (
        pd.Series(
            pd.to_datetime(
                data[date_col].dropna().unique()
            )
        )
        .sort_values()
        .reset_index(drop=True)
    )

    required_days = validation_days + test_days

    if len(dates) <= required_days:
        raise ValueError(
            "Not enough dates for the requested "
            "validation and test periods."
        )

    test_start = dates.iloc[-test_days]

    validation_start = dates.iloc[
        -(validation_days + test_days)
    ]

    validation_end = dates.iloc[
        -test_days - 1
    ]

    train_data = data[
        data[date_col] < validation_start
    ].copy()

    validation_data = data[
        data[date_col].between(
            validation_start,
            validation_end
        )
    ].copy()

    test_data = data[
        data[date_col] >= test_start
    ].copy()

    return (
        train_data,
        validation_data,
        test_data
    )


def create_validation_windows(
    validation_data,
    date_col="ds"
):
    """
    Divide the validation period into monthly forecast windows.

    The model will be refitted before each window.
    """
    validation_start = validation_data[
        date_col
    ].min()

    validation_end = validation_data[
        date_col
    ].max()

    month_starts = pd.date_range(
        start=validation_start,
        end=validation_end,
        freq="MS"
    )

    boundaries = (
        [validation_start]
        + [
            date
            for date in month_starts
            if date > validation_start
        ]
        + [
            validation_end
            + pd.Timedelta(days=1)
        ]
    )

    windows = []

    for window_number in range(
        len(boundaries) - 1
    ):
        window_start = boundaries[
            window_number
        ]

        window_end = (
            boundaries[window_number + 1]
            - pd.Timedelta(days=1)
        )

        windows.append({
            "window": window_number + 1,
            "train_end": (
                window_start
                - pd.Timedelta(days=1)
            ),
            "validation_start": window_start,
            "validation_end": window_end,
            "forecast_days": (
                window_end - window_start
            ).days + 1
        })

    return pd.DataFrame(windows)


def main():
    category_daily = pd.read_parquet(
        INPUT_PATH
    )

    category_daily["ds"] = pd.to_datetime(
        category_daily["ds"]
    )

    category_daily = (
        category_daily
        .sort_values(["cat_id", "ds"])
        .reset_index(drop=True)
    )

    (
        train_data,
        validation_data,
        test_data
    ) = split_data(
        data=category_daily,
        validation_days=VALIDATION_DAYS,
        test_days=TEST_DAYS
    )

    validation_windows = (
        create_validation_windows(
            validation_data=validation_data
        )
    )

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    train_data.to_parquet(
        OUTPUT_DIR / "train_data.parquet",
        index=False
    )

    validation_data.to_parquet(
        OUTPUT_DIR / "validation_data.parquet",
        index=False
    )

    test_data.to_parquet(
        OUTPUT_DIR / "test_data.parquet",
        index=False
    )

    validation_windows.to_parquet(
        OUTPUT_DIR / "validation_windows.parquet",
        index=False
    )

    print(
        "Train:",
        train_data["ds"].min().date(),
        "to",
        train_data["ds"].max().date()
    )

    print(
        "Validation:",
        validation_data["ds"].min().date(),
        "to",
        validation_data["ds"].max().date()
    )

    print(
        "Test:",
        test_data["ds"].min().date(),
        "to",
        test_data["ds"].max().date()
    )

    print(
        "Validation days:",
        validation_data["ds"].nunique()
    )

    print(
        "Test days:",
        test_data["ds"].nunique()
    )

    print(
        "Monthly validation windows:",
        len(validation_windows)
    )


if __name__ == "__main__":
    main()