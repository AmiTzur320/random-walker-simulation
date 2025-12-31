import numpy as np

import helper

GRAVITY_FORCE = 6.674 * (10 ** -11)
WALKER_MASS = 1e-14
BLACK_HOLE_MASS = 1.5 * 10 ** 24
VISUAL_BLACK_HOLE_RADIUS = 1  # This is the radius of the black hole that will be displayed in the visualization ,
FORCE_THRESHOLD = 0.01  # This is the threshold for the gravitational force that determines if the walker is in the
# horizon event or not
SMALL_CONSTANT = 1e-9


class BlackHole3d:
    """
    The BlackHole3d class represents a black hole in a 3D simulation.

    Attributes:
        center_loc (tuple[float, float, float]): The location of the center of the black hole.
        radius (float): The radius of the black hole.
        mass (float): The mass of the black hole.
    """

    def __init__(self)->None:
        """
        Constructs a new BlackHole3d instance with a random location, a predefined radius, and a predefined mass.
        """
        self.center_loc = helper.generate_random_coordinate_3d()
        self.radius = VISUAL_BLACK_HOLE_RADIUS
        self.mass = BLACK_HOLE_MASS

    def is_in_horizon_event_zone(self, location: tuple[float, float, float]) -> bool:
        """
        Checks if a given location is in the event horizon zone of the black hole. the
        event horizon zone is the zone where the gravitational force is greater than the threshold.
        and being determined by the formula F = G * (m1 * m2) / r^2

        Parameters:
            location (tuple[float, float, float]): The location to check.

        Returns:
            bool: True if the location is in the event horizon zone, False otherwise.
        """

        dx, dy, dz = np.subtract(location, self.center_loc)
        distance = np.sqrt(dx ** 2 + dy ** 2 + dz ** 2)
        # Calculate the gravitational force using the formula F = G * (m1 * m2) / r^2
        force = (GRAVITY_FORCE * WALKER_MASS * self.mass) / (distance ** 2+SMALL_CONSTANT)
        return force > FORCE_THRESHOLD

    def calculate_horizon_event_radius(self) -> float:
        """
        Calculates the radius of the event horizon zone of the black hole with
        the formula r = sqrt((G * m1 * m2) / F).

        Returns:
            float: The radius of the event horizon zone.
        """
        return np.sqrt((GRAVITY_FORCE * WALKER_MASS * self.mass) / FORCE_THRESHOLD)

