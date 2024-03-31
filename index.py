from rocketpy import Fluid, CylindricalTank, MassFlowRateBasedTank, HybridMotor
from rocketpy import SolidMotor
import datetime
from tkcalendar import Calendar
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

parameters = {
    "lat": 0,
    "long": 0,
    "date": None,
}
def next(x,y,z):
    parameters["lat"] = x 
    parameters["long"] = y 
    parameters["date"] = z
def infobox(title,prompt):
    messagebox.showinfo(title + " Info",prompt)



root = Tk()
root.title("Your Rocket Flight Simulator")

frame = ttk.Frame(root, padding="3 3 12 12")
frame.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
#rocket raidus, mass wihtout motor (kg), inertia (tuple), upload pwr on drag, position of motor relative to centerof mass, nose cone  length and positon,  fin position, tail top and bottom radius , Inclination
ttk.Label(frame, text = "Latitude: ").grid(column=1, row=1, sticky=(W, E)).bind('<Button-1>', infobox("Latitude","North/South Coordinate of the rocket"))
ttk.Label(frame, text = "Longitude: ").grid(column=1, row=2, sticky=(W, E)).bind('<Button-1>', infobox("Longitude","East/West Coordinate of the rocket"))
ttk.Label(frame, text = "Altitude (m): ").grid(column=1, row=3, sticky=(W, E)).bind('<Button-1>', infobox("Altitude","How high the rocket before launching"))
ttk.Label(frame, text = "Date: ").grid(column=1, row=4, sticky=(W, E))
ttk.Label(frame, text = "Motors: ").grid(column=1, row=5, sticky=(W, E)).bind('<Button-1>', infobox("Motors","First two motors are solid motors (uses solid fuel). Second two are hybrid motors (solid and gas/liquid fuel). Third two are liquid motors (uses liquid fuel). Liquid motors are better at throttling, shutting down, and restarting. "))
ttk.Label(frame, text = "Rocket Radius (m): ").grid(column=1, row=6, sticky=(W, E)).bind('<Button-1>', infobox("Rocket Radius","Largest radius of the rocket in meters"))
ttk.Label(frame, text = "Mass without motor (kg): ").grid(column=1, row=7, sticky=(W, E)).bind('<Button-1>', infobox("Mass","Mass of the rocket without the motor installed"))
ttk.Label(frame, text = "Inertia: ").grid(column=1, row=8, sticky=(W, E)).bind('<Button-1>', infobox("Inertia","The first and second parameter"))
ttk.Label(frame, text = "Upload Power on drag: ").grid(column=1, row=9, sticky=(W, E))
ttk.Label(frame, text = "Position of motor relative to center of mass: ").grid(column=1, row=10, sticky=(W, E))
ttk.Label(frame, text = "Nose cone length and poosition: ").grid(column=1, row=11, sticky=(W, E))
ttk.Label(frame, text = "Fin Po: ").grid(column=1, row=5, sticky=(W, E))







latitude = DoubleVar()
lat = ttk.Entry(frame, width=7, textvariable=latitude)
lat.grid(column=2, row=1, sticky=(W, E))

longitude = DoubleVar()
longi = ttk.Entry(frame, width=7, textvariable=longitude)
longi.grid(column=2, row=2, sticky=(W, E))
cal = Calendar(frame, selectmode = 'day',
               year = 2020, month = 5,
               day = 22)
cal.grid(column=2,row=4)


motor = StringVar()


motors = ["Pro75M1670 ","D2_3T", "G130-PVC", "G300-PVC", "H222-HP", "H300-HP"]
place = [None,None,None,None,None,None]
for i in range(len(motors)):
    place[i] = ttk.Radiobutton(frame, text = motors[i], variable=motor, value=motors[i]).grid(column =2, row = 5+i)

altitude = DoubleVar()
alt = ttk.Entry(frame, width=10, textvariable=altitude)
alt.grid(column=2, row=3, sticky=(W, E))


#ttk.Button(frame, text="Next", command=next(lat,longi,cal.get_date())).grid(column=3, row=4, sticky=W)


for child in frame.winfo_children(): 
    child.grid_configure(padx=5, pady=5)



root.mainloop()
# from tkinter import *
# from tkinter import ttk
# root = Tk()
# root.title("Rocket Simulation")

# location = ttk.Frame(root)
# def submitForm():
    # print("hi")
# button = ttk.Button(location, text='Okay', command=submitForm)





Pro75M1670 = SolidMotor(
    thrust_source="data/motors/Cesaroni_M1670.eng",
    dry_mass=1.815,
    dry_inertia=(0.125, 0.125, 0.002),
    center_of_dry_mass_position=0.317,
    grains_center_of_mass_position=0.397,
    burn_time=3.9,
    grain_number=5,
    grain_separation=0.005,
    grain_density=1815,
    grain_outer_radius=0.033,
    grain_initial_inner_radius=0.015,
    grain_initial_height=0.12,
    nozzle_radius=0.033,
    throat_radius=0.011,
    interpolation_method="linear",
    nozzle_position=0,
    coordinate_system_orientation="nozzle_to_combustion_chamber",
)

D2_3T = SolidMotor(
  thrust_source="../data/motors/Cesaroni_M1670.eng",
  dry_mass=1.920,
  dry_inertia=(0.235, 0.235, 0.005),
  nozzle_radius=20 / 1000,
  grain_number=4,
  grain_density=1340,
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

# Define the fluids
oxidizer_liq = Fluid(name="N2O_l", density=1220)
oxidizer_gas = Fluid(name="N2O_g", density=1.9277)

# Define tank geometry
tank_shape = CylindricalTank(115 / 2000, 0.705)

# Define tank
oxidizer_tank = MassFlowRateBasedTank(
    name="oxidizer tank",
    geometry=tank_shape,
    flux_time=5.2,
    initial_liquid_mass=4.11,
    initial_gas_mass=0,
    liquid_mass_flow_rate_in=0,
    liquid_mass_flow_rate_out=(4.11 - 0.5) / 5.2,
    gas_mass_flow_rate_in=0,
    gas_mass_flow_rate_out=0,
    liquid=oxidizer_liq,
    gas=oxidizer_gas,
)



