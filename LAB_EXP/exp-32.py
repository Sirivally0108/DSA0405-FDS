import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import (
    mean_squared_error,
    r2_score
)

# Load dataset
data = pd.read_csv("house_prices.csv")

# Select variables
X = data[["size"]]
y = data["price"]

# Bivariate analysis
plt.scatter(
    data["size"],
    data["price"]
)

plt.xlabel("House Size")
plt.ylabel("House Price")
plt.title("House Size vs House Price")
plt.show()

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# Linear Regression
model = LinearRegression()
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r2 = r2_score(y_test, y_pred)

print("MODEL PERFORMANCE")
print("-----------------")
print("MSE :", round(mse, 2))
print("RMSE:", round(rmse, 2))
print("R2  :", round(r2, 3))

print("\nRegression Equation:")
print(
    "Price =",
    round(model.coef_[0], 2),
    "* Size +",
    round(model.intercept_, 2)
)

# Regression line
plt.scatter(
    X,
    y
)

plt.plot(
    X,
    model.predict(X)
)

plt.xlabel("House Size")
plt.ylabel("House Price")
plt.title("Linear Regression: Size vs Price")
plt.show()