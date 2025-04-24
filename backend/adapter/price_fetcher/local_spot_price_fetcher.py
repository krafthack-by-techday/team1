from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd

from backend.ports.price_fetcher import PriceFetcher


class LocalSpotPriceFetcher(PriceFetcher):
    """Class for providing spot prices for Norway from local file."""

    def __init__(self, path_to_norway_data: Path) -> None:
        """

        Args:
            path_to_norway_data:
                Path to a folder which contains spot prices for Norway, structured as
                path_to_norway_data/
                    |-- PriceDayAheadNO1_2022_2025.csv
                    |-- PriceDayAheadNO2_2022_2025.csv
                    |-- PriceDayAheadNO3_2022_2025.csv
                    |-- PriceDayAheadNO4_2022_2025.csv
                    |-- PriceDayAheadNO5_2022_2025.csv

        """
        self.path_to_norway_data = path_to_norway_data
        if not self.path_to_norway_data.exists():
            raise ValueError(f"{path_to_norway_data=} does not exist")
        self.files = list(self.path_to_norway_data.iterdir())
        if any("PriceDayAheadNO" not in str(file) for file in self.files):
            msg = f"Unexpected content in folder: {self.files}"
            raise ValueError(msg)

    def get_price(
        self,
        price_area: str,
        start: datetime,
        end: datetime,
    ) -> list[tuple[datetime, float]]:
        if price_area not in ["NO1", "NO2", "NO3", "NO4", "NO5"]:
            raise ValueError
        file = next(
            iter(
                file for file in self.files if f"PriceDayAhead{price_area}" in str(file)
            )
        )
        content = pd.read_csv(file)

        time_price_pairs: list[tuple[datetime, float]] = [
            (time, float(value.replace(",", ".")))
            for timestamp, value in zip(
                content["timestamp"], content["value"], strict=True
            )
            if (
                time := datetime.fromisoformat(timestamp).replace(
                    tzinfo=ZoneInfo("UTC")
                )
                # TODO check API docs (???) if the times in the csv files are actually UTC
            )
            >= start
            and time <= end
        ]

        return sorted(time_price_pairs, key=lambda pair: pair[0])
