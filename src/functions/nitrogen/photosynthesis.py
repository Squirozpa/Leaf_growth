import numpy as np


def f_r_ph(N_leaf_area, N_max, a_PR, b_PR):
    """
    Photosynthetic rate r_ph as a function of leaf nitrogen area concentration N_leaf^area.
    r_ph = f(N_leaf^area) (section 3.2). Returns rate in µmol C cm⁻² d⁻¹.
    """
    return a_PR * (1 - np.exp(-b_PR * (N_leaf_area / N_max)))
