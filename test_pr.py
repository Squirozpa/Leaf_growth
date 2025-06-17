import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0.35, 1.0, 200)
b =0.7
a =84.9
y = a*(x -0.25)**b + 1

plt.figure(figsize=(5, 5))
plt.plot(x, y, 'k-', linewidth=2)
plt.xlabel("N_area (todavia no toy seguro de las unidades bien)", fontsize=12)
plt.ylabel("Maximum photosynthetic rate\n(µmol cm⁻² d⁻¹)", fontsize=12)
plt.ylim(0, 75)
plt.xlim(0.3, 1.05)
plt.grid(True, linestyle=':', linewidth=0.5)
plt.tight_layout()
plt.show()
