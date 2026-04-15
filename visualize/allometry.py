"""
Standalone plots for all fitted allometric relationships.
Usage: python visualize/allometry.py
"""
import numpy as np
import matplotlib.pyplot as plt

from src.functions.allometry.lma import _x_das, _lma_data, LMA, _interp_lma
from src.functions.allometry.root_mass import _x_leaf as _x_leaf_root, _z_root, _interp_mass as _interp_root_mass
from src.functions.allometry.shoot_mass import _x_leaf as _x_leaf_shoot, _y_shoot, _interp_mass as _interp_shoot_mass
from src.functions.allometry.partition import (
    _x_time, _leaf_partition, _leaf_area_partition, _interp_lp, _interp_lap,
)


def plot_LMA():
    x_fit = np.linspace(min(_x_das), max(_x_das), 100)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(_x_das, _lma_data, color="blue", label="Original data", zorder=3)
    ax.plot(x_fit, LMA(x_fit, method="inverse"), color="green", label="Logistic fit")
    ax.plot(x_fit, _interp_lma(x_fit), color="orange", linestyle="--", label="Quadratic interpolation")
    ax.set_xlabel("Days after sowing")
    ax.set_ylabel("LMA (g cm⁻²)")
    ax.set_title("Days after sowing vs Leaf Mass per Area (LMA)")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()


def plot_R_root():
    x_fit = np.linspace(min(_x_leaf_root), max(_x_leaf_root), 100)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(_x_leaf_root, _z_root, color="blue", label="Original data", zorder=3)
    ax.plot(x_fit, _interp_root_mass(x_fit), color="green", linestyle="--", label="Quadratic interpolation")
    ax.set_xlabel("LW — Leaf dry mass (g)")
    ax.set_ylabel("RW — Root dry mass (g)")
    ax.set_title("R_root: Leaf dry mass vs Root dry mass")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()


def plot_R_shoot():
    x_fit = np.linspace(min(_x_leaf_shoot), max(_x_leaf_shoot), 100)
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.scatter(_x_leaf_shoot, _y_shoot, color="blue", label="Original data", zorder=3)
    ax.plot(x_fit, np.exp(_interp_shoot_mass(x_fit)), color="green", linestyle="--", label="Quadratic interpolation")
    ax.set_xlabel("LW — Leaf dry mass (g)")
    ax.set_ylabel("SW — Shoot dry mass (g)")
    ax.set_title("R_shoot: Leaf dry mass vs Shoot dry mass")
    ax.legend()
    ax.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()


def plot_k():
    x_fit = np.linspace(min(_x_time), max(_x_time), 100)
    all_y = np.concatenate([_leaf_partition, _leaf_area_partition])
    y_min, y_max = all_y.min(), all_y.max()
    margin = (y_max - y_min) * 0.1

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    ax = axes[0]
    ax.scatter(_x_time, _leaf_partition, color="blue", label="Original data", s=50, zorder=3)
    ax.plot(x_fit, _interp_lp(x_fit), color="green", label="Quadratic interpolation")
    ax.set_xlabel("Days after sowing")
    ax.set_ylabel("k_weight")
    ax.set_title("Carbon allocation to leaf weight (k_weight)")
    ax.set_ylim(y_min - margin, y_max + margin)
    ax.grid(True, alpha=0.3)
    ax.legend()

    ax = axes[1]
    ax.scatter(_x_time, _leaf_area_partition, color="blue", label="Original data", s=50, zorder=3)
    ax.plot(x_fit, _interp_lap(x_fit), color="orange", label="Quadratic interpolation")
    ax.set_xlabel("Days after sowing")
    ax.set_ylabel("k_area")
    ax.set_title("Carbon allocation to leaf area (k_area)")
    ax.set_ylim(y_min - margin, y_max + margin)
    ax.grid(True, alpha=0.3)
    ax.legend()

    plt.tight_layout()
    plt.show()
    plt.close()


if __name__ == "__main__":
    plot_LMA()
    plot_R_root()
    plot_R_shoot()
    plot_k()
