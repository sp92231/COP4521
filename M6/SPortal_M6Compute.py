"""

Name: Shanie Portal
Date: 10/07/2024
Assignment: Module 6: Dask Large Dataset
Due Date: 10/06/2024
About this project: This program uses Dask to compute and visualize minimum temperatures by date from a large dataset.
All work below was performed by Shanie Portal

"""
import dask.dataframe as dd

dtypes = {
    "date": str,
    "actual_mean_temp": int,
    "actual_min_temp": int,
    "actual_max_temp": int,
    "average_min_temp": int,
    "average_max_temp": int,
    "record_min_temp": int,
    "record_max_temp": int,
    "record_min_temp_year": int,
    "record_max_temp_year": int,
    "actual_precipitation": float,
    "average_precipitation": float,
    "record_precipitation": float
}

if __name__ == '__main__':
    df = dd.read_csv('KNYC.csv', dtype=dtypes)
    print(df.head())

    # Group by date and aggregate min temps.
    df_grouped = df.groupby("date").aggregate({"actual_min_temp": "min", "average_min_temp": "min"})

    # Display computed dataframe.
    print(df_grouped.compute())

    # Save result for visualization script.
    df_grouped.to_parquet('grouped_data.parquet')
