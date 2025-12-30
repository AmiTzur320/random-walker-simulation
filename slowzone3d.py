import helper
from walker3d import Walker3d


class SlowZone3d:
    """
    The SlowZone3d class represents a slow zone in a 3D simulation.

    Attributes:
        center_loc (tuple[float, float, float]): The location of the center of the slow zone.
        radius (float): The radius of the slow zone.
        slowed_walkers3d (list[walker3d.Walker3d]): The list of walkers that are inside the slow zone.
    """

    def __init__(self):
        """
        Constructs a new SlowZone3d instance with a random radius and center location.
        """

        self.center_loc = helper.generate_random_coordinate_3d()
        self.radius = helper.generate_random_length()
        self.slowed_walkers3d = []

    def is_inside_slow_zone(self,new_location3d: tuple[float, float, float]) -> bool:
        """
        Checks if a walker is inside the slow zone.

        Parameters:
            new_location3d (tuple[float, float, float]): The new location of the walker.

        Returns:
            bool: True if the walker is inside the slow zone, False otherwise.
        """
        x, y, z = new_location3d
        center_x, center_y, center_z = self.center_loc
        distance = ((x - center_x) ** 2 + (y - center_y) ** 2 + (z - center_z) ** 2) ** 0.5
        return distance <= self.radius

    def enter_slow_zone(self, walker: Walker3d) -> None:
        """
        Adds a walker to the list of slowed walkers if the walker is inside the slow zone.

        Parameters:
            walker (Walker3d): The walker to add.
        """
        if self.is_inside_slow_zone(walker.get_current_location_3d()):
            self.slowed_walkers3d.append(walker)

