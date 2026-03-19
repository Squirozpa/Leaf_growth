import matplotlib.pyplot as plt
import numpy as np

# Define the effective area function E_A(A) based on the LaTeX formula
def effective_area_function(A, max_irradiance_area=50, partial_shade_band_width=50):
    """
    Calculates the cumulative effective area based on total leaf area A.
    """
    if A < 0:
        raise ValueError("Leaf area (A) must be non-negative.")
    if A <= max_irradiance_area:
        return A
    elif A <= max_irradiance_area + partial_shade_band_width:
        area_in_segment = A - max_irradiance_area
        return max_irradiance_area + area_in_segment * (1 - 0.009 * area_in_segment)
    else:
        return max_irradiance_area + 27.5 + 0.1 * (A - (max_irradiance_area + partial_shade_band_width))

# Define the point-wise photosynthetic rate P(A) based on the initial description
def photosynthetic_rate_percentage(A):
    """
    Calculates the point-wise photosynthetic rate percentage for a given leaf area A.
    """
    if A < 0:
        raise ValueError("Leaf area (A) must be non-negative.")
    if A <= 50:
        return 100.0  # 100%
    elif A <= 100:
        return 100.0 - 1.8 * (A - 50)
    else:
        return 10.0  # 10%

if __name__ == "__main__":
    # Generate a range of leaf area values from 0 to 150
    A_values = np.linspace(0, 150, 500) 

    # Calculate effective area and photosynthetic rate for each A value
    effective_areas = [effective_area_function(A) for A in A_values]
    photosynthetic_rates = [photosynthetic_rate_percentage(A) for A in A_values]

    # Create the plots
    plt.figure(figsize=(12, 6))

    # Plot 1: Effective Area
    plt.subplot(1, 2, 1)  # 1 row, 2 columns, first plot
    plt.plot(A_values, effective_areas, label='Effective Area ($A_{eff}$)', color='green', linewidth=3.5)
    plt.title('Effective Area vs. Total Leaf Area')
    plt.xlabel('Total Leaf Area ($A$, cm$^2$)')
    plt.ylabel('Effective Area (cm$^2$)')
    plt.grid(True)
    plt.legend()
    plt.axvline(x=50, color='blue', linestyle='--', linewidth=2)
    plt.text(50, max(effective_areas) * 0.9, '50 cm²', color='blue', fontsize=10, rotation=90)
    plt.axvline(x=100, color='red', linestyle='--', linewidth=2)
    plt.text(100, max(effective_areas) * 0.9, '100 cm²', color='red', fontsize=10, rotation=90)

    # Plot 2: Photosynthetic Rate Percentage
    plt.subplot(1, 2, 2)  
    plt.plot(A_values, photosynthetic_rates, label='Photosynthetic Rate (%)', color='orange', linewidth=3.5)
    plt.title('Photosynthetic Rate vs. Total Leaf Area')
    plt.xlabel('Total Leaf Area ($A$, cm$^2$)')
    plt.ylabel('Photosynthetic Rate (%)')
    plt.grid(True)
    plt.legend()
    plt.axvline(x=50, color='blue', linestyle='--', linewidth=2)
    plt.text(50, max(photosynthetic_rates) * 0.9, '50 cm²', color='blue', fontsize=10, rotation=90)
    plt.axvline(x=100, color='red', linestyle='--', linewidth=2)
    plt.text(100, max(photosynthetic_rates) * 0.9, '100 cm²', color='red', fontsize=10, rotation=90)

    plt.tight_layout() 
    plt.show()