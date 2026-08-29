import pandas as pd

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# Load dataset
data = pd.read_csv("customers.csv")

features = [
    "annual_income",
    "spending_score",
    "purchase_frequency"
]

X = data[features]

# Standardize
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means
kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

data["cluster"] = kmeans.fit_predict(X_scaled)

print("Customer Cluster Distribution:")
print(data["cluster"].value_counts().sort_index())

print("\nCluster Centers:")
print(
    scaler.inverse_transform(
        kmeans.cluster_centers_
    )
)

# New customer
income = float(input("\nEnter annual income: "))
score = float(input("Enter spending score: "))
frequency = float(
    input("Enter purchase frequency: ")
)

new_customer = [[income, score, frequency]]

new_scaled = scaler.transform(new_customer)

cluster = kmeans.predict(new_scaled)[0]

print("\nNew Customer belongs to Cluster:",
      cluster)