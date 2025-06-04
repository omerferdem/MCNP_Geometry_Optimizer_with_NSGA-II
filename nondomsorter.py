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

import csv
import numpy as np
import pandas as pd
from pathlib import Path
import sys

if __name__ == "__main__":
    #print(sys.argv)
    if len(sys.argv) != 4:
        print(sys.argv)
        print("Usage: python nondomsorter.py <x_len> <y_len> <min_parents>")
        sys.exit(1)
    try:
        x_len = int(sys.argv[1])
        y_len = int(sys.argv[2])
        min_parent_ind = int(sys.argv[3])
    except ValueError:
        print("The x_len, y_len and min_parent_ind must be integers.")
        sys.exit(1)

"""
x_len=2
y_len=2
min_parent_ind=8
"""

def get_pareto_front(csv_path):
    df = pd.read_csv(csv_path)
    data = df.values 
    pareto_front = non_dominated_sorting(data)
    return pareto_front

def get_top_indices(counts): #, top_n=10):
    # Create a list of (index, value) tuples
    indexed_counts = list(enumerate(counts))
    
    # Sort the list of tuples based on the values, in descending order
    sorted_counts = sorted(indexed_counts, key=lambda x: x[1], reverse=False)
    
    # Extract the indices of the top_n highest values
    top_indices = [index for index, value in sorted_counts[:len(counts)]] # [:len(top_n)]]
    
    return top_indices

def non_dominated_sorting(data):
    # Implementation of non-dominated sorting
    num_points = len(data)
    domination_count = np.zeros(num_points, dtype=int)
    
    for i in range(num_points):
        for j in range(i + 1, num_points):
            if dominates(data[i], data[j]):
                domination_count[j] += 1
            elif dominates(data[j], data[i]):
                domination_count[i] += 1
    
    pareto_front = []
    for i in range(num_points):
        if domination_count[i] == 0:
            if not any(np.array_equal(data[i], front) for front in pareto_front):
                pareto_front.append(data[i])
    if len(pareto_front)<min_parent_ind:
        lesser_fronts = get_top_indices(domination_count) # ,min_parent_ind)
        j=0
        while len(pareto_front)<min_parent_ind:
            index = lesser_fronts[j]
            if not any(np.array_equal(data[index], front) for front in pareto_front):
                pareto_front.append(data[index])
            j+=1
    return pareto_front

def dominates(point1_all, point2_all):
    # Helper function to check domination for maximization
    point1=point1_all[x_len:]
    point2=point2_all[x_len:]
    return all(p1 >= p2 for p1, p2 in zip(point1, point2)) and any(p1 > p2 for p1, p2 in zip(point1, point2))

def list_to_csv(input_list, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        for item in input_list:
            writer.writerow(item)

file_path_merged = Path('Merged_Outputs.csv')
file_path_read = Path('Read_Outputs.csv')

if file_path_merged.exists():
    csv_path = str(file_path_merged)
else:
    csv_path = str(file_path_read)

# Get Pareto front
pareto_front = get_pareto_front(csv_path)
pareto_front = np.array(pareto_front)

final_list=[]
line=[]
for i in range(x_len):
    line.append("input"+str(i+1))
for i in range(x_len , x_len+y_len):
    line.append("output"+str(i+1-x_len))
final_list.append(line) 
for row in pareto_front:
    final_list.append(row)
list_to_csv(final_list,"Pareto_Front.csv")