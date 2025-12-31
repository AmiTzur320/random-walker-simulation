import random
import math


def distance_from_origin(point: tuple[float, float]) -> float:
    """
    Calculates the distance of a point from the origin.

    Parameters:
        point (tuple[float,float]): The point.

    Returns:
        float: The distance of the point from the origin.
    """

    return math.sqrt(point[0] ** 2 + point[1] ** 2)


def avg(lst: list[float]) -> float:
    """
    Calculates the average of a list of floats.

    Parameters:
        lst (list[float]): The list of floats.

    Returns:
        float: The average of the list.
    """

    return sum(lst) / len(lst)


def generate_random_coordinate() -> tuple:
    """
    Generates a random 2D coordinate.

    Returns:
        tuple: A tuple representing the x and y coordinates.
    """

    x = random.uniform(-60, 60)
    y = random.uniform(-60, 60)
    return x, y


def generate_random_coordinate_3d() -> tuple[float, float, float]:
    """
    Generates a random 3D coordinate.

    Returns:
        tuple[float, float, float]: A tuple representing the x, y, and z coordinates.
    """

    x = random.uniform(-40, 40)
    y = random.uniform(-40, 40)
    z = random.uniform(-40, 40)
    return x, y, z


def is_valid_coordinate(coordinate) -> bool:
    """
    Checks if a coordinate is valid.

    Parameters:
        coordinate: The coordinate to check.

    Returns:
        bool: True if the coordinate is valid, False otherwise.
    """

    if isinstance(coordinate, (tuple, list)) and len(coordinate) == 2:
        return all(isinstance(value, (int, float)) for value in coordinate)
    return False


def is_valid_length(length) -> bool:
    """
    Checks if a length is valid.

    Parameters:
        length: The length to check.

    Returns:
        bool: True if the length is valid, False otherwise.
    """

    return isinstance(length, (int, float)) and length > 0


def generate_random_length() -> float:
    """
    Generates a random length.

    Returns:
        float: A random length.
    """

    return random.uniform(10, 20)


def generate_random_color() -> tuple[float, float, float]:
    """
    Generates a random color.

    Returns:
        tuple[float, float, float]: A tuple representing the red, green, and blue values of the color.
    """

    r = random.random()
    g = random.random()
    b = random.random()
    return r, g, b


def generate_random_orientation() -> str:
    """
    Generates a random orientation.

    Returns:
        str: A random orientation.
    """

    return random.choice(["horizontal", "vertical"])


def remove_direction(direction_list: list[str], direction_to_remove: str) -> list[str]:
    """
    Removes a direction from a list of directions.

    Parameters:
        direction_list (list[str]): The list of directions.
        direction_to_remove (str): The direction to remove.

    Returns:
        list[str]: The updated list of directions.
    """

    if direction_to_remove in direction_list:
        direction_list.remove(direction_to_remove)
    return direction_list


def min_max_coordinates_for_cubes(center_loc: tuple[float, float, float], length: float) -> tuple[
    tuple[float, float, float], tuple[float, float, float]]:
    """
    Calculates the minimum and maximum coordinates for a cube.

    Parameters:
        center_loc (tuple[float, float, float]): The center location of the cube.
        length (float): The length of the cube's sides.

    Returns:
        tuple: A tuple containing two tuples. The first tuple contains the minimum x, y, and z coordinates, and the second tuple contains the maximum x, y, and z coordinates.
    """

    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x = max(max_x, center_loc[0] + length / 2)
    max_y = max(max_y, center_loc[1] + length / 2)
    max_z = max(max_z, center_loc[2] + length / 2)

    min_x = min(min_x, center_loc[0] - length / 2)
    min_y = min(min_y, center_loc[1] - length / 2)
    min_z = min(min_z, center_loc[2] - length / 2)
    return (min_x, min_y, min_z), (max_x, max_y, max_z)


def min_max_coordinates_for_sphere(center_loc: tuple[float, float, float], radius: float) -> tuple[
    tuple[float, float, float], tuple[float, float, float]]:
    """
    Calculates the minimum and maximum coordinates for a sphere.

    Parameters:
        center_loc (tuple[float, float, float]): The center location of the sphere.
        radius (float): The radius of the sphere.

    Returns:
        tuple: A tuple containing two tuples. The first tuple contains the minimum x, y, and z coordinates, and the second tuple contains the maximum x, y, and z coordinates.
    """

    max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')
    min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
    max_x = max(max_x, center_loc[0] + radius)
    max_y = max(max_y, center_loc[1] + radius)
    max_z = max(max_z, center_loc[2] + radius)

    min_x = min(min_x, center_loc[0] - radius)
    min_y = min(min_y, center_loc[1] - radius)
    min_z = min(min_z, center_loc[2] - radius)
    return (min_x, min_y, min_z), (max_x, max_y, max_z)
