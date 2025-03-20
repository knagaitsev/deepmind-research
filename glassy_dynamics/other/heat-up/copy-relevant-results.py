import os
import shutil

def copy_files(src_base_dir, dest_base_dir):
    # Loop through each directory inside the 'large-heat-up-data' directory
    for dir_name in os.listdir(src_base_dir):
        dir_path = os.path.join(src_base_dir, dir_name)
        
        # Check if it's a directory
        if os.path.isdir(dir_path):
            silica_file = os.path.join(dir_path, 'silica.data')
            disp_atoms_file = os.path.join(dir_path, 'disp_atoms.data')
            
            # Check if both files exist
            if os.path.isfile(silica_file) and os.path.isfile(disp_atoms_file):
                # Create destination directory if it doesn't exist
                dest_dir = os.path.join(dest_base_dir, dir_name)
                os.makedirs(dest_dir, exist_ok=True)
                
                # Copy files
                shutil.copy(silica_file, os.path.join(dest_dir, 'silica.data'))
                shutil.copy(disp_atoms_file, os.path.join(dest_dir, 'disp_atoms.data'))
                print(f"Copied files from {dir_name} to {dest_dir}")
            else:
                # Print the directory name if one or both files are missing
                print(f"Skipping {dir_name} as it is missing one or both files")

# Example usage
src_base_dir = 'large-heat-up'
dest_base_dir = 'large-heat-up-data'
copy_files(src_base_dir, dest_base_dir)
