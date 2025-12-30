import helper
import walker3d
from walker3d import Walker3d


class Traps3d:
    """
    The Traps3d class represents a trap in a 3D simulation.

    Attributes:
        radius (float): The radius of the trap.
        center_loc (tuple[float, float, float]): The location of the center of the trap.
        trapped_walkers (list[walker3d.Walker3d]): The list of walkers trapped in the trap.
    """

    def __init__(self) -> None:
        """
        Constructs a new Traps3d instance with a random radius and center location.
        """

        self.radius = helper.generate_random_length()
        self.center_loc = helper.generate_random_coordinate_3d()
        self.trapped_walkers: list[Walker3d]= []

    def is_inside_trap_3d(self, walker: Walker3d, new_location3d: tuple[float, float, float]) -> bool:
        """
        Checks if a walker is inside the trap.

        Parameters:
            walker (Walker3d): The walker to check.
            new_location3d (tuple[float, float, float]): The new location of the walker.

        Returns:
            bool: True if the walker is inside the trap, False otherwise.
        """

        if walker in self.trapped_walkers:
            return True
        x, y, z = new_location3d
        center_x, center_y, center_z = self.center_loc
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2 + (z - center_z) ** 2) ** 0.5
        return distance <= self.radius

    def enter_trap_3d(self, walker: Walker3d) -> None:
        """
        Adds a walker to the list of trapped walkers if the walker is inside the trap.

        Parameters:
            walker (Walker3d): The walker to add.
        """
        if self.is_inside_trap_3d(walker, walker.get_current_location_3d()):
            self.trapped_walkers.append(walker)

