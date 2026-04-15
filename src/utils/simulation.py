from src.functions.allometry.lma import LMA
from src.functions.allometry.root_mass import R_root
from src.functions.allometry.shoot_mass import R_shoot
from src.functions.growth.carbon_growth import growth_carbon
from src.functions.growth.nitrogen_growth import growth_nitrogen


def run_simulation(config):
    """
    Run Euler integration for a single scenario determined by config.simulation.nitrogen.
    nitrogen == -1 runs the carbon-only model; any other value runs the nitrogen model.
    Returns a dict with keys: time, leaf_weight, leaf_area, shoot_weight, root_weight.
    """
    sim = config.simulation
    dt = sim.dt
    num_steps = int((sim.total_time - sim.start_time) / dt)
    use_nitrogen = sim.nitrogen >= 0

    LW = sim.starting_leaf_area * LMA(sim.start_time)
    LA = sim.starting_leaf_area

    results = {"time": [], "leaf_weight": [], "leaf_area": [], "shoot_weight": [], "root_weight": []}

    def record(t, LW, LA, SW, RW):
        results["time"].append(float(t))
        results["leaf_weight"].append(float(LW))
        results["leaf_area"].append(float(LA))
        results["shoot_weight"].append(float(SW))
        results["root_weight"].append(float(RW))

    record(sim.start_time, LW, LA, LW * R_shoot(LW), LW * R_root(LW))

    current_t = sim.start_time
    for _ in range(num_steps):
        if use_nitrogen:
            dLW, dLA, SW, RW = growth_nitrogen(current_t, dt, LW, LA, sim.nitrogen, config)
        else:
            dLW, dLA, SW, RW = growth_carbon(current_t, dt, LW, LA, config)
        LW += dLW
        LA += dLA
        current_t += dt
        record(current_t, LW, LA, SW, RW)

    return results
