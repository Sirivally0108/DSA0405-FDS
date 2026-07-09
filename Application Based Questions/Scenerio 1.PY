import numpy as np

# Load CSV file
house_data = np.genfromtxt(
    "house_data.csv",
    delimiter=",",
    skip_header=1,
    usecols=(1,2,3)
)

# Select houses with more than 4 bedrooms
filtered = house_data[house_data[:,0] > 4]

# Calculate average sale price
average_price = np.mean(filtered[:,2])

print("Average Sale Price =", average_price)