def michaelis_menten(S, vmax, Km):
    """Michaelis-Menten uptake rate. S: substrate concentration, vmax: max rate, Km: half-saturation constant."""
    return (vmax * S) / (Km + S)
