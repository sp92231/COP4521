"""

Name: Shanie Portal
Date: 09/08/2024
Assignment: Module 2: Using Threads
Due Date: 09/08/2024
About this project: Python script that computes area using threads.
All work below was performed by: Shanie Portal

"""

import random
from concurrent.futures import ThreadPoolExecutor


def random_gen(x1, x2):
    # Generates a random number between x1 and x2.
    random_num = random.randint(x1, x2)

    # result holds computed expression.
    result = (random_num ** 2) - (3 * random_num)
    # Returns result.
    return result


def main():
    # Defines the range for random_num.
    x1 = 1
    x2 = 6
    num_trials = 100000

    # Create ThreadPoolExecutor with max_workers=3.
    with ThreadPoolExecutor(max_workers=3) as executor:
        # Submit tasks using map and collect results.
        results = list(executor.map(lambda _: random_gen(x1, x2), range(num_trials)))

    # Compute the sum of the results.
    sum_results = sum(results)

    # Compute the area.
    area = sum_results * (x2 - x1) / float(num_trials)

    # Display area.
    print(f"The computed area is: {area}")


if __name__ == "__main__":
    main()
