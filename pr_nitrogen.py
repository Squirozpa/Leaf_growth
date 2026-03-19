import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline, splrep, splev

## una curva que se parece a la de Suigura 2011 figura 1A
b = 2.7
a = 55.5
n_max = 0.9

def adjusted_pr(x, optimal_x):
    return a * (1 - np.exp(-b * (x / optimal_x)))
##Ajustamos a desface para que el maximo sea 0.5 umol cm⁻² d⁻¹ (estamos usando una tasa para concentración y por ende es asumiendo una tasa maxima por area de hoja)
def nitrogen_effect_on_photosynthesis(N_leaf, N_max=n_max):
    return adjusted_pr(N_leaf, N_max)


if __name__ == "__main__":
    x = np.linspace(0, 1, 200)
    y = nitrogen_effect_on_photosynthesis(x)
    plt.figure(figsize=(5, 5))
    plt.plot(x, y, 'k-', linewidth=2)
    plt.xlabel("$N_{area}^{in}$", fontsize=12)
    plt.ylabel("Maximum photosynthetic rate\n(µmolC cm⁻² d⁻¹)", fontsize=12)
    plt.ylim(0, 68)
    plt.xlim(0, n_max+0.2)
    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.tight_layout()
    plt.show()
