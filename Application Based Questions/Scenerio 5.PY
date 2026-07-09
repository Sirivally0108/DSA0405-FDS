from sklearn.tree import DecisionTreeClassifier, export_text
import numpy as np

# Features: [Income, Credit_Score, Existing_Loans]
X = np.array([
    [45000, 720, 0],
    [30000, 650, 1],
    [60000, 780, 0],
    [28000, 620, 2],
    [52000, 710, 1]
])

# Target: Approved (1) or Rejected (0)
y = np.array([1, 0, 1, 0, 1])

# Train Decision Tree (CART)
model = DecisionTreeClassifier(criterion="gini", random_state=0)
model.fit(X, y)

# User input
income = int(input("Enter Monthly Income: "))
credit = int(input("Enter Credit Score: "))
loans = int(input("Enter Existing Loans: "))

new_applicant = np.array([[income, credit, loans]])

prediction = model.predict(new_applicant)

if prediction[0] == 1:
    print("Loan Approved")
else:
    print("Loan Rejected")

# Display Decision Rules
print("\nDecision Tree Rules:")
rules = export_text(model,
                    feature_names=["Income", "Credit_Score", "Existing_Loans"])
print(rules)
