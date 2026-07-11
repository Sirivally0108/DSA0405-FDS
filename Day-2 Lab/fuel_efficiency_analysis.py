import numpy as np

fuel_data = np.loadtxt(
    "Fuel_d.csv",
    delimiter=",",
    skiprows=1,
    usecols=(1, 2, 3)   # Read only numeric columns
)

engine = fuel_data[:, 0]
fuel = fuel_data[:, 1]
distance = fuel_data[:, 2]

efficiency = distance / fuel

print("Fuel Efficiency (km/l):")
print(np.round(efficiency, 2))

print("Average Fuel Efficiency:", round(np.mean(efficiency), 2), "km/l")