import random
import helper
from typing import Union


class Obstacle3d:
    """
    Returns the corners of the obstacle.

    Returns:
        list[tuple[float, float]]: A list of tuples representing the corners of the obstacle.
    """

    def __init__(self, length=None, center_loc=None):
        """
        Constructs a new Obstacle3d instance.

        Parameters:
            length (float, optional): The length of the obstacle. If not provided, a random length is generated.
            center_loc (tuple[float, float, float], optional): The center location of the obstacle. If not provided, a random location is generated.
        """
        self.length = helper.generate_random_length() if length is None else length
        self.center_loc = helper.generate_random_coordinate_3d() if center_loc is None else center_loc

    def is_inside_obstacle_3d(self, position_of_walker3d: tuple[float, float, float]) -> bool:
        """
        Checks if a walker is inside the 3D obstacle.

        Parameters:
            position_of_walker3d (tuple[float, float, float]): The position of the walker.

        Returns:
            bool: True if the walker is inside the obstacle, False otherwise.
        """
        x, y, z = position_of_walker3d
        corners_list = self.obstacle_corners_3d()
        if corners_list[0][0] <= x <= corners_list[4][0] and corners_list[0][1] <= y <= corners_list[2][1] and \
                corners_list[0][2] <= z <= corners_list[1][2]:
            return True
        return False

    def obstacle_block(self, position_of_walker3d: tuple[float, float, float]) -> Union[
        tuple[float, float, float], bool]:
        """
                Checks if a walker is blocked by the 3D obstacle.

                Parameters:
                    position_of_walker3d (tuple[float, float, float]): The position of the walker.

                Returns:
                    tuple[float, float, float] or bool: The position of the walker if it is inside the obstacle, False otherwise.
                """
        if self.is_inside_obstacle_3d(position_of_walker3d) is True:
            return position_of_walker3d
        return False

    def obstacle_corners_3d(self) -> list[tuple[float, float, float]]:
        """
        Returns the corners of the 3D obstacle.

        Returns:
            list[tuple[float, float, float]]: A list of tuples representing the corners of the obstacle.
        """
        x, y, z = self.center_loc
        half_length = self.length / 2
        corners = [
            (x - half_length, y - half_length, z - half_length),
            (x - half_length, y - half_length, z + half_length),
            (x - half_length, y + half_length, z - half_length),
            (x - half_length, y + half_length, z + half_length),
            (x + half_length, y - half_length, z - half_length),
            (x + half_length, y - half_length, z + half_length),
            (x + half_length, y + half_length, z - half_length),
            (x + half_length, y + half_length, z + half_length)
        ]
        return corners
