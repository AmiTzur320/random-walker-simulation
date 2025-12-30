from __future__ import annotations

import csv
from pathlib import Path
import json
from typing import List
import helper
from simulation import Simulation
from interactive import Interactive
from walker import Walker
from portal import Portal
from obstacle import Obstacle
from pprint import pprint
import math
import matplotlib.pyplot as plt
import sys
from typing import Any, Dict, Union
from trap import Trap
from slowZone import SlowZone

TEN_RADIUS = 10



def avg(lst: List[Union[float,int]]) -> float:
    """
    Calculates the average of a list of floats.

    Parameters:
        lst (list[float]): The list of floats.

    Returns:
        float: The average of the list.
    """

    return sum(lst) / len(lst)


def distance_from_origin(point: tuple[float, float]) -> float:
    """
    Calculates the distance of a point from the origin.

    Parameters:
        point (tuple[float,float]): The point.

    Returns:
        float: The distance of the point from the origin.
    """

    return math.sqrt(point[0] ** 2 + point[1] ** 2)


def distance_from_origin_at_end_of_path(path: list[tuple[float, float]]) -> float:
    """
    Calculates the distance of the last point in a path from the origin.

    Parameters:
        path (list[tuple[float, float]]): The path.

    Returns:
        float: The distance of the last point in the path from the origin.
    """

    return distance_from_origin(path[-1])


def distance_from_x_axis_at_end_of_path(path: list[tuple[float, float]]) -> float:
    """
    Calculates the distance of the last point in a path from the x-axis.

    Parameters:
        path (list[tuple[float, float]]): The path.

    Returns:
        float: The distance of the last point in the path from the x-axis.
    """

    return abs(path[-1][1])


def distance_from_y_axis_at_end_of_path(path: list[tuple[float, float]]) -> float:
    """
    Calculates the distance of the last point in a path from the y-axis.

    Parameters:
        path (list[tuple[float, float]]): The path.

    Returns:
        float: The distance of the last point in the path from the y-axis.
    """

    return abs(path[-1][0])


def num_steps_until_exit_circle(path: list[tuple[float, float]]) -> Union[int,float] | None:
    """
    Calculates the number of steps until a path exits a circle of radius 10.

    Parameters:
        path (list[tuple[float, float]]): The path.

    Returns:
        int | None: The number of steps until the path exits the circle, or None if the path never exits the circle.
    """

    for i, point in enumerate(path):
        if distance_from_origin(point) > 10:
            return i
    return None


def num_y_axis_crosses(path: list[tuple[float, float]]) -> Union[int,float]:
    """
    Calculates the number of times a path crosses the y-axis.

    Parameters:
        path (list[tuple[float, float]]): The path.

    Returns:
        int: The number of times the path crosses the y-axis.
    """

    total = 0
    for i in range(1, len(path)):
        if path[i][0] * path[i - 1][0] < 0:
            total += 1
    return total


def calculate_stats(paths: list[list[tuple[float, float]]], stats: dict[str, dict[int, float]], num_steps: int) -> dict[
    str, dict[int, float]]:
    """
    Calculates various statistics for a list of paths.

    Parameters:
        paths (list[list[tuple[float, float]]]): The list of paths.
        stats (dict[str, dict[int, float]]): The current statistics.
        num_steps (int): The number of steps.

    Returns:
        dict[str, dict[int, float]]: The updated statistics.
    """

    distances_from_origin_at_end_of_path = [distance_from_origin_at_end_of_path(path) for path in paths]
    num_steps_until_exit_circle_stats = [num_steps_until_exit_circle(path) for path in paths]
    clean_num_steps_stats = [num for num in num_steps_until_exit_circle_stats if (num is not None)]
    distances_from_x_axis_at_end_of_path = [distance_from_x_axis_at_end_of_path(path) for path in paths]
    distances_from_y_axis_at_end_of_path = [distance_from_y_axis_at_end_of_path(path) for path in paths]
    num_walker_crosses = [num_y_axis_crosses(path) for path in paths]

    stats["avg_distance_from_origin"][num_steps] = avg(distances_from_origin_at_end_of_path)
    stats["avg_distance_from_x_axis"][num_steps] = avg(distances_from_x_axis_at_end_of_path)
    stats["avg_distance_from_y_axis"][num_steps] = avg(distances_from_y_axis_at_end_of_path)
    if len(clean_num_steps_stats) > 0:
        stats["avg_num_steps_to_exit_circle"][num_steps] = avg(clean_num_steps_stats)
    stats["avg_total_walker_crosse_y_axis"][num_steps] = avg(num_walker_crosses)
    return stats


def stats_to_png(stats: dict[str, dict[int, float]]) -> None:
    """
    Saves the statistics as a PNG image.

    Parameters:
        stats (dict[str, dict[int, float]]): The statistics.
    """

    for stat_name, stat in stats.items():
        plt.close("all")
        plt.title(stat_name)
        plt.xlabel("N (num of steps)")
        plt.ylabel(stat_name)
        plt.plot(list(stat.keys()), list(stat.values()))
        plt.savefig(f'{stat_name}.png')


def stats_to_csv(stats: dict[str, dict[int, float]]) -> None:
    """
    Saves the statistics as a CSV file.

    Parameters:
        stats (dict[str, dict[int, float]]): The statistics.
    """

    with open('stats.csv', 'w', newline='') as csvfile:
        fieldnames = ['num_steps', 'avg_distance_from_origin', 'avg_distance_from_x_axis', 'avg_distance_from_y_axis',
                      'avg_num_steps_to_exit_circle', 'avg_total_walker_crosse_y_axis']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for num_steps in stats["avg_distance_from_origin"].keys():
            writer.writerow({
                'num_steps': num_steps,
                'avg_distance_from_origin': stats["avg_distance_from_origin"].get(num_steps, ''),
                'avg_distance_from_x_axis': stats["avg_distance_from_x_axis"].get(num_steps, ''),
                'avg_distance_from_y_axis': stats["avg_distance_from_y_axis"].get(num_steps, ''),
                'avg_num_steps_to_exit_circle': stats["avg_num_steps_to_exit_circle"].get(num_steps, ''),
                'avg_total_walker_crosse_y_axis': stats["avg_total_walker_crosse_y_axis"].get(num_steps, '')
            })


def create_simulation_with_config(config: dict[str, Any]) -> Simulation:
    """
    Creates a new Simulation instance with the given configuration.

    Parameters:
        config (dict[str, Any]): The configuration for the simulation.

    Returns:
        Simulation: A new Simulation instance.
    """

    walkers = [Walker(config["walker_type"], config["restart_option"]) for _ in range(config["num_concurrent_walkers"])]
    ice_option = config["ice_option"]
    # num_steps = config["num_steps_for_statistics"][-1]
    num_steps = config["num_steps"]

    if isinstance(config["portals_list"], list) and isinstance(config["portals_list"][0], dict):
        portals_list = [Portal(p["exit_point"], p["length"], p["center_loc"]) for p in config["portals_list"]]
        obstacles_list = [Obstacle(o["length"], o["center_loc"]) for o in config["obstacles_list"]]
    else:
        portals_list = [Portal() for _ in range(config["portals_list"])]
        obstacles_list = [Obstacle() for _ in range(config["obstacles_list"])]

    trap_list = [Trap() for _ in range(config["traps_amount"])]
    slow_zone_list = [SlowZone() for _ in range(config["slow_zone_amount"])]

    simulation = Simulation(
        walkers,
        portals_list=portals_list,
        obstacles_list=obstacles_list,
        trap_list=trap_list,
        slow_zone_list=slow_zone_list,
        num_steps=num_steps,
        ice_option=ice_option
    )
    return simulation


def non_interactive(config: dict[str, Any]):
    """
    Runs a non-interactive simulation with the given configuration.

    Parameters:
        config (dict[str, Any]): The configuration for the simulation.
    """

    stats:Dict[str, Dict[int, float]] = {
        "avg_distance_from_origin": {},
        "avg_distance_from_x_axis": {},
        "avg_distance_from_y_axis": {},
        "avg_num_steps_to_exit_circle": {},
        "avg_total_walker_crosse_y_axis": {}
    }
    for num_steps in config["num_steps_for_statistics"]:
        print(f"running simulation on {num_steps} steps ({config['num_runs']} times)")
        paths = []
        for _ in range(config["num_runs"]):
            simulation = create_simulation_with_config(config)
            simulation.num_steps = num_steps
            paths += simulation.run()
        calculate_stats(paths, stats, num_steps)
    stats_to_png(stats)
    stats_to_csv(stats)
    print("done!")


def interactive(config: dict[str, Any]):
    """
    Runs an interactive simulation with the given configuration.

    Parameters:
        config (dict[str, Any]): The configuration for the simulation.
    """

    simulation = create_simulation_with_config(config)
    simulation.ice_option = config["ice_option"]
    Interactive(simulation).plot_walk()

def validate_config(config):
    necessary_keys = {
        "walker_type": {"type": int, "range": (1, 6)},
        "num_steps": {"type": int, "range": (1, 1000)},
        "num_steps_for_statistics": {"type": list},
        "num_concurrent_walkers": {"type": int, "range": (1, 50)},
        "num_runs": {"type": int, "range": (1, 50)},
        "portals_list": {"type": list},
        "obstacles_list": {"type": list},
        "traps_amount": {"type": int, "range": (0, 5)},
        "slow_zone_amount": {"type": int, "range": (0, 5)},
        "ice_option": {"type": bool},
        "restart_option": {"type": bool},
        "check_interactive_or_non": {"type": bool}
    }

    for key, value in necessary_keys.items():
        expected_type = value["type"]
        if key not in config:
            print(f"Error: Missing key in configuration: {key}. Please try again.")
            return False
        if not isinstance(config[key], expected_type):
            print(f"Error: Unexpected type for key {key}. Expected {expected_type}, got {type(config[key])}. Please try again.")
            return False
        if "range" in value:
            min_val, max_val = value["range"]
            if not min_val <= config[key] <= max_val:
                print(f"Error: Invalid value for key {key}. Expected a value between {min_val} and {max_val}, got {config[key]}. Please try again.")
                return False

    return True

def main(argv):
    config = None
    if len(argv) > 0:
        try:
            with open(argv[0]) as file:
                config = json.load(file)
        except Exception as e:
            print(f"Error loading configuration from {argv[0]}: {e}")
            return
    else:
        try:
            config_str = Path("config.json").read_text()
            config = json.loads(config_str)
        except Exception as e:
            print(f"Invalid config: {e}")
            return

    if not validate_config(config):
        return

    if config["check_interactive_or_non"] is True:
        interactive(config)
    else:
        non_interactive(config)

if __name__ == "__main__":
    main(sys.argv[1:])