import math
import random
from typing import Union

import numpy as np
import helper

UNIT = 1
SLOW = 4
DIRECTIONS = ['r', 'l', 'u', 'd', 'origin']
SMALL_CONSTANT = 1e-9
BIAS = 30
FIFTY_PERCENT = 0.5
TEN_PERCENT = 0.1


class Walker3d:
    """
     The Walker3d class represents a walker in a 3D simulation.

     Attributes:
         current_location_3d (tuple[float, float, float]): The current location of the walker.
         walker_type (int): The type of the walker.
         loc_history (list[tuple[float, float, float]]): The history of the walker's locations.
         walker_color (tuple[float, float, float]): The color of the walker.
         is_slower (bool): A flag indicating whether the walker is slower.
         restart_option (bool): A flag indicating whether the walker has the restart option.
     """

    def __init__(self, walker_type: int, restart_option=False) -> None:

        """
        Constructs a new Walker3d instance with a specific type and restart option.
        """

        self.current_location_3d = (0, 0, 0)
        self.walker_type = walker_type
        self.loc_history: list[tuple[float, float, float]] = []
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
        x, y, z = self.get_current_location_3d()
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

    def new_loc_by_type_3d(self) -> tuple[float, float, float]:
        """
        Returns the new location that the walker would move to, based on its type.

        Returns:
            tuple[float, float, float]: The new location.
        """
        if self.walker_type == 1:  # random direction, distance of 1 unit
            return self.random_walk1_3d()
        elif self.walker_type == 2:  # random direction, distance of 0.5-1.5 units
            return self.random_walk2_3d()
        elif self.walker_type == 3:  # four district directions
            return self.random_walk3_3d()
        elif self.walker_type == 4:  # random walk with bias
            biased_direction = random.choice(DIRECTIONS)
            return self.random_walk4_3d([biased_direction])
        elif self.walker_type == 5:  # levy flight-there is a chance that a step will be very long
            return self.random_walk5_3d()
        elif self.walker_type == 6:  # random walk with rest
            return self.random_walk6_3d()
        return 0, 0, 0

    def step(self, new_location3d: tuple[float, float, float]) -> tuple[float, float, float]:
        """
        Updates the walker's location, with a probability of restart depending on input.

        Parameters:
            new_location3d (tuple[float, float, float]): The new location.

        Returns:
            tuple[float, float, float]: The updated location.
        """

        if new_location3d is not None:
            self.loc_history.append(self.current_location_3d)
            self.set_current_location_3d(new_location3d)
        self.check_restart()
        return self.get_current_location_3d()

    def random_walk1_3d(self) -> tuple[float, float, float]:
        """
        Returns the new location for the random_walk1 step.

        Returns:
            tuple[float, float, float]: The new location.
        """

        theta = random.uniform(0, 2 * math.pi)  # random angle for rotation around z-axis
        phi = random.uniform(0, math.pi)  # random angle for rotation from z-axis towards x-y plane
        if self.is_slower is True:
            return self.calc_new_location_3d(theta, phi, UNIT / SLOW)
        return self.calc_new_location_3d(theta, phi, UNIT)

    def random_walk2_3d(self) -> tuple[float, float, float]:
        """
        Returns the new location for the random_walk2 step.

        Returns:
            tuple[float, float, float]: The new location.
        """

        theta = random.uniform(0, 360)
        phi = random.uniform(0, math.pi)
        distance = random.uniform(0.5, 1.5)
        if self.is_slower is True:
            return self.calc_new_location_3d(theta, phi, distance / SLOW)
        return self.calc_new_location_3d(theta, phi, distance)

    def random_walk3_3d(self) -> tuple[float, float, float]:
        """
        Returns the new location for the random_walk3 step.

        Returns:
            tuple[float, float, float]: The new location.
        """

        directions = helper.remove_direction(DIRECTIONS, 'origin')
        current_direction_for_theta = random.choice(directions)
        theta = self.get_slope_from_direction(current_direction_for_theta)
        new_direction_for_phi = random.choice(directions)
        phi = self.get_slope_from_direction(random.choice(new_direction_for_phi))
        if self.is_slower is True:
            return self.calc_new_location_3d(theta, phi, UNIT / SLOW)
        return self.calc_new_location_3d(theta, phi, UNIT)

    def random_walk4_3d(self, random_biased_direction: list[str]) -> tuple[float, float, float]:
        """
        Returns the new location for the random_walk4 step using
        BIAS number in order to make the probability of a certain direction to be higher.

        Parameters:
            random_biased_direction (list[str]): The biased direction.

        Returns:
            tuple[float, float, float]: The new location.
        """
        new_direction_list = DIRECTIONS + random_biased_direction * BIAS
        current_direction_for_theta = random.choice(new_direction_list)
        theta = self.get_slope_from_direction(current_direction_for_theta)
        phi = self.get_slope_from_direction(random.choice(DIRECTIONS))
        if self.is_slower is True:
            return self.calc_new_location_3d(theta, phi, UNIT / SLOW)
        return self.calc_new_location_3d(theta, phi, UNIT)

    def random_walk5_3d(self) -> tuple[float, float, float]:
        """
        Returns the new location for the random_walk5 step,
        which is a Lévy flight (there is a chance that a step will be longer).

        Returns:
            tuple[float, float, float]: The new location.
        """
        alpha = 1.5
        step_length = np.random.pareto(alpha) + 1
        theta = np.random.uniform(0, 2 * np.pi)
        phi = np.random.uniform(0, np.pi)
        if self.is_slower is True:
            return self.calc_new_location_3d(theta, phi, step_length / SLOW)
        return self.calc_new_location_3d(theta, phi, step_length)

    def random_walk6_3d(self) -> tuple[float, float, float]:
        """
        Returns the new location for the random_walk6 step - there is a chance of a walker taking a rest.

        Returns:
            tuple[float, float, float]: The new location.
        """

        num = random.random()
        if num < TEN_PERCENT:
            return self.get_current_location_3d()
        else:
            theta = random.uniform(0, 2 * np.pi)
            phi = random.uniform(0, math.pi)
            if self.is_slower is True:
                return self.calc_new_location_3d(theta, phi, UNIT / SLOW)
            return self.calc_new_location_3d(theta, phi, UNIT)

    def calc_new_location_3d(self, theta: float, phi: float, step_size: Union[int, float]) -> tuple[
        float, float, float]:
        """
        Calculates the new location based on the step size and the angles.

        Parameters:
            theta (float): The angle for rotation around z-axis.
            phi (float): The angle for rotation from z-axis towards x-y plane.
            step_size (int or float): The step size.

        Returns:
            tuple[float, float, float]: The new location.
        """

        x, y, z = self.get_current_location_3d()
        return x + step_size * math.sin(phi) * math.cos(theta), y + step_size * math.sin(phi) * math.sin(
            theta), z + step_size * math.cos(phi)

    def set_current_location_3d(self, loc: tuple) -> None:
        """
        Sets the current location of the walker to the given location.

        Parameters:
            loc (tuple): The new location."""
        self.current_location_3d = loc

    def get_current_location_3d(self) -> tuple[float, float, float]:
        """Returns the current location of the walker."""
        return self.current_location_3d

    def get_loc_history(self) -> list:
        """Returns the location history of the walker."""
        return self.loc_history

    def distance_from_origin(self) -> float:
        """Returns the distance of the walker from the origin."""
        x, y, z = self.get_current_location_3d()
        return math.sqrt(x ** 2 + y ** 2 + z ** 2)

    def reset_walker(self) -> None:
        """Resets the walker's location to the origin."""
        self.current_location_3d = (0, 0, 0)

    def slow_down(self) -> None:
        """Slows down the walker."""
        self.is_slower = True

    def regular_speed(self) -> None:
        """Resets the walker's speed to normal."""
        self.is_slower = False

    def check_restart(self) -> None:
        """Checks if the walker should restart."""
        if self.restart_option and random.random() < TEN_PERCENT:
            self.reset_walker()

    def step_towards_location(self, location_to_reach: tuple[float, float, float]) -> tuple[float, float, float]:
        """
        Moves the walker towards a given location. side note - used mostly for black hole

        Parameters:
            location_to_reach (tuple[float, float, float]): The location to reach.

        Returns:
            tuple[float, float, float]: The new location.
        """

        dx, dy, dz = np.subtract(location_to_reach, self.get_current_location_3d())
        distance = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2) + SMALL_CONSTANT
        unit_vector = dx / distance, dy / distance, dz / distance
        step_size = min(distance, UNIT)
        step = unit_vector[0] * step_size, unit_vector[1] * step_size, unit_vector[2] * step_size
        return self.current_location_3d[0] + step[0], self.current_location_3d[1] + step[1], self.current_location_3d[
            2] + step[2]


if __name__ == '__main__':
    pass
