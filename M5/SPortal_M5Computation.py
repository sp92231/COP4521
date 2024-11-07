"""

Name: Shanie Portal
Date: 10/03/2024
Assignment: Module 4: Using Threads with Locks
Due Date: 10/02/2024
About this project: This program calculates the sum of the terms of the alternating harmonic series using Dask
for parallel computation.
All work below was performed by Shanie Portal

"""

import math
from dask.distributed import Client

# Initialize Dask client.
client = Client(processes=False, threads_per_worker=4, n_workers=1, memory_limit="1GB")


# Function for first part of series.
def function1(x):
    return math.pow(-1, (x+1))/((2*x)-1)


# Function for second part of series.
def function2(x):
    return math.pow(-1, (x+1))/((2*x)-1)


# Function for third part of series.
def function3(x):
    return math.pow(-1, (x+1))/((2*x)-1)


if __name__ == '__main__':
    # Set data ranges for series computation.
    data1 = [*range(1, 101, 3)]
    data2 = [*range(2, 101, 3)]
    data3 = [*range(3, 101, 3)]

    # Map functions to data.
    res = client.map(function1, data1)
    res2 = client.map(function2, data2)
    res3 = client.map(function3, data3)

    # Wait for computations and gather results.
    total_sum = client.gather([res, res2, res3])

    # Flatten results.
    flat_results = [item for sublist in total_sum for item in sublist]

    # Compute final sum.
    final_sum = sum(flat_results)

    client.shutdown()

    # Output final result.
    print(f"Sum = {final_sum:.4f}")
