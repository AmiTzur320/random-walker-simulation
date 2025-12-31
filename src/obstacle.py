from typing import Union

import helper


class Obstacle:
    """
    The Obstacle class represents an obstacle in the simulation.

    Attributes:
        length (float): The length of the obstacle.
        center_loc (tuple[float, float]): The center location of the obstacle.
    """

    def __init__(self, length=None, center_loc=None):
        """
        Constructs a new Obstacle instance.

        Parameters:
            length (float, optional): The length of the obstacle. If not provided, a random length is generated.
            center_loc (tuple[float, float], optional): The center location of the obstacle. If not provided, a random location is generated.
        """
        self.title = "Obstacle"
        self.length = helper.generate_random_length() if length is None else length
        self.center_loc = helper.generate_random_coordinate() if center_loc is None else center_loc

    def is_inside_obstacle(self, position_of_walker: tuple) -> bool:
        """
        Checks if a walker is inside the obstacle.

        Parameters:
            position_of_walker (tuple[float, float]): The position of the walker.

        Returns:
            bool: True if the walker is inside the obstacle, False otherwise.
        """
        x, y = position_of_walker
        corner_list = self.obstacle_corners()
        top_left_x, top_left_y = corner_list[0]
        bottom_left_x, bottom_left_y = corner_list[1]
        top_right_x, top_right_y = corner_list[2]
        bottom_right_x, bottom_right_y = corner_list[3]
        if top_left_x <= x <= top_right_x and bottom_left_y <= y <= top_left_y:
            return True
        return False

    def obstacle_block(self, position_of_walker: tuple) -> Union[tuple, bool]:
        """
        Checks if a walker is blocked by the obstacle.

        Parameters:
            position_of_walker (tuple[float, float]): The position of the walker.

        Returns:
            tuple[float, float] or bool: The position of the walker if it is inside the obstacle, False otherwise.
        """
        if self.is_inside_obstacle(position_of_walker) is True:
            return position_of_walker
        return False

    def obstacle_corners(self) -> list[tuple[float, float]]:
        """
        Returns the corners of the obstacle.

        Returns:
            list[tuple[float, float]]: A list of tuples representing the corners of the obstacle.
        """
        x, y = self.center_loc
        half_length = self.length / 2
        point_list = [(x - half_length, y + half_length), (x - half_length, y - half_length),
                      (x + half_length, y + half_length), (x + half_length, y - half_length)]
        return point_list
