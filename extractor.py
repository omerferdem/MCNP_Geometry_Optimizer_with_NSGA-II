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
import csv
import numpy as np
import re
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(sys.argv)
        print("Usage: python init_pop_create.py <x_len> <tally_nums> <cell_nums>")
        sys.exit(1)
    try:
        x_len = int(sys.argv[1])
        tally_numbers = sys.argv[2].split()
        cell_numbers = sys.argv[3].split()
    except ValueError:
        print("The limits must be floats, and population must be an integer.")
        sys.exit(1) 

try:
    if len(tally_numbers)==len(cell_numbers):
        y_len=len(cell_numbers)
except ValueError as e:
    print("Length of tally and cell names must be equal:", e)

"""
x_len=2
tally_numbers="4 14".split()
cell_numbers="3 4".split()
y_len = len(tally_numbers)
"""

tally_names=[]
cell_names=[]
for tally in tally_numbers:
    tally_string = "1tally         "
    string_stop = len(tally_string)-len(tally)
    tally = tally_string[:string_stop] + tally
    tally_names.append(tally)
for cell in cell_numbers:
    cell_string = "cell   "
    string_stop = len(cell_string)-len(cell)
    cell = cell_string[:string_stop] + cell
    cell_names.append(cell)

def extract_e(file_path,tally_name,cell_name):
    floats_list = []
    with open(file_path, 'r') as file:
        lines = file.readlines()
        found_tally = False
        for i in range(len(lines)):
            line = lines[i].strip()
            if line.startswith(tally_name): #'1tally        4'):
                found_tally = True
            elif found_tally and line.startswith(cell_name): #'cell  3'):
                m = i+1
                while m < len(lines) and lines[m].strip():  # Skip empty lines
                    data = lines[m].split()
                    if len(data) >= 3:
                        try:
                            floats_list.append(float(data[1]))
                        except ValueError:
                            pass  # Skip if conversion to float fails
                    m += 1
                break
    try:
        energy1_100ev = floats_list[1]
    except:
        return None
    return energy1_100ev

def extract_floats(input_string):
    # Define a regular expression to match floats
    float_pattern = r"[-+]?\d*\.\d+|\d+"  # Pattern for matching floats
    
    floats = re.findall(float_pattern, input_string)
    
    floats = list(map(float, floats))
    
    if len(floats) == 0:
        raise ValueError("Input string does not contain floats")
    
    return floats

def filename2parameter(file_path):
    file_name = Path(file_path).stem  
    float_pattern = re.compile(r'\b\d+\.\d+|\b\d+|\.\d+|\d+e[+-]?\d+', re.IGNORECASE)
    # Find all matches in the file name
    matches = float_pattern.findall(file_name)
    # Convert matches to floats
    floats = [float(match) for match in matches]
    return floats

def list_to_csv(input_list, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for item in input_list:
            if not np.all(np.array(item) == 0):
                writer.writerow(item)

inp_dir = Path.cwd()
target_dir = inp_dir / 'mcnp_inputs'

o_files_path = list(target_dir.glob('*.o'))
o_files = [str(file) for file in o_files_path]

final_list = [[0]*(x_len+y_len) for i in range(len(o_files)+1)]
for i in range(x_len):
    final_list[0][i] = "input"+str(i+1)
for i in range(x_len , x_len+y_len):
    final_list[0][i] = "output"+str(i+1-x_len)
for file_index in range(len(o_files)):
    file_name = o_files[file_index]

    x = filename2parameter(file_name)
    y=[0]*y_len
    for i in range(y_len):
        y[i] = extract_e(file_name,tally_names[i],cell_names[i])

    line=[]
    for i in range(x_len):
        line.append(x[i])
    for i in range(y_len):
        if y[i] is not None:
            line.append(y[i])
    final_list[file_index+1] = line
list_to_csv(final_list,"Read_Outputs.csv")