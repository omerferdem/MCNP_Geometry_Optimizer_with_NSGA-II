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
from deap import base, creator, tools, algorithms
import numpy as np
from math import inf, pi
import random
import csv
import copy
import sys

inp_file = "Pareto_Front.csv"

if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Usage: python init_pop_create.py <low_bounds> <high_bounds> <y_len> <population> <cr_prob> <mut_prob> <indpb> <sigma>")
        sys.exit(1)
    try:
        lows_str = sys.argv[1].split()
        highs_str = sys.argv[2].split()
        y_len = int(sys.argv[3])
        population = int(sys.argv[4])
        cr_ov_prob_read=float(sys.argv[5])
        mut_prob_read=float(sys.argv[6])
        indpb_read=float(sys.argv[7])
        sigma_read=float(sys.argv[8])
    except ValueError:
        print("The limits must be floats, population must be an integer, the rest must be floats.")
        sys.exit(1)

if cr_ov_prob_read+mut_prob_read>1:
    raise ValueError("The sum of cr_ov_prob_read and mut_prob_read should not be greater than 1.")
'''
lows_str = '0.001 0.1'.split()
highs_str = '0.5 1'.split()
y_len = int('2')
population = int('25')
'''

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

def get_unique_pop(population):
    unique_population = []
    seen_individuals = set()    
    for ind in population:
        # Convert individual to tuple for comparison
        ind_tuple = tuple(ind)
        if ind_tuple not in seen_individuals:
            unique_population.append(ind)
            seen_individuals.add(ind_tuple)
    return unique_population

def outOfBounds(individual):
    isOut = 0
    for i in range(len(individual)):
        if individual[i]<low_bounds[i]:
            isOut=1
        if individual[i]>high_bounds[i]:
            isOut=1
    return isOut

def gaussian_mutation(individual, mu=0, sigma=1, indpb=0.2):
    for i, gene in enumerate(individual):
        if random.random() < indpb:
            individual[i] = gene + random.gauss(mu, sigma)
    return individual,

def generate_offspring_from_population(csv_path, num_offspring, 
                                        mutation_prob=mut_prob_read, crossover_prob=cr_ov_prob_read, output_csv_path='New_Population.csv'):
    """
    Generate a specified number of offspring from the current population.

    Parameters:
    - current_population: The current population of individuals.
    - num_offspring: The number of offspring individuals to generate.
    - mutation_prob: Probability of mutation.
    - crossover_prob: Probability of crossover.

    Returns:
    - A list of offspring individuals.
    """
    # Create the necessary DEAP objects
    creator.create("FitnessMulti", base.Fitness, weights=(1.0,) * y_len)
    creator.create("Individual", list, fitness=creator.FitnessMulti)

    toolbox = base.Toolbox()
    
    for i in range(x_len):
        toolbox.register("attr_float"+str(i), np.random.uniform, low_bounds[i], high_bounds[i])
    inp_names_tuple = tuple(f"attr_float{i}" for i in range(x_len))
    toolbox.register("individual", tools.initRepeat, creator.Individual, inp_names_tuple, n=1)
    toolbox.register("mate", tools.cxBlend, alpha=0.5)
    toolbox.register("mutate", gaussian_mutation, mu=0, sigma=sigma_read, indpb=indpb_read)

    # Read the CSV file
    df = pd.read_csv(csv_path)
    
    # Extract the first and second columns as individuals
    current_population = df.iloc[:, [0, 1]].values
    #print(df.iloc[:, [0, 1]].values)
    offspring = []
    population = list(current_population)  # Make a copy to avoid modifying the original

    '''
    if len(population)<5:
        while len(offspring) < num_offspring:
            parent1, parent2 = random.sample(population, 2)
            child1, child2 = toolbox.clone(parent1), toolbox.clone(parent2)
            toolbox.mutate(child1)
            toolbox.mutate(child2)
            print()
            if not any(np.array_equal(child1, arr) for arr in offspring):
                offspring.append(child1)
            if not any(np.array_equal(child2, arr) for arr in offspring):
                offspring.append(child2)
            del child1
            del child2

    else:
    '''

    while len(offspring) < num_offspring:
        # Select two parents from the current population
        parent1, parent2 = random.sample(population, 2)
        child1, child2 = toolbox.clone(parent1), toolbox.clone(parent2)

        # Apply crossover and mutation
        random_number = random.random()
        if random_number < crossover_prob:
            toolbox.mate(child1, child2)
            if not any(np.array_equal(child1, arr) for arr in offspring) and not outOfBounds(child1):
                offspring.append(child1)
            if not any(np.array_equal(child2, arr) for arr in offspring) and not outOfBounds(child2):
                offspring.append(child2)
            del child1
            del child2
        if 1-random_number < mutation_prob:
            toolbox.mutate(child1)
            toolbox.mutate(child2)
            if not any(np.array_equal(child1, arr) for arr in offspring) and not outOfBounds(child1):
                offspring.append(child1)
            if not any(np.array_equal(child2, arr) for arr in offspring) and not outOfBounds(child2):
                offspring.append(child2)
            del child1
            del child2

    offspring = np.array(offspring)
    # Ensure that we do not exceed the desired number of offspring
    if len(offspring) > num_offspring:
        offspring = offspring[:num_offspring]


    # Convert the new population to a DataFrame
    new_population = [ind[:] for ind in offspring]
    
    unique_pop = get_unique_pop(new_population)

    population_df = pd.DataFrame(unique_pop)

    headers=[]
    for i in range(x_len):
        header='input'
        header+=str(i+1)
        headers.append(header)
    population_df.columns = headers

    # Write the new population to a CSV file
    population_df.to_csv(output_csv_path, index=False)

# Generate the desired number of offspring
generate_offspring_from_population('Pareto_Front.csv', population, crossover_prob=0.75, mutation_prob=0.25, output_csv_path='New_Population.csv')