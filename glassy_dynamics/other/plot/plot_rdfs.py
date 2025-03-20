import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial.distance import pdist, squareform

def parse_atoms(filename):
    atom_types = []
    positions = []
    
    with open(filename, 'r') as f:
        lines = f.readlines()
        read_atoms = False
        for line in lines:
            if "Atoms" in line:
                read_atoms = True
                continue
            if read_atoms and line.strip():
                parts = line.split()
                if len(parts) < 7:
                    continue  # Ensure the line has enough columns
                atom_types.append(int(parts[2]))  # Atom type (1 or 2)
                positions.append([float(parts[4]), float(parts[5]), float(parts[6])])  # x, y, z
    
    return np.array(atom_types), np.array(positions)

def compute_rdf(atom_types, positions, dr=0.1, r_max=10.0):
    distances = pdist(positions)
    bins = np.arange(0, r_max, dr)
    rdf_11 = np.zeros(len(bins) - 1)
    rdf_12 = np.zeros(len(bins) - 1)
    rdf_22 = np.zeros(len(bins) - 1)
    
    pair_indices = np.triu_indices(len(positions), k=1)
    type_i = atom_types[pair_indices[0]]
    type_j = atom_types[pair_indices[1]]
    
    for d, ti, tj in zip(distances, type_i, type_j):
        bin_index = np.digitize(d, bins) - 1
        if bin_index < len(rdf_11):
            if ti == 1 and tj == 1:
                rdf_11[bin_index] += 2  # Each pair is counted twice
            elif (ti == 1 and tj == 2) or (ti == 2 and tj == 1):
                rdf_12[bin_index] += 2
            elif ti == 2 and tj == 2:
                rdf_22[bin_index] += 2
    
    # Normalize
    volume = 4/3 * np.pi * (np.power(bins[1:], 3) - np.power(bins[:-1], 3))
    density = len(positions) / (np.max(positions[:, 0])**3)  # Approximate uniform density
    norm_factor = density * volume
    
    rdf_11 /= norm_factor
    rdf_12 /= norm_factor
    rdf_22 /= norm_factor
    
    return bins[:-1], rdf_11, rdf_12, rdf_22

def plot_rdf(bins, rdf_11, rdf_12, rdf_22, filename):
    plt.figure(figsize=(8, 6))
    plt.plot(bins, rdf_11, label='Si-Si', linestyle='-')
    plt.plot(bins, rdf_12, label='Si-O', linestyle='-')
    plt.plot(bins, rdf_22, label='O-O', linestyle='-')
    plt.xlabel('r (Angstrom)')
    plt.ylabel('g(r)')
    plt.legend()
    plt.grid()
    plt.savefig(filename)
    plt.show()

# Example usage
filename = 'silica.data'
atom_types, positions = parse_atoms(filename)
bins, rdf_11, rdf_12, rdf_22 = compute_rdf(atom_types, positions)
plot_rdf(bins, rdf_11, rdf_12, rdf_22, 'rdf_output.pdf')
