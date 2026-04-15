def L_R_opt(SNAR_adj, LR_0, a_LR, b_LR):
    """Optimal leaf-to-root ratio as a saturating function of SNAR_adj (section 3.2)."""
    return LR_0 + a_LR * SNAR_adj / (b_LR + SNAR_adj)


def L_R_adj(SNAR_adj, actual_ratio, LR_0, a_LR, b_LR, adjustment_factor):
    """Adjusted L:R ratio as the midpoint between actual and optimal (section 3.2)."""
    return actual_ratio + adjustment_factor * (L_R_opt(SNAR_adj, LR_0, a_LR, b_LR) - actual_ratio)
