import helper
import walker
from walker import Walker


class SlowZone:
    """
    The SlowZone class represents a slow zone in a 2D simulation.

    Attributes:
        center_loc (tuple[float, float]): The location of the center of the slow zone.
        radius (float): The radius of the slow zone.
        slowed_walkers (list[walker.Walker]): The list of walkers that are inside the slow zone.
    """

    def __init__(self)-> None:
        """
        Constructs a new SlowZone instance with a random radius and center location.
        """
        self.center_loc = helper.generate_random_coordinate()
        self.radius = helper.generate_random_length()
        self.slowed_walkers: list[Walker] = []

    def is_inside_slow_zone(self, new_location: tuple) -> bool:
        """
        Checks if a walker is inside the slow zone.

        Parameters:
            new_location (tuple): The new location of the walker.

        Returns:
            bool: True if the walker is inside the slow zone, False otherwise.
        """
        x, y = new_location
        center_x, center_y = self.center_loc
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        return distance <= self.radius

    def enter_slow_zone(self, walker: Walker) -> None:
        """
        Adds a walker to the list of slowed walkers if the walker is inside the slow zone.

        Parameters:
            walker (Walker): The walker to add.
        """
        if self.is_inside_slow_zone(walker.get_current_location()):
            self.slowed_walkers.append(walker)
