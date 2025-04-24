from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from backend.adapter.price_fetcher.local_spot_price_fetcher import (
    LocalSpotPriceFetcher,
)


class TestLocalSpotPriceFetcher:
    def test_get_price(self) -> None:
        prices = LocalSpotPriceFetcher(
            path_to_norway_data=Path(__file__).parent / "testfiles"
        ).get_price(
            price_area="NO1",
            start=datetime(2025, 4, 16, hour=20, tzinfo=ZoneInfo("UTC")),
            end=datetime(2025, 4, 16, hour=21, tzinfo=ZoneInfo("UTC")),
        )

        assert prices == [
            (datetime(2025, 4, 16, hour=20, tzinfo=ZoneInfo("UTC")), 12.34),
            (datetime(2025, 4, 16, hour=21, tzinfo=ZoneInfo("UTC")), 42.00),
        ]
