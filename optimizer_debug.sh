#!/bin/bash

# *** Notice ***
# © 2025. Triad National Security, LLC. All rights reserved.
# This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL), 
# which is operated by Triad National Security, LLC for the U.S. Department of Energy/National Nuclear Security Administration. 
# All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear Security Administration. 
# The Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, 
# prepare. derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.
# *** End of Notice ***

set -e

input_len=2
input_low_bounds="0.001 0.1"
input_high_bounds="0.5 1"
output_len=2
tally_nums="4 14"
cell_nums="3 4"
numcores=912

population=30
generation=4
min_parent_ind=10

# Individual cr_ov and mut probability, individuals each attribute mutation prob, mutation_stddev
crossover_prob=0.75
mutation_prob=0.25
each_attribute_mut_prob=0.2
mutation_gauss_stddev=1

# Enter only 2 objectives to plot, starting from index 1
plotted_objectives="1 2"
LOGFILE="optimizer_log.txt"

# Record start time
start_time=$(date +%s%3N)

# Clean up existing files
rm -rf mcnp_inputs
rm -f bests_history.csv population_history.csv Read_Outputs.csv Merged_Outputs.csv Pareto_Front.csv Pareto_Front_Prev.csv New_Population.csv historied_fronts.png historied_generations.png output_log.txt

python init_pop_create.py "$input_low_bounds" "$input_high_bounds" "$population"

current_dir=$(pwd)
target_dir="$current_dir/mcnp_inputs"

mkdir -p "$target_dir"

for input_file in "$target_dir"/*.txt; do
    base_name=$(basename "$input_file" .txt)
    output_file="$target_dir/${base_name}.o"
    runtpe_file="$target_dir/${base_name}.r"
    o_temp_file="$target_dir/${base_name}_temp.o"
    r_temp_file="$target_dir/${base_name}_temp.r"

    # Run MCNP6
    mcnp6 i="$input_file" o="$o_temp_file" r="$r_temp_file"

    mv -f "$o_temp_file" "$output_file"
    mv -f "$r_temp_file" "$runtpe_file"
    rm -f "$runtpe_file"
done

sleep 2
python extractor.py "$input_len" "$tally_nums" "$cell_nums"
echo "extractor complete"

sleep 2
python nondomsorter.py "$input_len" "$output_len" "$min_parent_ind"
echo "sorter complete"

sleep 2
python history_the_pop_and_pf.py "$input_len" "$output_len"
echo "historian complete"

sleep 2
python crossover_mutation.py "$input_low_bounds" "$input_high_bounds" "$output_len" "$population" "$crossover_prob" "$mutation_prob" "$each_attribute_mut_prob" "$mutation_gauss_stddev"
echo "mutation complete"

mv -f Pareto_Front.csv Pareto_Front_Prev.csv

rm -f "$target_dir"/*.txt

mkdir -p "$target_dir/all_outputs"
mv -f "$target_dir"/*.o "$target_dir/all_outputs/"

sleep 2
python pop_create.py "$input_len"
echo "new population inputs created"

convergence=0
count=1

while [ "$convergence" -eq 0 ]; do
    for input_file in "$target_dir"/*.txt; do
        base_name=$(basename "$input_file" .txt)
        output_file="$target_dir/${base_name}.o"
        runtpe_file="$target_dir/${base_name}.r"
        o_temp_file="$target_dir/${base_name}_temp.o"
        r_temp_file="$target_dir/${base_name}_temp.r"

        # Run MCNP6
        mcnp6 i="$input_file" o="$o_temp_file" r="$r_temp_file"

        mv -f "$o_temp_file" "$output_file"
        mv -f "$r_temp_file" "$runtpe_file"
        rm -f "$runtpe_file"
    done

    sleep 2
    python extractor.py "$input_len" "$tally_nums" "$cell_nums"
    echo "extractor complete"

    sleep 2
    python merge_parent_offspring.py
    echo "parent merger complete"
    
    sleep 2
    python nondomsorter.py "$input_len" "$output_len" "$min_parent_ind"
    echo "sorter complete"

    sleep 2
    python history_the_pop_and_pf.py "$input_len" "$output_len"
    echo "historian complete"

    sleep 2
    python crossover_mutation.py "$input_low_bounds" "$input_high_bounds" "$output_len" "$population" "$crossover_prob" "$mutation_prob" "$each_attribute_mut_prob" "$mutation_gauss_stddev"
    echo "mutation complete"

    mv -f Pareto_Front.csv Pareto_Front_Prev.csv

    rm -f "$target_dir"/*.txt
    
    mkdir -p "$target_dir/all_outputs"
    mv -f "$target_dir"/*.o "$target_dir/all_outputs/"

    sleep 2
    output=$(python comparator.py)
    if [ "$output" -eq 1 ]; then
        convergence=1
    fi
    echo "convergence check complete"

    sleep 2
    if [ "$count" -ge "$generation" ]; then
        break
    fi
    count=$((count + 1))
    echo "epoch check complete"

    sleep 2
    python pop_create.py "$input_len"
    echo "new inputs created"
done

# Record end time and calculate elapsed time
end_time=$(date +%s%3N)
elapsed_time=$((end_time - start_time))

elapsed_seconds=$((elapsed_time / 1000))
elapsed_minutes=$((elapsed_seconds / 60))
elapsed_hours=$((elapsed_minutes / 60))
remaining_seconds=$((elapsed_seconds % 60))
remaining_minutes=$((elapsed_minutes % 60))
remaining_milliseconds=$((elapsed_time % 1000))

echo "Total running time: ${elapsed_hours} hours, ${remaining_minutes} minutes, ${remaining_seconds} seconds, and ${remaining_milliseconds} milliseconds."

python scatter_bests_histories.py "$input_len" "$output_len" "$plotted_objectives"
python scatter_pop_histories.py "$input_len" "$output_len" "$plotted_objectives"
