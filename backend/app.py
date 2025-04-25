import os
import warnings
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from backend.adapter.price_fetcher.local_spot_price_fetcher import LocalSpotPriceFetcher
from utils.ReadElhubExport import read_elhub_data

STROEMSTOETTE_THRESHOLD = 0.75  # NOK/kWh


def calculate_stroemstoette(price_in_NOK_per_kWh: float) -> float:
    # Strømstøtte dekker 90 % av strømprisen over 93,75 øre/kWh (75 øre/kWh ekskl. mva.)

    if price_in_NOK_per_kWh > STROEMSTOETTE_THRESHOLD:
        price_in_NOK_per_kWh = (
            STROEMSTOETTE_THRESHOLD
            + (price_in_NOK_per_kWh - STROEMSTOETTE_THRESHOLD) * 0.1
        )
    return price_in_NOK_per_kWh


class Backend:
    def __init__(self) -> None:
        try:
            path = os.environ["PATH_TO_NORWAY_PRICES"]
        except KeyError:
            msg = "Environment variable PATH_TO_NORWAY_PRICES not set, skipping test"
            warnings.warn(msg)
            return

        self.fetcher = LocalSpotPriceFetcher(path_to_norway_data=Path(path))

    def get_spotpris_cost_per_hour(
        self,
        start: datetime,
        end: datetime,
        meter_name: str = "Trydal_1",
        price_area: str = "NO1",
    ) -> pd.Series:
        prices_in_eur = self.fetcher.get_price(
            price_area=price_area, start=start, end=end
        )

        # fra Eur/MWh til NOK/kWh
        prices = [
            (date, calculate_stroemstoette(price * 11 / 1e3))
            for (date, price) in prices_in_eur
        ]

        all_data = read_elhub_data(meter_dirs=[meter_name])

        sample_consumption_data = all_data[meter_name]

        # Calculate cost using the spot price
        return self._calculate_consumption_cost_per_hour(
            sample_consumption_data, prices, start=start, end=end
        )

    def get_fastpris_cost_per_hour(
        self,
        start: datetime,
        end: datetime,
        fastpris_in_NOK: float,
        meter_name: str = "Trydal_1",
    ) -> pd.Series:
        prices = []

        time = start
        while time <= end:
            prices.append((time, fastpris_in_NOK))
            time += timedelta(hours=1)

        all_data = read_elhub_data(meter_dirs=[meter_name])

        sample_consumption_data = all_data[meter_name]

        # Calculate cost using the spot price
        return self._calculate_consumption_cost_per_hour(
            sample_consumption_data, prices, start=start, end=end
        )

    @staticmethod
    def _calculate_consumption_cost_per_hour(
        consumption_data: pd.DataFrame,
        price_per_kwh: list[tuple[datetime, float]],
        start: datetime,
        end: datetime,
        consumption_column: str = "KWH 60 Forbruk",
        time_column: str = "Fra",
    ) -> pd.Series:
        """
        Multiply consumption values by time-based price factors to calculate cost.

        Parameters:
        -----------
        consumption_data : DataFrame
            Meter reading data containing consumption values
        price_per_kwh : list[Tuple[datetime, float]]
            list of tuples containing (timestamp, price) pairs
        consumption_column : str, optional
            Name of the column containing consumption values, default is "KWH 60 Forbruk"
        cost_column : str, optional
            Name of the column to store the calculated cost, default is "Cost"
        time_column : str, optional
            Name of the column containing timestamps, default is "Fra"

        Returns:
        --------
        Series with cost per hour
        """

        consumption: list[tuple[datetime, float]] = [
            (time, value)
            for timestamp, value in zip(
                consumption_data[time_column],
                consumption_data[consumption_column],
                strict=True,
            )
            if (time := timestamp.to_pydatetime().replace(tzinfo=ZoneInfo("UTC")))
            >= start
            and time <= end
        ]

        consumption = sorted(consumption, key=lambda value: value[0])

        consumption_series = pd.Series(dict(consumption))
        price_per_kwh_series = pd.Series(dict(price_per_kwh))

        consumption_series, price_per_kwh_series = consumption_series.align(
            price_per_kwh_series, join="inner"
        )

        return consumption_series * price_per_kwh_series
