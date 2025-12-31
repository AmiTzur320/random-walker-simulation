from __future__ import annotations
from pathlib import Path
import json
from simulation3d import Simulation3d
from walker3d import Walker3d
from traps3d import Traps3d
from slowzone3d import SlowZone3d
from interactive3d import Interactive3d
from portal3d import Portal3d
from obstacle3d import Obstacle3d
from blackhole3d import BlackHole3d
from typing import Any


def create_simulation_with_config(config3d: dict[str, Any]) -> Simulation3d:
    """
    Creates a new Simulation3d instance with the given configuration.

    Parameters:
        config3d (dict[str, Any]): The configuration for the simulation.

    Returns:
        Simulation3d: A new Simulation3d instance.
    """
    walkers = [Walker3d(config3d["walker_type"], config3d["restart_option"]) for _ in
               range(config3d["num_concurrent_walkers"])]
    portals_list = [Portal3d() for _ in range(config3d["portals3d"])]
    obstacles_list = [Obstacle3d() for _ in range(config3d["obstacles3d"])]
    trap_list = [Traps3d() for _ in range(config3d["traps_amount"])]
    slow_zone_list = [SlowZone3d() for _ in range(config3d["slow_zone_amount"])]
    black_hole_list = [BlackHole3d() for _ in range(config3d["black_hole_amount"])]
    num_steps = config3d["num_steps"]
    ice_option = config3d["ice_option"]

    simulation3d = Simulation3d(
        walkers,
        portals3d_list=portals_list,
        obstacles3d_list=obstacles_list,
        walls3d_list=[],
        trap3d_list=trap_list,
        slow_zone3d_list=slow_zone_list,
        black_hole_list=black_hole_list,
        num_steps=num_steps,
        ice_option=ice_option,

    )
    return simulation3d


def interactive(config3d):
    """
    Creates a new interactive simulation with the given configuration.

    Parameters:
        config3d (dict[str, Any]): The configuration for the simulation.
    """
    simulation3d = create_simulation_with_config(config3d)
    simulation3d.ice_option = config3d["ice_option"]
    inter = Interactive3d(simulation3d)
    inter.set_initial_viewing_angle(30, 60)  # Add this line
    inter.plot_walk_3d()


def validate_config(config):
    necessary_keys = {
        "walker_type": {"type": int, "range": (1, 6)},
        "num_steps": {"type": int, "range": (1, 1000)},
        "num_concurrent_walkers": {"type": int, "range": (1, 50)},
        "portals3d": {"type": int, "range": (0, 5)},
        "obstacles3d": {"type": int, "range": (0, 5)},
        "traps_amount": {"type": int, "range": (0, 5)},
        "slow_zone_amount": {"type": int, "range": (0, 5)},
        "black_hole_amount": {"type": int, "range": (0, 5)},
        "ice_option": {"type": bool},
        "restart_option": {"type": bool}
    }

    for key, value in necessary_keys.items():
        expected_type = value["type"]
        if key not in config:
            print(f"Error: Missing key in configuration: {key}. Please try again.")
            return False
        if not isinstance(config[key], expected_type):
            print(
                f"Error: Unexpected type for key {key}. Expected {expected_type}, got {type(config[key])}. Please try again.")
            return False
        if "range" in value:
            min_val, max_val = value["range"]
            if not min_val <= config[key] <= max_val:
                print(
                    f"Error: Invalid value for key {key}. Expected a value between {min_val} and {max_val}, got {config[key]}. Please try again.")
                return False

    return True


def main(config: dict[str, Any]):
    """
    The main function of the program. It creates and runs an interactive simulation with the given configuration.

    Parameters:
        config (dict[str, Any]): The configuration for the simulation.
    """
    if not validate_config(config):
        return
    interactive(config)


if __name__ == "__main__":
    pass
