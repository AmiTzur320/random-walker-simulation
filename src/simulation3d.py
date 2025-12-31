import pprint
import random

import helper
from portal3d import Portal3d
from obstacle3d import Obstacle3d
from walker3d import Walker3d
from traps3d import Traps3d
from slowzone3d import SlowZone3d
from blackhole3d import BlackHole3d


class Simulation3d:
    def __init__(self, walkers3d_list, portals3d_list, obstacles3d_list, walls3d_list, trap3d_list,
                 slow_zone3d_list, black_hole_list, num_steps, ice_option) -> None:
        """initialize the simulation with the given walkers, elements, number of steps and ice option (probability of the
        frame to pause so that the user can see the movement of the walkers easier)"""
        self.walkers3d = walkers3d_list
        self.elements3d = portals3d_list + obstacles3d_list + walls3d_list + trap3d_list + slow_zone3d_list + black_hole_list
        self.num_steps = num_steps
        self.ice_option = ice_option

    def make_a_move(self, specific_walker3d: Walker3d) -> tuple[float, float, float]:
        """make a move for the walker, check if the walker is inside any element, if so, take the necessary action"""
        new_location = specific_walker3d.new_loc_by_type_3d()
        inside_element = False
        for element in self.elements3d:
            if isinstance(element, Portal3d) and element.is_inside_portal_3d(new_location):
                """if the walker is inside a portal, move the walker to the exit point of the portal"""
                new_location = element.exit_point
                specific_walker3d.step(new_location)
                inside_element = True
                break

            elif isinstance(element, Obstacle3d) and element.is_inside_obstacle_3d(new_location):
                """if the walker is inside an obstacle, move the walker to the previous location 
                (no change- it will do a step to same location)"""
                inside_element = True
                break

            elif isinstance(element, Traps3d):
                """if the walker is inside a trap and the new location is not inside the trap, move the walker to the new location
                else, no change in the location of the walker (no change- it will do a step to same location)"""
                if element.is_inside_trap_3d(specific_walker3d, specific_walker3d.get_current_location_3d()):
                    if not element.is_inside_trap_3d(specific_walker3d, new_location):
                        """if the walker is inside a trap and new location is not inside the trap, step to same location"""
                        inside_element = True
                        break
                elif not element.is_inside_trap_3d(specific_walker3d,
                                                   specific_walker3d.get_current_location_3d()) and element.is_inside_trap_3d(
                    specific_walker3d, new_location):
                    """if the walker is not yet inside the trap and the new location is inside the trap, let him move
                    into the trap and add the walker to the trap's list of walkers inside the trap"""
                    element.enter_trap_3d(specific_walker3d)
                    specific_walker3d.step(new_location)
                    inside_element = True
                    break

            elif isinstance(element, SlowZone3d):
                """if the walker is inside a slow zone, slow down the walker and add the walker
                 to the list of walkers inside the slow zone"""
                if element.is_inside_slow_zone(specific_walker3d.get_current_location_3d()):
                    if specific_walker3d in element.slowed_walkers3d:
                        break
                    specific_walker3d.slow_down()
                    element.enter_slow_zone(specific_walker3d)
                if not element.is_inside_slow_zone(specific_walker3d.get_current_location_3d()):
                    if specific_walker3d in element.slowed_walkers3d:
                        element.slowed_walkers3d.remove(specific_walker3d)
                        specific_walker3d.regular_speed()

            elif isinstance(element, BlackHole3d):
                """if the walker is inside a the event horizon of black hole, move the walker to the center of the black hole"""
                if element.is_in_horizon_event_zone(specific_walker3d.get_current_location_3d()):
                    new_location = specific_walker3d.step_towards_location(element.center_loc)
                    specific_walker3d.step(new_location)
                    inside_element = True
                    break

        # If walker is not inside any portal or obstacle, take a step
        if not inside_element:
            specific_walker3d.step(new_location)
            return new_location
        return specific_walker3d.get_current_location_3d()

    def run(self) -> list[list[tuple[float, float, float]]]:
        """run the simulation for the given number of steps and return the paths of the walkers"""
        paths = []
        for walker3d in self.walkers3d:
            path = [walker3d.current_location_3d]
            for _ in range(self.num_steps):
                path.append(self.make_a_move(walker3d))
            paths.append(path)
        return paths

    def ice_probability_in_simulation(self) -> float:
        """return the probability of the frame to pause so that the user can see the movement of the walkers easier"""
        if self.ice_option is False:
            return 0.0001
        else:
            random_number = random.random()
            # If the random number is less than 0.5, pause for 0.3 seconds, else pause for 0.0001 seconds
            pause_time = 0.5 if random_number < 0.05 else 0.0001
            return pause_time

    def reset_walkers3d(self) -> None:
        """reset the walkers to their initial location"""
        for walk in self.walkers3d:
            walk.reset_walker3d()

    def get_walkers3d(self) -> list[Walker3d]:
        """return the list of walkers"""
        return self.walkers3d


if __name__ == '__main__':
    pass
