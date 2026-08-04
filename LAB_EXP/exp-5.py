import numpy as np

fuel_data = np.genfromtxt(
    "Fuel_d.csv",
    delimiter=",",
    skip_header=1,
    dtype=str
)

fuel_efficiency = fuel_data[:, 6].astype(float)
make = fuel_data[:, 1]

average_efficiency = np.mean(fuel_efficiency)

mazda_eff = fuel_efficiency[make == "mazda"]
audi_eff = fuel_efficiency[make == "audi"]

mazda_avg = np.mean(mazda_eff)
audi_avg = np.mean(audi_eff)

percentage_improvement = ((mazda_avg - audi_avg) / audi_avg) * 100

print("Average Fuel Efficiency of all cars:", round(average_efficiency, 2), "MPG")
print("Average Fuel Efficiency of Mazda:", round(mazda_avg, 2), "MPG")
print("Average Fuel Efficiency of Audi:", round(audi_avg, 2), "MPG")
print("Percentage Improvement from Mazda to Audi:", round(percentage_improvement, 2), "%")