import pandas as pd
from typing import Union, Dict

def calculate_consumption_cost(
    consumption_data: pd.DataFrame, 
    price_per_kwh: float, 
    consumption_column: str = "KWH 60 Forbruk",
    cost_column: str = "Cost"
) -> Union[pd.DataFrame, Dict[str, pd.DataFrame]]:
    """
    Multiply consumption values by a fixed price factor to calculate cost.
    
    Parameters:
    -----------
    consumption_data : DataFrame
        Meter reading data containing consumption values
    price_per_kwh : float
        Price per kWh in the desired currency
    consumption_column : str, optional
        Name of the column containing consumption values, default is "KWH 60 Forbruk"
    cost_column : str, optional
        Name of the column to store the calculated cost, default is "Cost"
        
    Returns:
    --------
    DataFrame with added cost column
    """
    # Handle both single DataFrame and dictionary of DataFrames
    # Create a copy to avoid modifying the original DataFrame
    result_df = consumption_data.copy()
    
    # Calculate cost and add it as a new column
    result_df[cost_column] = result_df[consumption_column] * price_per_kwh
    
    # Calculate total cost
    total_cost = result_df[cost_column].sum()
    print(f"Total cost: {total_cost:.2f}")
    
    return result_df