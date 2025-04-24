from datetime import datetime

from backend.ports.price_fetcher import PriceFetcher


class EEXMarketPriceFetcher(PriceFetcher):
    """Class for providing EEX market prices for Norway."""

    def get_price(
        self,
        price_area: str,
        start: datetime,
        end: datetime,
    ) -> list[tuple[datetime, float]]:
        raise NotImplementedError
