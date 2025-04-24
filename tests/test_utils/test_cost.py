import pandas as pd
import pytest
import sys
from pathlib import Path

# Add the project root to the Python path to import the utility module
sys.path.append(str(Path(__file__).parent.parent))

from utils.CostPerHour import calculate_consumption_cost

@pytest.fixture
def sample_consumption_data():
    """Create sample consumption data for testing."""
    data = {
        'Fra': pd.to_datetime(['01.04.2025 00:00', '01.04.2025 01:00', '01.04.2025 02:00'], format='%d.%m.%Y %H:%M'),
        'Til': pd.to_datetime(['01.04.2025 01:00', '01.04.2025 02:00', '01.04.2025 03:00'], format='%d.%m.%Y %H:%M'),
        'KWH 60 Forbruk': [10.0, 5.0, 7.5],
        'Kvalitet': ['Avlest', 'Avlest', 'Avlest']
    }
    return pd.DataFrame(data)

def test_calculate_consumption_cost_basic(sample_consumption_data, capsys):
    """Test basic functionality of the cost calculation function."""
    # Test with a price of 1.2 NOK per kWh
    price = 1.2
    result = calculate_consumption_cost(sample_consumption_data, price)
    
    # Check that a new Cost column was added
    assert 'Cost' in result.columns
    
    # Check that the costs were calculated correctly
    expected_costs = [10.0 * price, 5.0 * price, 7.5 * price]
    for i, expected_cost in enumerate(expected_costs):
        assert result.iloc[i]['Cost'] == expected_cost
    
    # Check total cost is calculated correctly
    expected_total = sum(expected_costs)
    assert result['Cost'].sum() == expected_total
    
    # Check output message
    captured = capsys.readouterr()
    assert f"Total cost: {expected_total:.2f}" in captured.out
    
    # Ensure original dataframe is not modified
    assert 'Cost' not in sample_consumption_data.columns

def test_calculate_consumption_cost_custom_columns(sample_consumption_data):
    """Test cost calculation with custom column names."""
    # Create a DataFrame with a different consumption column name
    custom_df = sample_consumption_data.rename(columns={'KWH 60 Forbruk': 'Energy'})
    
    # Test with custom column names
    price = 2.5
    result = calculate_consumption_cost(
        custom_df, 
        price,
        consumption_column='Energy',
        cost_column='Price'
    )
    
    # Check that the custom column was added
    assert 'Price' in result.columns
    assert 'Cost' not in result.columns
    
    # Check that costs were calculated correctly
    expected_costs = [10.0 * price, 5.0 * price, 7.5 * price]
    for i, expected_cost in enumerate(expected_costs):
        assert result.iloc[i]['Price'] == expected_cost

def test_calculate_consumption_cost_edge_cases(sample_consumption_data):
    """Test cost calculation with edge cases."""
    # Test with zero price
    result_zero = calculate_consumption_cost(sample_consumption_data, 0.0)
    assert all(result_zero['Cost'] == 0.0)
    
    # Test with negative price (not realistic but should work mathematically)
    result_negative = calculate_consumption_cost(sample_consumption_data, -1.0)
    expected_costs = [-10.0, -5.0, -7.5]
    for i, expected_cost in enumerate(expected_costs):
        assert result_negative.iloc[i]['Cost'] == expected_cost

def test_calculate_consumption_cost_errors():
    """Test error handling in the cost calculation function."""
    # Test with invalid DataFrame (missing required column)
    invalid_df = pd.DataFrame({
        'Time': ['01:00', '02:00', '03:00'],
        'SomeOtherColumn': [1, 2, 3]
    })
    
    with pytest.raises(KeyError):
        calculate_consumption_cost(invalid_df, 1.0)