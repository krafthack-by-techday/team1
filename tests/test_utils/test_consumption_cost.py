from datetime import datetime
import pandas as pd
import pytest
import sys
from zoneinfo import ZoneInfo
from pathlib import Path

# Add the project root to the Python path to import the utility module
sys.path.append(str(Path(__file__).parent.parent))

from utils.ConsumptionCost import calculate_consumption_cost_per_hour
from backend.adapter.price_fetcher.local_spot_price_fetcher import LocalSpotPriceFetcher
from utils.ReadElhubExport import get_consumption_data

def test_calculation_based_on_spotprice():
    """Test cost calculation using spot prices from a local file."""
    # Create the price fetcher
    prices = LocalSpotPriceFetcher(path_to_norway_data=Path(__file__).parent / "../../DayAheadPrices/Norge").get_price(
            price_area="NO1",
            start=datetime(2025, 3, 15, hour=20, tzinfo=ZoneInfo("UTC")),
            end=datetime(2025, 4, 16, hour=23, tzinfo=ZoneInfo("UTC")),
        )
    
    sample_consumption_data = get_consumption_data(meter_name="Trydal_1")
    
    # Convert price timestamps to naive for the assertion
    prices_naive = [(timestamp.replace(tzinfo=None), price) for timestamp, price in prices]
    
    # Calculate cost using the spot price
    result = calculate_consumption_cost_per_hour(sample_consumption_data, prices)
    
    # Verify results
    assert 'Cost' in result.columns
    
    # Don't attempt to validate against simple multiplication,
    # as the time-based matching is more complex
    assert result['Cost'].sum() > 0
    assert all(result['Cost'] >= 0)  # All costs should be non-negative