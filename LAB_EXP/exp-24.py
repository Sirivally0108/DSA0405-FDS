import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

# Load dataset
data = pd.read_csv("patients.csv")

# Features
X = data[
    ["fever", "cough", "fatigue", "pain"]
]

# Target
y = data["condition"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Scale features
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# User input for k
k = int(input("Enter value of k: "))

# Create KNN model
model = KNeighborsClassifier(n_neighbors=k)

# Train model
model.fit(X_train, y_train)

# Test accuracy
y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print("Model Accuracy:",
      round(accuracy * 100, 2), "%")

# New patient input
print("\nEnter details of new patient:")

fever = float(input("Fever (0/1): "))
cough = float(input("Cough (0/1): "))
fatigue = float(input("Fatigue (0/1): "))
pain = float(input("Pain (0/1): "))

new_patient = [[
    fever,
    cough,
    fatigue,
    pain
]]

# Scale new patient
new_patient = scaler.transform(new_patient)

# Prediction
prediction = model.predict(new_patient)

if prediction[0] == 1:
    print("\nPrediction: Patient has the condition.")
else:
    print("\nPrediction: Patient does not have the condition.")