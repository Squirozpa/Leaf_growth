"""
Usage: python visualize/rgr.py results.csv [measured_data.csv]
"""
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

_RGR_AREA_DAYS = [44, 66, 80]
_RGR_AREA_MEASURED = [5.36e-2, 3.30e-2, 7.91e-3]

_RGR_WEIGHT_DAYS = [44, 66, 86]
_RGR_WEIGHT_MEASURED = [5.24e-2, 3.63e-2, 2.16e-2]

_DEFAULT_MEASURED = "data/Data Sheet 2 model.csv"


def _rgr(values, dt):
    return [(values[i + 1] - values[i]) / dt / values[i] for i in range(len(values) - 1)]


def plot_rgr_area(results_path, measured_data_path=None):
    df = pd.read_csv(results_path)
    t = df["time"].values
    dt = t[1] - t[0]

    fig, ax = plt.subplots(figsize=(10, 6))

    if measured_data_path is not None:
        try:
            mdf = pd.read_csv(measured_data_path)
            mdf.columns = mdf.columns.str.strip()
            mdf["Area cm2"] = mdf["area"] * 10000
            daily = mdf["Area cm2"].groupby(mdf.index // 24).mean().values
            model_rgr = [(daily[i + 1] - daily[i]) / daily[i] for i in range(len(daily) - 1)]
            ax.plot(np.linspace(t[0], t[-1], len(model_rgr)), model_rgr, color="black", label="Weraduwage et al. 2014 model")
        except FileNotFoundError:
            pass

    ax.scatter(
        np.linspace(t[0], t[-1], len(_RGR_AREA_DAYS)),
        _RGR_AREA_MEASURED,
        color="red", zorder=5, s=50, label="Measured RGR (Weraduwage et al. 2014)",
    )
    ax.plot(t[:-1], _rgr(df["leaf_area"].tolist(), dt), color="orange", label="Simulation")

    ax.set_xlabel("Time (days)")
    ax.set_ylabel("RGR leaf area (cm² cm⁻² day⁻¹)")
    ax.set_title("Relative growth rate of leaf area over time")
    ax.set_ylim(0, 0.25)
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.show()
    plt.close()


def plot_rgr_weight(results_path):
    df = pd.read_csv(results_path)
    t = df["time"].values
    dt = t[1] - t[0]
    total = (df["leaf_weight"] + df["shoot_weight"] + df["root_weight"]).tolist()

    fig, ax = plt.subplots(figsize=(6, 6))

    ax.scatter(
        np.linspace(t[0], t[-1], len(_RGR_WEIGHT_DAYS)),
        _RGR_WEIGHT_MEASURED,
        color="red", zorder=5, s=50, label="Measured RGR (Weraduwage et al. 2014)",
    )
    rgr = _rgr(total, dt)
    ax.plot(t[1:-1], rgr[1:], color="orange", label="Simulation")

    ax.set_xlabel("Time (days)")
    ax.set_ylabel("RGR total weight (g g⁻¹ day⁻¹)")
    ax.set_title("Relative growth rate of total weight over time")
    ax.set_ylim(0, 0.25)
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.show()
    plt.close()


if __name__ == "__main__":
    results = sys.argv[1] if len(sys.argv) > 1 else "results.csv"
    measured = sys.argv[2] if len(sys.argv) > 2 else _DEFAULT_MEASURED
    plot_rgr_area(results, measured)
    plot_rgr_weight(results)
