from obstacle3d import Obstacle3d
import helper


class Portal3d(Obstacle3d):
    """
        The Portal3d class represents a 3-dimensional portal in the simulation.

        Attributes:
            exit_point (tuple[float, float, float]): The exit point of the portal.
        """
    def __init__(self, exit_point=None, length=None, center_loc=None):
        """
                Constructs a new Portal3d instance.

                Parameters:
                    exit_point (tuple[float, float, float], optional): The exit point of the portal. If not provided, a random coordinate is generated.
                    length (float, optional): The length of the portal. Inherited from Obstacle3d.
                    center_loc (tuple[float, float, float], optional): The center location of the portal. Inherited from Obstacle3d.
                """
        super().__init__(length, center_loc)
        self.exit_point = helper.generate_random_coordinate_3d() if exit_point is None else exit_point

    def is_inside_portal_3d(self, position_of_walker: tuple[float, float, float]) -> bool:
        """
                Checks if a walker is inside the portal.

                Parameters:
                    position_of_walker (tuple[float, float, float]): The position of the walker.

                Returns:
                    bool: True if the walker is inside the portal, False otherwise.
                """
        return self.is_inside_obstacle_3d(position_of_walker)

    def portal_jump(self, position_of_walker: tuple[float, float, float]) -> tuple[float, float, float]:
        """
                Moves the walker to the exit point of the portal if the walker is inside the portal.

                Parameters:
                    position_of_walker (tuple[float, float, float]): The position of the walker.

                Returns:
                    tuple[float, float, float]: The new position of the walker after the portal jump.
                """
        if self.is_inside_portal_3d(position_of_walker) is True:
            return self.exit_point
        else:
            return position_of_walker

    def portal_corners_3d(self) -> list[tuple[float, float, float]]:
        """
                Returns the corners of the portal.

                Returns:
                    list[tuple[float, float, float]]: A list of tuples representing the corners of the portal.
                """
        return self.portal_corners_3d()
