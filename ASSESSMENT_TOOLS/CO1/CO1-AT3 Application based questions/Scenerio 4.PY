import csv
import numpy as np
from sklearn.linear_model import LinearRegression

# Read CSV file
data = []
with open("car_data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        data.append([int(row[1]), int(row[2]), int(row[3]), int(row[4])])

data = np.array(data)

# Features and Target
X = data[:, :3]
y = data[:, 3]

# Train model
model = LinearRegression()
model.fit(X, y)

# User input
age = int(input("Enter Car Age: "))
kms = int(input("Enter Kilometers Driven: "))
engine = int(input("Enter Engine Capacity (CC): "))

new_car = np.array([[age, kms, engine]])

price = model.predict(new_car)

print("Estimated Resale Price = ₹", round(price[0], 2))