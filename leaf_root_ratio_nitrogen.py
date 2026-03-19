import numpy as np
import matplotlib.pyplot as plt

# Parameters
a = 12.5     
b = 1900      

# Saturating curve
leaf_to_root_ratio = lambda SAR: 1.9 + a * SAR / (b + SAR)

def L_R(SAR):
    return leaf_to_root_ratio(SAR)

def adjusted_L_R(SAR, actual_ratio, adjustment_factor=0.5):
    """Adjust the leaf-to-root ratio based on actual weights."""
    optimal_ratio = L_R(SAR)
    adjustment = adjustment_factor * (optimal_ratio - actual_ratio)
    return actual_ratio + adjustment

if __name__ == "__main__":
    # Generate SAR values and actual ratios
    SAR_values = np.linspace(800, 3500, 100)  # SAR values in µmol N g⁻¹ d⁻¹
    actual_ratios = np.linspace(0.5, 15, 50)  # Actual L:R ratios

    # Create a meshgrid for SAR and actual ratios
    SAR_mesh, actual_ratio_mesh = np.meshgrid(SAR_values, actual_ratios)

    # Calculate adjusted ratios for the meshgrid
    adjusted_ratio_mesh = adjusted_L_R(SAR_mesh, actual_ratio_mesh)
    adjustment_strength_mesh = adjusted_ratio_mesh - actual_ratio_mesh

    # Create a 3D plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(111, projection='3d')

    # Plot the surface
    surf = ax.plot_surface(
        actual_ratio_mesh,  # X-axis: Actual ratio
        SAR_mesh,  # Z-axis: SAR values
        adjustment_strength_mesh,  # Y-axis: Adjusted ratio
        cmap='viridis',
        edgecolor='none',
        alpha=0.9
    )

    ax.set_xlabel('Actual L:R Ratio', fontsize=12)
    ax.set_zlabel('Adjusted L:R Ratio', fontsize=12)
    ax.set_ylabel('SNAR (µmol N g⁻¹ d⁻¹)', fontsize=12)
    ax.set_title('3D Plot of L:R Adjustment vs SNAR', fontsize=14)

    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=10, label='Adjusted Ratio')

    plt.tight_layout()
    plt.show()
    plt.close()

    plt.figure(figsize=(8, 6))
    plt.plot(SAR_values, L_R(SAR_values), 'b-', linewidth=2)
    plt.xlabel('SNAR (µmol N g⁻¹ d⁻¹)', fontsize=12)
    plt.ylabel('Optimal Leaf:Root Ratio', fontsize=12)
    plt.ylim(0, 12)
    plt.xlim(800, 3500)
    plt.grid(True, linestyle=':', linewidth=0.5)
    plt.title('Optimal Leaf:Root Ratio vs SNAR', fontsize=14)
    plt.tight_layout()
    plt.show()

