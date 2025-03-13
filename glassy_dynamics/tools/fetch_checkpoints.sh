#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$(dirname "$(realpath "$0")")"

# Directory to store the files, relative to the script location
DIR="${SCRIPT_DIR}/../all_checkpoints/"

# Create the directory if it doesn't exist
mkdir -p "$DIR"

wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/glassy_dynamics_checkpoints/t044_salpha.ckpt.data-00000-of-00001" -P "$DIR"
wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/glassy_dynamics_checkpoints/t044_salpha.ckpt.index" -P "$DIR"
wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/glassy_dynamics_checkpoints/t044_salpha.ckpt.meta" -P "$DIR"

# Loop to download files from 1 to 9
for i in $(seq 1 9)
do
    wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/glassy_dynamics_checkpoints/t044_s0${i}.ckpt.data-00000-of-00001" -P "$DIR"
    wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/glassy_dynamics_checkpoints/t044_s0${i}.ckpt.index" -P "$DIR"
    wget "https://storage.googleapis.com/deepmind-research-glassy-dynamics/glassy_dynamics_checkpoints/t044_s0${i}.ckpt.meta" -P "$DIR"
done
