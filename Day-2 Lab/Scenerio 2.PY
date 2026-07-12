import csv
import numpy as np
from sklearn.linear_model import LogisticRegression

# Read CSV file
data = []
with open("email_data.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)      # Skip header
    for row in reader:
        data.append([int(row[1]), int(row[2]), int(row[3]), int(row[4])])

data = np.array(data)

# Features and Target
X = data[:, :3]
y = data[:, 3]

# Train model
model = LogisticRegression()
model.fit(X, y)

# User input
links = int(input("Enter Number of Links: "))
caps = int(input("Enter Number of Capitalized Words: "))
length = int(input("Enter Email Length: "))

new_email = np.array([[links, caps, length]])

prediction = model.predict(new_email)

if prediction[0] == 1:
    print("Prediction: SPAM Email")
else:
    print("Prediction: NOT SPAM Email")