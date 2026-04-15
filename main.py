import sys

from src.utils.config import Config
from src.utils.simulation import run_simulation
from src.utils.output import save_results

DEFAULT_PARAMS = "params/default.json"
DEFAULT_OUTPUT = "results.csv"


def main():
    params_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_PARAMS
    output_path = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_OUTPUT

    config = Config.from_json(params_path)
    results = run_simulation(config)
    save_results(results, output_path)
    print(f"Simulation complete. Results saved to {output_path}")


if __name__ == "__main__":
    main()
