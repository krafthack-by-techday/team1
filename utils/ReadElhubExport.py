import glob
import os
from pathlib import Path

import pandas as pd


def read_elhub_data(base_path=None, meter_dirs=None) -> dict[str, pd.DataFrame]:
    """
    Read all CSV files from specified meter directories and concatenate them.

    Parameters:
    -----------
    base_path : str, optional
        Base path to the data directory. Defaults to project's data directory.
    meter_dirs : list, optional
        List of meter directories to process. If None, processes all meter directories.

    Returns:
    --------
    dict: Dictionary with meter names as keys and concatenated pandas DataFrames as values.
    """
    if base_path is None:
        # Assuming project structure, navigate to data directory
        base_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
    if Path(base_path).exists() is False:
        raise ValueError
    # If no meter dirs specified, get all directories in data
    if meter_dirs is None:
        meter_dirs = [
            d
            for d in os.listdir(base_path)
            if os.path.isdir(os.path.join(base_path, d))
        ]

    meter_data = {}

    for meter_dir in meter_dirs:
        meter_path = os.path.join(base_path, meter_dir)

        # Skip if not a directory
        if not os.path.isdir(meter_path):
            continue

        # Get all CSV files in the meter directory
        csv_files = glob.glob(os.path.join(meter_path, "*.csv"))

        if not csv_files:
            print(f"No CSV files found in {meter_path}")
            continue

        # List to store DataFrames from each file
        dfs = []

        for csv_file in csv_files:
            try:
                # Read CSV file with correct encoding and separator
                df = pd.read_csv(csv_file, sep=";", encoding="utf-8")

                # Convert comma to dot in numeric values and convert to float
                if "KWH 60 Forbruk" in df.columns:
                    df["KWH 60 Forbruk"] = (
                        df["KWH 60 Forbruk"].str.replace(",", ".").astype(float)
                    )

                # Convert date columns to datetime
                if "Fra" in df.columns and "Til" in df.columns:
                    df["Fra"] = pd.to_datetime(df["Fra"], format="%d.%m.%Y %H:%M")
                    df["Til"] = pd.to_datetime(df["Til"], format="%d.%m.%Y %H:%M")

                dfs.append(df)
                print(f"Successfully read: {os.path.basename(csv_file)}")

            except Exception as e:
                print(f"Error reading {csv_file}: {e}")

        if dfs:
            # Concatenate all DataFrames
            concatenated_df = pd.concat(dfs, ignore_index=True)

            # Remove duplicates based on time range (Fra and Til)
            concatenated_df = concatenated_df.drop_duplicates(subset=["Fra", "Til"])

            # Sort by start time
            concatenated_df = concatenated_df.sort_values("Fra")

            meter_data[meter_dir] = concatenated_df
            print(
                f"Processed {len(dfs)} files for {meter_dir}, final DataFrame shape: {concatenated_df.shape}"
            )

    return meter_data


def get_consumption_data(meter_name=None) -> pd.DataFrame:
    """
    Get consumption data for a specific meter or all meters.

    Parameters:
    -----------
    meter_name : str, optional
        Name of the meter to get data for. If None, returns data for all meters.

    Returns:
    --------
    pandas.DataFrame or dict: DataFrame for specified meter or dictionary of DataFrames.
    """
    all_data = read_elhub_data()

    if meter_name is not None:
        data = all_data.get(meter_name)
    if data is None:
        raise ValueError("Data is None")
    return data


if __name__ == "__main__":
    # Example usage
    data = read_elhub_data()

    # Print summary of loaded data
    for meter, df in data.items():
        print(f"\nMeter: {meter}")
        print(f"Data period: {df['Fra'].min()} to {df['Til'].max()}")
        print(f"Total consumption: {df['KWH 60 Forbruk'].sum():.2f} kWh")
        print(f"Number of records: {len(df)}")
