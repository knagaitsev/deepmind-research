#!/bin/bash

# Define source directory
SRC_DIR="copy-src"

# Define target parent directory
TARGET_PARENT_DIR="large"

# Ensure source directory exists
if [ ! -d "$SRC_DIR" ]; then
    echo "Source directory '$SRC_DIR' does not exist. Exiting."
    exit 1
fi

# Loop through each subdirectory in the target parent directory
for TARGET_DIR in "$TARGET_PARENT_DIR"/*/; do
    # Ensure it's a directory
    if [ -d "$TARGET_DIR" ]; then
        echo "Copying files to: $TARGET_DIR"
        cp -r "$SRC_DIR"/* "$TARGET_DIR"
    fi
done

echo "Copy operation completed."
