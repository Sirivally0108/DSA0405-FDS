import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
data = pd.read_csv("housing.csv")

# Features and target
X = data[["area", "bedrooms"]]
y = data["price"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Create and train model
model = LinearRegression()
model.fit(X_train, y_train)

# Test prediction
y_pred = model.predict(X_test)

# Evaluation
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("Model Performance")
print("Mean Squared Error:", round(mse, 2))
print("R2 Score:", round(r2, 3))

# User input
area = float(input("\nEnter house area: "))
bedrooms = int(input("Enter number of bedrooms: "))

new_house = [[area, bedrooms]]

predicted_price = model.predict(new_house)

print("Predicted House Price:",
      round(predicted_price[0], 2))