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

from pathlib import Path
import pandas as pd
import time
import csv
from pathlib import Path
import sys

if __name__ == "__main__":
    #print(sys.argv)
    if len(sys.argv) != 3:
        print(sys.argv)
        print("Usage: python history.py <x_len> <y_lim>")
        sys.exit(1)
    try:
        x_len = int(sys.argv[1])
        y_len = int(sys.argv[2])
    except ValueError:
        print("The x_len and y_len must be integers.")
        sys.exit(1)

def is_file_accessible(file_path):
    path = Path(file_path)
    try:
        # Try to open the file in exclusive creation mode.
        with path.open('a', newline='') as f:
            return True
    except IOError:
        return False

def update_history_csv(directory):
    directory_path = Path(directory)
    bests_history_csv_path = directory_path / 'bests_history.csv'
    pop_history_csv_path = directory_path / 'population_history.csv'
    population_csv_path = directory_path / 'Read_Outputs.csv'
    pf_csv_path = directory_path / 'Pareto_Front.csv'

    # Check if history.csv exists
    if not bests_history_csv_path.is_file():
        # Create history.csv with initial generation set to 0
        pf_df = pd.read_csv(pf_csv_path)
        headers=[]
        for i in range(x_len):
            header='input'
            header+=str(i+1)
            headers.append(header)
        for i in range(y_len):
            header='output'
            header+=str(i+1)
            headers.append(header)
        pf_df.columns = headers
        pf_df['generation'] = 0
        pf_df.to_csv(bests_history_csv_path, index=False)
        #print("Created 'history.csv' with initial generation 0.")
    else:
        # If history.csv exists, get the last generation value
        history_df = pd.read_csv(bests_history_csv_path)
        last_generation = history_df['generation'].max() if not history_df.empty else -1
        
        # Read Pareto_Front.csv and add rows with updated generation value
        pf_df = pd.read_csv(pf_csv_path)
        pf_df['generation'] = last_generation + 1
        
        # If accessible, append to history.csv
        while not is_file_accessible(bests_history_csv_path):
            time.sleep(1)  # Wait 1 sec before checking again
        pf_df.to_csv(bests_history_csv_path, mode='a', header=False, index=False) 
        #print(f"Appended rows to 'history.csv' with generation {last_generation + 1}.")

    # Check if history.csv exists
    if not pop_history_csv_path.is_file():
        # Create history.csv with initial generation set to 0
        pop_df = pd.read_csv(population_csv_path) # ,header=None
        headers=[]
        for i in range(x_len):
            header='input'
            header+=str(i+1)
            headers.append(header)
        for i in range(y_len):
            header='output'
            header+=str(i+1)
            headers.append(header)
        pop_df.columns = headers
        pop_df['generation'] = 0
        pop_df.to_csv(pop_history_csv_path, index=False)
        #print("Created 'history.csv' with initial generation 0.")
    else:
        # If history.csv exists, get the last generation value
        history_df = pd.read_csv(pop_history_csv_path)
        last_generation = history_df['generation'].max() if not history_df.empty else -1
        
        # Read Pareto_Front.csv and add rows with updated generation value
        pop_df = pd.read_csv(population_csv_path)
        pop_df['generation'] = last_generation + 1
        
        # If accessible, append to history.csv
        while not is_file_accessible(pop_history_csv_path):
            time.sleep(1)  # Wait 1 sec before checking again
        pop_df.to_csv(pop_history_csv_path, mode='a', header=False, index=False)
        #print(f"Appended rows to 'history.csv' with generation {last_generation + 1}.")

# Example usage:
directory = Path.cwd()
update_history_csv(directory)