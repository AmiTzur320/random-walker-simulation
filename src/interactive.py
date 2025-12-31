from PyQt5.QtWidgets import QApplication
# from mpl_toolkits.mplot3d import Axes3D
from simulation import Simulation
import matplotlib.pyplot as plt
import helper
from portal import Portal
from obstacle import Obstacle
from slowZone import SlowZone
from trap import Trap


class Interactive:
    """
    The Interactive class is responsible for the visual representation of the simulation. It uses matplotlib to draw the simulation's state at each step and PyQt5 to handle GUI events.

    Attributes:
        simulation (Simulation): An instance of the Simulation class that represents the current simulation.
        fig (Figure): The top level container for all the plot elements.
        ax (Axes): The Axes contains most of the figure elements: Axis, Tick, Line2D, Text, Polygon, etc., and sets the coordinate system.
    """

    def __init__(self, simulation: Simulation):
        """
        The constructor for the Interactive class.

        Parameters:
            simulation (Simulation): An instance of the Simulation class that represents the current simulation.
        """

        self.simulation = simulation
        self.fig, self.ax = plt.subplots()

    def draw_rectangle(self, element, element_color):
        """
        Draws a rectangle on the plot representing an element (Portal or Obstacle).

        Parameters:
            element (Portal or Obstacle): The element to be drawn.
            element_color (str): The color of the element.

        Returns:
            Rectangle: A matplotlib.patches.Rectangle instance representing the drawn element.
        """

        portal_center = element.center_loc
        portal_length = element.length
        portal_bottom_left = (portal_center[0] - portal_length / 2, portal_center[1] - portal_length / 2)
        portal_rect = plt.Rectangle(portal_bottom_left, portal_length, portal_length, fill=True,
                                    facecolor=element_color,
                                    edgecolor=element_color)
        return portal_rect

    def draw_circle(self, element, element_color):
        """
        Draws a circle on the plot representing an element (Trap or SlowZone).

        Parameters:
            element (Trap or SlowZone): The element to be drawn.
            element_color (str): The color of the element.

        Returns:
            Circle: A matplotlib.patches.Circle instance representing the drawn element.
        """

        trap_center = element.center_loc
        trap_radius = element.radius
        trap_circle = plt.Circle(trap_center, trap_radius, fill=False, edgecolor=element_color)
        return trap_circle

    def draw_board(self) -> None:
        """
        Draws the board on the plot. This includes all the elements (Portals, Obstacles, Traps, SlowZones) in the simulation.
        """

        for element in self.simulation.elements:
            # draw the portal and the obstacle as a rectangle
            if isinstance(element, Portal) or isinstance(element, Obstacle):
                if isinstance(element, Portal):
                    element_color = 'blue'
                elif isinstance(element, Obstacle):
                    element_color = 'red'
                portal_rect = self.draw_rectangle(element, element_color)
                self.ax.add_patch(portal_rect)

            elif isinstance(element, Trap):
                # Draw the trap as a circle
                element_color = 'purple'
                trap_circle = self.draw_circle(element, element_color)
                self.ax.add_patch(trap_circle)

            elif isinstance(element, SlowZone):
                # Draw the slow zone as a circle
                element_color = 'green'
                slow_zone_circle = self.draw_circle(element, element_color)
                self.ax.add_patch(slow_zone_circle)


    def plot_walk(self) -> None:
        """
        Plots the walk of the walkers in the simulation. It updates the plot at each step of the simulation, showing the current position of each walker. It also handles GUI events to keep the GUI responsive.
        """
        plt.ion()
        paths = self.simulation.run()
        graph = []
        colors = [helper.generate_random_color() for _ in range(len(paths))]
        for i in range(len(paths[0])):
            point = []
            for j, path in enumerate(paths):
                point.append([path[i], colors[j]])
            graph.append(point)

        walker_moves:list[list] = [[] for _ in self.simulation.walkers]
        lines = [None for _ in self.simulation.walkers]

        step_label = plt.text(-45, 45, '', fontsize=12)
        self.draw_board()
        for step, step_moves in enumerate(graph):
            if not plt.fignum_exists(1):
                break
            step_label.set_text(f'Step: {step + 1}')

            for i in range(len(lines)):
                if lines[i] is not None:
                    lines[i].remove()
                    lines[i] = None

            for i, move in enumerate(step_moves):
                x, y = move[0]
                walker_moves[i].append((x, y))

            for i, (moves, walker) in enumerate(zip(walker_moves, self.simulation.walkers)):
                xs, ys = zip(*moves)
                lines[i], = plt.plot(xs, ys, '-', color=walker.walker_color)

            plt.draw()
            pause_time = self.simulation.ice_probability_in_simulation()
            plt.pause(pause_time)

            QApplication.processEvents()

        plt.ioff()
        if plt.fignum_exists(1):
            plt.show()
