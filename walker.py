import math
import random
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
import helper

UNIT = 1
SLOW = 2
DIRECTIONS = ['r', 'l', 'u', 'd', 'origin']
BIAS = 30
FIFTY_PERCENT = 0.5
TEN_PERCENT = 0.1


class Walker:
    """
    The Walker class represents a walker in a 2D simulation.

    Attributes:
        current_location (tuple[float, float]): The current location of the walker.
        walker_type (int): The type of the walker.
        loc_history (list[tuple[float, float]]): The history of the walker's locations.
        walker_color (tuple[float, float, float]): The color of the walker.
        is_slower (bool): A flag indicating whether the walker is slower.
        restart_option (bool): A flag indicating whether the walker has the restart option.
    """

    def __init__(self, walker_type: int, restart_option: bool) -> None:
        """
        Constructs a new Walker instance with a specific type and restart option.
        """

        self.current_location = (0, 0)
        self.walker_type = walker_type
        self.loc_history: list[tuple[float,float]] = []
        self.walker_color = helper.generate_random_color()
        self.is_slower = False
        self.restart_option = restart_option

    def get_slope_from_direction(self, direction: str) -> float:
        """
        Returns the slope from a given direction.

        Parameters:
            direction (str): The direction.

        Returns:
            float: The slope from the direction.
        """

        x, y = self.get_current_location()
        if direction == 'r':
            return 0
        elif direction == 'l':
            return math.radians(180)
        elif direction == 'u':
            return math.radians(90)
        elif direction == 'd':
            return math.radians(270)
        elif direction == 'origin':
            return math.atan2(-y, -x)
        raise ValueError(f'Invalid direction: {direction}')

    def new_loc_by_type(self) -> tuple:
        """
        Returns the new location that the walker would move to, based on its type.

        Returns:
            tuple or bool: The new location or False if the walker type is not recognized.
        """

        if self.walker_type == 1:
            return self.random_walk1()
        elif self.walker_type == 2:
            return self.random_walk2()
        elif self.walker_type == 3:
            return self.random_walk3()
        elif self.walker_type == 4:
            return self.random_walk4()
        elif self.walker_type == 5:
            return self.random_walk5()
        elif self.walker_type == 6:
            return self.random_walk6()
        else:
            raise ValueError(f'Invalid walker type: {self.walker_type}')

    def step(self, new_location: tuple) -> None:
        """
        Updates the walker's location, with a probability of restart depending on input.

        Parameters:
            new_location (tuple): The new location.
        """

        self.loc_history.append(self.current_location)
        self.set_current_location(new_location)
        self.check_restart()

    def random_walk1(self) -> tuple:
        """
        Returns the new location for the random_walk1 step.

        Returns:
            tuple: The new location.
        """

        slope_radians = random.uniform(0, 2*math.pi)
        if self.is_slower is True:
            return self.calc_new_location(slope_radians, UNIT / SLOW)
        return self.calc_new_location(slope_radians, UNIT)

    def random_walk2(self) -> tuple:
        """
        Returns the new location for the random_walk2 step.

        Returns:
            tuple: The new location.
        """

        slope_radians = random.uniform(0, 2*math.pi)
        distance = random.uniform(0.5, 1.5)
        if self.is_slower is True:
            return self.calc_new_location(slope_radians, distance / SLOW)
        return self.calc_new_location(slope_radians, distance)

    def random_walk3(self) -> tuple:
        """
        Returns the new location for the random_walk3 step.

        Returns:
            tuple: The new location.
        """

        directions = helper.remove_direction(DIRECTIONS, 'origin')
        current_direction = random.choice(directions)
        slope_radians = self.get_slope_from_direction(current_direction)
        if self.is_slower is True:
            return self.calc_new_location(slope_radians, UNIT / SLOW)
        return self.calc_new_location(slope_radians, UNIT)

    def random_walk4(self) -> tuple:
        """
        Returns the new location for the random_walk4 step.

        Parameters:
            random_biased_direction (list[str]): The biased direction.

        Returns:
            tuple: The new location.
        """

        if random.random() <= TEN_PERCENT:
            slope_radians = math.pi + math.atan2(self.current_location[1], self.current_location[0])
        else:
            # slope_radians = random.uniform(0, 2*math.pi)
            slope_radians = self.get_slope_from_direction(random.choice(DIRECTIONS))

        if self.is_slower is True:
            return self.calc_new_location(slope_radians, UNIT / SLOW)
        return self.calc_new_location(slope_radians, UNIT)

    def random_walk5(self) -> tuple:
        """
        Returns the new location for the random_walk5 step.

        Returns:
            tuple: The new location.
        """

        alpha = 1.5
        step_length = np.random.pareto(alpha) + 1
        slope_radians = np.random.uniform(0, 2 * np.pi)
        if self.is_slower is True:
            return self.calc_new_location(slope_radians, step_length / SLOW)
        return self.calc_new_location(slope_radians, step_length)

    def random_walk6(self) -> tuple:
        """
        Returns the new location for the random_walk6 step.

        Returns:
            tuple: The new location.
        """

        num = random.random()
        if num < FIFTY_PERCENT:
            return self.get_current_location()
        else:
            slope_radians = random.uniform(0, 2 * np.pi)
            if self.is_slower is True:
                return self.calc_new_location(slope_radians, UNIT / SLOW)
            return self.calc_new_location(slope_radians, UNIT)

    def calc_new_location(self, slope_radians: float, distance: Union[int,float]) -> tuple:
        """
        Calculates the new location based on the slope and distance.

        Parameters:
            slope (float): The slope in radians.
            distance (int or float): The distance.

        Returns:
            tuple: The new location.
            """
        x, y = self.get_current_location()
        if distance == 1:
            return x + math.cos(slope_radians), y + math.sin(slope_radians)
        else:
            return distance * math.cos(slope_radians) + x, distance * math.sin(slope_radians) + y

    def set_current_location(self, loc: tuple) -> None:
        """sets the walker's current location"""
        self.current_location = loc

    def get_current_location(self) -> tuple:
        """gets the walker's current location"""
        return self.current_location

    def get_loc_history(self) -> list:
        """gets the walker's location history"""
        return self.loc_history

    def distance_from_origin(self) -> float:
        """calculates the walker's distance from the origin"""
        x, y = self.get_current_location()
        return math.sqrt(x ** 2 + y ** 2)

    def reset_walker(self) -> None:
        """resets the walker's location"""
        self.current_location = (0, 0)

    def slow_down(self) -> None:
        """slows the walker down by"""
        self.is_slower = True

    def regular_speed(self) -> None:
        """resets the walker's speed"""
        self.is_slower = False

    def check_restart(self) -> None:
        """checks if the walker should restart by the restart option and a random chance of 10%"""
        if self.restart_option and random.random() < TEN_PERCENT:
            self.reset_walker()


if __name__ == '__main__':
    pass
