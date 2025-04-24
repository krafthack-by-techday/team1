import abc
from abc import ABC
from datetime import datetime


class PriceFetcher(ABC):
    @abc.abstractmethod
    def get_price(
        self,
        price_area: str,
        start: datetime,
        end: datetime,
    ) -> list[tuple[datetime, float]]:
        raise NotImplementedError
