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
import matplotlib.pyplot as plt
import sys

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python scatter_bests_histories.py <x_len> <y_len> <plotted_objectives>")
        sys.exit(1)
    try:
        x_len = int(sys.argv[1])
        y_len = int(sys.argv[2])
        plots_str = sys.argv[3].split()
    except ValueError:
        print("The x_lim and y_lim must be integers, and plotted_objectives must be a space delimited string.")
        sys.exit(1)
plot_indices = []
for item in plots_str:
    try:
        number = int(item)
        plot_indices.append(number)
    except ValueError:
        print(f"Warning: '{item}' is not a valid number for plot_indices.")
"""
x_len=2
y_len=2
plots_str="1 2".split()
plot_indices = []
for item in plots_str:
    number = int(item)
    plot_indices.append(number)
"""

df = pd.read_csv('bests_history.csv')

gen_index = x_len+y_len
generation = df.iloc[:, gen_index]  # 5th column for x_len=2 y_len=2 (index 4)

if max(generation)>5:
    gens_normalized = generation/max(generation)
    count = 0
    gens_to_print = []
    for index in range(len(gens_normalized)):
        norm_generation = gens_normalized[index]
        if norm_generation >= 0.2*count:
            gens_to_print.append(generation[index])
            count+=1

    filtered_df = df[df.iloc[:, gen_index].isin(gens_to_print)]
    x = filtered_df.iloc[:, x_len+plot_indices[0]-1]  # 3rd column (index 2)
    y = filtered_df.iloc[:, x_len+plot_indices[1]-1]  # 4th column (index 3)
else:
    gens_to_print=[i for i in range(6)]
    x = df.iloc[:, x_len+plot_indices[0]-1]  # 3rd column (index 2)
    y = df.iloc[:, x_len+plot_indices[1]-1]  # 4th column (index 3)

colors = {
    gens_to_print[0]: 'blue',
    gens_to_print[1]: 'lightblue',
    gens_to_print[2]: 'lightgreen',
    gens_to_print[3]: 'yellow',
    gens_to_print[4]: 'orange',
    gens_to_print[5]: 'red',
}

if max(generation)>5:
    color_values = filtered_df.iloc[:, gen_index].map(colors)
else:
    color_values = df.iloc[:, gen_index].map(colors)

# Create the scatter plot
plt.figure(figsize=(10, 6))
scatter = plt.scatter(x, y, c=color_values, s=50)

# Create a legend for the generations
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=color, markersize=10) for gen, color in colors.items()]
labels = [f'Generation {gen}' for gen in colors]
plt.legend(handles, labels, title='Generations')

# Add labels and title
plt.xlabel('1-100eV Tally')
plt.ylabel('0.5-10keV Tally')
plt.title('Best Individuals with Generations')

# Save the plot to a PNG file with 200 DPI
plt.savefig('historied_fronts.png', dpi=200)

# Show the plot (optional)
plt.show()