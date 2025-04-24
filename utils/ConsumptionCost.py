import pandas as pd
from datetime import datetime
from typing import Union, Dict, List, Tuple

def calculate_consumption_cost_per_hour(
    consumption_data: pd.DataFrame, 
    price_per_kwh: List[Tuple[datetime, float]], 
    consumption_column: str = "KWH 60 Forbruk",
    cost_column: str = "Cost",
    time_column: str = "Fra"
) -> pd.DataFrame:
    """
    Multiply consumption values by time-based price factors to calculate cost.
    
    Parameters:
    -----------
    consumption_data : DataFrame
        Meter reading data containing consumption values
    price_per_kwh : List[Tuple[datetime, float]]
        List of tuples containing (timestamp, price) pairs
    consumption_column : str, optional
        Name of the column containing consumption values, default is "KWH 60 Forbruk"
    cost_column : str, optional
        Name of the column to store the calculated cost, default is "Cost"
    time_column : str, optional
        Name of the column containing timestamps, default is "Fra"
        
    Returns:
    --------
    DataFrame with added cost column
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = consumption_data.copy()
    
    # Create a price DataFrame from the price_per_kwh list
    price_df = pd.DataFrame(price_per_kwh, columns=['timestamp', 'price'])
    
    # Extract timezone information from price data (if available)
    timezone_info = None
    if len(price_df) > 0 and price_df['timestamp'].iloc[0].tzinfo is not None:
        timezone_info = price_df['timestamp'].iloc[0].tzinfo
        
    # Sort by timestamp
    price_df = price_df.sort_values('timestamp')
    
    # Create a cost column in the result DataFrame
    result_df[cost_column] = 0.0
    
    # Ensure consumption timestamps are datetime objects
    result_df[time_column] = pd.to_datetime(result_df[time_column])
    
    # Handle timezone consistency
    if timezone_info is not None and result_df[time_column].dt.tz is None:
        # If prices have timezone but consumption doesn't, localize consumption to the same timezone
        result_df[time_column] = result_df[time_column].dt.tz_localize('UTC')
    elif timezone_info is None and result_df[time_column].dt.tz is not None:
        # If consumption has timezone but prices don't, remove timezone from prices
        price_df['timestamp'] = price_df['timestamp'].dt.tz_localize(None)
    
    # For each consumption data point
    for idx, row in result_df.iterrows():
        consumption_time = row[time_column]
        consumption_value = row[consumption_column]
        
        # Find applicable price (the most recent price before or equal to this timestamp)
        try:
            applicable_price = price_df[price_df['timestamp'] <= consumption_time.tz_localize('UTC')]
        except KeyError:
            print(f"Except: No price found before {consumption_time}, using earliest price")
        
        if not applicable_price.empty:
            # Get the most recent price
            price = applicable_price.iloc[-1]['price']
            result_df.at[idx, cost_column] = consumption_value * price
        else:
            # If no price is found before this timestamp, use the earliest price
            if not price_df.empty:
                earliest_price = price_df.iloc[0]['price']
                result_df.at[idx, cost_column] = consumption_value * earliest_price
                print(f"Warning: No price found before {consumption_time}, using earliest price")
            else:
                print(f"Error: No price data available for {consumption_time}")
    
    # Calculate total cost
    total_cost = result_df[cost_column].sum()
    print(f"Total cost: {total_cost:.2f}")
    
    return result_df