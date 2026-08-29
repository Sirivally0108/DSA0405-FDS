import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load dataset
df = pd.read_csv("patient_treatment.csv")

print("Dataset:")
print(df)

# Convert Gender into numerical values
df["Gender"] = df["Gender"].map({"Male": 0, "Female": 1})

# Convert target
df["Outcome"] = df["Outcome"].map({"Bad": 0, "Good": 1})

# Features and target
features = ["Age", "Gender", "Blood_Pressure", "Cholesterol"]

X = df[features]
y = df["Outcome"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Standardize
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# KNN model
model = KNeighborsClassifier(n_neighbors=3)
model.fit(X_train, y_train)

# Prediction
y_pred = model.predict(X_test)

# Metrics
print("\nEvaluation Results")
print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred, zero_division=0))
print("Recall   :", recall_score(y_test, y_pred, zero_division=0))
print("F1 Score :", f1_score(y_test, y_pred, zero_division=0))

# Prediction results
result = pd.DataFrame({
    "Actual": y_test.values,
    "Predicted": y_pred
})

print("\nPredictions:")
print(result)