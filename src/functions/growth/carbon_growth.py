from src.functions.carbon.balance import C_available
from src.functions.allometry.partition import k_weight, k_area
from src.functions.allometry.root_mass import R_root
from src.functions.allometry.shoot_mass import R_shoot
from src.functions.allometry.lma import LMA


def growth_carbon(t, dt, LW, LA, config):
    """
    Euler step for the carbon-only growth model.
    Returns (dLW, dLA, SW, RW).
    """
    p = config.physiology
    l = config.light

    RW = LW * R_root(LW)
    SW = LW * R_shoot(LW)

    C_avail = C_available(
        p.PR_base, LA, LW, p.p,
        p.r_root, RW,
        p.r_shoot, SW,
        p.r_leaf,
        l.max_irradiance_area, l.partial_shade_band_width,
    )
    dLW = (C_avail * k_weight(t) / (p.beta + p.rho)) * dt
    dLA = (C_avail * k_area(t) / ((p.beta + p.rho) * LMA(t))) * dt

    if dLW < 0:
        raise ValueError(f"Negative dLW ({dLW:.6f}) at t={t:.4f}. Check parameters.")

    return dLW, dLA, SW, RW
