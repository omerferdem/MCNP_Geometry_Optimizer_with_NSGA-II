# O4855 - MCNP_Geometry_Optimizer_with_NSGA-II

The codes for an automatic geometry optimizer for a number of objectives (tallies) and a number of input parameters (geometry). 

## Copyright Notice

© 2025. Triad National Security, LLC. All rights reserved.
This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL), which is operated by Triad National Security, LLC for the U.S. Department of Energy/National Nuclear Security Administration. All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear Security Administration. The Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, prepare. derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.

---

## 📜 License

This program is Open-Source under the **BSD-3 License**.

Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors may be used to endorse or promote products derived from this software without specific prior written permission.

> **DISCLAIMER:**  
> THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.  
> IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

---

## ⚙️ How to Use

To use this optimizer, you need to:

1. **Edit the MCNP input template**:
   - Modify the template MCNP file inside `init_pop_create.py` and `pop_create.py` to reflect your geometry structure and input format.

2. **Configure hyperparameters**:
   - Choose one of the following files to adjust the hyperparameters for the optimization:
     - `optimizer.bat` or `optimizer_debug.bat` (for Windows)
     - `optimizer.sh` or `optimizer_debug.sh` (for Linux)

   - **Debug** versions generate step-by-step CSV outputs for inspection.  
     **Standard** versions only produce the final optimization results.

3. **Run the optimization**:
   - The code will:
     - Initialize with a random population in the defined input parameter space.
     - Run MCNP simulations for each individual.
     - Extract objective (tally) results from each simulation.
     - Use the **NSGA-II** algorithm to evolve the population based on multi-objective performance.
     - Write new geometry files and repeat this process iteratively.

---

## 🔧 Environment Setup

Make sure you have the following Python packages installed:

- `pandas`
- `numpy`
- `deap`

📌 **Tested with Python 3.10**, but should work with any Python version that supports these libraries.

You can install dependencies with:

```bash
pip install pandas numpy deap
```

## 📁 File Structure Overview

MCNP_Geometry_Optimizer_with_NSGA-II/
├── comparator.py # Compares parent and offspring populations for selection
├── crossover_mutation.py # Applies crossover and mutation operators to individuals
├── extractor.py # Extracts tally results from MCNP output files
├── history_the_pop_and_pf.py # Stores and tracks the history of populations and Pareto fronts
├── init_pop_create.py # Generates the initial MCNP input files for the first population
├── merge_parent_offspring.py # Merges parent and offspring populations for NSGA-II sorting
├── nondomsorter.py # Performs nondominated sorting (NSGA-II core logic)
├── optimizer.bat # Windows runner for optimization (final results only)
├── optimizer.sh # Linux runner for optimization (final results only)
├── optimizer_debug.bat # Windows runner with detailed CSV output for debugging
├── optimizer_debug.sh # Linux runner with detailed CSV output for debugging
├── pop_create.py # Generates new population MCNP input files from evolved individuals
├── scatter_bests_histories.py # Plots best individuals' objective values over generations
├── scatter_pop_histories.py # Plots entire population objective values across generations
└── README.md # Project documentation (this file)

## 📬 Contact & Contributions

Contributions and issues are welcome!
If you use or extend this code, consider giving credit or sharing your improvements with the community.
