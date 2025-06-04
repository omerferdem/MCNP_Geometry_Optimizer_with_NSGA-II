"""
*** Notice ***
© 2025. Triad National Security, LLC. All rights reserved.
This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL), 
which is operated by Triad National Security, LLC for the U.S. Department of Energy/National Nuclear Security Administration. 
All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear Security Administration. 
The Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, 
prepare. derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.
*** End of Notice ***
"""

import pandas as pd
import numpy as np

def calculate_relative_distances(file1, file2):
    """
    Calculate the average relative distance between individuals in file2 and their closest match in file1.

    Parameters:
    - file1: Path to the first CSV file (asd.csv).
    - file2: Path to the second CSV file (bfg.csv).

    Prints:
    - The average relative distance.
    """
    try:
        # Read the CSV files into DataFrames
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        # Extract columns 3 and 4 (index 2 and 3) from each DataFrame
        prev_params = df1.iloc[:, [2, 3]].values
        cur_params = df2.iloc[:, [2, 3]].values

        # Function to compute the relative distance between two individuals
        def relative_distance(ind1, ind2):
            rel_col3 = (ind1[0] - ind2[0]) / ind2[0]
            rel_col4 = (ind1[1] - ind2[1]) / ind2[1]
            return np.sqrt(rel_col3**2 + rel_col4**2)

        distances = []

        # For each individual in bfg.csv, find the closest individual in asd.csv
        for cur_ind in cur_params:
            # Compute the distances to all individuals in asd.csv
            distances_to_prev = [relative_distance(cur_ind, prev_ind) for prev_ind in prev_params]
            # Find the minimum distance
            min_distance = min(distances_to_prev)
            distances.append(min_distance)

        # Calculate the average of the minimum distances
        average_distance = np.mean(distances)
        if average_distance <= 0.01:
            print(1)
            #print(f"{average_distance}")
        else:
            print(0)
    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file1 = 'Pareto_Front_Prev.csv'  # Path to the first CSV file (asd.csv)
file2 = 'Pareto_Front.csv'  # Path to the second CSV file (bfg.csv')

calculate_relative_distances(file1, file2)