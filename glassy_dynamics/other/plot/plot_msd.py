import os
import matplotlib.pyplot as plt
import numpy as np
import json

# Define the directory and files
# temps = [400, 440, 500, 550, 620]
temps = [2600]
# temps = [400]
# directories = [f"alphas/1.25/{temp}_degrees/msd_molecule.data" for temp in temps]
# directories = ["heat-up-2/msd_all.data"]
directories = ["large-heat-up-test/0-0/msd_all.data"]

# Initialize a list to hold the diffusion coefficients
diffusion_coefficients = []

# Set up the plot
plt.figure(figsize=(10, 6))

# Loop through each file and process the data
for (directory, temp) in zip(directories, temps):
    # Initialize lists to hold the timesteps and MSD totals
    timesteps = []
    msd_totals = []
    
    # Open the file and read the lines
    with open(directory, 'r') as file:
        # Skip the first two lines
        next(file)
        next(file)
        
        # Loop over the remaining lines in the file
        for line in file:
            # Split the line by whitespace
            columns = line.split()
            
            # Extract the Timestep and MSD total
            timesteps.append(int(columns[0]))  # Timestep is the first column
            msd_totals.append(float(columns[4]))  # MSD total is the fifth column

    # Convert timesteps to time (in femtoseconds)
    time = np.array(timesteps)  # Multiply timestep by .001 to get femtoseconds (metal units are in ps)
    time -= time[0]  # Subtract the initial timestep to normalize time to zero
    
    msd = np.array(msd_totals)
    
    # Fit the MSD data to the form MSD(t) = 6Dt
    # We want to fit to msd = 6 * D * time, so we fit to msd ~ time and compute D from the slope
    slope, intercept = np.polyfit(time, msd, 1)  # Linear fit: slope = 6D
    
    # Extract the diffusion coefficient (D)
    D = slope / 6  # The slope corresponds to 6D, so D = slope / 6
    diffusion_coefficients.append(D)
    
    # Plot the MSD vs Timestep for the current file
    plt.plot(time, msd, label=f"{temp}")
    
    # Generate the fitted line and plot it (using both slope and intercept)
    fitted_line = slope * time + intercept  # Equation of the fitted line
    plt.plot(time, fitted_line, linestyle='--', label=f"Fit: {temp}")

# Set both x and y axes to log scale
plt.xscale('log')
plt.yscale('log')

# Customize the plot
plt.title('MSD vs Timestep for Different Temperatures')
plt.xlabel('Time (fs)')
plt.ylabel('MSD Total (Å²)')
plt.legend(title='Temperature', loc='upper left')

# Save the figure as a PDF
plt.tight_layout()
plt.savefig('msd.pdf', format='pdf')

# Display the plot
plt.show()

# Print the diffusion coefficients for each temperature in Å²/fs
# for temp, D in zip(temps, diffusion_coefficients):
#     print(f"Temperature {temp} K: Diffusion Coefficient D = {D:.2e} Å²/fs")

# Convert the diffusion coefficients from Å²/fs to m²/s
D_m2_s = np.array(diffusion_coefficients) * 1e-20 * 1e15  # Conversion factor from Å²/fs to m²/s

for temp, D in zip(temps, D_m2_s):
    print(f"Temp: {temp} K, D = {D:.2e} m²/s")

# Take the natural logarithm of the diffusion coefficients
ln_D = np.log(D_m2_s)

# Print the raw array of ln(D)
print("\nNatural logarithm of (D (m²/s)):")
print(json.dumps(list(ln_D)))
