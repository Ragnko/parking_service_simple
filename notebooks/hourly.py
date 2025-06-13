import matplotlib.pyplot as plt
import pandas as pd
import os

if __name__ == "__main__":
    file_path = "/Users/pityradko/IdeaProjects/prediction_service_simple/data/raw/park_gate_2weeks.csv"
    v1_skypark_final = pd.read_csv(file_path)
    print(v1_skypark_final.head())
    print(v1_skypark_final.columns)

    # # Convert datetime columns to datetime typeI HAVE INTELIJ BUT I
    v1_skypark_final['intervalFrom'] = pd.to_datetime(v1_skypark_final['intervalFrom'])
    v1_skypark_final['intervalTo'] = pd.to_datetime(v1_skypark_final['intervalTo'])
    print(min(v1_skypark_final['intervalFrom']))
    print(max(v1_skypark_final['intervalFrom']))

    #
    # Create a date range from 28.4.2025 to 11.5.2025
    date_range = pd.date_range(start='2025-04-28', end='2025-05-11', freq='D')
    #
    # # Generate all 24 hours for each day
    #
    time_slots = [f"{hour:02d}:00:00" for hour in range(24)]
    #
    # # Create a list to store results
    results = []
    #
    # # Iterate over each date and time slot
    for date in date_range:
        for slot in time_slots:
            datetime_combined = pd.to_datetime(f"{date.date()} {slot}")
            occupancy = v1_skypark_final[
                (v1_skypark_final['intervalFrom'] <= datetime_combined) &
                (v1_skypark_final['intervalTo'] > datetime_combined)
                ].shape[0]
            results.append({'date': date.date(), 'time_slot': slot, 'occupancy': occupancy})

    # Convert results to a DataFrame
    occupancy_df = pd.DataFrame(results)
    # Combine 'date' and 'time_slot' into a single datetime column for plotting
    occupancy_df['datetime'] = pd.to_datetime(occupancy_df['date'].astype(str) + ' ' + occupancy_df['time_slot'])
    # Save this to processed
    print(occupancy_df)