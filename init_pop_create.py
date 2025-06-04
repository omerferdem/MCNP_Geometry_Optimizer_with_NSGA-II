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

import itertools
from pathlib import Path
import sys
import numpy as np
from math import sqrt
import random

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print(sys.argv)
        print("Usage: python init_pop_create.py <low_bounds> <high_bounds> <population>")
        sys.exit(1)
    try:
        lows_str = sys.argv[1].split()
        highs_str = sys.argv[2].split()
        population = int(sys.argv[3])
    except ValueError:
        print("The limits must be floats, and population must be an integer.")
        sys.exit(1)

low_bounds = []
for item in lows_str:
    try:
        # Try to convert to float (handles both integers and floats)
        number = float(item)
        low_bounds.append(number)
    except ValueError:
        print(f"Warning: '{item}' is not a valid number for low_bounds.")

high_bounds = []
for item in highs_str:
    try:
        # Try to convert to float (handles both integers and floats)
        number = float(item)
        high_bounds.append(number)
    except ValueError:
        print(f"Warning: '{item}' is not a valid number for high_bounds.")
        
try:
    if len(low_bounds)==len(high_bounds):
        x_len=len(low_bounds)
except ValueError as e:
    print("Length of low and high bounds must be equal:", e)
    
# Define the output directory
directory = Path.cwd()
output_dir = directory / "mcnp_inputs"
output_dir.mkdir(parents=True, exist_ok=True)

# Define template for the MCNP input file
mcnp_template = """c Insert MCNP input file template here. The input variables should be marked with {x}, {y} etc."""

for i in range(population):
    x=[]
    for j in range(x_len):
        x.append(round(random.uniform(low_bounds[j],high_bounds[j]), 5))
    
    # Calculate the necessary positions
    x_y = round(x[0] + x[1], 5)
    x_y_0_2 = round(x[0] + x[1] + 0.1, 5)
    x_y_0_4 = round(x[0] + x[1] + 0.2, 5)
    sphere=round(x[0] + x[1] + 1, 5)
    
    # Generate the filename based on the variable values
    filename = "mcnp"
    for j in range(x_len):
        filename = filename + "_" + str(x[j])
    filename += ".txt"
    # Create the input content by substituting the variables in the template
    input_content = mcnp_template.format(x=x[0], y=x[1], x_y=x_y, x_y_0_2=x_y_0_2, x_y_0_4=x_y_0_4, sphere=sphere)
    # Write the content to the file
    file_path = output_dir / filename
    with open(file_path, 'w') as f:
        f.write(input_content)