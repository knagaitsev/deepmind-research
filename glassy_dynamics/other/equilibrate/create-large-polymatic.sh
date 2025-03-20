#!/bin/bash

# Loop 200 times
total_runs=200
for idx in $(seq 1 $total_runs); do
    # Define the output directory
    out_dir="large2/${idx}"
    
    # Create the directory if it doesn't exist
    mkdir -p "$out_dir"
    
    # Run the command
    ./pack.pl -i 1 sio.data 120 -l 60 -o "$out_dir/sio-pack.data"
    
    # Remove lines 20-24 from the output file
    sed -i '' '20,24d' "$out_dir/sio-pack.data"
done
