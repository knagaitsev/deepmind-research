import os
import numpy as np

import pickle

def elementwise_mean(array_list):
    """
    Compute the element-wise mean across a list of NumPy arrays.

    Parameters:
    array_list (list of np.ndarray): List of NumPy arrays of the same shape.

    Returns:
    np.ndarray: Element-wise mean array.
    """
    return np.mean(np.array(array_list), axis=0)

def parse_silica_data(filepath):
    """Parses silica.data to extract atom positions sorted by ID."""
    atom_data = []

    with open(filepath, 'r') as file:
        for _ in range(5):
            next(file)

        bx = file.readline().strip().split(" ")
        bx_lo = float(bx[0])
        bx_hi = float(bx[1])

        by = file.readline().strip().split(" ")
        by_lo = float(by[0])
        by_hi = float(by[1])

        bz = file.readline().strip().split(" ")
        bz_lo = float(bz[0])
        bz_hi = float(bz[1])

        for _ in range(8):
            next(file)

        for line in file:
            if not line.strip():  # Stop at empty line
                break
            parts = line.split()
            if len(parts) < 7:
                continue  # Skip malformed lines
            atom_id = int(parts[0])
            atom_type = int(parts[2]) - 1
            x, y, z = map(float, (parts[4], parts[5], parts[6]))
            atom_data.append((atom_id, atom_type, x, y, z))

    # Sort by atom ID and store only positions
    atom_data.sort()
    init_positions = np.array([[x - bx_lo, y - by_lo, z - bz_lo] for _, _, x, y, z in atom_data])
    atom_types = np.array([atom_type for _, atom_type, _, _, _ in atom_data])
    box = np.array([bx_hi - bx_lo, by_hi - by_lo, bz_hi - bz_lo])

    return init_positions, atom_types, box

def parse_disp_atoms_data(filepath, target_timesteps):
    """
    Parses disp_atoms.data to extract c_disp[4] values for specified timesteps.
    
    Args:
        filepath (str): Path to disp_atoms.data.
        target_timesteps (list of int): List of timesteps to extract.
    
    Returns:
        list of np.ndarray: List of displacement arrays, one for each target timestep.
    """
    disp_data = []
    target_timesteps = sorted(target_timesteps)  # Ensure sorted order
    found_timesteps = set()
    current_displacements = None
    current_timestep = None

    with open(filepath, 'r') as file:
        for line in file:
            parts = line.split()

            if parts[0] == "ITEM:" and parts[1] == "TIMESTEP":
                current_timestep = int(next(file).strip())

                # Check if we need to capture this timestep
                if target_timesteps and current_timestep >= target_timesteps[0]:
                    found_timesteps.add(target_timesteps.pop(0))
                    current_displacements = []

            elif parts[0] == "ITEM:" and parts[1] == "ATOMS":
                if current_displacements is not None:
                    for _ in range(1080):  # Assuming fixed number of atoms
                        atom_line = next(file).split()
                        current_displacements.append(float(atom_line[-1]))  # Last column (c_disp[4])
                    
                    disp_data.append(np.array(current_displacements))
                    current_displacements = None  # Reset until next valid timestep

                if len(target_timesteps) == 0:  # Stop if all timesteps are found
                    break

    return disp_data

base_dir = "large-heat-up-data"
samples = {}

# Group velocity directories by sample
for entry in os.listdir(base_dir):
    if "-" in entry:
        sample_index, velocity_index = entry.split("-")
        sample_path = os.path.join(base_dir, entry)

        if sample_index not in samples:
            samples[sample_index] = []

        samples[sample_index].append((velocity_index, sample_path))

os.makedirs("silica-final/test", exist_ok=True)
os.makedirs("silica-final/train", exist_ok=True)

# Process each sample
pickle_idx = 0
for sample_index, velocity_dirs in samples.items():
    velocity_dirs.sort(key=lambda x: int(x[0]))  # Sort by velocity index
    first_velocity_dir = velocity_dirs[0][1]  # First velocity directory
    silica_data_path = os.path.join(first_velocity_dir, "silica.data")

    if os.path.exists(silica_data_path):
        init_positions, atom_types, box = parse_silica_data(silica_data_path)
        # print(f"Init positions shape: {init_positions.shape}, head: {init_positions[:10]}")
        # print(f"Atom types shape: {atom_types.shape}, head: {atom_types[:10]}")
        # print(f"Box: {box}")
    else:
        continue

    propensity_count = 0

    target_timesteps = [50000, 1000000, 1500000, 2000000, 2500000]

    timestep_groups = []
    for ts in target_timesteps:
        timestep_groups.append([])

    for velocity_index, velocity_path in velocity_dirs:
        disp_atoms_path = os.path.join(velocity_path, "disp_atoms.data")
        if os.path.exists(disp_atoms_path):
            propensity_count += 1
            res = parse_disp_atoms_data(disp_atoms_path, target_timesteps)
            for (i, v) in enumerate(res):
                timestep_groups[i].append(v)

    targets = []

    if propensity_count < len(target_timesteps):
        continue

    print(f"Groups count: {len(timestep_groups)}")

    for idx, g in enumerate(timestep_groups):
        vs = elementwise_mean(g)
        # print(f"Idx: {idx}, targets shape: {vs.shape}, targets_head: {vs[:2]}")
        targets.append(vs.tolist())

    d = {
        'positions': init_positions.tolist(),
        'types': atom_types.tolist(),
        'box': box.tolist(),
        'trajectory_target_positions': targets,
    }

    filename = f"aggregated_data_{pickle_idx}.pickle"

    p = f"silica-final/train/{filename}"
    if pickle_idx >= 100:
        p = f"silica-final/test/{filename}"

    with open(p, "wb") as f:
        pickle.dump(d, f)

    pickle_idx += 1

    print(f"Sample {sample_index}: {propensity_count} velocities")
