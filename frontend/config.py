from typing import Literal, List, Any
import datetime

from pydantic import BaseModel


class Config(BaseModel):
    metering_point_id: str
    compare_based_on: Literal["History", "Forecast"]
    assumed_fixed_price: float
    time_window: List[Any]
    select_user: str

    @property
    def input_is_set(self) -> bool:
        return self.compare_based_on != ""
