import numpy as np

house_data = np.array([
    [3, 1400, 7500000],
    [5, 2200, 12500000],
    [4, 1800, 9800000],
    [6, 3000, 18500000],
    [2, 1100, 5200000]
])
filtered_houses = house_data[house_data[:, 0] > 4]
average_price = np.mean(filtered_houses[:, 2])

print("Average Sale Price:", average_price)