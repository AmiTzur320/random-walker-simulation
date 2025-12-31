import subprocess
import tempfile
import tkinter as tk
import json
import sys
import run3d

NUM_STEPS_FOR_STATISTICS = [100, 150, 200, 250, 300, 350, 400, 450, 500, 550, 600, 650, 700, 750, 800, 850, 900, 950,
                            1000]

"""

This module provides a graphical user interface (GUI) for configuring and running a random walker simulation in either 2D or 3D.

Functions: create_greeting_page(window=None): Creates the greeting page of the GUI. create_dimension_page(window): 
Creates the dimension selection page of the GUI. create_label_and_widget(frame, row, label_text, widget_class, 
**widget_kwargs): Creates a label and a widget (e.g., Scale, Checkbutton) for a configuration option. 
create_frames_for_p_and_o(window, num_frames, title, row, extra_fields=None): Creates frames for portals and 
obstacles. create_gui_3d(window): Creates the GUI for the 3D simulation. run_main_3d(window, walker_type, num_steps, 
num_concurrent_walkers, portal_list, obstacle_list, traps_amount, slow_zone_amount, black_hole_amount, ice_option, 
restart_option): Runs the main function for the 3D simulation with the given configuration. create_gui_2d(window): 
Creates the GUI for the 2D simulation. run_main_2d(window, num_steps, walker_type, num_runs, 
num_steps_for_statistics, num_concurrent_walkers, portal_frames, obstacle_frames, traps_amount, slow_zone_amount, 
ice_option, restart_option, simulation_mode): Runs the main function for the 2D simulation with the given 
configuration."""


def create_greeting_page(window=None):
    """
    Creates the greeting page of the GUI.

    Parameters:
        window (Tk, optional): The Tk window to destroy before creating the greeting page. If not provided, a new Tk window is created.
    """

    if window is not None:
        window.destroy()

    window = tk.Tk()
    window.minsize(750, 400)
    window.title("Greeting Page")
    title_label = tk.Label(window, text="Random Walker Simulation", font=("David", 24))
    title_label.pack(pady=20)
    explanation_text = tk.Text(window, width=100, height=50, wrap=tk.WORD, font=("David", 12))
    explanation_text.insert(tk.END,
                            "Welcome to our Random Walker Simulation! In this simulation,  here you will witness a "
                            "random walker simulation in real time!."
                            "\n\n- The program supports two main modes: interactive, and non-interactive (controlled "
                            "by the 'interactive?' checkbox)."
                            "\n - In interactive-mode, the walk is visualized on the screen (with matplotlib)."
                            "\n- In non-interactive-mode, the program runs several experiments with different "
                            "num-of-steps,"
                            "\nand outputs the experiment-results into files."
                            "\n\n- charts are outputted into 'png' files and a 'stats.csv' file:"
                                  "\navg_distance_from_origin.png"
                                  "\navg_distance_from_x_axis.png"
                                  "\navg_distance_from_y_axis.png"
                                  "\navg_num_steps_to_exit_circle.png"
                                  "\navg_total_walker_crosse_y_axis.png"
                            
                            "\n\nthe walker can be one of six different types:"
                            "\n-walker1: moves 1 unit in a random direction (out of 360)."
                            "\n-walker2: moves randomly between [0.5,1.5] units in a random direction (out of 360)."
                            "\n-walker3: moves 1 unit in a random direction out of 4 (Up,Down,Right,left)."
                            "\n-walker4: biased walk - moves 1 unit in a random direction out of 360, but is biased "
                            "towards the origin."
                            "\n-walker5: same as walker1, but makes bigger steps"
                            "\n-walker6: same as walker1, but has a 50% change to 'take a rest'."
                            
                            "\n\n- The program also supports 3d (but only in interactive-mode)."
                            
                            "\n\n- The program supports few types of elements (supports 2d and 3d):"
                            
                              "\n\n- obstacles: a list of points that the walker cannot cross."
                              "\n\n- portals: a list of points that if the walker crossed them ,the walker teleports to other point in universe."
                              "\n\n-black holes (only in 3d): \n if the walker crosse the 'horizon event' it will be sucked into the blackhole and will never return."
                              "\nthe horizon event was created with physics formulas of gravitational force, taking notice of the mass of a walker and"
                              "the mass of the black hole.\n the formula used was F = G * (m1 * m2) / r^2"
                              "where F is the force, G is the gravitational constant, m1 is the mass of the walker, m2 is the mass of the black hole" 
                              "and r is the distance between the walker and the black hole."
                              "\n\ntraps- if the walker crosse the trap, he cannot walk out of it."
                              "\n\nslow zones- if the walker crosse the slow zone, he will move slower."
                            
                             "\n\nThe program supports also:"
                              "\n-restart option (check box): if checked, there will be a probability that the walker will teleport to the origin and keep walking from there."
                              "\n- ice option (check box): if checked, there will  be a probability that the frame will pause in slower pace, so we can analyze the walk better."

                            "\n\nEnjoy the simulation!")
    explanation_text.pack(pady=20)
    next_button = tk.Button(window, text="Next", command=lambda: create_dimension_page(window))
    next_button.pack()
    window.mainloop()


def create_dimension_page(window):
    """
    Creates the dimension selection page of the GUI.

    Parameters:
        window (Tk): The Tk window to destroy before creating the dimension selection page.
    """

    window.destroy()
    window = tk.Tk()
    window.minsize(150, 170)
    window.title("Dimension Page")
    tk.Label(window, text="Please choose a dimension:").grid(row=0, column=0, pady=20)
    two_d_button = tk.Button(window, text="2D", command=lambda: create_gui_2d(window))
    two_d_button.grid(row=1, column=0, pady=10)
    three_d_button = tk.Button(window, text="3D", command=lambda: create_gui_3d(window))
    three_d_button.grid(row=2, column=0, pady=10)
    back_button = tk.Button(window, text="Back", command=lambda: create_greeting_page(window))
    back_button.grid(row=3, column=0)


def create_label_and_widget(frame, row, label_text, widget_class, **widget_kwargs):
    """
    Creates a label and a widget (e.g., Scale, Checkbutton) for a configuration option.

    Parameters:
        frame (Frame): The frame to add the label and widget to.
        row (int): The row number to add the label and widget at.
        label_text (str): The text for the label.
        widget_class (class): The class of the widget to create.
        **widget_kwargs: Keyword arguments to pass to the widget's constructor.

    Returns:
        widget (widget_class): The created widget.
    """

    tk.Label(frame, text=label_text).grid(row=row, column=0)
    if widget_class == tk.Checkbutton:
        var = tk.BooleanVar(frame, **widget_kwargs)
        widget = widget_class(frame, variable=var)
    else:
        widget = widget_class(frame, **widget_kwargs)
    widget.grid(row=row, column=1)
    return widget if widget_class != tk.Checkbutton else var


def create_frames_for_p_and_o(window, num_frames, title, row, extra_fields=None):
    """
    Creates frames for portals and obstacles.

    Parameters:
        window (Tk): The Tk window to add the frames to.
        num_frames (int): The number of frames to create.
        title (str): The title for the frames.
        row (int): The row number to add the frames at.
        extra_fields (list[str], optional): A list of extra fields to add to the frames. If not provided, no extra fields are added.

    Returns:
        frames (list[Frame]): The created frames.
    """

    if extra_fields is None:
        extra_fields = []

    frames = []
    for i in range(num_frames):
        frame = tk.LabelFrame(window, text=f"{title} {i + 1}", width=150, height=150)
        frame.length_scale = create_label_and_widget(frame, 0, "Length:", tk.Scale, from_=1, to=100,
                                                     orient=tk.HORIZONTAL)
        frame.center_loc_x_scale = create_label_and_widget(frame, 1, "Center Location X:", tk.Scale, from_=-100, to=100,
                                                           orient=tk.HORIZONTAL)
        frame.center_loc_x_scale.set(100)
        frame.center_loc_y_scale = create_label_and_widget(frame, 2, "Center Location Y:", tk.Scale, from_=-100, to=100,
                                                           orient=tk.HORIZONTAL)
        frame.center_loc_y_scale.set(-100)
        for j, field in enumerate(extra_fields, start=3):
            setattr(frame, f"{field}_scale",
                    create_label_and_widget(frame, j, f"{field}:", tk.Scale, from_=-100, to=100,
                                            orient=tk.HORIZONTAL))

        frames.append(frame)

    for i, frame in enumerate(frames):
        frame.grid(row=row, column=i, sticky='nsew')

    return frames


def create_gui_3d(window):
    """
    Creates the GUI for the 3D simulation.

    Parameters:
        window (Tk): The Tk window to destroy before creating the 3D GUI.
    """

    window.destroy()
    window = tk.Tk()
    window.minsize(260, 450)
    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
    window.title("My GUI 3D")

    walker_type_scale = create_label_and_widget(window, 1, "Walker type:", tk.Scale, from_=1, to=6,
                                                orient=tk.HORIZONTAL)
    num_steps_scale = create_label_and_widget(window, 3, "Number of  steps:", tk.Scale, from_=1, to=1000,
                                              orient=tk.HORIZONTAL)

    num_concurrent_walkers_scale = create_label_and_widget(window, 2, "total walkers:", tk.Scale, from_=1,
                                                           to=50, orient=tk.HORIZONTAL)
    traps_amount_scale = create_label_and_widget(window, 4, "Traps amount:", tk.Scale, from_=0, to=5,
                                                 orient=tk.HORIZONTAL)
    slow_zone_amount_scale = create_label_and_widget(window, 5, "Slow zone amount:", tk.Scale, from_=0, to=5,
                                                     orient=tk.HORIZONTAL)
    obstacle_amount_scale = create_label_and_widget(window, 6, "obstacle amount:", tk.Scale, from_=0, to=5,
                                                    orient=tk.HORIZONTAL)
    portal_amount_scale = create_label_and_widget(window, 7, "portal amount:", tk.Scale, from_=0, to=5,
                                                  orient=tk.HORIZONTAL)
    black_hole_amount_scale = create_label_and_widget(window, 8, "black hole amount:", tk.Scale, from_=0, to=5,
                                                      orient=tk.HORIZONTAL)
    ice_option_var = create_label_and_widget(window, 9, "Ice option:", tk.Checkbutton)
    restart_option_var = create_label_and_widget(window, 10, "Restart option:", tk.Checkbutton)

    run_button = tk.Button(window, text="run", command=lambda: run_main_3d(
        window,
        walker_type_scale.get(),
        num_steps_scale.get(),
        num_concurrent_walkers_scale.get(),
        portal_amount_scale.get(),
        obstacle_amount_scale.get(),
        traps_amount_scale.get(),
        slow_zone_amount_scale.get(),
        black_hole_amount_scale.get(),
        ice_option_var.get(),
        restart_option_var.get(),

    ))
    run_button.grid(row=11, column=2)

    back_button = tk.Button(window, text="Back", command=lambda: create_dimension_page(window))
    back_button.grid(row=12, column=2)

    window.mainloop()


def run_main_3d(window, walker_type, num_steps, num_concurrent_walkers, portal_list, obstacle_list, traps_amount,
                slow_zone_amount, black_hole_amount, ice_option, restart_option):
    """
    Runs the main function for the 3D simulation with the given configuration.

    Parameters:
        window (Tk): The Tk window to use for the simulation.
        walker_type (int): The type of the walker.
        num_steps (int): The number of steps for the walker to take.
        num_concurrent_walkers (int): The number of walkers to run concurrently.
        portal_list (list[dict]): A list of portals to add to the simulation.
        obstacle_list (list[dict]): A list of obstacles to add to the simulation.
        traps_amount (int): The number of traps to add to the simulation.
        slow_zone_amount (int): The number of slow zones to add to the simulation.
        black_hole_amount (int): The number of black holes to add to the simulation.
        ice_option (bool): Whether to enable the ice option.
        restart_option (bool): Whether to enable the restart option.
    """

    config = {
        "walker_type": int(walker_type),
        "num_steps": int(num_steps),
        "num_concurrent_walkers": int(num_concurrent_walkers),
        "portals3d": portal_list,
        "obstacles3d": obstacle_list,
        "traps_amount": int(traps_amount),
        "slow_zone_amount": int(slow_zone_amount),
        "black_hole_amount": int(black_hole_amount),
        "ice_option": ice_option,
        "restart_option": restart_option,
    }
    run3d.main(config)


def create_gui_2d(window):
    """
    Creates the GUI for the 2D simulation.

    Parameters:
        window (Tk): The Tk window to destroy before creating the 2D GUI.
    """

    window.destroy()

    window = tk.Tk()
    window.minsize(450, 510)
    window.protocol("WM_DELETE_WINDOW", lambda: window.destroy())
    window.title("My GUI")

    num_steps_scale = create_label_and_widget(window, 2, "Number of steps (interactive only):", tk.Scale, from_=1,
                                              to=1000, orient=tk.HORIZONTAL)
    walker_type_scale = create_label_and_widget(window, 3, "Walker type:", tk.Scale, from_=1, to=6,
                                                orient=tk.HORIZONTAL)
    num_of_run_combobox = create_label_and_widget(window, 4, "Number of runs (non-interactive only):", tk.Scale, from_=1, to=50,
                                                  orient=tk.HORIZONTAL)
    num_concurrent_walkers_scale = create_label_and_widget(window, 5, "total walkers:", tk.Scale, from_=1,
                                                           to=50, orient=tk.HORIZONTAL)
    traps_amount_scale = create_label_and_widget(window, 6, "Traps amount:", tk.Scale, from_=0, to=5,
                                                 orient=tk.HORIZONTAL)
    slow_zone_amount_scale = create_label_and_widget(window, 7, "Slow zone amount:", tk.Scale, from_=0, to=5,
                                                     orient=tk.HORIZONTAL)
    ice_option_var = create_label_and_widget(window, 8, "Ice option:", tk.Checkbutton)
    restart_option_var = create_label_and_widget(window, 9, "Restart option:", tk.Checkbutton)
    interactive_non_interactive_var = create_label_and_widget(window, 10, "Interactive?",
                                                              tk.Checkbutton)

    obstacle_frames = create_frames_for_p_and_o(window, 2, "Obstacle", 0)
    portal_frames = create_frames_for_p_and_o(window, 2, "Portal", 1, extra_fields=["exit_point_X", "exit_point_Y"])

    back_button = tk.Button(window, text="Back", command=lambda: create_dimension_page(window))
    back_button.grid(row=11, column=2)
    run = tk.Button(window, text="Run", command=lambda: run_main_2d(
        window,
        num_steps_scale.get(),
        walker_type_scale.get(),
        num_of_run_combobox.get(),
        num_concurrent_walkers_scale.get(),
        portal_frames,
        obstacle_frames,
        traps_amount_scale.get(),
        slow_zone_amount_scale.get(),
        ice_option_var.get(),
        restart_option_var.get(),
        interactive_non_interactive_var.get()
    ))
    run.grid(row=9, column=2)

    window.mainloop()


def run_main_2d(window, num_steps, walker_type, num_runs, num_concurrent_walkers,
                portal_frames, obstacle_frames,
                traps_amount,
                slow_zone_amount, ice_option, restart_option, simulation_mode):
    """
    Runs the main function for the 2D simulation with the given configuration.

    Parameters:
        window (Tk): The Tk window to use for the simulation.
        num_steps (int): The number of steps for the walker to take.
        walker_type (int): The type of the walker.
        num_runs (int): The number of runs for the simulation.
        num_concurrent_walkers (int): The number of walkers to run concurrently.
        portal_frames (list[Frame]): A list of frames for the portals.
        obstacle_frames (list[Frame]): A list of frames for the obstacles.
        traps_amount (int): The number of traps to add to the simulation.
        slow_zone_amount (int): The number of slow zones to add to the simulation.
        ice_option (bool): Whether to enable the ice option.
        restart_option (bool): Whether to enable the restart option.
        simulation_mode (bool): Whether to run the simulation in interactive mode.
    """

    obstacle_list = [
        {
            "length": frame.length_scale.get(),
            "center_loc": [frame.center_loc_x_scale.get(), frame.center_loc_y_scale.get()]
        }
        for frame in obstacle_frames
    ]
    portal_list = [
        {
            "length": frame.length_scale.get(),
            "center_loc": [frame.center_loc_x_scale.get(), frame.center_loc_y_scale.get()],
            "exit_point": [frame.exit_point_X_scale.get(), frame.exit_point_Y_scale.get()]
        }
        for frame in portal_frames
    ]
    config = {
        "walker_type": int(walker_type),
        "num_runs": int(num_runs),
        "num_steps": int(num_steps),
        "num_steps_for_statistics": NUM_STEPS_FOR_STATISTICS,
        "num_concurrent_walkers": int(num_concurrent_walkers),
        "portals_list": portal_list,
        "obstacles_list": obstacle_list,
        "traps_amount": int(traps_amount),
        "slow_zone_amount": int(slow_zone_amount),
        "ice_option": ice_option,
        "restart_option": restart_option,
        "check_interactive_or_non": simulation_mode
    }
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode='w') as temp:
        json.dump(config, temp)
        temp_path = temp.name
    subprocess.run(["python", "run2d.py", temp_path])

def print_help_message():
    help_message = """
    Welcome to the Random Walker Simulation!

    This simulation allows you to observe a random walker navigating through an infinite universe. You can customize 
    the simulation by choosing the type of walker, the number of steps the walker will take, and the number of 
    walkers that will be concurrently walking. You can also add various elements to the universe such as portals, 
    obstacles, traps, slow zones, and black holes.

    The UI is self-explanatory - choose your parameters, press 'Run', and enjoy!

    Usage: main.py [--help]

    Options:
    --help            Show this help message and exit
    """
    print(help_message)

def main():
    if "--help" in sys.argv:
        print_help_message()
    else:
        create_greeting_page()

if __name__ == "__main__":
    main()
