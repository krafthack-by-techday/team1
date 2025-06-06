from datetime import datetime
from zoneinfo import ZoneInfo

from backend.app import Backend


def test_calculation_based_on_spotprice():
    """Test cost calculation using spot prices from a local file."""

    app = Backend()

    # Calculate cost using the spot price
    result = app.get_spotpris_cost_per_hour(
        start=datetime(2023, 1, 1, hour=0, tzinfo=ZoneInfo("UTC")),
        end=datetime(2023, 12, 31, hour=23, tzinfo=ZoneInfo("UTC")),
    )

    assert len(result) > 360 * 24


def test_get_fastpris_cost_per_hour():
    """Test cost calculation using fast price prices from a local file."""

    app = Backend()

    # Calculate cost using the spot price
    result = app.get_fastpris_cost_per_hour(
        fastpris_in_NOK=10,
        start=datetime(2023, 1, 1, hour=0, tzinfo=ZoneInfo("UTC")),
        end=datetime(2023, 12, 31, hour=23, tzinfo=ZoneInfo("UTC")),
    )

    assert len(result) > 360 * 24
