import csv

_FIELDS = ["time", "leaf_weight", "leaf_area", "shoot_weight", "root_weight"]


def save_results(results, path):
    """Write simulation results to a CSV file at path."""
    n = len(results["time"])
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(_FIELDS)
        for i in range(n):
            writer.writerow([results[field][i] for field in _FIELDS])
