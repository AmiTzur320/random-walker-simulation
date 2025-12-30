import helper
import walker
from walker import Walker


class Trap:
    """
    The Trap class represents a trap in a 2D simulation.

    Attributes:
        radius (float): The radius of the trap.
        center_loc (tuple[float, float]): The location of the center of the trap.
        trapped_walkers (list[walker.Walker]): The list of walkers trapped in the trap.
    """

    def __init__(self) -> None:
        """
        Constructs a new Trap instance with a random radius and center location.
        """
        self.radius = helper.generate_random_length()
        self.center_loc = helper.generate_random_coordinate()
        self.trapped_walkers: list[Walker] = []

    def is_inside_trap(self, walker: Walker, new_location: tuple) -> bool:
        """
        Checks if a walker is inside the trap.

        Parameters:
            walker (Walker): The walker to check.
            new_location (tuple): The new location of the walker.

        Returns:
            bool: True if the walker is inside the trap, False otherwise.
        """
        if walker in self.trapped_walkers:
            return True
        x, y = new_location
        center_x, center_y = self.center_loc
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2) ** 0.5
        return distance <= self.radius

    def enter_trap(self, walker: Walker) -> None:
        """
        Adds a walker to the list of trapped walkers if the walker is inside the trap.

        Parameters:
            walker (Walker): The walker to add.
        """
        if self.is_inside_trap(walker, walker.get_current_location()):
            self.trapped_walkers.append(walker)
