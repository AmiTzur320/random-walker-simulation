
from typing import Tuple, Union

import numpy as np
from PyQt5.QtWidgets import QApplication
from mpl_toolkits.mplot3d.art3d import Poly3DCollection #type: ignore
from mpl_toolkits.mplot3d import Axes3D #type: ignore
from simulation3d import Simulation3d
import matplotlib.pyplot as plt
import helper
from portal3d import Portal3d
from obstacle3d import Obstacle3d
from walker3d import Walker3d
from traps3d import Traps3d
from slowzone3d import SlowZone3d
from blackhole3d import BlackHole3d


class Interactive3d:
    """
    The Interactive3d class is responsible for creating an interactive 3D plot of the simulation.

    Attributes:
        simulation3d (Simulation3d): The 3D simulation to be plotted.
        fig (Figure): The figure for the plot.
        ax (Axes3D): The 3D axes for the plot.
    """

    def __init__(self, simulation3d: Simulation3d):
        """
        Constructs a new Interactive3d instance.

        Parameters:
            simulation3d (Simulation3d): The 3D simulation to be plotted.
        """

        self.simulation3d = simulation3d
        self.fig = plt.figure()
        self.ax: Axes3D = self.fig.add_subplot(111, projection='3d')
        # self.ax = Axes3D(self.fig)

    def set_initial_viewing_angle(self, elev: float, azim: float) -> None:
        """
        Sets the initial viewing angle for the 3D plot.

        Parameters:
            elev (float): The elevation angle.
            azim (float): The azimuth angle.
        """

        self.ax.view_init(elev=elev, azim=azim)

    def draw_cube(self, element: Union[Obstacle3d ,Portal3d], element_color: str) -> Poly3DCollection:
        """
        Draws a cube representing an Obstacle3d or Portal3d in the 3D plot.

        Parameters:
            element (Obstacle3d or Portal3d): The Obstacle3d or Portal3d to be drawn.
            element_color (str): The color of the element.

        Returns:
            Poly3DCollection: A collection of polygons representing the faces of the cube.
        """

        cube_center = element.center_loc
        cube_length = element.length
        cube_height = element.length  # Assuming the height of the cube is stored in `length`

        x = [cube_center[0] - cube_length / 2, cube_center[0] + cube_length / 2]
        y = [cube_center[1] - cube_length / 2, cube_center[1] + cube_length / 2]
        z = [cube_center[2] - cube_height / 2, cube_center[2] + cube_height / 2]
        corners = [(xi, yi, zi) for xi in x for yi in y for zi in z]

        faces = [[corners[0], corners[1], corners[5], corners[4]],
                 [corners[1], corners[3], corners[7], corners[5]],
                 [corners[3], corners[2], corners[6], corners[7]],
                 [corners[2], corners[0], corners[4], corners[6]],
                 [corners[0], corners[2], corners[3], corners[1]],
                 [corners[4], corners[5], corners[7], corners[6]]]

        # Create a 3D polygon for each face
        face_collection = Poly3DCollection(faces, facecolors=["g"], linewidths=1, edgecolors=element_color,
                                           alpha=0.1)
        return face_collection

    def draw_sphere(self, element, orbital=None) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """
        Draws a sphere representing a Traps3d, SlowZone3d, or BlackHole3d in the 3D plot.

        Parameters:
            element: The Traps3d, SlowZone3d, or BlackHole3d to be drawn.
            orbital (optional): The orbital radius for a BlackHole3d.

        Returns:
            tuple[np.ndarray, np.ndarray, np.ndarray]: The x, y, and z coordinates of the points on the sphere.
        """

        sphere_center = element.center_loc
        if orbital is None:
            sphere_radius = element.radius
        else:
            sphere_radius = orbital
        # Draw the trap as a sphere by creating points in a 3D grid
        phi = np.linspace(0, np.pi, 20)
        theta = np.linspace(0, 2 * np.pi, 40)
        x = sphere_center[0] + sphere_radius * np.outer(np.sin(phi), np.cos(theta))
        y = sphere_center[1] + sphere_radius * np.outer(np.sin(phi), np.sin(theta))
        z = sphere_center[2] + sphere_radius * np.outer(np.cos(phi), np.ones_like(theta))
        return x, y, z

    def calculate_min_max_coordinates_in_paths(self, paths) -> tuple[float, float, float, float, float, float]:
        """
        Calculates the minimum and maximum coordinates of the paths in the 3D simulation.

        Parameters:
            paths (list): The paths in the 3D simulation.

        Returns:
            tuple[int, int, int, int, int, int]: The minimum and maximum x, y, and z coordinates.
        """

        min_x, min_y, min_z = float('inf'), float('inf'), float('inf')
        max_x, max_y, max_z = float('-inf'), float('-inf'), float('-inf')

        for path in paths:
            for point in path:
                x, y, z = point
                min_x, min_y, min_z = min(min_x, x), min(min_y, y), min(min_z, z)
                max_x, max_y, max_z = max(max_x, x), max(max_y, y), max(max_z, z)

        return min_x, min_y, min_z, max_x, max_y, max_z

    def draw_board_3d(self, paths) -> None:
        """
        Draws the 3D simulation board.

        Parameters:
            paths (list): The paths in the 3D simulation.
        """

        min_x, min_y, min_z, max_x, max_y, max_z = self.calculate_min_max_coordinates_in_paths(paths)
        min_num = min(min_x, min_y, min_z)
        max_num = max(max_x, max_y, max_z)
        self.ax.set_xlim(min_num, max_num)  # Set x-axis limits
        self.ax.set_ylim(min_num, max_num)  # Set y-axis limits
        self.ax.set_zlim(min_num, max_num)  # Set z-axis limits

        for element in self.simulation3d.elements3d:
            # Draw the elements in the 3D plot
            if isinstance(element, Portal3d) or isinstance(element, Obstacle3d):
                # Draw the portal or obstacle as a cube
                if isinstance(element, Portal3d):
                    element_color = "blue"
                else:
                    isinstance(element, Obstacle3d)
                    element_color = "red"
                face_collection = self.draw_cube(element, element_color)
                self.ax.add_collection3d(face_collection)

            elif isinstance(element, Traps3d):
                # Draw the trap as a sphere
                x, y, z = self.draw_sphere(element)
                self.ax.plot_surface(x, y, z, color='purple', alpha=0.1)

            elif isinstance(element, SlowZone3d):
                # Draw the slow zone as a sphere
                x, y, z = self.draw_sphere(element)
                self.ax.plot_surface(x, y, z, color='green', alpha=0.1)

            elif isinstance(element, BlackHole3d):
                # Draw the black hole as a sphere
                x, y, z = self.draw_sphere(element)
                self.ax.plot_surface(x, y, z, color='black', alpha=0.5)
                horizon_event_radius = element.calculate_horizon_event_radius()
                x_horizon, y_horizon, z_horizon = self.draw_sphere(element, horizon_event_radius)
                self.ax.plot_surface(x_horizon, y_horizon, z_horizon, color='yellow', alpha=0.1)

    def plot_walk_3d(self) -> None:
        """
        Plots the 3D simulation.
        """
        plt.ion()
        paths = self.simulation3d.run()
        graph = []
        colors = [helper.generate_random_color() for _ in range(len(paths))]
        for i in range(len(paths[0])):
            point = []
            for j, path in enumerate(paths):
                point.append([path[i], colors[j]])
            graph.append(point)

        walker_moves: list[list] = [[] for _ in self.simulation3d.walkers3d]
        lines = [None for _ in self.simulation3d.walkers3d]
        step_label = self.ax.text(-45, 45, 0, '', fontsize=12)
        self.draw_board_3d(paths)

        for step, step_moves in enumerate(graph):
            if not plt.fignum_exists(1):
                break
            step_label.set_text(f'Step: {step + 1}')
            # Remove the old lines from the plot
            for i in range(len(lines)):
                if lines[i] is not None:
                    lines[i].remove()
                    lines[i] = None

            # Plot each walker's moves as a line
            for i, move in enumerate(step_moves):
                x, y, z = move[0]
                walker_moves[i].append((x, y, z))

            for i, (moves, walker) in enumerate(zip(walker_moves, self.simulation3d.walkers3d)):
                xs, ys, zs = zip(*moves)
                lines[i], = self.ax.plot(xs, ys, zs, '-', color=walker.walker_color)

            plt.draw()
            pause_time = self.simulation3d.ice_probability_in_simulation()
            plt.pause(pause_time)

            QApplication.processEvents()

        plt.ioff()
        if plt.fignum_exists(1):
            plt.show()


if __name__ == '__main__':
    pass
