from sklearn.datasets import load_iris
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# Load Iris dataset
iris = load_iris()

X = iris.data
y = iris.target

# Split dataset
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)

# Create Decision Tree
model = DecisionTreeClassifier(
    random_state=42
)

# Train model
model.fit(X_train, y_train)

# Test model
y_pred = model.predict(X_test)

# Accuracy
accuracy = accuracy_score(y_test, y_pred)

print("Decision Tree Accuracy:",
      round(accuracy * 100, 2), "%")

# User input
print("\nEnter flower measurements:")

sepal_length = float(
    input("Sepal Length: ")
)

sepal_width = float(
    input("Sepal Width: ")
)

petal_length = float(
    input("Petal Length: ")
)

petal_width = float(
    input("Petal Width: ")
)

# New flower
new_flower = [[
    sepal_length,
    sepal_width,
    petal_length,
    petal_width
]]

# Prediction
prediction = model.predict(new_flower)

species = iris.target_names[prediction[0]]

print("\nPredicted Species:", species)