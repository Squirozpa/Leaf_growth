import numpy as np
import matplotlib.pyplot as plt

# Define the Gaussian function for leaf accumulation
def gaussian(x, aL, bL, cL):
    return aL * np.exp(-((x - bL)**2) / (2 * cL**2))

# Example values (adjust based on your specific case)
x_values = np.linspace(0, 150, 100)  # Time range in days
aL = 1.0  # Peak growth rate
bL = 75   # Time of peak leaf accumulation
cL = 20   # Width of significant leaf growth

# Generate the Gaussian curve
y_values = gaussian(x_values, aL, bL, cL)

# Plot the graph
plt.figure(figsize=(8, 5))
plt.plot(x_values, y_values, label="Leaf Accumulation Rate", color="green")
plt.axvline(x=bL, color='r', linestyle='--', label="Peak Leaf Growth (bL)")
plt.fill_between(x_values, y_values, where=((x_values >= bL-cL) & (x_values <= bL+cL)), color='yellow', alpha=0.3, label="Significant Growth Window (cL)")
plt.xlabel("Time (days)")
plt.ylabel("Growth Rate")
plt.title("Gaussian Distribution of Leaf Accumulation")
plt.legend()
plt.show()