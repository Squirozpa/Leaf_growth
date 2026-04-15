"""
Usage: python visualize/leaf_area.py results.csv [measured_data.csv]
"""
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

_MEASURED_DAYS = [5, 26, 44, 66, 86]
_MEASURED_AREA = [0.05, 1.74e-1, 32.3, 148, 190]
_DEFAULT_MEASURED = "data/Data Sheet 2 model.csv"


def plot_leaf_area(results_path, measured_data_path=None):
    df = pd.read_csv(results_path)
    t = df["time"].values

    fig, ax = plt.subplots(figsize=(10, 6))

    if measured_data_path is not None:
        try:
            mdf = pd.read_csv(measured_data_path)
            mdf.columns = mdf.columns.str.strip()
            mdf["Area cm2"] = mdf["area"] * 10000
            daily_mean = mdf["Area cm2"].groupby(mdf.index // 24).mean()
            ax.plot(range(len(daily_mean)), daily_mean, color="black", label="Weraduwage et al. 2014 model")
        except FileNotFoundError:
            pass

    ax.scatter(
        np.linspace(t[0], t[-1], len(_MEASURED_DAYS)),
        _MEASURED_AREA,
        color="red", zorder=5, s=50, label="Measured (Weraduwage et al. 2014)",
    )
    ax.plot(t, df["leaf_area"], color="orange", label="Simulation")

    ax.set_xlabel("Time (days)")
    ax.set_ylabel("Leaf area (cm²)")
    ax.set_title("Leaf area over time")
    ax.grid(True)
    ax.legend()
    plt.tight_layout()
    plt.show()
    plt.close()


if __name__ == "__main__":
    results = sys.argv[1] if len(sys.argv) > 1 else "results.csv"
    measured = sys.argv[2] if len(sys.argv) > 2 else _DEFAULT_MEASURED
    plot_leaf_area(results, measured)
