import numpy as np
from scipy.interpolate import interp1d

_x_leaf = np.array([2.45e-5, 8.86e-2, 3.94e-1, 5.17e-1])
_z_root = np.array([0.000001, 0.005516, 0.038069, 0.061947])

_poly_R_root = np.poly1d(np.polyfit(_x_leaf, _z_root / _x_leaf, 2))
_interp_mass = interp1d(_x_leaf, _z_root, kind="quadratic", bounds_error=False, fill_value="extrapolate")


def R_root(LW, method="interpolation"):
    """Root-to-leaf weight ratio R_root(LW) such that RW = LW · R_root(LW) (eq. 9)."""
    if method == "polynomial":
        return _poly_R_root(LW)
    elif method == "interpolation":
        return _interp_mass(LW) / LW
    raise ValueError(f"Unknown method: {method}")
