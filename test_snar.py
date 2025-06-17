import numpy as np
import matplotlib.pyplot as plt

# Parameters
SAR = np.linspace(0, 3500, 500)  # SAR values in µmol N g⁻¹ d⁻¹
a = 8.3       # asymptotic L:R at high SAR
b = 1100       # half-saturation SAR value (tune for shape)

# Saturating curve
L_R = 1.9 + a * SAR / (b + SAR)

# Plot
plt.figure(figsize=(6, 5))
plt.plot(SAR, L_R, linewidth=3, color='black')  # thick solid line
plt.xlabel('SAR (µmol N g⁻¹ d⁻¹)', fontsize=12)
plt.ylabel('Optimal L:R', fontsize=12)
plt.title('Optimal Leaf:Root Ratio vs SAR', fontsize=14)
plt.xlim(0, 3500)
plt.ylim(0, 20)
plt.grid(True)
plt.tight_layout()
plt.show()
