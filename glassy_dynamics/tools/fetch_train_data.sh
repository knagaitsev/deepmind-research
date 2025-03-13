#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Directory to store the files, relative to the script location
DIR="${SCRIPT_DIR}/../data/temperature_044/train/"

# Create the directory if it doesn't exist
mkdir -p "$DIR"

# Loop to download files from 1 to 400
for i in $(seq 1 400)
do
    wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/public_dataset/temperature_044/train/aggregated_data_${i}.pickle" -P "$DIR"
done
