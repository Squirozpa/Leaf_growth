import numpy as np
from scipy.interpolate import interp1d

_x_leaf = np.array([1.87e-5, 8.86e-2, 3.94e-1, 5.17e-1])
_y_shoot = np.array([1.31e-10, 3.39e-7, 1.58e-2, 8.57e-2])
_y_shoot_log = np.log(_y_shoot)

_poly_R_shoot = np.poly1d(np.polyfit(_x_leaf, _y_shoot_log, 1))
_interp_mass = interp1d(_x_leaf, _y_shoot_log, kind="quadratic", bounds_error=False, fill_value="extrapolate")


def R_shoot(LW, method="interpolation"):
    """Shoot-to-leaf weight ratio R_shoot(LW) such that SW = LW · R_shoot(LW) (eq. 9)."""
    if method == "polynomial":
        return np.exp(_poly_R_shoot(LW)) / LW
    elif method == "interpolation":
        return np.exp(_interp_mass(LW)) / LW
    raise ValueError(f"Unknown method: {method}")
