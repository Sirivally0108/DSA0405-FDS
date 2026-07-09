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

# Create and train the Logistic Regression model
model = LogisticRegression()
model.fit(X, y)
# New email to predict
# Example: 3 links, 8 capitalized words, 200 email length
new_email = np.array([[3, 8, 200]])

# Prediction
prediction = model.predict(new_email)

if prediction[0] == 1:
    print("The new email is SPAM.")
else:
    print("The new email is NOT SPAM.")