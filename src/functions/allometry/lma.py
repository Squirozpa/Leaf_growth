import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

_x_das = np.array([5, 46, 66, 86])
_leaf_area = np.array([3.52e-2, 60.5, 171, 189])
_leaf_weight = np.array([1.87e-5, 8.86e-2, 3.74e-1, 5.17e-1])
_lma_data = _leaf_weight / _leaf_area


def _logistic(x, L, k, x0):
    return L / (1 + np.exp(-k * (x - x0)))


_params, _ = curve_fit(
    _logistic, _x_das, _lma_data, p0=[max(_lma_data), 0.1, np.median(_x_das)]
)
_interp_lma = interp1d(_x_das, _lma_data, kind="quadratic", bounds_error=False, fill_value="extrapolate")


def LMA(day, method="inverse"):
    """
    Leaf Mass per Area (g cm⁻²) as a function of days after sowing.
    Methods: 'inverse' (logistic fit), 'interpolation' (quadratic).
    """
    if method == "inverse":
        return _logistic(day, *_params)
    elif method == "interpolation":
        return _interp_lma(day)
    raise ValueError(f"Unknown method: {method}")
