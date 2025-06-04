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

def merge_csv_files(file1, file2, output_file='Merged_Outputs.csv'):
    try:
        # Read the two CSV files into DataFrames
        df1 = pd.read_csv(file1)
        df2 = pd.read_csv(file2)

        if df1.shape[1] != df2.shape[1]:
            raise ValueError("The number of columns in the two files do not match.")
        
        # Concatenate the dataframes
        merged_df = pd.concat([df1, df2], ignore_index=True)
        
        # Save the merged dataframe to a new CSV file
        merged_df.to_csv(output_file, index=False)

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
file1 = 'Read_Outputs.csv'  # Path to the first CSV file
file2 = 'Pareto_Front_Prev.csv'  # Path to the second CSV file

merge_csv_files(file1, file2)