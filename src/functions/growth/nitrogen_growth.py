from src.functions.carbon.balance import C_available
from src.functions.nitrogen.michaelis_menten import michaelis_menten
from src.functions.nitrogen.photosynthesis import f_r_ph
from src.functions.nitrogen.leaf_root_ratio import L_R_adj
from src.functions.allometry.partition import k_weight, k_area
from src.functions.allometry.root_mass import R_root
from src.functions.allometry.shoot_mass import R_shoot
from src.functions.allometry.lma import LMA


def growth_nitrogen(t, dt, LW, LA, N_soil, config):
    """
    Euler step for the nitrogen-coupled growth model.
    N_soil: soil nitrogen concentration [N_soil] (µmol g⁻¹).
    Returns (dLW, dLA, SW, RW).
    """
    p = config.physiology
    n = config.nitrogen
    ph = config.photosynthesis
    l = config.light
    lr = config.leaf_root_ratio

    SW = LW * R_shoot(LW)

    SNAR_adj = michaelis_menten(N_soil, n.SNAR_max, n.K_m)
    actual_LR = 1.0 / R_root(LW)
    LR = L_R_adj(SNAR_adj, actual_LR, lr.LR_0, lr.a_LR, lr.b_LR, lr.adjustment_factor)
    RW = LW / LR

    N_in = SNAR_adj * RW
    N_leaf_area = (LW / (LW + SW + RW)) * N_in / LA
    r_ph = f_r_ph(N_leaf_area, ph.N_max, ph.a_PR, ph.b_PR)

    C_avail = C_available(
        r_ph, LA, LW, p.p,
        p.r_root, RW,
        p.r_shoot, SW,
        p.r_leaf,
        l.max_irradiance_area, l.partial_shade_band_width,
    )
    dLW = (C_avail * k_weight(t) / (p.beta + p.rho)) * dt
    dLA = (C_avail * k_area(t) / ((p.beta + p.rho) * LMA(t))) * dt

    return dLW, dLA, SW, RW
