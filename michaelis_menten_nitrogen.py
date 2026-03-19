import matplotlib.pyplot as plt
import numpy as np
Km = 400
vmax = 3360.96

def michaelis_menten(S, vmax=vmax, Km=Km):
    """
    Calculate the Michaelis-Menten rate of reaction.
    
    Parameters:
    S (float): Substrate concentration (e.g., soil nitrogen).
    
    Returns:
    float: Rate of reaction.
    """
    return (vmax * S) / (Km + S)


if __name__ == "__main__":
    fig = plt.figure(figsize=(8, 6))
    S_values = np.linspace(0, 3500, 500)  # Substrate concentration from 0 to 2000
    rates = [michaelis_menten(S) for S in S_values]
    plt.plot(S_values, rates, color='black', linewidth=2)
    plt.axhline(y=vmax, color='red', linestyle='--', label='Vmax = 3360.96')
    plt.axvline(x=Km, color='blue', linestyle='--', label='Km = 400')
    plt.legend()
    plt.title('Michaelis-Menten Kinetics')
    plt.xlabel('Substrate Concentration (S)')
    plt.ylabel('Rate of Reaction')
    plt.xlim(0, 3500)
    plt.ylim(0, 3500)
    plt.grid(True)
    plt.tight_layout()
    plt.show()
