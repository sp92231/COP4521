"""

Name: Shanie Portal
Date: 10/03/2024
Assignment: Module 4: Using Threads with Locks
Due Date: 10/02/2024
About this project: This program calculates the sum of the terms of the alternating harmonic series using Dask
for parallel computation.
All work below was performed by Shanie Portal

"""

import dask.delayed as delayed
import math

# Function for first part of series.
def function1(x):
    return math.pow(-1, (x + 1)) / ((2 * x) - 1)


# Function for second part of series.
def function2(x):
    return math.pow(-1, (x + 1)) / (2 * x)


# Function for third part of series.
def function3(x):
    return math.pow(-1, (x + 1)) / ((2 * x) + 1)

# Set data ranges for series computation.
data1 = [*range(1, 101, 3)]
data2 = [*range(2, 101, 3)]
data3 = [*range(3, 101, 3)]

# Create delayed computations.
posA = [delayed(function1)(i) for i in data1]
negB = [delayed(function2)(j) for j in data2]
negC = [delayed(function3)(k) for k in data3]

# Sum the results of each function.
SumA = delayed(sum)(posA)
SumB = delayed(sum)(negB)
SumC = delayed(sum)(negC)

# Final result.
result = delayed(lambda x, y, z: x + y + z)(SumA, SumB, SumC)

# Visualize the Dask computation graph.
result.visualize(filename='visualization_graph', format='png')
