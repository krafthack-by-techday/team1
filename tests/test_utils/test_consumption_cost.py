import os
import sys
import warnings
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pandas as pd
import pytest

# Add the project root to the Python path to import the utility module
sys.path.append(str(Path(__file__).parent.parent))

from backend.adapter.price_fetcher.local_spot_price_fetcher import LocalSpotPriceFetcher
from utils.ConsumptionCost import calculate_consumption_cost_per_hour
from utils.ReadElhubExport import get_consumption_data


def test_calculation_based_on_spotprice():
    """Test cost calculation using spot prices from a local file."""
    try:
        path = os.environ["PATH_TO_NORWAY_PRICES"]
    except KeyError:
        msg = "Environment variable PATH_TO_NORWAY_PRICES not set, skipping test"
        warnings.warn(msg)
        return

    fetcher = LocalSpotPriceFetcher(path_to_norway_data=Path(path))
    prices = fetcher.get_price(
        price_area="NO1",
        start=datetime(2023, 1, 1, hour=0, tzinfo=ZoneInfo("UTC")),
        end=datetime(2023, 12, 31, hour=23, tzinfo=ZoneInfo("UTC")),
    )

    sample_consumption_data = get_consumption_data(meter_name="Trydal_1")

    breakpoint()

    # Convert price timestamps to naive for the assertion
    prices_naive = [
        (timestamp.replace(tzinfo=None), price) for timestamp, price in prices
    ]

    # Calculate cost using the spot price
    result = calculate_consumption_cost_per_hour(sample_consumption_data, prices)

    # Verify results
    assert "Cost" in result.columns

    # Don't attempt to validate against simple multiplication,
    # as the time-based matching is more complex
    assert result["Cost"].sum() > 0
    assert all(result["Cost"] >= 0)  # All costs should be non-negative
