import csv
import numpy as np
from sklearn.tree import DecisionTreeClassifier, export_text

# Read CSV file
data = []
with open("loan_data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        data.append([int(row[1]), int(row[2]), int(row[3]), int(row[4])])

data = np.array(data)

# Features and Target
X = data[:, :3]
y = data[:, 3]

# Train CART model
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

print("\nDecision Tree Rules:")
print(export_text(model,
feature_names=["Income", "Credit_Score", "Existing_Loans"]))