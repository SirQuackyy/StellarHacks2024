import datetime
from rocketpy import Environment, SolidMotor, Rocket, Flight
import requests
import pandas as pd
from tkinter import filedialog
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import csv

def display_csv_data(file_path):
    with open(file_path, 'r', newline='') as file:
        csv_reader = csv.reader(file)
        header = next(csv_reader)  # Read the header row
        tree.delete(*tree.get_children())  # Clear the current data

        tree["columns"] = header
        for col in header:
            tree.heading(col, text=col)
            tree.column(col, width=100)

        for row in csv_reader:
            tree.insert("", "end", values=row)


# def create_rocket(date, lat, long, elev, motor, )

tomorrow = datetime.date.today() + datetime.timedelta(days=1)

env = Environment(latitude=32.990254, longitude=-106.974998, elevation=1400)
env.set_date(
    (tomorrow.year, tomorrow.month, tomorrow.day, 12)
)

env.set_atmospheric_model(type="Forecast", file="GFS")

env.info()

Pro75M1670 = SolidMotor(
    thrust_source="data/motors/Cesaroni_6026M1670-P.eng",
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    nozzle_radius=33 / 1000,
    grain_number=5,
    grain_density=1815,
    grain_outer_radius=33 / 1000,
    grain_initial_inner_radius=15 / 1000,
    grain_initial_height=120 / 1000,
    grain_separation=5 / 1000,
    grains_center_of_mass_position=0.397,
    center_of_dry_mass_position=0.317,
    nozzle_position=0,
    burn_time=3.9,
    throat_radius=11 / 1000,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

Pro75M1670.info()

calisto = Rocket(
    radius=127 / 2000,
    mass=14.426,
    inertia=(6.321, 6.321, 0.034),
    power_off_drag="data/calisto/powerOnDragCurve.csv",
    power_on_drag="data/calisto/powerOnDragCurve.csv",
    center_of_mass_without_motor=0,
    coordinate_system_orientation="tail_to_nose",
)

calisto.add_motor(Pro75M1670, position=-1.255)

rail_buttons = calisto.set_rail_buttons(
    upper_button_position=0.0818,
    lower_button_position=-0.6182,
    angular_position=45,
)

nose_cone = calisto.add_nose(
    length=0.55829, kind="von karman", position=1.278
)

fin_set = calisto.add_trapezoidal_fins(
    n=4,
    root_chord=0.120,
    tip_chord=0.060,
    span=0.110,
    position=-1.04956,
    cant_angle=0.5,
    airfoil=("data/calisto/NACA0012-radians.csv","radians"),
)

tail = calisto.add_tail(
    top_radius=0.0635, bottom_radius=0.0435, length=0.060, position=-1.194656
)

main = calisto.add_parachute(
    name="main",
    cd_s=10.0,
    trigger=800,      # ejection altitude in meters
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

drogue = calisto.add_parachute(
    name="drogue",
    cd_s=1.0,
    trigger="apogee",  # ejection at apogee
    sampling_rate=105,
    lag=1.5,
    noise=(0, 8.3, 0.5),
)

# Stability Graph (If negative, unstable and will fail, if unreasonably high, will fail)
calisto.plots.static_margin()

# Positions of all added components drawn (Make sure everything is correct)
calisto.draw()

# Create Test Flight
test_flight = Flight(
    rocket=calisto, environment=env, rail_length=5.2, inclination=85, heading=0
    )

root = tk.Tk()
root.title("Rocket Launch Simulator")

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
ttk.Label(frame, text = "Launch Date: {}".format(tomorrow)).grid(column=1, row=1, sticky=(W, E))
ttk.Label(frame, text = "Launch Site Latitude: {}".format(32.990254)).grid(column=1, row=2, sticky=(W, E))
ttk.Label(frame, text = "Launch Site Longitude: {}".format(-106.974998)).grid(column=1, row=3, sticky=(W, E))
ttk.Label(frame, text = "Launch Site Surface Elevation: {}".format(1400)).grid(column=1, row=4, sticky=(W, E))

ttk.Label(frame, text = "Surface Wind Speed: {}".format(env.wind_speed(1400))).grid(column=1, row=6, sticky=(W, E))
ttk.Label(frame, text = "Surface Wind Direction: {}".format(env.wind_direction(1400))).grid(column=1, row=7, sticky=(W, E))
ttk.Label(frame, text = "Surface Wind Heading: {}".format(env.wind_heading(1400))).grid(column=1, row=8, sticky=(W, E))
ttk.Label(frame, text = "Surface Pressure: {}".format(env.pressure(1400))).grid(column=1, row=9, sticky=(W, E))
ttk.Label(frame, text = "Surface Temperature: {}".format(env.temperature(1400))).grid(column=1, row=10, sticky=(W, E))
ttk.Label(frame, text = "Surface Air Density: {}".format(env.density(1400))).grid(column=1, row=11, sticky=(W, E))
ttk.Label(frame, text = "Surface Speed of Sound: {}".format(env.speed_of_sound(1400))).grid(column=1, row=12, sticky=(W, E))

ttk.Label(frame, text = "Nozzle Radius: {}".format(Pro75M1670.nozzle_radius)).grid(column=1, row=14, sticky=(W, E))
ttk.Label(frame, text = "Nozzle Throat Radius: {}".format(Pro75M1670.throat_radius)).grid(column=1, row=15, sticky=(W, E))

ttk.Label(frame, text = "Number of Grains: {}".format(Pro75M1670.grain_number)).grid(column=1, row=17, sticky=(W, E))
ttk.Label(frame, text = "Grain Spacing: {}".format(Pro75M1670.grain_separation)).grid(column=1, row=18, sticky=(W, E))
ttk.Label(frame, text = "Grain Density: {}".format(Pro75M1670.grain_density)).grid(column=1, row=19, sticky=(W, E))
ttk.Label(frame, text = "Grain Outer Radius: {}".format(Pro75M1670.grain_outer_radius)).grid(column=1, row=20, sticky=(W, E))
ttk.Label(frame, text = "Grain Inner Radius: {}".format(Pro75M1670.grain_initial_inner_radius)).grid(column=1, row=21, sticky=(W, E))
ttk.Label(frame, text = "Grain Height: {}".format(Pro75M1670.grain_initial_height)).grid(column=1, row=22, sticky=(W, E))
ttk.Label(frame, text = "Grain Volume: {}".format(Pro75M1670.grain_initial_volume)).grid(column=1, row=23, sticky=(W, E))
ttk.Label(frame, text = "Grain Mass: {}".format(Pro75M1670.grain_initial_mass)).grid(column=1, row=24, sticky=(W, E))

ttk.Label(frame, text = "Total Burning Time: {}".format(Pro75M1670.burn_duration)).grid(column=1, row=26, sticky=(W, E))
ttk.Label(frame, text = "Total Propellant Mass: {}".format(Pro75M1670.propellant_initial_mass)).grid(column=1, row=27, sticky=(W, E))
ttk.Label(frame, text = "Average Thrust: {}".format(Pro75M1670.average_thrust)).grid(column=1, row=28, sticky=(W, E))
ttk.Label(frame, text = "Maximum Thrust: {}".format(Pro75M1670.max_thrust)).grid(column=1, row=29, sticky=(W, E))
ttk.Label(frame, text = "Total Impulse: {}".format(Pro75M1670.total_impulse)).grid(column=1, row=30, sticky=(W, E))

ttk.Label(frame, text = "Apogee Altitude: {}".format(test_flight.apogee)).grid(column=1, row=32, sticky=(W, E))
ttk.Label(frame, text = "Apogee Time: {}".format(test_flight.apogee_time)).grid(column=1, row=33, sticky=(W, E))

ttk.Label(frame, text = "X Impact: {}".format(test_flight.x_impact)).grid(column=1, row=35, sticky=(W, E))
ttk.Label(frame, text = "Y Impact: {}".format(test_flight.y_impact)).grid(column=1, row=36, sticky=(W, E))
ttk.Label(frame, text = "Velocity at Impact: {}".format(test_flight.impact_velocity)).grid(column=1, row=37, sticky=(W, E))

# Trajectory in graph format
test_flight.plots.trajectory_3d()

frame.destroy()

# Velocity and Acceleration graphs all three dimensions
test_flight.plots.linear_kinematics_data()

# Angular data of flight path (Flight path angle and Attitude Angle should be close if rocket is stable)
test_flight.plots.flight_path_angle_data()

# Angular Velocity and Acceleration graphs
test_flight.plots.angular_kinematics_data()

# Kinetic/Mechanical Energy and Power Graphs
test_flight.plots.energy_data()

# Google Earth Trajectory Visualization
test_flight.export_kml(
    file_name="trajectory.kml",
    extrude=True,
    altitude_mode="relative_to_ground",
)

test_flight.export_data(
    "calisto_flight_data.csv",
    'x',
    'y',
    'z',
    'vx',
    'vy',
    'vz',
    'ax',
    'ay',
    'az',
    'angle_of_attack',
    time_step=1.0,
)

frame = ttk.Frame(root, padding="3 3 12 12")
tree = ttk.Treeview(frame, show="headings")

display_csv_data('calisto_flight_data.csv')

root.mainloop()