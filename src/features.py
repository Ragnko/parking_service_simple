from loguru import logger
from tqdm import tqdm
import typer
import pandas as pd
import os
import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config import PROCESSED_DATA_DIR, RAW_DATA_DIR

app = typer.Typer()

def process_occupancy_data(raw_data_path: Path, output_path: Path) -> pd.DataFrame:
    """
    Process raw occupancy data and calculate hourly occupancy for a date range.
    Saves results to output_path as CSV.
    """
    df = pd.read_csv(raw_data_path)
    logger.info(f"Loaded raw data from {raw_data_path}")

    # Convert datetime columns
    df['intervalFrom'] = pd.to_datetime(df['intervalFrom'])
    df['intervalFrom'] = pd.to_datetime(df['intervalFrom'])
    df['intervalTo'] = pd.to_datetime(df['intervalTo'])
    logger.info(f"Converted datetime columns")

    min_date = df['intervalTo'].min().date()
    max_date = df['intervalTo'].max().date()
    # Create date range and time slots
    date_range = pd.date_range(start=min_date, end=max_date, freq='D')
    time_slots = [f"{hour:02d}:00:00" for hour in range(24)]
    results = []

    # Calculate occupancy for each date and time slot
    for date in tqdm(date_range, desc="Processing dates"):
        for slot in time_slots:
            datetime_combined = pd.to_datetime(f"{date.date()} {slot}")
            occupancy = df[
                (df['intervalFrom'] <= datetime_combined) &
                (df['intervalTo'] > datetime_combined)
                ].shape[0]
            results.append({'date': date.date(), 'time_slot': slot, 'occupancy': occupancy})

    # Convert results to DataFrame
    occupancy_df = pd.DataFrame(results)
    occupancy_df['datetime'] = pd.to_datetime(occupancy_df['date'].astype(str) + ' ' + occupancy_df['time_slot'])

    # Save to output
    os.makedirs(output_path.parent, exist_ok=True)
    occupancy_df.to_csv(output_path, index=False)
    logger.success(f"Saved features to {output_path}")
    return occupancy_df

@app.command()
def main(
        input_path: Path = RAW_DATA_DIR / "park_gate_2weeks.csv",
        output_path: Path = PROCESSED_DATA_DIR / "occupancy_2weeks.csv",
):
    logger.info("Generating features from dataset...")
    process_occupancy_data(input_path, output_path)
    logger.success("Features generation complete.")


if __name__ == "__main__":
    app()
