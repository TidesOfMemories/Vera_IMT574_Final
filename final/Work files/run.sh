#!/bin/bash

# maps the workload to the number of processes
# for i in {1..999}; do
#     python3 worker.py $i 
# done

# wait

# merge the results in result_parts folder as one csv
cat result_parts/*.csv > final_result.csv
