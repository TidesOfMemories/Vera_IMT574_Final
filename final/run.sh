#!/bin/bash

# maps the workload to the number of processes
for i in {0..999}; do
    python worker.py $i &
done

wait

# merge the results in result_parts folder as one csv
cat result_parts/*.csv > final_result.csv
