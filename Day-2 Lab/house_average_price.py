import numpy as np

house_data = np.loadtxt(
    "House_d.csv",
    delimiter=",",
    skiprows=1
)

# Houses with more than 4 bedrooms
houses_more_than_4 = house_data[house_data[:, 0] > 4]

# Average sale price
average_price = np.mean(houses_more_than_4[:, 2])

print("Average Price of Houses with More Than 4 Bedrooms:",
      round(average_price, 2))