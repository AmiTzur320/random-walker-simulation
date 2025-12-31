import random

import helper
import slowZone
from walker import Walker
from portal import Portal
from obstacle import Obstacle
from trap import Trap
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import numpy as np
from slowZone import SlowZone
import pprint


class Simulation:
    """
        The Simulation class represents a simulation of walkers moving in a 2D space with various elements such as portals, obstacles, traps, and slow zones.
        """

    def __init__(self, walkers_list, portals_list, obstacles_list, trap_list,
                 slow_zone_list, num_steps, ice_option):
        """
        Initializes the simulation with the given walkers, portals, obstacles, traps, slow zones, number of steps and ice option.

        Parameters:
        walkers_list (list): A list of Walker objects participating in the simulation.
        portals_list (list): A list of Portal objects in the simulation.
        obstacles_list (list): A list of Obstacle objects in the simulation.
        trap_list (list): A list of Trap objects in the simulation.
        slow_zone_list (list): A list of SlowZone objects in the simulation.
        num_steps (int): The number of steps each walker will take in the simulation.
        ice_option (bool): An optional parameter that, if True, introduces a chance for the simulation to "freeze" for a short period.
        """
        self.walkers = walkers_list
        self.elements = portals_list + obstacles_list + trap_list + slow_zone_list
        self.num_steps = num_steps
        self.ice_option = ice_option

    def make_a_move(self, specific_walker: Walker) -> tuple[float, float]:
        """
        Makes a move for a specific walker and returns the new location after the move.

        Parameters:
        specific_walker (Walker): The walker that is to make a move.

        Returns:
        tuple[float, float]: The new location of the walker after the move.
        """
        new_location = specific_walker.new_loc_by_type()
        inside_element = False
        for element in self.elements:
            if isinstance(element, Portal) and element.is_inside_portal(new_location):
                """if the walker is inside a portal, move the walker to the exit point of the portal and break the 
                loop"""
                new_location = element.exit_point
                specific_walker.step(new_location)
                inside_element = True
                break

            elif isinstance(element, Obstacle) and element.is_inside_obstacle(new_location):
                """if the walker is inside an obstacle, break the loop and do not move the walker to the new location but 
                to the current location"""
                inside_element = True
                break


            elif isinstance(element, Trap):
                """if the walker in inside a trap, and new location is not inside the trap, move the walker to the 
                new"""
                if element.is_inside_trap(specific_walker, specific_walker.get_current_location()):
                    if not element.is_inside_trap(specific_walker, new_location):
                        inside_element = True
                        break
                elif not element.is_inside_trap(specific_walker,
                                                specific_walker.get_current_location()) and element.is_inside_trap(
                    specific_walker, new_location):
                    element.enter_trap(specific_walker)
                    specific_walker.step(new_location)
                    inside_element = True
                    break

            elif isinstance(element, SlowZone):
                if element.is_inside_slow_zone(specific_walker.get_current_location()):
                    if specific_walker in element.slowed_walkers:
                        break
                    specific_walker.slow_down()
                    element.enter_slow_zone(specific_walker)
                if not element.is_inside_slow_zone(specific_walker.get_current_location()):
                    if specific_walker in element.slowed_walkers:
                        element.slowed_walkers.remove(specific_walker)
                        specific_walker.regular_speed()

        if not inside_element:
            specific_walker.step(new_location)
            return new_location
        return specific_walker.get_current_location()

    def run(self) -> list[list[tuple[float, float]]]:
        """
                Runs the simulation for the specified number of steps and returns the paths of all walkers.
                Returns:
                list[list[tuple[float, float]]]: A list of paths of all walkers. Each path is a list of tuples representing the locations of a walker at each step.
                """
        paths = []
        for walker in self.walkers:
            path = [walker.current_location]
            for _ in range(self.num_steps):
                path.append(self.make_a_move(walker))
            paths.append(path)
        return paths

    def ice_probability_in_simulation(self) -> float:
        """
                Determines the probability of the simulation "freezing" based on the ice_option attribute.

                Returns:
                float: The probability of the simulation "freezing". If ice_option is False, the probability is 0.0001. Otherwise, the probability is randomly determined to be either 0.5 or 0.0001.
                """
        if self.ice_option is False:
            return 0.0001
        else:
            random_number = random.random()
            # If the random number is less than 0.5, pause for 0.3 seconds, else pause for 0.0001 seconds
            pause_time = 0.5 if random_number < 0.05 else 0.0001
            return pause_time

    def reset_walkers(self) -> None:
        """
               Resets all walkers to their initial state.

               Returns:
               None
               """
        for walk in self.walkers:
            walk.reset_walker()

    def get_walkers(self) -> list[Walker]:
        """
                Returns the list of walkers participating in the simulation.

                Returns:
                list[Walker]: The list of walkers participating in the simulation.
                """
        return self.walkers


if __name__ == '__main__':
    pass
