import os
import shutil
import subprocess

def copy_silica_files():
    source_dirs = ["large"]
    destination_base = "large-heat-up"
    source_copy_dir = "copy-src"
    seed_idx = 1  # Unique seed index
    
    os.makedirs(destination_base, exist_ok=True)
    
    idx = 0
    target_dirs = []
    
    for source_dir in source_dirs:
        if not os.path.exists(source_dir):
            print(f"Warning: Source directory '{source_dir}' does not exist.")
            continue
        
        for dir_name in sorted(os.listdir(source_dir)):
            source_path = os.path.join(source_dir, dir_name, "silica.data")
            
            if os.path.exists(source_path):
                for i in range(0, 5):
                    dest_dir = os.path.join(destination_base, f"{idx}-{i}")
                    os.makedirs(dest_dir, exist_ok=True)
                    shutil.copy2(source_path, os.path.join(dest_dir, "silica.data"))
                    target_dirs.append(dest_dir)
                    
                    # Copy all files from heat-up-copy-src to target directory
                    if os.path.exists(source_copy_dir):
                        for file_name in os.listdir(source_copy_dir):
                            src_file_path = os.path.join(source_copy_dir, file_name)
                            dest_file_path = os.path.join(dest_dir, file_name)
                            
                            if file_name == "input.lammps":
                                with open(src_file_path, "r") as src_file, open(dest_file_path, "w") as dest_file:
                                    dest_file.write(f"variable Vseed equal {seed_idx}\n")
                                    dest_file.writelines(src_file.readlines())
                                seed_idx += 1
                            else:
                                shutil.copy2(src_file_path, dest_file_path)
                idx += 1
            else:
                print(f"Warning: '{dir_name}' in '{source_dir}' does not contain 'silica.data'.")
    
    # Execute qsub submit.sh in each target directory
    for target_dir in target_dirs:
        try:
            result = subprocess.run(["qsub", "submit.sh"], cwd=target_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"Error submitting job in {target_dir}")

if __name__ == "__main__":
    copy_silica_files()
