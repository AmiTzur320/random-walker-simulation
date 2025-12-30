from obstacle import Obstacle
import helper


class Portal(Obstacle):
    """
    The Portal class represents a portal in the simulation.

    Attributes:
        exit_point (tuple[float, float]): The exit point of the portal.
    """

    def __init__(self, exit_point=None, length=None, center_loc=None):
        """
        Constructs a new Portal instance.

        Parameters:
            exit_point (tuple[float, float], optional): The exit point of the portal. If not provided, a random coordinate is generated.
            length (float, optional): The length of the portal. Inherited from Obstacle.
            center_loc (tuple[float, float], optional): The center location of the portal. Inherited from Obstacle.
        """
        super().__init__(length, center_loc)
        self.title = "Portal"
        self.exit_point = helper.generate_random_coordinate() if exit_point is None else exit_point

    def is_inside_portal(self, position_of_walker: tuple) -> bool:
        """
        Checks if a walker is inside the portal.

        Parameters:
            position_of_walker (tuple[float, float]): The position of the walker.

        Returns:
            bool: True if the walker is inside the portal, False otherwise.
        """
        return self.is_inside_obstacle(position_of_walker)

    def portal_jump(self, position_of_walker) -> tuple[float, float]:
        """
        Moves the walker to the exit point of the portal if the walker is inside the portal.

        Parameters:
            position_of_walker (tuple[float, float]): The position of the walker.

        Returns:
            tuple[float, float]: The new position of the walker after the portal jump.
        """
        if self.is_inside_portal(position_of_walker) is True:
            return self.exit_point
        else:
            return position_of_walker

    def portal_corners(self) -> list[tuple[float, float]]:
        """
        Returns the corners of the portal.

        Returns:
            list[tuple[float, float]]: A list of tuples representing the corners of the portal.
        """
        return self.portal_corners()
