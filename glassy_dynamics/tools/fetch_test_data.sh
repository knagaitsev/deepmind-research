#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Directory to store the files, relative to the script location
DIR="${SCRIPT_DIR}/../data/temperature_044/test/"

# Create the directory if it doesn't exist
mkdir -p "$DIR"

# Loop to download files from 10001 to 10050
for i in $(seq 10001 10050)
do
    wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/public_dataset/temperature_044/test/aggregated_data_${i}.pickle" -P "$DIR"
done
