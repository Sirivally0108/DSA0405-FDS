from sklearn.linear_model import LinearRegression
import numpy as np

# Features: [Age, Kms_Driven, Engine_CC]
X = np.array([
    [2, 25000, 1200],
    [5, 60000, 1500],
    [3, 40000, 1300],
    [7, 90000, 1800],
    [1, 15000, 1000]
])

# Target: Resale Price
y = np.array([650000, 420000, 520000, 300000, 720000])

# Train Linear Regression model
model = LinearRegression()
model.fit(X, y)

# User input
age = int(input("Enter Car Age (Years): "))
kms = int(input("Enter Kilometers Driven: "))
engine = int(input("Enter Engine Capacity (CC): "))

new_car = np.array([[age, kms, engine]])

predicted_price = model.predict(new_car)

print("Estimated Resale Price = ₹", predicted_price[0])