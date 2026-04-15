import numpy as np
from scipy.interpolate import interp1d

_x_time = np.array([26, 44, 66, 86])
_leaf_partition = np.array([0.71, 0.70, 0.49, 0.20])
_leaf_area_partition = np.array([0.57, 0.56, 0.42, 0.12])

_poly_k_weight = np.poly1d(np.polyfit(_x_time, _leaf_partition, 2))
_poly_k_area = np.poly1d(np.polyfit(_x_time, _leaf_area_partition, 2))
_interp_lp = interp1d(_x_time, _leaf_partition, kind="quadratic", bounds_error=False, fill_value="extrapolate")
_interp_lap = interp1d(_x_time, _leaf_area_partition, kind="quadratic", bounds_error=False, fill_value="extrapolate")


def k_weight(day, method="polynomial"):
    """Carbon allocation fraction to leaf weight growth (eq. 6)."""
    if method == "polynomial":
        return _poly_k_weight(day)
    elif method == "interpolation":
        return _interp_lp(day)
    raise ValueError(f"Unknown method: {method}")


def k_area(day, method="interpolation"):
    """Carbon allocation fraction to leaf area expansion (eq. 7)."""
    if method == "polynomial":
        return _poly_k_area(day)
    elif method == "interpolation":
        return _interp_lap(day)
    raise ValueError(f"Unknown method: {method}")
