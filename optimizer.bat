REM *** Notice ***
REM © 2025. Triad National Security, LLC. All rights reserved.
REM This program was produced under U.S. Government contract 89233218CNA000001 for Los Alamos National Laboratory (LANL), 
REM which is operated by Triad National Security, LLC for the U.S. Department of Energy/National Nuclear Security Administration. 
REM All rights in the program are reserved by Triad National Security, LLC, and the U.S. Department of Energy/National Nuclear Security Administration. 
REM The Government is granted for itself and others acting on its behalf a nonexclusive, paid-up, irrevocable worldwide license in this material to reproduce, 
REM prepare. derivative works, distribute copies to the public, perform publicly and display publicly, and to permit others to do so.
REM *** End of Notice ***
@echo off
setlocal enabledelayedexpansion

set input_len=2
set "input_low_bounds=0.001 0.1"
set "input_high_bounds=0.5 1"
set output_len=2
set "tally_nums=4 14"
set "cell_nums=3 4"
set numcores=912

set population=30
set generation=4
set min_parent_ind=10

REM Individual cr_ov and mut probability, individuals each attribute mutation prob, mutation_stddev
set crossover_prob=0.75
set mutation_prob=0.25
set each_attribute_mut_prob=0.2
set mutation_gauss_stddev=1

REM Enter only 2 objectives to plot, starting from index 1
set "plotted_objectives=1 2"
set "LOGFILE=optimizer_log.txt"

:: Record start time
for /f "tokens=1-4 delims=:.," %%a in ("%time%") do (
    set "start_hour=%%a"
    set "start_minute=%%b"
    set "start_second=%%c"
    set "start_millisecond=%%d"
)

if exist "mcnp_inputs\" (
    rmdir /s /q "mcnp_inputs"
)
if exist "bests_history.csv" (
    del /q "bests_history.csv"
)
if exist "population_history.csv" (
    del /q "population_history.csv"
)
if exist "Read_Outputs.csv" (
    del /q "Read_Outputs.csv"
)
if exist "Merged_Outputs.csv" (
    del /q "Merged_Outputs.csv"
)
if exist "Pareto_Front.csv" (
    del /q "Pareto_Front.csv"
)
if exist "Pareto_Front_Prev.csv" (
    del /q "Pareto_Front_Prev.csv"
)
if exist "New_Population.csv" (
    del /q "New_Population.csv"
)
if exist "historied_fronts.png" (
    del /q "historied_fronts.png"
)
if exist "historied_generations.png" (
    del /q "historied_generations.png"
)
if exist "output_log.txt" (
    del /q "output_log.txt"
)

python init_pop_create.py "%input_low_bounds%" "%input_high_bounds%" %population%

set current_dir=%cd%
set target_dir=%current_dir%\mcnp_inputs

for %%f in (%target_dir%\*.txt) do (
    set "input_file=%%f"
    set "base_name=%%~nf"

    set "output_file=%target_dir%\!base_name!.o"
    set "runtpe_file=%target_dir%\!base_name!.r"
    set "o_temp_file=%target_dir%\!base_name!_temp.o"
    set "r_temp_file=%target_dir%\!base_name!_temp.r"

    REM echo. > !output_file!
    REM echo. > !runtpe_file!

    mcnp6 i="!input_file!" o="!o_temp_file!" r="!r_temp_file!"

    move /Y "!o_temp_file!" "!output_file!"
    move /Y "!r_temp_file!" "!runtpe_file!"
    del /Q "!runtpe_file!"
)

python extractor.py %input_len% "%tally_nums%" "%cell_nums%"
echo extractor complete

python nondomsorter.py %input_len% %output_len% %min_parent_ind%
echo sorter complete

python history_the_pop_and_pf.py %input_len% %output_len%
echo historian complete

del /Q "Read_Outputs.csv"

python crossover_mutation.py "%input_low_bounds%" "%input_high_bounds%" %output_len% %population% %crossover_prob% %mutation_prob% %each_attribute_mut_prob% %mutation_gauss_stddev%
echo mutation complete

move /Y Pareto_Front.csv Pareto_Front_Prev.csv >nul 2>&1

del /q "%target_dir%\*.txt"
    
if not exist "%target_dir%\all_outputs" mkdir "%target_dir%\all_outputs"
move /Y "%target_dir%\*.o" "%target_dir%\all_outputs\" >nul 2>&1

python pop_create.py %input_len%
echo new population inputs created

del /Q "New_Population.csv"

set convergence=0
set count=1
:loop
if !convergence! equ 0 (
    for %%f in (%target_dir%\*.txt) do (
        set "input_file=%%f"
        set "base_name=%%~nf"

        set "output_file=%target_dir%\!base_name!.o"
        set "runtpe_file=%target_dir%\!base_name!.r"
        set "o_temp_file=%target_dir%\!base_name!_temp.o"
        set "r_temp_file=%target_dir%\!base_name!_temp.r"

        REM echo. > !output_file!
        REM echo. > !runtpe_file!

        mcnp6 i="!input_file!" o="!o_temp_file!" r="!r_temp_file!"

        move /Y "!o_temp_file!" "!output_file!"
        move /Y "!r_temp_file!" "!runtpe_file!"
        del /Q "!runtpe_file!"
    )

    python extractor.py %input_len% "%tally_nums%" "%cell_nums%"
    echo extractor complete

    python merge_parent_offspring.py
    echo parent merger complete
    
    python nondomsorter.py %input_len% %output_len% %min_parent_ind%
    echo sorter complete

    python history_the_pop_and_pf.py %input_len% %output_len%
    echo historian complete

    del /Q "Merged_Outputs.csv"

    del /Q "Read_Outputs.csv"

    timeout /t 2
    python crossover_mutation.py "%input_low_bounds%" "%input_high_bounds%" %output_len% %population% %crossover_prob% %mutation_prob% %each_attribute_mut_prob% %mutation_gauss_stddev%
    echo mutation complete

    move /Y Pareto_Front.csv Pareto_Front_Prev.csv >nul 2>&1

    del /q "%target_dir%\*.txt"
    
    if not exist "%target_dir%\all_outputs" mkdir "%target_dir%\all_outputs"
    move /Y "%target_dir%\*.o" "%target_dir%\all_outputs\" >nul 2>&1

    for /f "delims=" %%a in ('python comparator.py') do set output=%%a
    if !output! equ 1 set convergence=1
    echo convergence check complete

    if !count! geq %generation% goto :end
    set /a count+=1
    echo epoch check complete

    python pop_create.py %input_len%
    echo new inputs created

    del /Q "New_Population.csv"

    goto :loop
    )
:end
del /Q "Pareto_Front_Prev.csv"
del /Q "New_Population.csv"

REM Record end time
for /f "tokens=1-4 delims=:.," %%a in ("%time%") do (
    set "end_hour=%%a"
    set "end_minute=%%b"
    set "end_second=%%c"
    set "end_millisecond=%%d"
)

REM Calculate elapsed time
set /a start_total_milliseconds=(start_hour * 3600 * 1000) + (start_minute * 60 * 1000) + (start_second * 1000) + start_millisecond
set /a end_total_milliseconds=(end_hour * 3600 * 1000) + (end_minute * 60 * 1000) + (end_second * 1000) + end_millisecond
set /a elapsed_milliseconds=end_total_milliseconds - start_total_milliseconds

REM Convert milliseconds to hours, minutes, seconds, and milliseconds
set /a elapsed_seconds=elapsed_milliseconds / 1000
set /a elapsed_minutes=elapsed_seconds / 60
set /a elapsed_hours=elapsed_minutes / 60
set /a remaining_seconds=elapsed_seconds %% 60
set /a remaining_minutes=elapsed_minutes %% 60
set /a remaining_milliseconds=elapsed_milliseconds %% 1000

REM Print total running time
echo Total running time: %elapsed_hours% hours, %remaining_minutes% minutes, %remaining_seconds% seconds, and %remaining_milliseconds% milliseconds.

python scatter_bests_histories.py %input_len% %output_len% "%plotted_objectives%"
python scatter_pop_histories.py %input_len% %output_len% "%plotted_objectives%"