from src.functions.carbon.effective_area import A_eff


def C_out_day(r_root, RW, r_shoot, SW, p):
    """Diurnal maintenance cost Ċ_out^day (eq. 4)."""
    return p * (r_root * RW + r_shoot * SW)


def C_out_night(r_leaf, LW, r_root, RW, r_shoot, SW, p):
    """Nocturnal maintenance cost Ċ_out^night (eq. 5)."""
    return (1 - p) * (r_leaf * LW + r_root * RW + r_shoot * SW)


def C_out(r_leaf, LW, r_root, RW, r_shoot, SW, p):
    """Total maintenance cost Ċ_out = LW·r_leaf·(1-p) + RW·r_root + SW·r_shoot (eq. 6)."""
    return LW * r_leaf * (1 - p) + RW * r_root + SW * r_shoot


def C_in(r_ph, LA, p, max_irradiance_area, partial_shade_band_width):
    """Carbon intake Ċ_in = r_ph · A_eff · p (eq. 2)."""
    return r_ph * A_eff(LA, max_irradiance_area, partial_shade_band_width) * p


def C_available(r_ph, LA, LW, p, r_root, RW, r_shoot, SW, r_leaf, max_irradiance_area, partial_shade_band_width):
    """Net available carbon Ċ_available = Ċ_in - Ċ_out (eq. 1)."""
    return (
        C_in(r_ph, LA, p, max_irradiance_area, partial_shade_band_width)
        - C_out(r_leaf, LW, r_root, RW, r_shoot, SW, p)
    )
