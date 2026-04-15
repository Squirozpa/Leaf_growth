def A_eff(LA, max_irradiance_area, partial_shade_band_width):
    """Effective photosynthetic area A_eff as a piecewise function of total leaf area LA (eq. 3)."""
    if LA < 0:
        raise ValueError("Leaf area must be non-negative.")
    if LA <= max_irradiance_area:
        return LA
    elif LA <= max_irradiance_area + partial_shade_band_width:
        band = LA - max_irradiance_area
        return max_irradiance_area + band * (1 - 0.009 * band)
    else:
        return max_irradiance_area + 27.5 + 0.1 * (LA - (max_irradiance_area + partial_shade_band_width))
