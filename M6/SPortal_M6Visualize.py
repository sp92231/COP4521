"""

Name: Shanie Portal
Date: 10/07/2024
Assignment: Module 6: Dask Large Dataset
Due Date: 10/06/2024
About this project: This program uses Dask to compute and visualize minimum temperatures by date from a large dataset.
All work below was performed by Shanie Portal

"""
import dask.dataframe as dd

if __name__ == '__main__':
    # Load data from compute script.
    df_grouped = dd.read_parquet('grouped_data.parquet')

    # Visualize.
    df_grouped.visualize("mydask.png")
