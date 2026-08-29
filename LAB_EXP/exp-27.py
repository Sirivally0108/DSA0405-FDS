import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import StandardScaler

# Load dataset
data = pd.read_csv("customer_churn.csv")

# Features and target
X = data[
    ["usage_minutes",
     "contract_months",
     "monthly_charge"]
]

y = data["churn"]

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Standardization
scaler = StandardScaler()

X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Train Logistic Regression
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)

print("Accuracy:",
      round(accuracy_score(y_test, y_pred), 3))

print("\nClassification Report:")
print(classification_report(y_test, y_pred))

# New customer input
usage = float(input("\nEnter usage minutes: "))
contract = float(input("Enter contract duration (months): "))
charge = float(input("Enter monthly charge: "))

new_customer = [[usage, contract, charge]]
new_customer = scaler.transform(new_customer)

prediction = model.predict(new_customer)[0]
probability = model.predict_proba(new_customer)[0][1]

if prediction == 1:
    print("Prediction: Customer is likely to CHURN")
else:
    print("Prediction: Customer is NOT likely to churn")

print("Churn Probability:",
      round(probability * 100, 2), "%")