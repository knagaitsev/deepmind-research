#!/bin/bash

# Loop 200 times
total_runs=200
for idx in $(seq 1 $total_runs); do
    # Change directory and submit job
    (cd "large/${idx}" && qsub submit.sh)
done
