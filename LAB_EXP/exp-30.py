import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error, r2_score

# Load dataset
data = pd.read_csv("cars.csv")

features = [
    "mileage",
    "age",
    "engine_cc"
]

X = data[features]
y = data["price"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

# CART Regression Tree
model = DecisionTreeRegressor(
    max_depth=4,
    random_state=42
)

model.fit(X_train, y_train)

# Test prediction
y_pred = model.predict(X_test)

print("MODEL PERFORMANCE")
print("MSE:",
      round(mean_squared_error(y_test, y_pred), 2))
print("R2 Score:",
      round(r2_score(y_test, y_pred), 3))

# User input
mileage = float(input("\nEnter mileage: "))
age = float(input("Enter car age: "))
engine = float(input("Enter engine capacity (cc): "))

new_car = pd.DataFrame(
    [[mileage, age, engine]],
    columns=features
)

prediction = model.predict(new_car)[0]

print("\nPredicted Car Price:",
      round(prediction, 2))

# Decision path
node_indicator = model.decision_path(new_car)
leaf_id = model.apply(new_car)[0]

print("\nDecision Path:")

node_ids = node_indicator.indices[
    node_indicator.indptr[0]:
    node_indicator.indptr[1]
]

for node_id in node_ids:

    if node_id == leaf_id:
        print("Reached prediction leaf.")
        continue

    feature_id = model.tree_.feature[node_id]
    threshold = model.tree_.threshold[node_id]

    feature_name = features[feature_id]

    value = new_car.iloc[0][feature_name]

    if value <= threshold:
        condition = "<="
    else:
        condition = ">"

    print(
        f"{feature_name} = {value} "
        f"{condition} {threshold:.2f}"
    )