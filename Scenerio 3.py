from sklearn.linear_model import LogisticRegression
import numpy as np

# Features: [Num_Links, Num_Caps_Words, Email_Length]
X = np.array([
    [1, 3, 120],
    [6, 15, 300],
    [0, 1, 80],
    [4, 10, 250],
    [2, 5, 160]
])

# Target: Spam (1) or Not Spam (0)
y = np.array([0, 1, 0, 1, 0])

# Train Logistic Regression model
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