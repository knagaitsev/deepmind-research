import numpy as np
import matplotlib.pyplot as plt

# Define temperature (K) and diffusion coefficient (cm^2/s)
temperatures = np.array([1500, 1750, 2000, 2250, 2500, 2750, 3000])
diffusion_coefficients = np.array([5.84e-11, 6.59e-11, 2.52e-10, 7.42e-10, 4.50e-09, 3.14e-08, 1.36e-07]) * 1e-3  # Multiply everything by 10^4

# Create plot
plt.figure(figsize=(7, 5))  # Expanded padding by increasing figure size
plt.plot(temperatures, diffusion_coefficients, marker='o', linestyle='-', color='b')
plt.xlabel('Temperature (K)')
plt.ylabel('Diffusion Coefficient (m²/s)')
plt.title('Diffusion Coefficient vs. Temperature')
plt.grid(True)
plt.tight_layout()  # Adjust layout for better spacing

# Save to PDF
plt.savefig('diffusions.pdf', format='pdf')
plt.show()
